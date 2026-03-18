"""symkan 结果导出与实验包读写工具。"""

import os
import pickle


def save_symbolic_summary(summary_df, csv_path: str = "kan_symbolic_summary.csv", encoding: str = "utf-8-sig"):
    """保存符号化汇总表到 CSV。

    Args:
        summary_df: 汇总结果 DataFrame。
        csv_path: 导出路径。
        encoding: 文件编码。

    Returns:
        str: 导出的 CSV 路径。
    """
    summary_df.to_csv(csv_path, index=False, encoding=encoding)
    return csv_path


def save_stage_logs(stage_df, csv_path: str = "kan_stage_logs.csv", encoding: str = "utf-8-sig"):
    """保存阶段训练日志到 CSV。

    Args:
        stage_df: 阶段日志 DataFrame。
        csv_path: 导出路径。
        encoding: 文件编码。

    Returns:
        str: 导出的 CSV 路径。
    """
    stage_df.to_csv(csv_path, index=False, encoding=encoding)
    return csv_path


def save_export_bundle(bundle: dict, path: str = "kan_export_bundle.pkl"):
    """将实验导出对象序列化为 pkl 文件。

    Args:
        bundle: 导出对象字典。
        path: 导出路径。

    Returns:
        str: 导出的文件路径。
    """
    with open(path, "wb") as f:
        pickle.dump(bundle, f, protocol=pickle.HIGHEST_PROTOCOL)
    return path


def load_export_bundle(path: str = "kan_export_bundle.pkl", *, trusted: bool = False):
    """读取导出的实验 bundle。

    Args:
        path: pkl 文件路径。
        trusted: 仅当该 pickle 文件由当前用户本地生成且来源可信时设为 ``True``。

    Returns:
        dict: 反序列化后的导出对象。

    Raises:
        FileNotFoundError: 当文件不存在时抛出。
        ValueError: 当调用方未显式确认该 pickle 文件可信时抛出。
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
