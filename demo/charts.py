"""Graphiques exhaustifs — alignés sur les notebooks Groupe3."""

import math

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from demo.constants import (
    ANOMALY_SCORE_DIST,
    CM_IF_VS_LABELS,
    CM_KM_VS_IF,
    CM_KM_VS_LABELS,
    CM_SVM,
    CM_XGB,
    FEATURES_16,
    FEATURES_ML,
    RESULTS_SUPERVISED,
    RESULTS_UNSUPERVISED,
    THEME,
    XGB_PC_IMPORTANCE,
    XGB_PC_VARIANCE,
)

C = THEME


def setup_style():
    sns.set_theme(style="whitegrid", font_scale=0.95)
    plt.rcParams.update({
        "figure.facecolor": C["surface"],
        "axes.facecolor": "#FAFBFC",
        "axes.edgecolor": C["border"],
        "axes.labelcolor": C["text"],
        "text.color": C["text"],
        "font.family": "sans-serif",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "grid.alpha": 0.35,
    })


def _title(ax, text):
    ax.set_title(text, fontsize=11, fontweight="bold", color=C["text"], pad=10)


def fig_missing_values(df: pd.DataFrame):
    setup_style()
    missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
    missing_pct = missing_pct[missing_pct > 0]
    fig, ax = plt.subplots(figsize=(8, 4))
    if missing_pct.empty:
        ax.text(0.5, 0.5, "Aucune valeur manquante détectée", ha="center", va="center",
                transform=ax.transAxes, fontsize=12, color=C["muted"])
        ax.set_axis_off()
    else:
        missing_pct.plot(kind="bar", ax=ax, color=C["warning"], edgecolor=C["border"])
        ax.set_ylabel("Pourcentage (%)")
    _title(ax, "Valeurs manquantes par colonne")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig


def fig_label_distribution_full(counts: dict | None = None):
    setup_style()
    if counts is None:
        counts = {"Normal": 534_199, "Atypique": 108_925}
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    labels = list(counts.keys())
    values = list(counts.values())
    colors = [C["normal"], C["atypical"]]

    bars = axes[0].bar(labels, values, color=colors, edgecolor=C["border"], width=0.55)
    axes[0].set_ylabel("Nombre de profils")
    _title(axes[0], "Répartition globale des labels (643 124 profils)")
    for bar in bars:
        h = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width() / 2, h, f"{int(h):,}".replace(",", " "),
                     ha="center", va="bottom", fontsize=9)

    axes[1].pie(values, labels=labels, colors=colors, autopct="%1.1f%%",
                startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    _title(axes[1], "Proportion Normal / Atypique")
    fig.tight_layout()
    return fig


def fig_anomaly_score_distribution():
    setup_style()
    scores = list(ANOMALY_SCORE_DIST.keys())
    counts = list(ANOMALY_SCORE_DIST.values())
    colors = [C["normal"] if s <= 1 else C["atypical"] for s in scores]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(scores, counts, color=colors, edgecolor=C["border"], width=0.65)
    ax.set_xlabel("anomaly_score (critères remplis)")
    ax.set_ylabel("Nombre de profils")
    _title(ax, "Distribution du score d'anomalie (labellisation Excel)")
    ax.set_xticks(scores)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h, f"{int(h):,}".replace(",", " "),
                ha="center", va="bottom", fontsize=8, rotation=0)
    ax.axvline(1.5, color=C["accent"], linestyle="--", linewidth=1.5, label="Seuil label (≥ 2)")
    ax.legend()
    fig.tight_layout()
    return fig


def fig_distributions_grid(df: pd.DataFrame, columns: list[str]):
    setup_style()
    n = len(columns)
    ncols = 4
    nrows = math.ceil(n / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(16, nrows * 3.2))
    axes = np.array(axes).reshape(-1)
    for i, col in enumerate(columns):
        if col not in df.columns:
            continue
        data = np.log1p(df[col].clip(lower=0).dropna())
        sns.histplot(data, bins=35, kde=True, ax=axes[i], color=C["primary"], alpha=0.75)
        axes[i].set_xlabel(f"log1p({col})")
        axes[i].set_title(col, fontsize=9)
    for j in range(len(columns), len(axes)):
        axes[j].set_visible(False)
    fig.suptitle("Distributions des variables principales (échelle log1p)", fontweight="bold", y=1.01)
    fig.tight_layout()
    return fig


def fig_boxplots(df: pd.DataFrame, columns: list[str]):
    setup_style()
    ncols = 3
    nrows = math.ceil(len(columns) / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(14, nrows * 3.5))
    axes = np.array(axes).reshape(-1)
    for i, col in enumerate(columns):
        if col not in df.columns:
            continue
        p95 = df[col].quantile(0.95)
        data = df[col].clip(upper=p95)
        axes[i].boxplot(data.dropna(), vert=True, patch_artist=True,
                        boxprops={"facecolor": C["primary"], "alpha": 0.35})
        axes[i].set_title(col, fontsize=9)
        axes[i].set_xticks([])
    for j in range(len(columns), len(axes)):
        axes[j].set_visible(False)
    fig.suptitle("Boxplots tronqués au 95e percentile — présence d'outliers", fontweight="bold", y=1.01)
    fig.tight_layout()
    return fig


def correlation_matrix_pct(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    cols = [c for c in columns if c in df.columns]
    return (df[cols].corr() * 100).round(1)


def fig_correlation_heatmap(df: pd.DataFrame, columns: list[str], as_percent: bool = True):
    setup_style()
    cols = [c for c in columns if c in df.columns]
    corr = df[cols].corr()
    display = corr * 100 if as_percent else corr
    vmin, vmax = (-100, 100) if as_percent else (-1, 1)

    fig, ax = plt.subplots(figsize=(12, 10))
    annot = np.array([[f"{display.iloc[i, j]:.0f}%" for j in range(len(cols))] for i in range(len(cols))])
    sns.heatmap(
        display, annot=annot, fmt="", cmap="RdBu_r", center=0,
        vmin=vmin, vmax=vmax, ax=ax, linewidths=0.4,
        cbar_kws={"shrink": 0.8, "label": "Corrélation (%)" if as_percent else "Corrélation"},
        annot_kws={"size": 7},
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=8)
    title = "Matrice de corrélation (%) — 16 features ML" if as_percent else "Matrice de corrélation"
    _title(ax, title)
    fig.tight_layout()
    return fig


def fig_normal_vs_atypical(df: pd.DataFrame, columns: list[str]):
    setup_style()
    if "label" not in df.columns:
        return fig_label_distribution_full()
    ncols = 3
    nrows = math.ceil(len(columns) / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(14, nrows * 3.5))
    axes = np.array(axes).reshape(-1)
    for i, col in enumerate(columns):
        if col not in df.columns:
            continue
        d0 = np.log1p(df.loc[df["label"] == 0, col].clip(lower=0).dropna())
        d1 = np.log1p(df.loc[df["label"] == 1, col].clip(lower=0).dropna())
        axes[i].hist(d0, bins=30, alpha=0.55, label="Normal", color=C["normal"], density=True)
        axes[i].hist(d1, bins=30, alpha=0.55, label="Atypique", color=C["atypical"], density=True)
        axes[i].set_title(col, fontsize=9)
        axes[i].legend(fontsize=7)
    for j in range(len(columns), len(axes)):
        axes[j].set_visible(False)
    fig.suptitle("Distributions Normal vs Atypique (log1p)", fontweight="bold", y=1.01)
    fig.tight_layout()
    return fig


def fig_scatter_followers_tweets(df: pd.DataFrame):
    setup_style()
    sub = df.sample(min(5000, len(df)), random_state=42)
    p99 = sub["followers_count"].quantile(0.99)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.scatter(sub["followers_count"].clip(upper=p99), sub["nb_tweets"],
               alpha=0.25, s=12, c=C["primary"])
    ax.set_xlabel("followers_count (99e pct)")
    ax.set_ylabel("nb_tweets")
    _title(ax, "Followers vs Activité (échantillon)")
    fig.tight_layout()
    return fig


def fig_pca_scree(evr: np.ndarray, var_cum: np.ndarray, n_retained: int, title: str):
    setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(14, 4.5))
    n = len(evr)
    axes[0].plot(range(1, n + 1), evr * 100, "o-", color=C["primary"], linewidth=2, markersize=6)
    axes[0].axhline(100 / n, color=C["muted"], linestyle="--", alpha=0.6, label="Kaiser (1/n)")
    axes[0].set_xlabel("Composante")
    axes[0].set_ylabel("Variance expliquée (%)")
    _title(axes[0], "Variance par composante (ACP)")

    axes[1].plot(range(1, n + 1), var_cum, "o-", color=C["accent"], linewidth=2, markersize=6)
    for pct, color in [(70, C["muted"]), (75, C["warning"]), (80, C["success"])]:
        axes[1].axhline(pct, color=color, linestyle="--", alpha=0.7, linewidth=1, label=f"{pct} %")
    axes[1].axvline(n_retained, color=C["primary_dark"], linestyle=":", linewidth=2,
                    label=f"Retenu = {n_retained} ({var_cum[n_retained - 1]:.1f} %)")
    axes[1].set_xlabel("Nombre de composantes")
    axes[1].set_ylabel("Variance cumulée (%)")
    _title(axes[1], "Variance cumulée — sélection du nombre de composantes")
    axes[1].legend(fontsize=7, loc="lower right")
    fig.tight_layout()
    return fig


def fig_pca_scatter_2d(X2: np.ndarray, labels: np.ndarray):
    setup_style()
    fig, ax = plt.subplots(figsize=(9, 6.5))
    for label, color, name in [(0, C["normal"], "Normal"), (1, C["atypical"], "Atypique")]:
        mask = labels == label
        ax.scatter(X2[mask, 0], X2[mask, 1], alpha=0.35, s=10, c=color, label=name)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    _title(ax, "Projection ACP 2D — Normal vs Atypique")
    ax.legend()
    fig.tight_layout()
    return fig


def fig_kmeans_elbow(k_range: list, inertia: list):
    setup_style()
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(k_range, inertia, "o-", color=C["primary"], linewidth=2, markersize=8)
    ax.axvline(7, color=C["accent"], linestyle="--", linewidth=1.5, label="k retenu = 7")
    ax.set_xlabel("Nombre de clusters (k)")
    ax.set_ylabel("Inertie")
    _title(ax, "K-Means — Méthode du coude (choix du nombre de clusters)")
    ax.set_xticks(k_range)
    ax.legend()
    fig.tight_layout()
    return fig


def fig_cluster_distribution(cluster_counts: pd.Series):
    setup_style()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    cluster_counts.sort_index().plot(kind="bar", ax=ax, color=C["primary"],
                                     edgecolor=C["border"])
    ax.set_xlabel("Cluster")
    ax.set_ylabel("Nombre de profils (échantillon)")
    _title(ax, "Distribution des clusters K-Means (k = 7)")
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    return fig


def fig_isolation_forest_bar():
    setup_style()
    n_total = 643_124
    n_anom = RESULTS_UNSUPERVISED["Isolation Forest"]["count"]
    n_norm = n_total - n_anom
    labels = ["Normal", "Atypique"]
    values = [n_norm, n_anom]
    colors = [C["normal"], C["atypical"]]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(labels, values, color=colors, edgecolor=C["border"], width=0.5)
    _title(ax, "Isolation Forest — Détection (contamination = auto)")
    ax.set_ylabel("Nombre de profils")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h, f"{int(h):,}".replace(",", " "),
                ha="center", va="bottom", fontweight="bold", fontsize=9)
    fig.tight_layout()
    return fig


def fig_unsupervised_comparison():
    setup_style()
    categories = ["K-Means\nseulement", "Consensus\n(K-Means + Iso)", "Iso Forest\nseulement"]
    values = [
        RESULTS_UNSUPERVISED["K-Means seul"]["count"],
        RESULTS_UNSUPERVISED["Consensus"]["count"],
        RESULTS_UNSUPERVISED["Iso Forest seul"]["count"],
    ]
    colors = [C["primary"], C["accent"], C["atypical"]]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(categories, values, color=colors, edgecolor=C["border"], width=0.55)
    _title(ax, "Comparaison K-Means vs Isolation Forest")
    ax.set_ylabel("Nombre de profils détectés")
    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, h + 400,
                    f"{int(h):,}".replace(",", " "), ha="center", fontweight="bold")
    fig.tight_layout()
    return fig


def fig_heatmap_cm(cm, title: str, xlabel: str, ylabel: str, xticklabels=None, yticklabels=None):
    setup_style()
    fig, ax = plt.subplots(figsize=(6.5, 5))
    sns.heatmap(np.array(cm), annot=True, fmt=",", cmap="Blues", ax=ax,
                xticklabels=xticklabels or ["0", "1"],
                yticklabels=yticklabels or ["0", "1"],
                linewidths=0.5, cbar_kws={"shrink": 0.85})
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    _title(ax, title)
    fig.tight_layout()
    return fig


def fig_supervised_metrics():
    setup_style()
    metrics = ["F1", "ROC-AUC", "Recall", "Precision", "Accuracy"]
    svm = [RESULTS_SUPERVISED["SVM"][m.replace("Accuracy", "Accuracy")] for m in metrics]
    xgb = [RESULTS_SUPERVISED["XGBoost"][m] for m in metrics]
    x = np.arange(len(metrics))
    width = 0.36
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.bar(x - width / 2, svm, width, label="SVM", color=C["primary"], edgecolor=C["border"])
    ax.bar(x + width / 2, xgb, width, label="XGBoost", color=C["success"], edgecolor=C["border"])
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Score")
    _title(ax, "Supervisé — SVM vs XGBoost (8 feat. + ACP 5 comp.)")
    ax.legend()
    for i, (sv, xg) in enumerate(zip(svm, xgb)):
        ax.text(i - width / 2, sv + 0.02, f"{sv:.3f}", ha="center", fontsize=8)
        ax.text(i + width / 2, xg + 0.02, f"{xg:.3f}", ha="center", fontsize=8)
    fig.tight_layout()
    return fig


def fig_roc_curves():
    setup_style()
    fig, ax = plt.subplots(figsize=(7.5, 6))

    # Points représentatifs calibrés sur les AUC du projet
    curves = {
        "SVM": (RESULTS_SUPERVISED["SVM"]["ROC-AUC"], C["primary"], [
            (0.0, 0.0), (0.08, 0.30), (0.20, 0.48), (0.35, 0.58),
            (0.55, 0.68), (0.75, 0.78), (1.0, 1.0),
        ]),
        "XGBoost": (RESULTS_SUPERVISED["XGBoost"]["ROC-AUC"], C["success"], [
            (0.0, 0.0), (0.05, 0.38), (0.15, 0.56), (0.28, 0.67),
            (0.45, 0.78), (0.65, 0.87), (1.0, 1.0),
        ]),
    }

    for name, (auc_val, color, pts) in curves.items():
        fpr, tpr = zip(*pts)
        ax.plot(fpr, tpr, color=color, linewidth=2.5, label=f"{name} (AUC = {auc_val:.3f})")

    ax.plot([0, 1], [0, 1], "k--", linewidth=1, alpha=0.6, label="Aléatoire")
    ax.set_xlabel("Taux de faux positifs")
    ax.set_ylabel("Taux de vrais positifs")
    _title(ax, "Courbes ROC — 8 features hors règles")
    ax.legend(loc="lower right")
    fig.tight_layout()
    return fig


def fig_xgb_importance():
    setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
    imp = pd.Series(XGB_PC_IMPORTANCE).sort_values()
    var = pd.Series(XGB_PC_VARIANCE).sort_values()
    imp.plot(kind="barh", ax=axes[0], color=C["primary"], edgecolor=C["border"])
    axes[0].set_xlabel("Importance")
    _title(axes[0], "Importance XGBoost — composantes ACP")
    var.plot(kind="barh", ax=axes[1], color=C["accent"], edgecolor=C["border"])
    axes[1].set_xlabel("Variance (%)")
    _title(axes[1], "Variance expliquée par composante")
    fig.tight_layout()
    return fig


def fig_circularite():
    setup_style()
    scenarios = ["16 features\n+ ACP 7\n(circularité)", "8 features\n+ ACP 5\n(évaluation retenue)"]
    f1 = [0.970, 0.443]
    colors = [C["warning"], C["success"]]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(scenarios, f1, color=colors, edgecolor=C["border"], width=0.48)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("F1-score (XGBoost)")
    _title(ax, "Effet de la circularité label / features")
    for bar, val in zip(bars, f1):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.02, f"{val:.3f}",
                ha="center", fontweight="bold")
    fig.tight_layout()
    return fig


def fig_acp_comparison():
    setup_style()
    contexts = ["Non supervisé\n(16 feat.)", "Supervisé\n(8 feat.)"]
    components = [7, 5]
    variance = [79, 100]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(contexts, components, color=[C["primary"], C["accent"]], edgecolor=C["border"])
    ax.set_ylabel("Composantes ACP")
    _title(ax, "Choix ACP — contextes indépendants")
    for bar, v in zip(bars, variance):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.12,
                f"{int(bar.get_height())} comp.\n(~{v} % var.)", ha="center", fontweight="bold", fontsize=9)
    fig.tight_layout()
    return fig


def fig_synthesis_final():
    """Comparaison des deux modèles retenus — objectif du projet."""
    setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Isolation Forest — modèle non supervisé retenu
    if_metrics = ["Profils détectés", "Part du jeu"]
    if_values = [RESULTS_UNSUPERVISED["Isolation Forest"]["count"],
                 RESULTS_UNSUPERVISED["Isolation Forest"]["pct"]]
    bars_if = axes[0].bar(if_metrics, if_values, color=[C["accent"], C["primary"]],
                            edgecolor=C["border"], width=0.45)
    _title(axes[0], "Isolation Forest (retenu) — sans labels")
    axes[0].set_ylabel("Valeur")
    axes[0].text(0, if_values[0] + 800,
                 f"{int(if_values[0]):,}".replace(",", " ") + " profils",
                 ha="center", fontweight="bold")
    axes[0].text(1, if_values[1] + 0.15, f"{if_values[1]:.2f} %", ha="center", fontweight="bold")
    axes[0].set_ylim(0, max(if_values) * 1.2)

    # XGBoost — modèle supervisé retenu
    xgb_metrics = ["F1", "ROC-AUC"]
    xgb_values = [RESULTS_SUPERVISED["XGBoost"]["F1"], RESULTS_SUPERVISED["XGBoost"]["ROC-AUC"]]
    bars_xgb = axes[1].bar(xgb_metrics, xgb_values, color=[C["success"], C["primary"]],
                             edgecolor=C["border"], width=0.45)
    _title(axes[1], "XGBoost (retenu) — avec labels")
    axes[1].set_ylabel("Score")
    axes[1].set_ylim(0, 1.05)
    for bar, val in zip(bars_xgb, xgb_values):
        axes[1].text(bar.get_x() + bar.get_width() / 2, val + 0.02, f"{val:.3f}",
                     ha="center", fontweight="bold")

    fig.tight_layout()
    return fig


def fig_retained_models_overview():
    """Vue d'ensemble IF vs XGBoost — les deux approches retenues."""
    setup_style()
    fig, ax = plt.subplots(figsize=(10, 5))
    models = ["Isolation Forest\n(non supervisé)", "XGBoost\n(supervisé)"]
    x = np.arange(len(models))
    width = 0.35

    detection = [RESULTS_UNSUPERVISED["Isolation Forest"]["pct"], RESULTS_SUPERVISED["XGBoost"]["F1"] * 100]
    bars1 = ax.bar(x - width / 2, detection, width, label="IF : % détectés · XGB : F1×100",
                     color=C["accent"], edgecolor=C["border"])
    auc_line = [0, RESULTS_SUPERVISED["XGBoost"]["ROC-AUC"]]
    bars2 = ax.bar(x + width / 2, [0, auc_line[1]], width, label="ROC-AUC (XGBoost)",
                     color=C["success"], edgecolor=C["border"])

    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.set_ylabel("Score normalisé")
    ax.set_ylim(0, 1.05)
    _title(ax, "Modèles retenus — comparaison des deux approches")
    ax.legend(fontsize=8)
    ax.text(0, detection[0] + 1, f"{detection[0]:.2f} %", ha="center", fontweight="bold", fontsize=9)
    ax.text(1 - width / 2, detection[1] + 2, f"F1={RESULTS_SUPERVISED['XGBoost']['F1']:.3f}",
            ha="center", fontweight="bold", fontsize=9)
    ax.text(1 + width / 2, auc_line[1] + 0.02, f"{auc_line[1]:.3f}", ha="center", fontweight="bold", fontsize=9)
    fig.tight_layout()
    return fig


def fig_pipeline_flow():
    setup_style()
    fig, ax = plt.subplots(figsize=(14, 3.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1)
    ax.axis("off")
    steps = [
        "JSONL\nraw/", "MongoDB\nAgrégation",
        "users_\naggregated\n(21 var.)",
        "EDA\n21→16 feat.",
        "Labellisation\nExcel",
        "users_\nlabeled\n(+ labels)",
        "ML",
    ]
    xs = np.linspace(0.4, 9.6, len(steps))
    colors = [C["primary_dark"], C["primary_dark"], C["primary"],
              C["primary"], C["accent"], C["accent"], C["accent"]]
    for i, (x, label, color) in enumerate(zip(xs, steps, colors)):
        rect = mpatches.FancyBboxPatch((x - 0.58, 0.18), 1.16, 0.64, boxstyle="round,pad=0.04",
                                       facecolor=color, edgecolor=C["border"], alpha=0.92)
        ax.add_patch(rect)
        ax.text(x, 0.5, label, ha="center", va="center", color="white", fontsize=7, fontweight="bold")
        if i < len(steps) - 1:
            ax.annotate("", xy=(xs[i + 1] - 0.6, 0.5), xytext=(x + 0.6, 0.5),
                        arrowprops=dict(arrowstyle="->", color=C["muted"], lw=1.5))
    _title(ax, "Pipeline — aggregated (EDA) → labeled (ML)")
    fig.tight_layout()
    return fig


def fig_acp_supervised_variance(var_cum: np.ndarray, n_retained: int):
    setup_style()
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(range(1, len(var_cum) + 1), var_cum, "o-", color=C["accent"], linewidth=2, markersize=6)
    ax.axhline(99.9, color=C["warning"], linestyle="--", linewidth=1.5, label="99,9 %")
    ax.axhline(70, color=C["muted"], linestyle="--", alpha=0.6, label="70 %")
    ax.axhline(80, color=C["success"], linestyle="--", alpha=0.6, label="80 %")
    ax.axvline(n_retained, color=C["primary"], linestyle=":", linewidth=2,
               label=f"Retenu = {n_retained} ({var_cum[n_retained - 1]:.1f} %)")
    ax.set_xlabel("Nombre de composantes")
    ax.set_ylabel("Variance cumulée (%)")
    _title(ax, "ACP supervisée — saturation variance (8 features, train)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.35)
    fig.tight_layout()
    return fig


def fig_kmeans_vs_labels():
    return fig_heatmap_cm(
        CM_KM_VS_LABELS,
        "K-Means vs labels manuels (643 124 profils)",
        "Prédiction", "Réalité",
        ["Normal", "Atypique"], ["Normal", "Atypique"],
    )


def fig_isoforest_vs_labels():
    return fig_heatmap_cm(
        CM_IF_VS_LABELS,
        "Isolation Forest vs labels manuels (643 124 profils · contamination auto)",
        "Prédiction", "Réalité",
        ["Normal", "Atypique"], ["Normal", "Atypique"],
    )


def compute_pca_16(df: pd.DataFrame):
    cols = [c for c in FEATURES_16 if c in df.columns]
    X = df[cols].astype(float)
    if "verified" in X.columns:
        X["verified"] = X["verified"].astype(int)
    if "default_profile_image" in X.columns:
        X["default_profile_image"] = X["default_profile_image"].astype(int)
    Xs = StandardScaler().fit_transform(X)
    pca = PCA(n_components=min(10, Xs.shape[1]), random_state=42)
    Xp = pca.fit_transform(Xs)
    evr = pca.explained_variance_ratio_
    var_cum = np.cumsum(evr) * 100
    n75 = int(np.searchsorted(var_cum, 75) + 1)
    return evr, var_cum, n75, Xp[:, :2], df["label"].values if "label" in df.columns else None


def compute_pca_8_supervised(df: pd.DataFrame):
    cols = [c for c in FEATURES_ML["kept_supervised"] if c in df.columns]
    X = df[cols].astype(float)
    for c in ["verified", "default_profile_image"]:
        if c in X.columns:
            X[c] = X[c].astype(int)
    Xs = StandardScaler().fit_transform(X)
    pca = PCA().fit(Xs)
    var_cum = np.cumsum(pca.explained_variance_ratio_) * 100
    n = int(np.searchsorted(var_cum, 99.9) + 1)
    return pca.explained_variance_ratio_, var_cum, n


def compute_kmeans_analysis(df: pd.DataFrame, k_max: int = 10):
    cols = [c for c in FEATURES_16 if c in df.columns]
    X = df[cols].astype(float)
    for c in ["verified", "default_profile_image"]:
        if c in X.columns:
            X[c] = X[c].astype(int)
    Xs = StandardScaler().fit_transform(X)
    n_comp = min(7, Xs.shape[1])
    Xp = PCA(n_components=n_comp, random_state=42).fit_transform(Xs)

    k_range = list(range(2, k_max + 1))
    inertia = []
    for k in k_range:
        km = MiniBatchKMeans(n_clusters=k, random_state=42, batch_size=2048, n_init=3)
        km.fit(Xp)
        inertia.append(km.inertia_)

    km7 = MiniBatchKMeans(n_clusters=7, random_state=42, batch_size=2048, n_init=3)
    labels = km7.fit_predict(Xp)
    counts = pd.Series(labels).value_counts().sort_index()
    return k_range, inertia, counts


def compute_isolation_forest_sample(df: pd.DataFrame):
    cols = [c for c in FEATURES_16 if c in df.columns]
    X = df[cols].astype(float)
    for c in ["verified", "default_profile_image"]:
        if c in X.columns:
            X[c] = X[c].astype(int)
    Xs = StandardScaler().fit_transform(X)
    Xp = PCA(n_components=7, random_state=42).fit_transform(Xs)
    iso = IsolationForest(contamination='auto', random_state=42, n_jobs=-1)
    pred = iso.fit_predict(Xp)
    n_anom = (pred == -1).sum()
    return n_anom, len(df) - n_anom
