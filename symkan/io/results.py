import os
import pickle


def save_symbolic_summary(summary_df, csv_path: str = "kan_symbolic_summary.csv", encoding: str = "utf-8-sig"):
    """@brief 保存符号化汇总表到 CSV。

    @param summary_df 汇总结果 DataFrame。
    @param csv_path 导出路径。
    @param encoding 文件编码。
    @return str 导出的 CSV 路径。
    """
    summary_df.to_csv(csv_path, index=False, encoding=encoding)
    return csv_path


def save_stage_logs(stage_df, csv_path: str = "kan_stage_logs.csv", encoding: str = "utf-8-sig"):
    """@brief 保存阶段训练日志到 CSV。

    @param stage_df 阶段日志 DataFrame。
    @param csv_path 导出路径。
    @param encoding 文件编码。
    @return str 导出的 CSV 路径。
    """
    stage_df.to_csv(csv_path, index=False, encoding=encoding)
    return csv_path


def save_export_bundle(bundle: dict, path: str = "kan_export_bundle.pkl"):
    """@brief 将实验导出对象序列化为 pkl 文件。

    @param bundle 导出对象字典。
    @param path 导出路径。
    @return str 导出的文件路径。
    """
    with open(path, "wb") as f:
        pickle.dump(bundle, f)
    return path


def load_export_bundle(path: str = "kan_export_bundle.pkl"):
    """@brief 读取导出的实验 bundle。

    @param path pkl 文件路径。
    @return dict 反序列化后的导出对象。
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, "rb") as f:
        return pickle.load(f)
