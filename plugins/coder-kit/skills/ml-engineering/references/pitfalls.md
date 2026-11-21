# Common ML pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Preprocessing fit on full data | Val score drops in prod | Fit scaler/encoder inside pipeline on train only |
| Random split on time series | Great offline, bad online | Time-based split, walk-forward CV |
| Same user in train and test | Inflated metrics | GroupKFold by entity |
| Target leakage via feature | Suspiciously high AUC (>0.99) | Check feature timestamps vs label time; feature importance audit |
| Accuracy on imbalanced data | 99% accuracy, useless model | PR-AUC, recall@k, cost-weighted metric |
| Tuning on test set | Optimistic estimate | Hold out untouched test set; tune on val/CV |
| Duplicates across splits | Inflated metrics | Dedupe before splitting (exact + near-duplicate) |
| Train/serve skew | Prod predictions differ | Shared feature code, feature store, log serving features |
| Single seed result | Not reproducible gains | Report mean ± std over seeds |
| Join explodes rows | Label distribution shifts | Assert row counts and key uniqueness after joins |
