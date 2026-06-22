"""
IF29 Groupe 3 — Portail de démonstration du projet.

Lancement : streamlit run demo/app.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd

from demo.paths import AGGREGATED_DATA_FILE, DATA_FILE
from demo.constants import (
    CM_KM_VS_IF,
    CM_SVM,
    CM_XGB,
    IF_VS_LABELS_METRICS,
    KM_VS_LABELS_METRICS,
    EDA_NUMERIC,
    FEATURES_16,
    FEATURES_EXCLUDED_FROM_ML,
    FEATURES_ML,
    FEATURES_ML_COUNT,
    LABEL_COMPARE_COLS,
    LABEL_RULES,
    NOTEBOOKS,
    PIPELINE_STEPS,
    PROJECT,
    RESULTS_SUPERVISED,
    RESULTS_UNSUPERVISED,
    THEME,
    VARIABLES_AGGREGATED_COUNT,
)
from demo.team import TEAM_MEMBERS, ML_DIMENSIONS
from demo import charts
from demo.interpretations import INTERP

# ---------------------------------------------------------------------------
# Page config & styles
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="IF29 Groupe 3 | Portail Projet",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    .block-container {{
        padding-top: 1.5rem;
        max-width: 1400px;
    }}

    .hero {{
        background: linear-gradient(135deg, {THEME['primary_dark']} 0%, {THEME['primary']} 55%, {THEME['accent']} 100%);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(13, 71, 161, 0.25);
    }}
    .hero h1 {{
        font-size: 1.85rem;
        font-weight: 700;
        margin: 0 0 0.4rem 0;
        color: white !important;
    }}
    .hero p {{
        font-size: 1rem;
        opacity: 0.92;
        margin: 0;
        color: white !important;
    }}
    .hero-tag {{
        display: inline-block;
        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 20px;
        padding: 0.25rem 0.85rem;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }}

    .section-head {{
        border-left: 4px solid {THEME['primary']};
        padding-left: 0.85rem;
        margin: 1.5rem 0 1rem 0;
    }}
    .section-head h2 {{
        font-size: 1.25rem;
        font-weight: 700;
        color: {THEME['text']};
        margin: 0;
    }}
    .section-head p {{
        color: {THEME['muted']};
        font-size: 0.88rem;
        margin: 0.2rem 0 0 0;
    }}

    .pipeline-step {{
        background: {THEME['surface']};
        border-left: 4px solid {THEME['primary']};
        padding: 0.85rem 1.1rem;
        margin: 0.35rem 0;
        border-radius: 0 10px 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid {THEME['border']};
        border-left: 4px solid {THEME['primary']};
    }}

    .notebook-card {{
        background: {THEME['surface']};
        border: 1px solid {THEME['border']};
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.75rem;
        transition: box-shadow 0.2s;
    }}
    .notebook-card:hover {{
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }}
    .nb-tag {{
        display: inline-block;
        background: {THEME['primary']};
        color: white;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        letter-spacing: 0.05em;
        margin-right: 0.5rem;
    }}

    div[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0B1929 0%, #152536 100%);
    }}
    div[data-testid="stSidebar"] .stMarkdown, div[data-testid="stSidebar"] label {{
        color: #E8EDF2 !important;
    }}
    div[data-testid="stSidebar"] hr {{
        border-color: rgba(255,255,255,0.12);
    }}
    div[data-testid="stMetric"] {{
        background: {THEME['surface']};
        border: 1px solid {THEME['border']};
        border-radius: 10px;
        padding: 0.75rem 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }}

    .chart-caption {{
        color: {THEME['muted']};
        font-size: 0.8rem;
        text-align: center;
        margin-top: -0.3rem;
        margin-bottom: 0.4rem;
    }}
    .interp-box {{
        background: #EEF4FB;
        border-left: 3px solid {THEME['primary']};
        border-radius: 0 8px 8px 0;
        padding: 0.7rem 1rem;
        margin: 0.25rem 0 1.5rem 0;
        font-size: 0.875rem;
        color: {THEME['text']};
        line-height: 1.55;
    }}
    .interp-box strong {{
        color: {THEME['primary_dark']};
    }}
    .member-card {{
        background: {THEME['surface']};
        border: 1px solid {THEME['border']};
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }}
    .member-name {{
        font-size: 1.05rem;
        font-weight: 700;
        color: {THEME['text']};
        margin-bottom: 0.25rem;
    }}
    .member-role {{
        font-size: 0.82rem;
        color: {THEME['primary']};
        font-weight: 600;
        margin-bottom: 0.5rem;
    }}
    .member-dim {{
        display: inline-block;
        background: #E8F4FD;
        color: {THEME['primary_dark']};
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        margin-bottom: 0.6rem;
    }}
    .page-footer {{
        background: {THEME['surface']};
        border: 1px solid {THEME['border']};
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-top: 2rem;
        text-align: center;
    }}
    .page-footer a {{
        color: {THEME['primary']};
        font-weight: 600;
        text-decoration: none;
    }}
    .page-footer a:hover {{
        text-decoration: underline;
    }}
</style>
""", unsafe_allow_html=True)


def section(title: str, subtitle: str = ""):
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f'<div class="section-head"><h2>{title}</h2>{sub}</div>', unsafe_allow_html=True)


def show_fig(fig, caption: str = "", interp_key: str = ""):
    st.pyplot(fig, clear_figure=True, width="stretch")
    if caption:
        st.markdown(f'<p class="chart-caption">{caption}</p>', unsafe_allow_html=True)
    if interp_key and interp_key in INTERP:
        st.markdown(
            f'<div class="interp-box"><strong>Interprétation :</strong> {INTERP[interp_key]}</div>',
            unsafe_allow_html=True,
        )


@st.cache_data(show_spinner=False)
def load_full_columns():
    if not DATA_FILE.exists():
        return pd.DataFrame()
    return pd.read_csv(DATA_FILE, nrows=0).columns.tolist()


@st.cache_data(show_spinner="Chargement des données labellisées…")
def load_sample(n: int = 15_000) -> pd.DataFrame:
    if not DATA_FILE.exists():
        return pd.DataFrame()
    header = load_full_columns()
    wanted = list(set(
        FEATURES_16 + EDA_NUMERIC + LABEL_COMPARE_COLS
        + ["label", "anomaly_score"]
    ))
    usecols = [c for c in wanted if c in header]
    df = pd.read_csv(DATA_FILE, usecols=usecols)
    for c in ["verified", "default_profile_image"]:
        if c in df.columns:
            df[c] = df[c].astype(int)
    if len(df) > n:
        df = df.sample(n, random_state=42)
    return df


@st.cache_data(show_spinner=False)
def _aggregated_columns():
    if not AGGREGATED_DATA_FILE.exists():
        return []
    return pd.read_csv(AGGREGATED_DATA_FILE, nrows=0).columns.tolist()


@st.cache_data(show_spinner="Chargement users_aggregated.csv (échantillon EDA)…")
def load_aggregated_sample(n: int = 15_000) -> pd.DataFrame:
    if not AGGREGATED_DATA_FILE.exists():
        return pd.DataFrame()
    header = _aggregated_columns()
    wanted = list(set(FEATURES_16 + EDA_NUMERIC))
    usecols = [c for c in wanted if c in header]
    df = pd.read_csv(AGGREGATED_DATA_FILE, usecols=usecols)
    for c in ["verified", "default_profile_image"]:
        if c in df.columns:
            df[c] = df[c].astype(int)
    if len(df) > n:
        df = df.sample(n, random_state=42)
    return df


@st.cache_data(show_spinner="Calcul describe — 643 124 profils…")
def load_aggregated_describe() -> pd.DataFrame:
    """describe() sur l'intégralité de users_aggregated.csv (avant labellisation)."""
    if not AGGREGATED_DATA_FILE.exists():
        return pd.DataFrame()
    df = pd.read_csv(AGGREGATED_DATA_FILE)
    for c in ["verified", "default_profile_image"]:
        if c in df.columns:
            df[c] = df[c].astype(int)
    num_cols = df.select_dtypes(include="number").columns.tolist()
    return df[num_cols].describe().T.round(2)


@st.cache_data(show_spinner="Calcul K-Means (échantillon)…")
def cached_kmeans(_hash: int):
    df = load_sample()
    return charts.compute_kmeans_analysis(df)


def footer_github():
    """Pied de page avec lien vers le dépôt GitHub."""
    url = PROJECT["github"]
    st.divider()
    st.markdown(f"""
    <div class="page-footer">
        <strong>Dépôt GitHub — IF29 Groupe 3</strong><br>
        <a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>
    </div>
    """, unsafe_allow_html=True)
    st.link_button("Ouvrir le dépôt GitHub", url, width="content")


def hero(title: str, subtitle: str, tag: str = "IF29 · Groupe 3"):
    st.markdown(f"""
    <div class="hero">
        <div class="hero-tag">{tag}</div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def page_accueil():
    hero(
        PROJECT["title"],
        f"{PROJECT['course']} — Portail de démonstration et synthèse des résultats",
    )

    c1, c2, c3, c4 = st.columns(4)
    iso = RESULTS_UNSUPERVISED["Isolation Forest"]
    xgb = RESULTS_SUPERVISED["XGBoost"]
    c1.metric("Profils analysés", f"{PROJECT['profiles']:,}".replace(",", " "))
    c2.metric("Labels atypiques (Excel)", f"{PROJECT['atypical_pct']} %")
    c3.metric("IF détectés (auto)", f"{iso['count']:,}".replace(",", " "), f"{iso['pct']} %")
    c4.metric("XGBoost F1", f"{xgb['F1']:.3f}", f"AUC {xgb['ROC-AUC']:.3f}")

    st.divider()

    col_l, col_r = st.columns(2)
    with col_l:
        section("Objectif du projet", "Comparer deux approches de détection")
        st.markdown("""
        | Approche | Comparé | **Retenu** |
        |----------|---------|------------|
        | Non supervisée | K-Means vs Isolation Forest | **Isolation Forest** |
        | Supervisée | SVM vs XGBoost | **XGBoost** |

        La **synthèse** confronte les deux modèles retenus : exploration sans labels
        (IF) et classification avec labels (XGBoost).
        """)
        show_fig(charts.fig_pipeline_flow(), interp_key="pipeline_flow")

    with col_r:
        section("Logique des fichiers", "Ordre strict du projet")
        st.markdown("""
        | Étape | Fichier | Contenu |
        |-------|---------|---------|
        | Agrégation | `users_aggregated.csv` | 21 variables · **sans label** |
        | **EDA** | `users_aggregated.csv` | describe · corrélations · **21→16** |
        | Labellisation | `users_labeled_manual.csv` | + `label` · + `anomaly_score` |
        | ML | `users_labeled_manual.csv` | 16 features (non sup.) ou 8 (sup.) |
        """)
        show_fig(charts.fig_retained_models_overview(), interp_key="retained_models")

    section("Synthèse — modèles retenus", "Isolation Forest vs XGBoost")
    show_fig(charts.fig_synthesis_final(), interp_key="synthesis_final")

    section("Parcours du portail")
    cols = st.columns(len(NOTEBOOKS))
    for col, nb in zip(cols, NOTEBOOKS):
        with col:
            st.markdown(f"**{nb['title']}**")
            st.caption(nb["file"])

    st.divider()
    section("Équipe projet", "5 membres — 5 dimensions du modèle ML")
    dim_df = pd.DataFrame(ML_DIMENSIONS, columns=["Dimension ML", "Rôle", "Membre"])
    st.dataframe(dim_df, width="stretch", hide_index=True)
    st.caption("Détails : page « Équipe & Rôles » · Document L4 : docs/EQUIPE_ROLES.md")

    footer_github()


def page_pipeline():
    hero("Pipeline & Données", "Agrégation → analyse exploratoire → labellisation → ML", "Étape 1")

    st.info(
        "La **labellisation Excel** intervient **après l'analyse exploratoire** : "
        "l'EDA oriente le choix des features et la définition des 4 critères d'atypicité."
    )

    for i, (step, detail) in enumerate(PIPELINE_STEPS, 1):
        st.markdown(
            f'<div class="pipeline-step"><strong>Étape {i} — {step}</strong><br>{detail}</div>',
            unsafe_allow_html=True,
        )

    st.divider()
    section("Schéma du pipeline")
    show_fig(charts.fig_pipeline_flow(), interp_key="pipeline_flow")

    section("Hypothèse fondamentale")
    st.warning(
        "L'analyse porte **uniquement sur l'auteur du tweet** (`user`). "
        "Les informations de `retweeted_status.user` ne sont **pas** utilisées."
    )

    section("Variables agrégées", f"{VARIABLES_AGGREGATED_COUNT} colonnes MongoDB — sortie de l'agrégation")
    st.markdown("""
    | Catégorie | Variables |
    |-----------|-----------|
    | Identifiants | user_id, screen_name, profile_lang |
    | Profil social | followers_count, friends_count, followers_friends_ratio, verified, default_profile_image |
    | Activité | nb_tweets, nb_retweets, retweet_ratio |
    | Contenu | avg_tweet_length, avg_hashtags, avg_urls, avg_mentions |
    | Engagement | avg_favorites, avg_retweet_count (collecte partielle) |
    | Temporel | active_days, tweet_frequency, first_tweet_date, last_tweet_date |
    """)

    section("Réduction 21 → 16 variables", "Décision prise après l'analyse exploratoire")
    st.markdown(f"""
    L'agrégation produit **{VARIABLES_AGGREGATED_COUNT} colonnes**. L'EDA conduit à en retenir
    **{FEATURES_ML_COUNT} features numériques** pour le ML :

    | Exclues après EDA ({len(FEATURES_EXCLUDED_FROM_ML)}) | Raison |
    |------------------------|--------|
    | `user_id`, `screen_name` | Identifiants — non prédictifs |
    | `profile_lang` | Variable catégorielle peu informative |
    | `first_tweet_date`, `last_tweet_date` | Redondantes avec `active_days` et `tweet_frequency` |
    """)
    st.caption(
        f"Features ML retenues ({FEATURES_ML_COUNT}) : "
        + ", ".join(f"`{f}`" for f in FEATURES_16)
    )


def page_eda():
    nb = next(n for n in NOTEBOOKS if n["id"] == "eda")
    hero("Analyse exploratoire", nb["summary"], f"Notebook · {nb['file']}")

    if not AGGREGATED_DATA_FILE.exists():
        st.error(f"`{AGGREGATED_DATA_FILE.name}` introuvable à la racine du projet.")
        return

    st.info(
        "**Étape 2 du pipeline** — analyse **uniquement** sur `users_aggregated.csv` "
        f"({VARIABLES_AGGREGATED_COUNT} variables, sans label). "
        f"Résultat : justification des **{FEATURES_ML_COUNT} features** ML. "
        "La labellisation (`users_labeled_manual.csv`) vient **après**."
    )

    df = load_aggregated_sample()
    describe_df = load_aggregated_describe()

    tabs = st.tabs([
        "Statistiques descriptives", "Qualité des données",
        "Distributions", "Features & Corrélation",
    ])

    with tabs[0]:
        section(
            "describe() — jeu complet",
            f"{PROJECT['profiles']:,} profils · toutes les colonnes numériques".replace(",", " "),
        )
        if describe_df.empty:
            st.warning("Impossible de calculer le describe.")
        else:
            st.dataframe(describe_df, width="stretch", height=520)
            st.caption(
                f"Aligné sur `Groupe3_Analyse_Exploratoire.ipynb` — "
                f"`df.select_dtypes(number).describe().T` sur `{AGGREGATED_DATA_FILE.name}`."
            )
            st.markdown(
                f'<div class="interp-box"><strong>Interprétation :</strong> '
                f'{INTERP["describe_aggregated"]}</div>',
                unsafe_allow_html=True,
            )

    with tabs[1]:
        section("Valeurs manquantes", "Échantillon représentatif pour les graphiques")
        show_fig(charts.fig_missing_values(df), interp_key="missing_values")

    with tabs[2]:
        section("Distributions log1p — 8 variables clés")
        show_fig(charts.fig_distributions_grid(df, EDA_NUMERIC), interp_key="distributions_grid")
        section("Followers vs Activité")
        show_fig(charts.fig_scatter_followers_tweets(df), interp_key="scatter_followers")

    with tabs[3]:
        section(
            "Sélection des features — 21 → 16 variables",
            "Décision documentée après describe et corrélations",
        )
        st.markdown(f"""
        | | Détail |
        |--|--------|
        | Variables agrégées MongoDB | **{VARIABLES_AGGREGATED_COUNT}** |
        | Features ML retenues | **{FEATURES_ML_COUNT}** |
        | Exclues | {", ".join(f"`{c}`" for c in FEATURES_EXCLUDED_FROM_ML)} |
        """)
        st.markdown(
            f'<div class="interp-box"><strong>Interprétation :</strong> '
            f'{INTERP["features_reduced"]}</div>',
            unsafe_allow_html=True,
        )

        section("Matrice de corrélation (%)", f"{FEATURES_ML_COUNT} features ML · échantillon EDA")
        cols = [c for c in FEATURES_16 if c in df.columns]
        corr_pct = charts.correlation_matrix_pct(df, cols)
        show_fig(charts.fig_correlation_heatmap(df, cols, as_percent=True), interp_key="correlation")
        st.dataframe(
            corr_pct.style.format("{:.1f}%"),
            width="stretch",
            height=420,
        )
        st.caption("Valeurs = coefficient de corrélation de Pearson × 100.")


def page_labellisation():
    nb = next(n for n in NOTEBOOKS if n["id"] == "label")
    hero(
        "Labellisation manuelle",
        "Création de users_labeled_manual.csv — après l'EDA sur users_aggregated.csv",
        f"Notebook · {nb['file']}",
    )

    st.info(
        "**Étape 3 du pipeline.** L'EDA sur `users_aggregated.csv` (21 variables) a permis "
        f"de retenir **{FEATURES_ML_COUNT} features** ML. La labellisation Excel enrichit "
        "ce même jeu de profils pour produire **`users_labeled_manual.csv`** "
        "(+ colonnes `label` et `anomaly_score`)."
    )

    section("Transformation des fichiers")
    st.markdown("""
    ```
    users_aggregated.csv  (21 var., sans label)
            ↓  labellisation Excel (4 critères)
    users_labeled_manual.csv  (21 var. + label + anomaly_score)
    ```
    """)

    section("Processus Excel", "Atypique si ≥ 2 critères sur 4")
    rules_df = pd.DataFrame(LABEL_RULES, columns=["Critère", "Condition", "Interprétation"])
    st.dataframe(rules_df, width="stretch", hide_index=True)

    c1, c2 = st.columns(2)
    c1.metric("Normal", f"{PROJECT['normal_count']:,}".replace(",", " "), "83,1 %")
    c2.metric("Atypique", f"{PROJECT['atypical_count']:,}".replace(",", " "), "16,9 %")

    section("Distribution anomaly_score")
    show_fig(charts.fig_anomaly_score_distribution(), interp_key="anomaly_score")

    section("Répartition finale des labels")
    show_fig(charts.fig_label_distribution_full(), interp_key="label_distribution")

    st.info(
        "Labellisation réalisée **uniquement sous Excel** (filtres, tri, inspection visuelle). "
        "Références : Ferrara et al. (2016), Chu et al. (2012), Varol et al. (2017)."
    )


def page_non_supervise():
    nb = next(n for n in NOTEBOOKS if n["id"] == "unsupervised")
    hero("Approche non supervisée", nb["summary"], f"Notebook · {nb['file']}")

    st.markdown(f"""
    - **Fichier ML :** `users_labeled_manual.csv` (produit par la labellisation)
    - **Features :** {FEATURES_ML['non_supervised']} variables (retenues après EDA)
    - **ACP :** 7 composantes (~79 % variance)
    - **Isolation Forest :** `contamination = 'auto'` (seuil inféré des scores d'anomalie)
    - **Labels :** exclus à l'entraînement — évaluation a posteriori
    """)

    tabs = st.tabs(["K-Means", "Isolation Forest", "Comparaison", "Matrices"])

    with tabs[0]:
        k_range, inertia, cluster_counts = cached_kmeans(len(load_sample()))
        show_fig(charts.fig_kmeans_elbow(k_range, inertia), interp_key="kmeans_elbow")
        show_fig(charts.fig_cluster_distribution(cluster_counts), interp_key="cluster_distribution")

    with tabs[1]:
        show_fig(charts.fig_isolation_forest_bar(), interp_key="isolation_forest_bar")
        km = RESULTS_UNSUPERVISED["K-Means"]
        iso = RESULTS_UNSUPERVISED["Isolation Forest"]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("K-Means", f"{km['count']:,}".replace(",", " "), f"{km['pct']} %")
        c2.metric("Consensus", f"{RESULTS_UNSUPERVISED['Consensus']['count']:,}".replace(",", " "))
        c3.metric("IF seul", f"{RESULTS_UNSUPERVISED['Iso Forest seul']['count']:,}".replace(",", " "))
        c4.metric("Isolation Forest (retenu)", f"{iso['count']:,}".replace(",", " "), f"{iso['pct']} %")

    with tabs[2]:
        show_fig(charts.fig_unsupervised_comparison(), interp_key="unsupervised_comparison")
        st.success(
            f"**Isolation Forest retenu** — `contamination = 'auto'`, "
            f"**{iso['count']:,} profils** ({iso['pct']} %) vs "
            f"**{km['count']:,}** pour K-Means ({km['pct']} %). "
            "Conçu pour la détection d'anomalies sur 643 124 profils.".replace(",", " ")
        )

    with tabs[3]:
        col1, col2 = st.columns(2)
        with col1:
            show_fig(charts.fig_heatmap_cm(
                CM_KM_VS_IF, "Concordance K-Means vs Isolation Forest",
                "Isolation Forest", "K-Means",
                ["Normal", "Atypique"], ["Normal", "Atypique"],
            ), interp_key="cm_km_vs_if")
        with col2:
            show_fig(charts.fig_kmeans_vs_labels(), interp_key="cm_km_vs_labels")
            m = KM_VS_LABELS_METRICS
            st.caption(f"K-Means vs labels — P={m['Precision']:.3f} · R={m['Recall']:.3f} · F1={m['F1']:.3f}")
        show_fig(charts.fig_isoforest_vs_labels(), interp_key="cm_if_vs_labels")
        m = IF_VS_LABELS_METRICS
        st.caption(f"Isolation Forest vs labels — P={m['Precision']:.3f} · R={m['Recall']:.3f} · F1={m['F1']:.3f}")


def page_supervise():
    nb = next(n for n in NOTEBOOKS if n["id"] == "supervised")
    hero("Approche supervisée", nb["summary"], f"Notebook · {nb['file']}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**8 features retenues**")
        for f in FEATURES_ML["kept_supervised"]:
            st.markdown(f"- `{f}`")
    with col2:
        st.markdown("**8 features exclues** (règles Excel)")
        for f in FEATURES_ML["excluded_supervised"]:
            st.markdown(f"- `{f}`")

    tabs = st.tabs(["Métriques", "Matrices de confusion", "Courbes ROC", "Circularité"])

    with tabs[0]:
        show_fig(charts.fig_supervised_metrics(), interp_key="supervised_metrics")
        results_df = pd.DataFrame(RESULTS_SUPERVISED).T
        results_df.columns = ["Accuracy", "F1", "Recall", "Precision", "ROC-AUC"]
        st.dataframe(results_df.round(3), width="stretch")

    with tabs[1]:
        col1, col2 = st.columns(2)
        with col1:
            show_fig(charts.fig_heatmap_cm(
                CM_SVM, "SVM — Matrice de confusion",
                "Prédiction", "Réalité",
                ["Normal", "Atypique"], ["Normal", "Atypique"],
            ), interp_key="cm_svm")
        with col2:
            show_fig(charts.fig_heatmap_cm(
                CM_XGB, "XGBoost — Matrice de confusion",
                "Prédiction", "Réalité",
                ["Normal", "Atypique"], ["Normal", "Atypique"],
            ), interp_key="cm_xgb")

    with tabs[2]:
        show_fig(charts.fig_roc_curves(), interp_key="roc_curves")

    with tabs[3]:
        show_fig(charts.fig_circularite(), interp_key="circularite")
        st.warning(
            "Avec les **16 features complètes**, XGBoost atteint F1 ~ **0,970** : "
            "le modèle recopie les règles Excel. "
            "Évaluation retenue : **8 features hors règles** → F1 = **0,443**."
        )


def page_synthese():
    nb = next(n for n in NOTEBOOKS if n["id"] == "final")
    hero(
        "Synthèse — Modèles retenus",
        "Comparer Isolation Forest et XGBoost : objectif central du projet",
        f"Notebook · {nb['file']}",
    )

    st.markdown("""
    **Objectif du projet :** confronter deux approches complémentaires de détection
    et retenir un modèle par famille — **Isolation Forest** (non supervisé) et
    **XGBoost** (supervisé).
    """)

    section("Tableau comparatif — modèles retenus")
    iso = RESULTS_UNSUPERVISED["Isolation Forest"]
    xgb = RESULTS_SUPERVISED["XGBoost"]
    st.markdown(f"""
    | | **Isolation Forest** | **XGBoost** |
    |--|----------------------|-------------|
    | Approche | Non supervisée | Supervisée |
    | Labels requis | Non | Oui (Excel, après EDA) |
    | Features | 16 MongoDB | 8 hors règles Excel |
    | Rôle | Exploration initiale | Classification avec labels |
    | Résultat clé | ~{iso['count']:,} profils ({iso['pct']:.2f} %) | F1 = {xgb['F1']:.3f} · ROC-AUC = {xgb['ROC-AUC']:.3f} |
    | Paramètre IF | `contamination = 'auto'` | 8 features hors règles Excel |
    | Baseline comparée | K-Means (non retenu) | SVM (non retenu) |
    """.replace(",", " "))

    section("Visualisation — les deux modèles retenus")
    show_fig(charts.fig_synthesis_final(), interp_key="synthesis_final")
    show_fig(charts.fig_retained_models_overview(), interp_key="retained_models")

    section("Complémentarité des approches")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        **Isolation Forest**
        - Détection sans annotation manuelle
        - ~{iso['pct']:.1f} % de profils déviants (`contamination = auto`)
        - Phase d'exploration sur 643 124 profils
        """)
        show_fig(charts.fig_isolation_forest_bar(), interp_key="isolation_forest_bar")
    with col2:
        st.markdown("""
        **XGBoost**
        - Classification une fois les labels définis
        - Meilleur F1 et AUC vs SVM linéaire
        - Évaluation sans circularité (8 features)
        """)
        show_fig(charts.fig_roc_curves(), interp_key="roc_curves")

    st.success(f"""
    **Conclusion globale**

    Sur **643 124 profils Twitter** agrégés depuis le corpus World Cup, nous avons construit un
    pipeline complet — de l'ingestion JSON/MongoDB à la modélisation — en respectant un ordre
    méthodologique strict : EDA sur données **sans labels**, puis labellisation Excel, puis ML.

    **Ce que nous avons comparé :** deux familles de méthodes du cours, chacune avec son baseline.
    K-Means face à Isolation Forest en non supervisé ; SVM linéaire face à XGBoost en supervisé.

    **Ce que nous retenons :**
    - **Isolation Forest** (~{iso['count']:,} profils, {iso['pct']:.2f} %, contamination auto) pour l'**exploration initiale** sans annotation manuelle ;
    - **XGBoost** (F1 = {xgb['F1']:.3f} · ROC-AUC = {xgb['ROC-AUC']:.3f}) pour la **classification supervisée** une fois les labels définis.

    **Message central :** les deux approches ne s'opposent pas — elles couvrent des besoins différents
    du cycle de détection. L'IF ouvre l'exploration sur l'ensemble de la base ; XGBoost exploite
    les labels pour discriminer les classes, avec une évaluation **honnête** (8 features hors règles Excel,
    F1 modeste assumé plutôt qu'un 0,97 trompeur par circularité).

    **Contribution du projet :** une démarche rigoureuse de bout en bout — choix de features justifiés
    par l'EDA, traitement explicite de la circularité label/features, et confrontation claire
    des modèles retenus. Les limites (labels subjectifs, biais thématique World Cup, seuil IF
    déterminé automatiquement par les scores d'anomalie) sont connues et documentées ; le livrable démontre une méthodologie reproductible
    plus qu'une solution de production immédiate.
    """.replace(",", " "))

    st.caption("Rapport complet : docs/RAPPORT_PROJET.md · Livrables L1–L4 documentés dans le README")

    st.link_button("Dépôt GitHub", PROJECT["github"], width="content")


def page_equipe():
    hero("Équipe & Rôles", "Répartition des tâches — Livrable L4 IF29", "Groupe 3 · 5 membres")

    section("Correspondance — Cinq dimensions du modèle ML")
    dim_df = pd.DataFrame(ML_DIMENSIONS, columns=["Dimension ML", "Rôle", "Membre"])
    st.dataframe(dim_df, width="stretch", hide_index=True)

    st.divider()
    section("Fiches membres")

    for m in TEAM_MEMBERS:
        roles_str = " · ".join(m["roles"])
        deliverables = ", ".join(f"`{d}`" for d in m["deliverables"])
        tasks_html = "".join(f"<li>{t}</li>" for t in m["tasks"])
        st.markdown(f"""
        <div class="member-card">
            <div class="member-name">Membre {m['id']} — {m['name']}</div>
            <div class="member-role">{roles_str}</div>
            <div class="member-dim">{m['ml_dimension']}</div>
            <p><strong>Soutenance :</strong> {m['soutenance']}</p>
            <p><strong>Livrables :</strong> {deliverables}</p>
            <ul style="margin:0.5rem 0 0 1rem; font-size:0.88rem; color:{THEME['muted']};">{tasks_html}</ul>
        </div>
        """, unsafe_allow_html=True)


def page_notebooks():
    hero("Notebooks Jupyter", "Accès centralisé aux 5 notebooks du projet")

    for nb in NOTEBOOKS:
        st.markdown(f"""
        <div class="notebook-card">
            <span class="nb-tag">{nb['tag']}</span>
            <strong>{nb['title']}</strong><br>
            <code>{nb['file']}</code><br><br>
            {nb['summary']}
        </div>
        """, unsafe_allow_html=True)
        for h in nb["highlights"]:
            st.markdown(f"- {h}")
        st.divider()

    st.info(
        f"Lancer : `jupyter notebook {NOTEBOOKS[0]['file']}` "
        f"(avec `{DATA_FILE.name}` à la racine). "
        "Rapport L1 : `docs/RAPPORT_PROJET.md`."
    )

    footer_github()


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------

PAGES = {
    "Accueil": page_accueil,
    "Pipeline & Données": page_pipeline,
    "Analyse exploratoire": page_eda,
    "Labellisation": page_labellisation,
    "Non supervisé": page_non_supervise,
    "Supervisé": page_supervise,
    "Synthèse": page_synthese,
    "Équipe & Rôles": page_equipe,
    "Notebooks": page_notebooks,
}

with st.sidebar:
    st.markdown("### IF29 · Groupe 3")
    st.markdown("*Portail de démonstration*")
    iso = RESULTS_UNSUPERVISED["Isolation Forest"]
    xgb = RESULTS_SUPERVISED["XGBoost"]
    st.markdown(
        f"**IF (auto)** : {iso['count']:,} profils ({iso['pct']} %)".replace(",", " ")
    )
    st.markdown(f"**XGBoost** : F1 = {xgb['F1']:.3f} · AUC = {xgb['ROC-AUC']:.3f}")
    st.divider()
    choice = st.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")
    st.divider()
    st.caption(PROJECT["course"])
    st.caption("Rapport : docs/RAPPORT_PROJET.md")
    if AGGREGATED_DATA_FILE.exists() and DATA_FILE.exists():
        st.caption("Données : agrégé + labellisé OK")
    elif AGGREGATED_DATA_FILE.exists():
        st.caption("Données : agrégé OK")
    elif DATA_FILE.exists():
        st.caption("Données : labellisé seul")
    else:
        st.caption("Données : CSV absents")

PAGES[choice]()
