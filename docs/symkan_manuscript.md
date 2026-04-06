# SymKAN Manuscript

## Abstract

Kolmogorov-Arnold Networks (KANs) have renewed interest in interpretable function learning, while symbolic regression and symbolic model extraction have continued to supply routes from numerical predictors to explicit formulas [1]-[5]. SymKAN is positioned at the intersection of these two lines, but its scope is narrower than either a new KAN training method or a generic symbolic regression engine. The maintained objective of this repository is to organize post-training KAN symbolization as a reproducible, comparable, and auditable engineering pipeline that preserves the numeric training semantics of the reference KAN implementation while making downstream symbolic claims traceable to stable artifacts. In this formulation, the central research object is not an isolated symbolic search routine, but the full path from configuration control and stagewise readiness to shared symbolic preparation, backend-specific symbolic completion, numerical validation, and structured export.

The present manuscript therefore treats SymKAN as a methodology for disciplined empirical study rather than as a universal performance claim. Within the repository, the internal evidence base is restricted to the maintained overall engineering rerun of March 18, 2026, the maintained ablation and LayerwiseFT reports, and the paired backend-compare rerun of April 1, 2026. These internal sources are used only for repository-specific empirical claims; external literature is used to position the task relative to KANs, symbolic regression, post-hoc symbolic model extraction, and reproducibility-oriented benchmark design [1]-[8].

Under that evidence policy, three findings remain defensible. First, the March 18 engineering rerun establishes that the current `baseline` path remains the quality-default engineering configuration, even though alternative strategy variants alter cost profiles. Second, the maintained ablation and LayerwiseFT studies show that `stagewise_train` functions as a readiness mechanism for later symbolization, progressive pruning primarily governs complexity, input compaction trades symbolic cost against fidelity, and LayerwiseFT does not yet justify a default-on role in the present two-layer KAN setting. Third, when shared numeric state, trace rhythm, and shared symbolic preparation are all aligned, the April 1 paired comparison supports a backend-only interpretation of the ICBR variant: the layered paired slice yields an approximately `1.75x` reduction in `symbolic_core_seconds` together with improved task quality, whereas the FAST_LIB paired slice yields an approximately `2.35x` reduction in core symbolic time with near-flat quality. The `baseline_icbr_fulllib` slice remains supplementary single-arm evidence rather than paired fairness evidence.

The strongest contribution that can presently be claimed for SymKAN is therefore methodological. The repository defines explicit configuration boundaries, phase boundaries, fairness gates, and artifact requirements for post-training KAN symbolization. This contribution is narrower than a blanket superiority claim, but it is also more durable: it specifies when a symbolic comparison is meaningful, what evidence can support it, and how the resulting claims can be audited.

## 1. Introduction

KANs have recently been introduced as an interpretable alternative to conventional multilayer perceptrons, with learnable functions placed on edges rather than fixed node activations [1]. At the same time, symbolic regression has developed along several complementary directions, including physics-inspired search procedures, neural-guided formula search, and post-hoc extraction of compact symbolic models from trained numerical systems [2]-[5]. These lines of work share an ambition for interpretable functional structure, but they do not solve the same problem. A system that trains a KAN numerically and then attempts to expose a symbolic representation faces a different methodological burden from a system that searches expressions directly from raw samples.

That burden becomes especially visible once exploratory notebook work is asked to support stable comparison, thesis writing, or paper-style reporting. In an exploratory environment, numeric training, pruning, symbolic search, validation, and interpretation are easily mixed into one flexible workflow. This flexibility is useful at the prototype stage, but it becomes problematic when the task shifts toward cross-seed aggregation, backend comparison, or claim reuse across reports and presentations. Reproducibility guidance in machine learning has repeatedly emphasized that claims degrade when procedural detail, artifact discipline, and comparison protocol are left implicit [6]-[8]. In symbolic regression, the benchmarking literature has likewise shown that method comparisons are highly sensitive to evaluation protocol, representation choices, and reporting discipline [2], [5], [7].

SymKAN addresses this problem by narrowing the object of study. It does not attempt to replace KAN numeric training, nor does it present itself as a generic symbolic regression package. Instead, it treats post-training KAN symbolization as a structured experimental pipeline: configuration sources are unified, readiness for symbolization is established explicitly, shared symbolic preparation is separated from backend-specific completion, exported formulas are numerically checked, and every claim must be recoverable from stable files. The repository is therefore designed not merely to "run symbolization," but to state under what conditions a symbolic result is attributable to a backend, to a preparation stage, or to a higher-level engineering decision.

This manuscript is written with that narrower objective in mind. It is not a runbook, and it does not replace the role of [design.md](design.md) as the boundary document for design logic and permissible claims. Rather, it reorganizes the maintained internal evidence into a paper-style narrative that asks two questions. Why does the current default pipeline take its present form? And, once the shared stages are aligned, how far can the repository legitimately go in writing about ICBR backend gains? The rest of the document answers these questions using external literature for conceptual positioning and repository-maintained reports for empirical support.

## 2. Problem Formulation and Design Constraints

### 2.1 Post-training KAN Symbolization as the Experimental Object

The experimental object considered here is a trained or trainable KAN that must still be driven into a regime suitable for downstream symbolization. This differs both from direct symbolic regression over raw observations and from purely numeric supervised learning. In symbolic-regression terms, the repository sits closer to the post-hoc or hybrid end of the design space, where a learned numerical model and a symbolic recovery procedure coexist [2]-[5]. In KAN terms, the repository keeps the numeric model family intact and studies how symbolic behavior can be exposed and compared after the numeric model has been prepared [1].

Formally, let

$$
\mathcal{D} = (X_{\text{train}}, Y_{\text{train}}, X_{\text{test}}, Y_{\text{test}})
$$

denote the dataset bundle and let `c = AppConfig(...)` denote the unified configuration object. The current pipeline first produces a numeric model

$$
M_{\text{num}} = T(\mathcal{D}, c_{\text{stagewise}}),
$$

then converts it into a prepared symbolic state

$$
B = P(M_{\text{num}}, c_{\text{shared}}),
$$

then performs backend-specific completion

$$
M_{\text{sym}} = S(B, c_{\text{backend}}),
$$

and finally exports evaluated artifacts

$$
R = E(M_{\text{sym}}, \mathcal{D}, c_{\text{eval}}).
$$

This decomposition is intentionally more explicit than the informal "train, symbolize, and inspect" workflow that often appears in exploratory notebook practice. Its purpose is not mathematical ornament. It is a way of forcing every downstream comparison to identify the stage at which variation enters. A backend claim is meaningful only if the differences are restricted to `c_backend`; a readiness claim is meaningful only if it is tied to `T`; an artifact-quality claim is meaningful only if it can be read back from `R`.

### 2.2 Four Non-negotiable Constraints

The first constraint is compatibility. The repository must preserve the numeric training semantics associated with the reference KAN implementation and remain compatible with notebook use, `python -m scripts.*` execution, and CSV-oriented downstream reporting. The second constraint is controllability. Stagewise training, pruning, input compaction, shared symbolic preparation, and backend-specific completion must remain distinguishable in both implementation and reporting; otherwise, the resulting experiments cannot support causal or mechanistic interpretation. The third constraint is comparability. A backend comparison is only admissible when the shared numeric state, the trace rhythm, and the shared symbolic-prep state are aligned. The fourth constraint is traceability. Claims are not allowed to rest on terminal output or narrative memory alone; they must resolve to files such as `symkanbenchmark_runs.csv`, `kan_stage_logs.csv`, `symbolize_trace.csv`, `formula_validation.csv`, `metrics.json`, and the paired compare artifacts.

These four constraints are consistent with the broader literature on reproducible machine learning and benchmark design. Reproducibility reports have argued that evaluation claims lose meaning when procedural information and artifacts are underspecified [6]. Benchmark-oriented methodological work likewise emphasizes that the validity of comparison depends on well-defined targets, controlled variance, and explicit reporting of assumptions [5], [7], [8]. Within SymKAN, these concerns translate into a practical rule: the repository should be understood as an engineering methodology for post-training KAN symbolization, not as a claim that one backend or one strategy variant universally dominates all alternatives.

## 3. Methods

### 3.1 Unified Configuration Boundary and Readiness Formation

The repository centers its runtime semantics on `symkan.config.AppConfig`, which absorbs notebook-style parameters, YAML-driven batch runs, and script-level overrides into one validated object. This unification is methodologically important because it reduces the number of hidden execution paths. When the same symbolic comparison could otherwise be launched from a notebook, a CLI, or a batch script with slightly different defaults, it becomes difficult to determine whether an observed difference is scientific, infrastructural, or accidental. A single configuration boundary makes cache-key definition, report synchronization, and claim auditing materially easier, which is precisely the kind of procedural discipline that reproducibility-oriented ML guidance recommends [6]-[8].

On top of this boundary, `stagewise_train` is treated as a readiness mechanism rather than as an accessory optimizer. The role of stagewise training in this repository is to move the numerical KAN toward a region in which downstream symbolic processing remains manageable. That interpretation is narrower than saying that stagewise training always improves final task accuracy, but it is also more faithful to the maintained evidence. The question asked here is whether later symbolization can proceed under controlled complexity, not whether another few points of training accuracy can be extracted at any cost.

### 3.2 Shared Symbolic Preparation and Backend-specific Completion

The repository's most consequential methodological decision is the internal decomposition of `symbolize_pipeline` into a shared symbolic-prep phase and a backend-specific completion phase. This separation echoes a broader theme in symbolic-model literature: if one wishes to compare competing symbolic procedures, it is necessary to control the state inherited from the numerical model rather than treat the whole symbolic path as an indivisible black box [3]-[5]. In SymKAN, the shared stage performs progressive pruning, input compaction, pre-symbolic fitting, and trace construction; only after those steps does the pipeline branch into the `baseline` or `icbr` backend.

This decomposition has three direct consequences. First, it narrows the interpretation of backend differences to the point where a backend-only claim can be audited. Second, it permits the repository to define distinct cache layers, one for the numerical model and one for the prepared symbolic bundle, without conflating their semantics. Third, it turns fairness from an informal promise into a file-level contract, because the paired compare outputs can check whether the shared stages were in fact aligned. In other words, the decomposition is not merely an implementation refactor. It is the mechanism that makes the phrase "backend-only comparison" empirically meaningful in this repository.

### 3.3 Validation, Export, and Artifact Discipline

The pipeline does not terminate when a plausible expression is found. It continues through numerical validation and structured export, reflecting the common lesson from symbolic-regression benchmarks that interpretable formulas must still be evaluated under explicit metrics and reporting rules [2], [5]. In SymKAN, the maintained artifact family includes `symkanbenchmark_runs.csv`, `kan_stage_logs.csv`, `symbolize_trace.csv`, `formula_validation.csv`, `metrics.json`, `variant_summary.csv`, `pairwise_delta_summary.csv`, `trace_summary.csv`, and the `baseline_icbr_*` compare files used for paired backend audits.

Table 1 summarizes the main methodological components used throughout this manuscript. The table is deliberately narrow. It is not intended to describe every implementation detail; it is meant to clarify which components carry methodological meaning and which internal evidence families they are allowed to support.

| Pipeline component | Repository locus | Methodological role in this manuscript | Internal evidence family |
| --- | --- | --- | --- |
| Unified configuration boundary | `symkan.config.AppConfig` | Keeps notebook, CLI, and batch semantics inside one validated contract | repository architecture and usage docs |
| Readiness formation | `stagewise_train` | Establishes symbolization-ready numeric states | maintained ablation report |
| Complexity governance | progressive pruning and input compaction | Separates complexity control from backend choice | maintained ablation report |
| Backend fairness gate | shared symbolic-prep vs backend completion | Restricts backend differences to the completion stage | April 1, 2026 paired compare report |
| Structured validation and export | validation tables and compare artifacts | Forces claims to resolve to inspectable files | March 18 and April 1, 2026 rerun reports |

## 4. Experimental Protocol and Evidence Hierarchy

### 4.1 Dataset, Model Skeleton, and Metrics

The maintained internal results discussed here are based primarily on the repository's prepared MNIST feature setting, with `60000` training samples, `10000` test samples, and stagewise seeds `42`, `52`, and `62`. The overall engineering rerun and the later backend compare share the same base model skeleton, including `inner_dim = 16`, `grid = 5`, `k = 3`, and `top_k = 120`. This stability matters because the manuscript is not attempting to compare unrelated training setups. It is attempting to ask what can be learned when the same engineering substrate is observed through different symbolic-processing choices.

The maintained metrics are grouped by role. `final_acc` and `macro_auc` are task-quality indicators. `final_n_edge` and `expr_complexity_mean` describe structural size. `validation_mean_r2` measures agreement between exported formulas and model outputs. `symbolic_core_seconds`, `symbolize_wall_time_s`, and `run_total_wall_time_s` distinguish core backend time, broader symbolic-stage wall time, and end-to-end runtime. This separation is essential: a repository that treats all runtime fields as interchangeable would undermine the very fairness boundary it claims to enforce.

### 4.2 Internal Evidence Hierarchy

The internal evidence hierarchy is the central discipline that prevents this manuscript from overstating its case. The maintained engineering rerun of March 18, 2026 supports statements about the current engineering baseline and strategy-level trade-offs. The maintained ablation report supports statements about module responsibilities. The improved LayerwiseFT report supports statements about whether LayerwiseFT should presently be considered default-worthy. The paired rerun of April 1, 2026 supports backend-only claims only where the shared-state audit confirms alignment. Finally, the `baseline_icbr_fulllib` branch supports only supplementary single-arm observations.

Table 2 makes this hierarchy explicit. Its purpose is not stylistic. It is a writing constraint that determines what kinds of sentences are licit in the results and discussion sections.

| Evidence line | Main internal source | Claims it may support | Claims it may not support |
| --- | --- | --- | --- |
| Overall engineering rerun | March 18, 2026 rerun report and archive | current baseline, strategy trade-offs, why `baseline` remains the quality-default path | backend-only conclusions about ICBR |
| Module ablation | maintained ablation report and archive | roles of stagewise training, pruning, input compaction, and LayerwiseFT | backend dominance claims |
| LayerwiseFT study | maintained improved LayerwiseFT report | current non-default status of LayerwiseFT in the two-layer setting | replacement for baseline or backend evidence |
| Layered paired compare | April 1, 2026 paired compare report and archive | most conservative backend-only evidence under aligned shared state | general law over all library settings |
| FAST_LIB paired compare | April 1, 2026 fast-library compare report and archive | speed boundary under expanded libraries with aligned shared state | replacement for layered fairness evidence |
| `baseline_icbr_fulllib` slice | April 1, 2026 supplementary archive | single-arm feasibility and supplementary observations | paired fairness proof |

## 5. Results I: Why the Default Pipeline Stands

### 5.1 Engineering Baseline and Strategy-level Comparison

The March 18 engineering rerun first establishes that the current main pipeline is no longer represented only by exploratory outputs. The three-seed mean of `benchmark_runs/symkanbenchmark_runs.csv` is `final_acc = 0.769167`, `final_n_edge = 87.666667`, `macro_auc = 0.956765`, `stage_total_seconds = 45.172832`, `symbolic_core_seconds = 35.651883`, `symbolize_wall_time_s = 75.699789`, `run_total_wall_time_s = 140.332975`, and `validation_mean_r2 = -0.630428`. These values should be read as an engineering anchor rather than as a claim of general optimality.

Within the same rerun family, the strategy variants `baseline`, `adaptive`, and `adaptive_auto` yield the following mean results.

| Variant | `final_acc` | `final_n_edge` | `macro_auc` | `run_total_wall_time_s` | `symbolic_core_seconds` | `symbolize_wall_time_s` | `validation_mean_r2` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | 0.777433 | 88.666667 | 0.956107 | 153.470521 | 33.867724 | 88.751556 | -0.672284 |
| `adaptive` | 0.742533 | 86.000000 | 0.945706 | 209.552334 | 47.499191 | 104.127099 | -0.646339 |
| `adaptive_auto` | 0.751467 | 89.000000 | 0.946249 | 130.715215 | 33.259280 | 74.526931 | -0.552361 |

At the level of result presentation, two facts are sufficient. `baseline` retains the highest `final_acc` and `macro_auc` among the three strategy variants. `adaptive_auto` lowers total runtime relative to `baseline`, but does so without replacing `baseline` as the quality-leading path. The manuscript therefore treats `baseline` as the current quality-default path because that is what the maintained internal evidence supports, not because of inherited convention.

### 5.2 Module Responsibilities from the Maintained Ablation Study

The maintained ablation report clarifies why the default pipeline contains its present set of modules. The relevant mean statistics are reproduced below.

| Variant | `final_acc` | `macro_auc` | expression complexity | `validation_mean_r2` | effective input dimension | symbolic time (s) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `full` | 0.7807 | 0.9548 | 126.90 | -0.6135 | 57.67 | 33.58 |
| `wostagewise` | 0.4430 | 0.8379 | 48.44 | -0.7657 | 23.00 | 16.64 |
| `wopruning` | 0.8017 | 0.9639 | 194.33 | -0.4976 | 70.00 | 43.51 |
| `wocompact` | 0.7577 | 0.9491 | 120.10 | +0.0275 | 120.00 | 41.34 |
| `wolayerwiseft` | 0.7838 | 0.9544 | 126.90 | -0.5937 | 57.67 | 20.41 |

Three observations belong in the results section itself. Removing stagewise training sharply lowers both `final_acc` and `macro_auc`. Removing pruning raises quality metrics but also inflates structural complexity and symbolic time. Removing input compaction improves `validation_mean_r2` while doubling effective input dimension and increasing symbolic-stage runtime. These results show that the repository's default path is not built from interchangeable "boosters." Each module carries a distinct cost-quality role.

### 5.3 Current Status of LayerwiseFT

The improved LayerwiseFT study isolates the present role of LayerwiseFT under the two-layer KAN configuration used throughout the maintained evidence family. The relevant means are listed below.

| Variant | `final_acc` | `macro_auc` | expression complexity | `validation_mean_r2` | symbolic time (s) | stagewise time (s) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `full` | 0.7807 | 0.9548 | 126.90 | -0.6135 | 33.58 | 40.33 |
| `layerwiseft_esreg` | 0.7807 | 0.9548 | 126.90 | -0.6135 | 33.28 | 40.02 |
| `wolayerwiseft` | 0.7838 | 0.9544 | 126.90 | -0.5937 | 20.41 | 39.54 |

The narrow factual conclusion is that `layerwiseft_esreg` does not establish a stable quality advantage over `wolayerwiseft`, while `wolayerwiseft` remains materially cheaper in symbolic-stage time. This does not prove that LayerwiseFT is useless in principle. It does, however, justify treating LayerwiseFT as non-default within the present maintained setting.

## 6. Results II: Backend Comparison, Gain, and Boundary

### 6.1 Layered Paired Compare as the Main Fairness Evidence

The April 1 layered paired slice is the repository's most conservative backend-only evidence because the shared-state audit confirms alignment across seeds. In `baseline_icbr_shared_check.csv`, all three seeds report `shared_numeric_aligned = True`, `trace_aligned = True`, and `shared_symbolic_prep_aligned = True`. Under that gate, the paired means are as follows.

| Variant | `final_acc` | `final_n_edge` | `macro_auc` | `run_total_wall_time_s` | `symbolic_core_seconds` | `symbolize_wall_time_s` | `validation_mean_r2` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline` | 0.777467 | 88.333333 | 0.951264 | 69.864499 | 33.297856 | 68.013948 | -0.486988 |
| `baseline_icbr` | 0.788667 | 88.333333 | 0.961440 | 62.462939 | 19.013927 | 60.000633 | -0.409281 |

The results section need only state the directly supported facts. The ICBR backend reduces mean `symbolic_core_seconds` from `33.297856` to `19.013927`, a ratio of approximately `1.751763x`. The two variants share the same mean `final_n_edge`. The ICBR branch also improves `final_acc`, `macro_auc`, and `validation_mean_r2` in this paired slice. Because the shared-state gate is satisfied, these differences may be treated as backend-level evidence rather than as a conflation of earlier-stage variation.

### 6.2 FAST_LIB Paired Compare as the Expanded-library Speed Boundary

The paired FAST_LIB slice retains the shared-state alignment condition and therefore remains admissible as backend-only evidence. Its means are reproduced below.

| Variant | `final_acc` | `final_n_edge` | `macro_auc` | `run_total_wall_time_s` | `symbolic_core_seconds` | `symbolize_wall_time_s` | `validation_mean_r2` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline_fastlib` | 0.794000 | 88.333333 | 0.962537 | 112.233492 | 75.187859 | 110.162969 | -0.451777 |
| `baseline_icbr_fastlib` | 0.793233 | 88.333333 | 0.962634 | 69.944645 | 31.990798 | 67.817348 | -0.456489 |

Here the factual pattern differs from the layered paired slice. The mean `symbolic_core_seconds` ratio is approximately `2.350452x` in favor of the ICBR backend. Structural size remains matched. Quality differences are very small: `final_acc` differs by `-0.000767`, `macro_auc` differs only at the third decimal place, and `validation_mean_r2` does not improve systematically. The repository can therefore use this slice to support an expanded-library speed boundary, but not to restate the stronger "speed plus quality improvement" sentence that is admissible in the layered paired case.

### 6.3 Full-library Single-arm Slice as Supplementary Evidence

The `baseline_icbr_fulllib` branch is kept because it shows that the full-library path remains executable under the ICBR backend, but it does not have a paired baseline companion and therefore does not meet the repository's fairness standard for backend-only inference. Its means are listed below.

| Variant | `final_acc` | `final_n_edge` | `macro_auc` | `final_target_mse` | `final_target_r2` | `symbolic_core_seconds` | `symbolize_wall_time_s` | `run_total_wall_time_s` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `baseline_icbr_fulllib` | 0.795433 | 88.333333 | 0.963225 | 0.035896 | 0.601003 | 35.218785 | 39.693965 | 41.757397 |

The result is therefore reported only as supplementary feasibility evidence. It shows that the full-library path remains operational and produces strong single-arm numbers under ICBR. It does not justify a paired fairness claim, and this manuscript does not treat it as one.

## 7. Discussion

The results jointly support a more disciplined interpretation of SymKAN than the one suggested by a simple leaderboard narrative. The current default pipeline is justified because the internal evidence separates four roles that would otherwise be confounded. Stagewise training establishes readiness for symbolization; pruning governs complexity; input compaction trades symbolic cost against fidelity; and LayerwiseFT remains optional under the current two-layer setting. None of these statements requires a generalized claim about KANs as a model class. They are local methodological conclusions about how this repository presently organizes post-training symbolization.

The backend comparison story is equally constrained. Prior work on symbolic regression and symbolic model extraction makes it clear that search procedure, inherited representation, and evaluation protocol all influence the apparent quality of an interpretable formula [2]-[5]. Reproducibility and benchmark-design literature further warns that comparisons become unstable when variance sources and leakage channels are not isolated [6]-[8]. In that context, the main value of SymKAN is not simply that the ICBR backend can be faster. It is that the repository defines a concrete audit trail for deciding when "faster" can be interpreted as a backend property. The shared symbolic-prep split and the paired audit artifacts are the instruments that make this sentence defensible.

This perspective also explains why the manuscript refuses to collapse all maintained results into one undifferentiated table. The March 18 rerun, the ablation study, the LayerwiseFT study, the layered paired compare, the FAST_LIB paired compare, and the supplementary full-library slice answer different questions at different evidential strengths. A manuscript that writes them as if they all carried the same inferential weight would erase the distinction between engineering baselines, module-responsibility evidence, and backend-only fairness evidence. The present document instead treats evidence hierarchy as part of the method itself.

## 8. Limitations and Conclusion

The present claims are bounded in several obvious ways. The maintained reruns rely on three seeds and should therefore be read as controlled engineering evidence rather than as large-sample statistical proof. The repository's object of study is limited to post-training KAN symbolization, so the conclusions do not automatically transfer to generic symbolic regression pipelines or to broader neuro-symbolic modeling regimes. The full-library branch remains single-arm evidence, which prevents the manuscript from extrapolating its observations into a universal backend claim. These limitations are not peripheral; they are the conditions that keep the repository's conclusions proportionate to its evidence.

Within those limits, the current manuscript can state three stable conclusions. First, SymKAN is most accurately understood as an engineering methodology for post-training KAN symbolization, organized around explicit configuration control, stage decomposition, and artifact discipline. Second, the default pipeline is not an arbitrary accumulation of modules; it is a maintained engineering compromise whose rationale is recoverable from the repository's overall rerun, ablation, and LayerwiseFT evidence lines. Third, once shared numeric state, trace rhythm, and shared symbolic preparation are aligned, the ICBR backend shows clear symbolic-core speed advantages in both the layered and FAST_LIB paired settings, although the strength and form of the quality claim differ between those two slices.

The most defensible one-sentence summary is therefore methodological rather than triumphalist: SymKAN establishes a reproducible, comparable, and auditable framework for post-training KAN symbolization. That claim is narrower than "a universally better KAN," but it is exactly the level of claim that the maintained evidence can support today.

## References

1. Z. Liu, Y. Wang, S. Vaidya, F. Ruehle, J. Halverson, M. Soljacic, T. Y. Hou, and M. Tegmark, "KAN: Kolmogorov-Arnold Networks," arXiv, 2024. DOI: [10.48550/arXiv.2404.19756](https://doi.org/10.48550/arXiv.2404.19756).
2. S.-M. Udrescu and M. Tegmark, "AI Feynman: A physics-inspired method for symbolic regression," *Science Advances*, vol. 6, no. 16, eaay2631, 2020. DOI: [10.1126/sciadv.aay2631](https://doi.org/10.1126/sciadv.aay2631).
3. M. Cranmer, A. Sanchez-Gonzalez, P. Battaglia, R. Xu, K. Cranmer, D. Spergel, and S. Ho, "Discovering Symbolic Models from Deep Learning with Inductive Biases," arXiv, 2020. DOI: [10.48550/arXiv.2006.11287](https://doi.org/10.48550/arXiv.2006.11287).
4. B. K. Petersen, M. Landajuela, T. N. Mundhenk, C. Santiago, S. Kim, and J. T. Kim, "Deep symbolic regression: Recovering mathematical expressions from data via risk-seeking policy gradients," arXiv, 2019. DOI: [10.48550/arXiv.1912.04871](https://doi.org/10.48550/arXiv.1912.04871).
5. W. La Cava, P. Orzechowski, B. Burlacu, F. O. de Franca, M. Virgolin, Y. Jin, M. Kommenda, and J. H. Moore, "Contemporary Symbolic Regression Methods and their Relative Performance," *Advances in Neural Information Processing Systems*, vol. 34, 2021. Available: [NeurIPS proceedings](https://proceedings.neurips.cc/paper/2021/hash/3edc8d8569a6c95fbd47c060b9d8e28b-Abstract.html).
6. J. Pineau, P. Vincent-Lamarre, K. Sinha, V. Lariviere, A. Beygelzimer, F. d'Alche-Buc, E. B. Fox, and H. Larochelle, "Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program)," arXiv, 2020. DOI: [10.48550/arXiv.2003.12206](https://doi.org/10.48550/arXiv.2003.12206).
7. J. Thiyagalingam, M. Shankar, G. Fox, and T. Hey, "Scientific machine learning benchmarks," *Nature Reviews Physics*, vol. 4, pp. 413-420, 2022. DOI: [10.1038/s42254-022-00441-7](https://doi.org/10.1038/s42254-022-00441-7).
8. S. Kapoor and A. Narayanan, "Leakage and the reproducibility crisis in machine-learning-based science," *Patterns*, vol. 4, no. 9, 100804, 2023. DOI: [10.1016/j.patter.2023.100804](https://doi.org/10.1016/j.patter.2023.100804).
