"""Result export and experiment bundle utilities for symkan."""

import os
import pickle


def save_symbolic_summary(summary_df, csv_path: str = "kan_symbolic_summary.csv", encoding: str = "utf-8-sig"):
    """Save the symbolic summary table to CSV.

    Args:
        summary_df: Summary DataFrame.
        csv_path: Output path.
        encoding: File encoding.

    Returns:
        str: Path of the exported CSV.
    """
    summary_df.to_csv(csv_path, index=False, encoding=encoding)
    return csv_path


def save_stage_logs(stage_df, csv_path: str = "kan_stage_logs.csv", encoding: str = "utf-8-sig"):
    """Save stage logs to CSV.

    Args:
        stage_df: Stage log DataFrame.
        csv_path: Output path.
        encoding: File encoding.

    Returns:
        str: Path of the exported CSV.
    """
    stage_df.to_csv(csv_path, index=False, encoding=encoding)
    return csv_path


def save_export_bundle(bundle: dict, path: str = "kan_export_bundle.pkl"):
    """Serialize an experiment bundle to a pickle file.

    Args:
        bundle: Export dictionary.
        path: Destination path.

    Returns:
        str: Path to the serialized bundle.
    """
    with open(path, "wb") as f:
        pickle.dump(bundle, f, protocol=pickle.HIGHEST_PROTOCOL)
    return path


def load_export_bundle(path: str = "kan_export_bundle.pkl", *, trusted: bool = False):
    """Deserialize an experiment bundle from disk.

    Args:
        path: Path to the pickle file.
        trusted: Must be True only for locally generated, trusted bundles.

    Returns:
        dict: Deserialized export bundle.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If ``trusted`` is False to protect against untrusted pickle.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    if not trusted:
        raise ValueError(
            "load_export_bundle() uses pickle deserialization and is unsafe for untrusted files; "
            "pass trusted=True only for bundles you created locally and trust."
        )
    with open(path, "rb") as f:
        return pickle.load(f)
