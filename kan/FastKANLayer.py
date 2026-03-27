import numpy as np
import torch
import torch.nn as nn

from .spline import extend_grid


def _sparse_mask(in_dim: int, out_dim: int) -> torch.Tensor:
    """Build a sparse binary mask similar to kan.utils.sparse_mask."""
    in_coord = torch.arange(in_dim) * (1.0 / in_dim) + 1.0 / (2.0 * in_dim)
    out_coord = torch.arange(out_dim) * (1.0 / out_dim) + 1.0 / (2.0 * out_dim)
    dist_mat = torch.abs(out_coord[:, None] - in_coord[None, :])

    in_nearest = torch.argmin(dist_mat, dim=0)
    in_connection = torch.stack([torch.arange(in_dim), in_nearest], dim=1)

    out_nearest = torch.argmin(dist_mat, dim=1)
    out_connection = torch.stack([out_nearest, torch.arange(out_dim)], dim=1)

    all_connection = torch.cat([in_connection, out_connection], dim=0)
    mask = torch.zeros(in_dim, out_dim)
    mask[all_connection[:, 0], all_connection[:, 1]] = 1.0
    return mask


class FastKANLayer(nn.Module):
    """A FastKAN-style numeric layer compatible with KANLayer public API.

    The layer keeps KAN-compatible outputs/caches but uses radial basis
    functions instead of B-spline bases.
    """

    def __init__(
        self,
        in_dim=3,
        out_dim=2,
        num=5,
        k=3,
        noise_scale=0.5,
        scale_base_mu=0.0,
        scale_base_sigma=1.0,
        scale_sp=1.0,
        base_fun=torch.nn.SiLU(),
        grid_eps=0.02,
        grid_range=[-1, 1],
        sp_trainable=True,
        sb_trainable=True,
        save_plot_data=True,  # kept for call-site compatibility
        device="cpu",
        sparse_init=False,
        denominator=None,
        den_trainable=True,
    ):
        super().__init__()

        self.out_dim = out_dim
        self.in_dim = in_dim
        self.num = num
        self.k = k
        self.base_fun = base_fun
        self.grid_eps = grid_eps
        self.save_plot_data = save_plot_data

        base_grid = torch.linspace(grid_range[0], grid_range[1], steps=num + 1)[None, :].expand(in_dim, num + 1)
        self.grid = torch.nn.Parameter(extend_grid(base_grid, k_extend=k)).requires_grad_(False)

        init_coef = (torch.rand(in_dim, out_dim, num + 1) - 0.5) * noise_scale / max(1, num)
        self.coef = torch.nn.Parameter(init_coef)

        if sparse_init:
            self.mask = torch.nn.Parameter(_sparse_mask(in_dim, out_dim)).requires_grad_(False)
        else:
            self.mask = torch.nn.Parameter(torch.ones(in_dim, out_dim)).requires_grad_(False)

        self.scale_base = torch.nn.Parameter(
            scale_base_mu * (1.0 / np.sqrt(in_dim))
            + scale_base_sigma * (torch.rand(in_dim, out_dim) * 2.0 - 1.0) * (1.0 / np.sqrt(in_dim))
        ).requires_grad_(sb_trainable)
        self.scale_sp = torch.nn.Parameter(
            torch.ones(in_dim, out_dim) * scale_sp * (1.0 / np.sqrt(in_dim)) * self.mask
        ).requires_grad_(sp_trainable)

        if denominator is None:
            denominator = float(grid_range[1] - grid_range[0]) / max(1, num)
        init_den = torch.full((in_dim, 1), float(denominator), dtype=torch.float32)
        init_den = torch.clamp(init_den, min=1e-4)
        self.log_denominator = torch.nn.Parameter(init_den.log()).requires_grad_(den_trainable)

        self.to(device)

    @property
    def denominator(self) -> torch.Tensor:
        return self.log_denominator.exp().clamp_min(1e-6)

    def to(self, device):
        super().to(device)
        self.device = device
        return self

    def _core_grid(self) -> torch.Tensor:
        if self.k > 0:
            return self.grid[:, self.k : -self.k]
        return self.grid

    def _rbf_basis(self, x: torch.Tensor) -> torch.Tensor:
        centers = self._core_grid()
        den = self.denominator
        return torch.exp(-((x[:, :, None] - centers[None, :, :]) / den[None, :, :]) ** 2)

    def _numeric_response(self, x: torch.Tensor) -> torch.Tensor:
        basis = self._rbf_basis(x)
        return torch.einsum("big,iog->bio", basis, self.coef)

    def _fit_coef_from_targets(self, x_eval: torch.Tensor, y_eval: torch.Tensor) -> torch.Tensor:
        """Solve least squares: basis @ coef ~= target per input channel."""
        basis = self._rbf_basis(x_eval).permute(1, 0, 2)  # [in_dim, batch, num+1]
        target = y_eval.permute(1, 0, 2)  # [in_dim, batch, out_dim]

        try:
            coef = torch.linalg.lstsq(basis, target).solution  # [in_dim, num+1, out_dim]
            coef = coef.permute(0, 2, 1).contiguous()  # [in_dim, out_dim, num+1]
        except Exception:
            # Keep old coefficients when numeric solving fails.
            coef = self.coef.detach().clone()
        return coef

    def _adaptive_grid_from_samples(self, x: torch.Tensor) -> torch.Tensor:
        x_pos = torch.sort(x, dim=0)[0]
        batch = x_pos.shape[0]
        ids = torch.linspace(0, max(0, batch - 1), steps=self.num + 1, device=x.device)
        ids = ids.round().long()
        grid_adaptive = x_pos[ids, :].permute(1, 0)

        margin = 0.0
        h = (grid_adaptive[:, [-1]] - grid_adaptive[:, [0]] + 2 * margin) / max(1, self.num)
        grid_uniform = grid_adaptive[:, [0]] - margin + h * torch.arange(self.num + 1, device=x.device)[None, :]

        return self.grid_eps * grid_uniform + (1.0 - self.grid_eps) * grid_adaptive

    def forward(self, x):
        batch = x.shape[0]
        preacts = x[:, None, :].clone().expand(batch, self.out_dim, self.in_dim)

        base = self.base_fun(x)
        y_numeric = self._numeric_response(x)  # [batch, in_dim, out_dim]
        postspline = y_numeric.permute(0, 2, 1).contiguous()  # [batch, out_dim, in_dim]

        y = self.scale_base[None, :, :] * base[:, :, None] + self.scale_sp[None, :, :] * y_numeric
        y = self.mask[None, :, :] * y
        postacts = y.permute(0, 2, 1).contiguous()

        y = torch.sum(y, dim=1)
        return y, preacts, postacts, postspline

    @torch.no_grad()
    def update_grid_from_samples(self, x, mode="sample"):
        x = x.to(self.grid.device)
        old_eval_x = torch.sort(x, dim=0)[0]
        old_eval_y = self._numeric_response(old_eval_x)

        core_grid = self._adaptive_grid_from_samples(old_eval_x)
        if mode == "grid":
            sample_ids = torch.linspace(
                0, max(0, old_eval_x.shape[0] - 1), steps=max(2, 2 * self.num + 1), device=x.device
            ).round().long()
            old_eval_x = old_eval_x[sample_ids]
            old_eval_y = self._numeric_response(old_eval_x)

        self.grid.data = extend_grid(core_grid, k_extend=self.k)
        self.coef.data = self._fit_coef_from_targets(old_eval_x, old_eval_y)

    @torch.no_grad()
    def initialize_grid_from_parent(self, parent, x, mode="sample"):
        x = x.to(self.grid.device)
        x_eval = torch.sort(x, dim=0)[0]

        if hasattr(parent, "_numeric_response"):
            y_eval = parent._numeric_response(x_eval.to(parent.grid.device)).to(self.grid.device)
        else:
            _, _, _, parent_postspline = parent(x_eval.to(parent.grid.device))
            y_eval = parent_postspline.permute(0, 2, 1).to(self.grid.device)

        core_grid = self._adaptive_grid_from_samples(x_eval)
        if mode == "grid":
            sample_ids = torch.linspace(
                0, max(0, x_eval.shape[0] - 1), steps=max(2, 2 * self.num + 1), device=x.device
            ).round().long()
            x_eval = x_eval[sample_ids]
            if hasattr(parent, "_numeric_response"):
                y_eval = parent._numeric_response(x_eval.to(parent.grid.device)).to(self.grid.device)
            else:
                _, _, _, parent_postspline = parent(x_eval.to(parent.grid.device))
                y_eval = parent_postspline.permute(0, 2, 1).to(self.grid.device)

        self.grid.data = extend_grid(core_grid, k_extend=self.k)
        self.coef.data = self._fit_coef_from_targets(x_eval, y_eval)

    def get_subset(self, in_id, out_id):
        spb = FastKANLayer(
            len(in_id),
            len(out_id),
            self.num,
            self.k,
            base_fun=self.base_fun,
            grid_eps=self.grid_eps,
            sparse_init=False,
            denominator=float(torch.mean(self.denominator).item()),
            den_trainable=self.log_denominator.requires_grad,
        ).to(self.device)

        in_idx = torch.as_tensor(in_id, dtype=torch.long, device=self.grid.device)
        out_idx = torch.as_tensor(out_id, dtype=torch.long, device=self.grid.device)

        spb.grid.data = self.grid[in_idx]
        spb.coef.data = self.coef[in_idx][:, out_idx]
        spb.scale_base.data = self.scale_base[in_idx][:, out_idx]
        spb.scale_sp.data = self.scale_sp[in_idx][:, out_idx]
        spb.mask.data = self.mask[in_idx][:, out_idx]
        spb.log_denominator.data = self.log_denominator[in_idx]
        return spb

    @torch.no_grad()
    def swap(self, i1, i2, mode="in"):
        def swap_(data, idx1, idx2, swap_mode="in"):
            if swap_mode == "in":
                data[idx1], data[idx2] = data[idx2].clone(), data[idx1].clone()
            elif swap_mode == "out":
                data[:, idx1], data[:, idx2] = data[:, idx2].clone(), data[:, idx1].clone()

        if mode == "in":
            swap_(self.grid.data, i1, i2, swap_mode="in")
            swap_(self.log_denominator.data, i1, i2, swap_mode="in")

        swap_(self.coef.data, i1, i2, swap_mode=mode)
        swap_(self.scale_base.data, i1, i2, swap_mode=mode)
        swap_(self.scale_sp.data, i1, i2, swap_mode=mode)
        swap_(self.mask.data, i1, i2, swap_mode=mode)
