param(
  [string]$PythonExe = "python",
  [string]$OutRoot = "outputs/rerun_v2_engine_safe_$(Get-Date -Format 'yyyyMMdd')"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-Step {
  param(
    [Parameter(Mandatory = $true)][string]$Title,
    [Parameter(Mandatory = $true)][string[]]$Args
  )

  Write-Host $Title
  & $PythonExe @Args
  if ($LASTEXITCODE -ne 0) {
    throw "Step failed with exit code ${LASTEXITCODE}: $Title"
  }
}

Invoke-Step "[1/6] Main benchmark rerun..." @(
  "-m", "scripts.symkanbenchmark",
  "--tasks", "all",
  "--stagewise-seeds", "42,52,62",
  "--config", "configs/symkanbenchmark.default.yaml",
  "--output-dir", "$OutRoot/benchmark_runs",
  "--quiet"
)

Invoke-Step "[2/6] A/B baseline..." @(
  "-m", "scripts.symkanbenchmark",
  "--tasks", "full",
  "--stagewise-seeds", "42,52,62",
  "--config", "configs/benchmark_ab/baseline.yaml",
  "--output-dir", "$OutRoot/benchmark_ab/baseline",
  "--quiet"
)

Invoke-Step "[3/6] A/B adaptive..." @(
  "-m", "scripts.symkanbenchmark",
  "--tasks", "full",
  "--stagewise-seeds", "42,52,62",
  "--config", "configs/benchmark_ab/adaptive.yaml",
  "--output-dir", "$OutRoot/benchmark_ab/adaptive",
  "--quiet"
)

Invoke-Step "[4/6] A/B adaptive_auto..." @(
  "-m", "scripts.symkanbenchmark",
  "--tasks", "full",
  "--stagewise-seeds", "42,52,62",
  "--config", "configs/benchmark_ab/adaptive_auto.yaml",
  "--output-dir", "$OutRoot/benchmark_ab/adaptive_auto",
  "--quiet"
)

Invoke-Step "[5/6] A/B comparison aggregation..." @(
  "-m", "scripts.benchmark_ab_compare",
  "--root", "$OutRoot/benchmark_ab",
  "--baseline", "baseline",
  "--variants", "adaptive,adaptive_auto",
  "--output", "$OutRoot/benchmark_ab/comparison"
)

Invoke-Step "[6/6] Ablation rerun + aggregate..." @(
  "-m", "scripts.ablation_runner",
  "--config", "configs/ablation_runner.default.yaml",
  "--stagewise-seeds", "42,52,62",
  "--output-dir", "$OutRoot/benchmark_ablation",
  "--quiet"
)

Write-Host "Done. Outputs are under: $OutRoot"
