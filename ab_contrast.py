import pandas as pd

baseline = pd.read_csv("benchmark_ab/baseline/symkanbenchmark_runs.csv")
adaptive  = pd.read_csv("benchmark_ab/adaptive/symkanbenchmark_runs.csv")

cols = ["stage_seed", "enhanced_acc", "final_acc", "final_n_edge",
        "macro_auc", "validation_mean_r2", "symbolic_total_seconds"]

comp = (
    baseline[cols].set_index("stage_seed")
    .join(adaptive[cols].set_index("stage_seed"), lsuffix="_base", rsuffix="_adapt")
)

# 核心差值
for metric in ["final_acc", "macro_auc", "validation_mean_r2"]:
    comp[f"Δ{metric}"] = comp[f"{metric}_adapt"] - comp[f"{metric}_base"]

print("--- 对比结果 ---")
print("adaptive - baseline:")
print(comp[[c for c in comp.columns if c.startswith("Δ")]].to_string())
print("\n--- 均值 ---")
print(comp[[c for c in comp.columns if c.startswith("Δ")]].mean())