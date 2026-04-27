import numpy as np
import pandas as pd
from scipy.stats import norm
from sklearn.metrics import roc_curve, roc_auc_score

# ----------------------------
# DeLong AUC
# ----------------------------
def _compute_midrank(x: np.ndarray) -> np.ndarray:
    J = np.argsort(x)
    Z = x[J]
    N = len(x)
    T = np.zeros(N, dtype=float)
    i = 0
    while i < N:
        j = i
        while j < N and Z[j] == Z[i]:
            j += 1
        T[i:j] = 0.5 * (i + j - 1)
        i = j
    out = np.empty(N, dtype=float)
    out[J] = T
    return out


def _fast_delong(pred_sorted: np.ndarray, n_pos: int):
    m = n_pos
    n = pred_sorted.shape[1] - m
    pos = pred_sorted[:, :m]
    neg = pred_sorted[:, m:]

    k = pred_sorted.shape[0]
    tx = np.empty((k, m), dtype=float)
    ty = np.empty((k, n), dtype=float)
    tz = np.empty((k, m + n), dtype=float)

    for r in range(k):
        tx[r] = _compute_midrank(pos[r])
        ty[r] = _compute_midrank(neg[r])
        tz[r] = _compute_midrank(pred_sorted[r])

    aucs = tz[:, :m].sum(axis=1) / (m * n) - (m + 1.0) / (2.0 * n)

    v01 = (tz[:, :m] - tx) / n
    v10 = 1.0 - (tz[:, m:] - ty) / m

    sx = np.atleast_2d(np.cov(v01))
    sy = np.atleast_2d(np.cov(v10))
    delong_cov = sx / m + sy / n
    return aucs, delong_cov


def delong_auc_ci(y_true, y_score, alpha=0.05):
    y_true = np.asarray(y_true).astype(int)
    y_score = np.asarray(y_score).astype(float)

    order = np.argsort(-y_score)
    y_true = y_true[order]
    y_score = y_score[order]

    n_pos = int(y_true.sum())
    pos_idx = y_true == 1
    neg_idx = ~pos_idx

    y_score_sorted = np.concatenate([y_score[pos_idx], y_score[neg_idx]])
    pred_sorted = y_score_sorted[np.newaxis, :]

    aucs, cov = _fast_delong(pred_sorted, n_pos)
    auc = float(aucs[0])
    var = float(cov[0, 0])
    se = np.sqrt(max(var, 0.0))

    z = norm.ppf(1 - alpha / 2)
    return auc, max(0.0, auc - z * se), min(1.0, auc + z * se)


# ----------------------------
# Bootstrap ROC band
# ----------------------------
def bootstrap_roc_band(y_true, y_score, n_boot=2000, seed=1):
    rng = np.random.default_rng(seed)
    y_true = np.asarray(y_true).astype(int)
    y_score = np.asarray(y_score).astype(float)

    grid = np.linspace(0, 1, 201)
    n = len(y_true)
    idx = np.arange(n)

    tprs, aucs = [], []

    for _ in range(n_boot):
        samp = rng.choice(idx, size=n, replace=True)

        if len(np.unique(y_true[samp])) < 2:
            continue

        fpr_b, tpr_b, _ = roc_curve(y_true[samp], y_score[samp])
        aucs.append(roc_auc_score(y_true[samp], y_score[samp]))

        tpr_interp = np.interp(grid, fpr_b, tpr_b)
        tpr_interp[0], tpr_interp[-1] = 0.0, 1.0
        tprs.append(tpr_interp)

    tprs = np.asarray(tprs)
    aucs = np.asarray(aucs)

    return (
        grid,
        np.percentile(tprs, 2.5, axis=0),
        np.percentile(tprs, 97.5, axis=0),
        np.percentile(aucs, 2.5),
        np.percentile(aucs, 97.5),
    )


# ----------------------------
# Binomial CI (Wilson)
# ----------------------------
def _binomial_ci(x, n, alpha=0.05):
    if n == 0:
        return (np.nan, np.nan)

    z = norm.ppf(1 - alpha / 2)
    p = x / n

    denom = 1 + z**2 / n
    center = (p + z**2 / (2*n)) / denom
    margin = z * np.sqrt((p*(1-p) + z**2/(4*n)) / n) / denom

    return max(0, center - margin), min(1, center + margin)


# ----------------------------
# Threshold metrics
# ----------------------------
def compute_threshold_metrics(y_true, y_score, thresholds, sf=None, alpha=0.05):

    def _round(x, sf=sf):
        try:
            if sf is None or x is None or np.isnan(x):
                return x
            return round(x, sf)
        except:
            return x

    y_true = np.asarray(y_true).astype(int)
    y_score = np.asarray(y_score).astype(float)

    results = {}

    for name, thr in thresholds.items():
        y_pred = (y_score >= thr).astype(int)

        tp = np.sum((y_pred == 1) & (y_true == 1))
        fp = np.sum((y_pred == 1) & (y_true == 0))
        tn = np.sum((y_pred == 0) & (y_true == 0))
        fn = np.sum((y_pred == 0) & (y_true == 1))

        sens = tp / (tp + fn) if (tp + fn) > 0 else np.nan
        spec = tn / (tn + fp) if (tn + fp) > 0 else np.nan

        sens_lo, sens_hi = _binomial_ci(tp, tp + fn, alpha)
        spec_lo, spec_hi = _binomial_ci(tn, tn + fp, alpha)

        results[name] = {
            "threshold": _round(thr,sf),

            "sensitivity": _round(sens,sf),
            "sens_ci_lo": _round(sens_lo,sf),
            "sens_ci_hi": _round(sens_hi,sf),

            "specificity": _round(spec,sf),
            "spec_ci_lo": _round(spec_lo,sf),
            "spec_ci_hi": _round(spec_hi,sf),

            "tp": int(tp),
            "fp": int(fp),
            "tn": int(tn),
            "fn": int(fn)
        }

    # formatted table
    rows = []
    for name, res in results.items():
        rows.append({
            "Threshold": name,
            "Cutoff": res["threshold"],
            "Sensitivity": f"{res['sensitivity']} ({res['sens_ci_lo']}–{res['sens_ci_hi']})",
            "Specificity": f"{res['specificity']} ({res['spec_ci_lo']}–{res['spec_ci_hi']})",
            "TP": res["tp"],
            "FP": res["fp"],
            "TN": res["tn"],
            "FN": res["fn"],
        })

    df = pd.DataFrame(rows)
    print(df)

    return results 