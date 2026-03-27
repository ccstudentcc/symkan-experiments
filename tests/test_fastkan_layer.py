import torch

from kan.FastKANLayer import FastKANLayer


def test_fastkan_layer_forward_shapes_and_mask_effect() -> None:
    torch.manual_seed(0)
    layer = FastKANLayer(in_dim=4, out_dim=3, num=6, k=3, device="cpu")
    x = torch.randn(16, 4)

    y, preacts, postacts, postspline = layer(x)
    assert y.shape == (16, 3)
    assert preacts.shape == (16, 3, 4)
    assert postacts.shape == (16, 3, 4)
    assert postspline.shape == (16, 3, 4)

    with torch.no_grad():
        layer.mask.data[0, 0] = 0.0
    _, _, postacts_masked, _ = layer(x)
    assert torch.allclose(postacts_masked[:, 0, 0], torch.zeros_like(postacts_masked[:, 0, 0]), atol=1e-6)
    assert int((layer.mask > 0).sum().item()) == 11


def test_fastkan_layer_get_subset_still_runs_forward() -> None:
    torch.manual_seed(1)
    layer = FastKANLayer(in_dim=5, out_dim=4, num=5, k=3, device="cpu")
    in_id = [1, 3]
    out_id = [0, 2]
    subset = layer.get_subset(in_id, out_id)

    x = torch.randn(10, len(in_id))
    y, preacts, postacts, postspline = subset(x)

    assert y.shape == (10, len(out_id))
    assert preacts.shape == (10, len(out_id), len(in_id))
    assert postacts.shape == (10, len(out_id), len(in_id))
    assert postspline.shape == (10, len(out_id), len(in_id))
    assert torch.allclose(subset.mask, layer.mask[in_id][:, out_id])


def test_fastkan_layer_grid_update_initialize_and_swap() -> None:
    torch.manual_seed(2)
    parent = FastKANLayer(in_dim=3, out_dim=2, num=5, k=3, device="cpu")
    child = FastKANLayer(in_dim=3, out_dim=2, num=8, k=3, device="cpu")
    x = torch.randn(64, 3)

    parent.update_grid_from_samples(x, mode="sample")
    child.initialize_grid_from_parent(parent, x, mode="sample")

    y_parent, _, _, _ = parent(x)
    y_child, _, _, _ = child(x)
    assert y_parent.shape == (64, 2)
    assert y_child.shape == (64, 2)
    assert parent.grid.shape == (3, parent.num + 1 + 2 * parent.k)
    assert child.grid.shape == (3, child.num + 1 + 2 * child.k)

    coef_before = child.coef.detach().clone()
    child.swap(0, 1, mode="in")
    assert torch.allclose(child.coef[0], coef_before[1])
    assert torch.allclose(child.coef[1], coef_before[0])

    coef_before_out = child.coef.detach().clone()
    child.swap(0, 1, mode="out")
    assert torch.allclose(child.coef[:, 0], coef_before_out[:, 1])
    assert torch.allclose(child.coef[:, 1], coef_before_out[:, 0])
