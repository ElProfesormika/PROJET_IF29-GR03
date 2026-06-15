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

from demo.config import (
    DATA_FILE,
    EDA_NUMERIC,
    FEATURES_16,
    FEATURES_ML,
    LABEL_COMPARE_COLS,
    LABEL_RULES,
    NOTEBOOKS,
    PIPELINE_STEPS,
    PROJECT,
    RESULTS_SUPERVISED,
    RESULTS_UNSUPERVISED,
    THEME,
    CM_KM_VS_IF,
    CM_SVM,
    CM_XGB,
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


@st.cache_data(show_spinner="Chargement des données…")
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


@st.cache_data(show_spinner="Calcul ACP (16 features)…")
def cached_pca_16(_hash: int):
    df = load_sample()
    return charts.compute_pca_16(df)


@st.cache_data(show_spinner="Calcul ACP supervisé…")
def cached_pca_8(_hash: int):
    df = load_sample()
    return charts.compute_pca_8_supervised(df)


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
    c1.metric("Profils analysés", f"{PROJECT['profiles']:,}".replace(",", " "))
    c2.metric("Tweets source", f"~{PROJECT['tweets']:,}".replace(",", " "))
    c3.metric("Profils atypiques", f"{PROJECT['atypical_pct']} %")
    c4.metric("Algorithmes comparés", "4")

    st.divider()

    col_l, col_r = st.columns(2)
    with col_l:
        section("Objectif", "Deux approches complémentaires de détection")
        st.markdown("""
        | Approche | Comparé | Retenu |
        |----------|---------|--------|
        | Non supervisée | K-Means vs Isolation Forest | **Isolation Forest** |
        | Supervisée | SVM vs XGBoost | **XGBoost** |
        """)
        show_fig(charts.fig_pipeline_flow(), interp_key="pipeline_flow")

    with col_r:
        section("Pipeline ML", "StandardScaler → ACP → modèles")
        st.code("features  →  StandardScaler  →  ACP  →  modèles", language="text")
        show_fig(charts.fig_acp_comparison(), interp_key="acp_comparison")

    section("Synthèse visuelle", "Résultats des méthodes retenues")
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
    hero("Pipeline & Données", "De Tweet_Worldcup aux profils prêts pour le ML", "Étape 1")

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

    section("Variables agrégées", "21 colonnes MongoDB")
    st.markdown("""
    | Catégorie | Variables |
    |-----------|-----------|
    | Profil social | followers_count, friends_count, followers_friends_ratio, verified, default_profile_image |
    | Activité | nb_tweets, nb_retweets, retweet_ratio |
    | Contenu | avg_tweet_length, avg_hashtags, avg_urls, avg_mentions |
    | Engagement | avg_favorites, avg_retweet_count (collecte partielle) |
    | Temporel | active_days, tweet_frequency, first/last_tweet_date |
    """)

    section("Répartition des labels")
    show_fig(charts.fig_label_distribution_full(), interp_key="label_distribution")


def page_eda():
    nb = next(n for n in NOTEBOOKS if n["id"] == "eda")
    hero("Analyse exploratoire", nb["summary"], f"Notebook · {nb['file']}")

    df = load_sample()
    if df.empty:
        st.error(f"`{DATA_FILE.name}` introuvable à la racine du projet.")
        return

    tabs = st.tabs([
        "Qualité des données", "Distributions", "Outliers & Corrélation",
        "Normal vs Atypique", "ACP",
    ])

    with tabs[0]:
        section("Valeurs manquantes")
        show_fig(charts.fig_missing_values(df), interp_key="missing_values")
        section("Répartition des labels (échantillon)")
        counts = df["label"].value_counts().sort_index()
        show_fig(charts.fig_label_distribution_full({
            "Normal": int(counts.get(0, 0)),
            "Atypique": int(counts.get(1, 0)),
        }), interp_key="label_distribution")

    with tabs[1]:
        section("Distributions log1p — 8 variables clés")
        show_fig(charts.fig_distributions_grid(df, EDA_NUMERIC), interp_key="distributions_grid")
        section("Followers vs Activité")
        show_fig(charts.fig_scatter_followers_tweets(df), interp_key="scatter_followers")

    with tabs[2]:
        section("Boxplots (95e percentile)")
        show_fig(charts.fig_boxplots(df, EDA_NUMERIC[:6]), interp_key="boxplots")
        section("Matrice de corrélation — 16 features ML")
        cols = [c for c in FEATURES_16 if c in df.columns]
        show_fig(charts.fig_correlation_heatmap(df, cols), interp_key="correlation")

    with tabs[3]:
        section("Comparaison Normal vs Atypique")
        show_fig(charts.fig_normal_vs_atypical(df, LABEL_COMPARE_COLS), interp_key="normal_vs_atypical")

    with tabs[4]:
        evr, var_cum, n75, X2, labels = cached_pca_16(len(df))
        section("Scree plot & variance cumulée", "Sélection : seuil 75 % → 7 composantes (~79 %)")
        show_fig(charts.fig_pca_scree(evr, var_cum, n75, "ACP non supervisée (16 features)"),
                  interp_key="pca_scree")
        if labels is not None:
            section("Projection ACP 2D")
            show_fig(charts.fig_pca_scatter_2d(X2, labels), interp_key="pca_scatter_2d")

        st.markdown("""
        | Critère | Composantes |
        |---------|-------------|
        | Kaiser (valeur propre > 1) | 5 |
        | Seuil 70 % | 6 |
        | **Seuil 75 % (retenu)** | **7 (~79 %)** |
        | Seuil 80 % | 8 |
        """)


def page_labellisation():
    nb = next(n for n in NOTEBOOKS if n["id"] == "label")
    hero("Labellisation manuelle", nb["summary"], f"Notebook · {nb['file']}")

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
    - **Features :** {FEATURES_ML['non_supervised']} variables MongoDB
    - **ACP :** 7 composantes (~79 % variance)
    - **Labels :** exclus à l'entraînement — évaluation a posteriori
    """)

    tabs = st.tabs(["ACP", "K-Means", "Isolation Forest", "Comparaison", "Matrices"])

    with tabs[0]:
        evr, var_cum, n75, _, _ = cached_pca_16(len(load_sample()))
        show_fig(charts.fig_pca_scree(evr, var_cum, 7, "ACP — 16 features (non supervisé)"),
                  interp_key="pca_scree")

    with tabs[1]:
        k_range, inertia, cluster_counts = cached_kmeans(len(load_sample()))
        show_fig(charts.fig_kmeans_elbow(k_range, inertia), interp_key="kmeans_elbow")
        show_fig(charts.fig_cluster_distribution(cluster_counts), interp_key="cluster_distribution")

    with tabs[2]:
        show_fig(charts.fig_isolation_forest_bar(), interp_key="isolation_forest_bar")
        km = RESULTS_UNSUPERVISED["K-Means"]
        iso = RESULTS_UNSUPERVISED["Isolation Forest"]
        c1, c2, c3 = st.columns(3)
        c1.metric("K-Means", f"{km['count']:,}".replace(",", " "), f"{km['pct']} %")
        c2.metric("Consensus", f"{RESULTS_UNSUPERVISED['Consensus']['count']:,}".replace(",", " "))
        c3.metric("Isolation Forest (retenu)", f"{iso['count']:,}".replace(",", " "), f"{iso['pct']} %")

    with tabs[3]:
        show_fig(charts.fig_unsupervised_comparison(), interp_key="unsupervised_comparison")
        st.success(
            "**Isolation Forest retenu** — conçu pour la détection d'anomalies, "
            "plus sensible que K-Means sur 643 000 profils."
        )

    with tabs[4]:
        col1, col2 = st.columns(2)
        with col1:
            show_fig(charts.fig_heatmap_cm(
                CM_KM_VS_IF, "Concordance K-Means vs Isolation Forest",
                "Isolation Forest", "K-Means",
                ["Normal", "Atypique"], ["Normal", "Atypique"],
            ), interp_key="cm_km_vs_if")
        with col2:
            show_fig(charts.fig_kmeans_vs_labels(), interp_key="cm_km_vs_labels")
        show_fig(charts.fig_isoforest_vs_labels(), interp_key="cm_if_vs_labels")


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

    tabs = st.tabs(["ACP", "Métriques", "Matrices de confusion", "Courbes ROC", "Circularité"])

    with tabs[0]:
        _, var_cum, n_comp = cached_pca_8(len(load_sample()))
        show_fig(charts.fig_acp_supervised_variance(var_cum, n_comp), interp_key="acp_supervised")
        show_fig(charts.fig_xgb_importance(), interp_key="xgb_importance")

    with tabs[1]:
        show_fig(charts.fig_supervised_metrics(), interp_key="supervised_metrics")
        results_df = pd.DataFrame(RESULTS_SUPERVISED).T
        results_df.columns = ["Accuracy", "F1", "Recall", "Precision", "ROC-AUC"]
        st.dataframe(results_df.round(3), width="stretch")

    with tabs[2]:
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

    with tabs[3]:
        show_fig(charts.fig_roc_curves(), interp_key="roc_curves")

    with tabs[4]:
        show_fig(charts.fig_circularite(), interp_key="circularite")
        st.warning(
            "Avec les **16 features complètes**, XGBoost atteint F1 ~ **0,970** : "
            "le modèle recopie les règles Excel. "
            "Évaluation retenue : **8 features hors règles** → F1 = **0,443**."
        )


def page_synthese():
    nb = next(n for n in NOTEBOOKS if n["id"] == "final")
    hero("Synthèse & Recommandations", nb["summary"], f"Notebook · {nb['file']}")

    section("Comparaison des approches retenues")
    st.markdown("""
    | | Isolation Forest | XGBoost |
    |--|------------------|---------|
    | Labels requis | Non | Oui (Excel) |
    | Features ML | 16 | 8 (hors règles) |
    | ACP | 7 composantes | 5 composantes |
    | Résultat | ~32 141 (5 %) | F1 = 0,443 |
    | Usage | Exploration | Prédiction avec labels |
    """)

    section("Graphiques de synthèse")
    show_fig(charts.fig_synthesis_final(), interp_key="synthesis_final")
    col1, col2 = st.columns(2)
    with col1:
        show_fig(charts.fig_unsupervised_comparison(), interp_key="unsupervised_comparison")
    with col2:
        show_fig(charts.fig_supervised_metrics(), interp_key="supervised_metrics")

    section("Circularité & recommandations")
    show_fig(charts.fig_circularite(), interp_key="circularite")
    st.success("""
    **Recommandation :**
    1. **Isolation Forest** en phase d'exploration (sans annotation).
    2. **XGBoost** une fois les labels définis, sans réutiliser les variables des règles Excel.
    """)

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
        f"(avec `{DATA_FILE.name}` à la racine)."
    )

    footer_github()


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------

PAGES = {
    "Accueil": page_accueil,
    "Équipe & Rôles": page_equipe,
    "Pipeline & Données": page_pipeline,
    "Analyse exploratoire": page_eda,
    "Labellisation": page_labellisation,
    "Non supervisé": page_non_supervise,
    "Supervisé": page_supervise,
    "Synthèse": page_synthese,
    "Notebooks": page_notebooks,
}

with st.sidebar:
    st.markdown("### IF29 · Groupe 3")
    st.markdown("*Portail de démonstration*")
    st.divider()
    choice = st.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")
    st.divider()
    st.caption(PROJECT["course"])
    st.caption("Détection profils atypiques Twitter")
    if DATA_FILE.exists():
        st.caption("Statut données : OK")
    else:
        st.caption("Statut données : CSV absent")

PAGES[choice]()
