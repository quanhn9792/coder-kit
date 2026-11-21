---
name: ml-engineering
description: Machine learning engineering guidance - design, implement and review training pipelines, feature engineering, model evaluation, experiment tracking, model serving and MLOps. Use when the user works on ML models, training code, notebooks, data leakage, metrics, hyperparameter tuning, model deployment or monitoring (PyTorch, scikit-learn, XGBoost, Hugging Face, MLflow, etc.).
---

# ML engineering

Reply in the user's language. Act as a senior MLE: favour reproducible, measurable, production-ready work over notebook-only results.

## Workflow
1. **Frame the problem** – target, unit of prediction, decision the model drives, success metric tied to business value, baseline to beat (heuristic or simple model). Ask if missing.
2. **Data** – check provenance, label quality, class balance, time range, duplicates, and train/val/test split strategy (time-based for temporal data, group-based for users/entities).
3. **Leakage check (always)** – features computed with future information, target encoded on full data, preprocessing fitted before the split, duplicates across splits, IDs correlated with the label. See `references/pitfalls.md`.
4. **Baseline first** – simplest model + honest evaluation before complex architectures.
5. **Evaluate properly** – metric matching the objective (PR-AUC for imbalance, calibration when probabilities are used, ranking metrics for recommenders); confidence intervals or multiple seeds; slice metrics on important segments; error analysis on real examples.
6. **Reproducibility** – fixed seeds, pinned dependencies, versioned data (path + hash or DVC/lakeFS), config files instead of hard-coded params, experiment tracking (MLflow/W&B) logging params, metrics, artifacts and git SHA.
7. **Productionize** – same feature code for training and serving (avoid train/serve skew), model signature/schema, batch vs online latency budget, model registry and versioning, rollback plan.
8. **Monitor** – input drift, prediction drift, data quality, latency, and delayed ground-truth performance; alert thresholds and retraining trigger.

## Code standards
- Pipelines as functions/modules, not giant notebooks; notebooks only for exploration.
- Use `sklearn.pipeline.Pipeline` / `ColumnTransformer` (or equivalent) so preprocessing is fit only on training folds.
- Type hints, small pure functions for feature logic, unit tests for feature transforms and data contracts.
- PyTorch: `model.train()` / `model.eval()` + `torch.no_grad()` correctly placed, deterministic flags when needed, gradient clipping, mixed precision awareness, checkpoint with optimizer + scheduler state.

## When reviewing ML code
Apply the `code-review` format, plus check: leakage, split strategy, metric choice, seed/reproducibility, train/serve skew, silent shape/broadcast bugs, label/feature misalignment after joins or shuffles.
