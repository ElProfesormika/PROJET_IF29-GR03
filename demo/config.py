"""Constantes et métriques du projet IF29 — Groupe 3."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "users_labeled_manual.csv"

PROJECT = {
    "title": "Détection de profils atypiques sur X (Twitter)",
    "course": "IF29 — Intelligence des données",
    "team": "Groupe 3",
    "github": "https://github.com/ElProfesormika/PROJET_IF29-GR03",
    "profiles": 643_124,
    "tweets": 1_161_999,
    "atypical_pct": 16.9,
    "atypical_count": 108_925,
    "normal_count": 534_199,
}

FEATURES_16 = [
    "followers_count", "friends_count", "followers_friends_ratio",
    "nb_tweets", "nb_retweets", "retweet_ratio",
    "avg_tweet_length", "avg_hashtags", "avg_urls", "avg_mentions",
    "avg_favorites", "avg_retweet_count",
    "active_days", "tweet_frequency", "verified", "default_profile_image",
]

EDA_NUMERIC = [
    "followers_count", "friends_count", "nb_tweets", "retweet_ratio",
    "avg_tweet_length", "avg_hashtags", "avg_urls", "avg_mentions",
]

LABEL_COMPARE_COLS = [
    "followers_count", "friends_count", "retweet_ratio",
    "avg_urls", "avg_mentions", "nb_tweets", "active_days",
]

NOTEBOOKS = [
    {
        "id": "eda",
        "file": "Groupe3_Analyse_Exploratoire.ipynb",
        "title": "Analyse exploratoire",
        "tag": "EDA",
        "summary": "Distributions, corrélations, choix ACP à 7 composantes (seuil 75 %).",
        "highlights": [
            "643 124 profils, distributions asymétriques",
            "log1p pour visualisation uniquement",
            "ACP retenue : 7 composantes (~79 % variance)",
        ],
    },
    {
        "id": "label",
        "file": "Groupe3_Labelisation.ipynb",
        "title": "Labellisation",
        "tag": "LABEL",
        "summary": "Processus Excel : 4 critères, score 0-4, label atypique si ≥ 2 critères.",
        "highlights": [
            "Labellisation manuelle sous Excel",
            "16,9 % de profils atypiques",
            "Inspirée EDA + littérature (Ferrara, Chu, Varol)",
        ],
    },
    {
        "id": "unsupervised",
        "file": "Groupe3_profils_atypiques_non_Sup.ipynb",
        "title": "Non supervisé",
        "tag": "UNSUP",
        "summary": "K-Means vs Isolation Forest sur 16 features + ACP 7 composantes.",
        "highlights": [
            "K-Means k=7 : ~3 500 profils (0,54 %)",
            "Isolation Forest 5 % : ~32 141 profils",
            "Retenu : Isolation Forest",
        ],
    },
    {
        "id": "supervised",
        "file": "Groupe3_profils_atypiques_Sup.ipynb",
        "title": "Supervisé",
        "tag": "SUP",
        "summary": "SVM vs XGBoost sur 8 features hors règles + ACP 5 composantes.",
        "highlights": [
            "Split train/test 80/20 stratifié",
            "XGBoost F1 = 0,443 · ROC-AUC = 0,794",
            "Annexe circularité : F1 ~ 0,970 avec 16 features",
        ],
    },
    {
        "id": "final",
        "file": "Groupe3_profils_atypiques_Final.ipynb",
        "title": "Synthèse finale",
        "tag": "FIN",
        "summary": "Comparaison des approches retenues et recommandations.",
        "highlights": [
            "Isolation Forest pour l'exploration",
            "XGBoost avec features hors règles",
            "Deux approches complémentaires",
        ],
    },
]

LABEL_RULES = [
    ("Amplification", "retweet_ratio ≥ 0,8", "Retweet quasi systématique"),
    ("Spam", "avg_urls ≥ 1,5 OU avg_mentions ≥ 2", "Contenu surchargé"),
    ("Burst", "active_days = 1 ET nb_tweets ≥ 2", "Activité concentrée"),
    ("Déséquilibre social", "followers_friends_ratio ≥ 30", "Audience disproportionnée"),
]

ANOMALY_SCORE_DIST = {
    0: 147_681,
    1: 386_518,
    2: 103_247,
    3: 5_600,
    4: 78,
}

FEATURES_ML = {
    "non_supervised": 16,
    "supervised": 8,
    "excluded_supervised": [
        "retweet_ratio", "avg_urls", "avg_mentions", "active_days",
        "nb_tweets", "followers_friends_ratio", "nb_retweets", "tweet_frequency",
    ],
    "kept_supervised": [
        "followers_count", "friends_count", "avg_tweet_length", "avg_hashtags",
        "avg_favorites", "avg_retweet_count", "verified", "default_profile_image",
    ],
}

RESULTS_UNSUPERVISED = {
    "K-Means": {"count": 3_500, "pct": 0.54},
    "Isolation Forest": {"count": 32_141, "pct": 5.00},
    "Consensus": {"count": 3_498, "pct": 0.54},
    "Iso Forest seul": {"count": 28_643, "pct": 4.45},
    "K-Means seul": {"count": 2, "pct": 0.00},
}

RESULTS_SUPERVISED = {
    "SVM": {
        "Accuracy": 0.559, "F1": 0.361, "Recall": 0.737,
        "Precision": 0.239, "ROC-AUC": 0.670,
    },
    "XGBoost": {
        "Accuracy": 0.667, "F1": 0.443, "Recall": 0.783,
        "Precision": 0.309, "ROC-AUC": 0.794,
    },
}

# Matrices dérivées des métriques (jeu test 20 %, 128 625 profils)
CM_SVM = [[55_875, 51_012], [5_717, 16_021]]
CM_XGB = [[68_824, 38_063], [4_717, 17_021]]
CM_KM_VS_IF = [[610_981, 28_643], [2, 3_498]]

XGB_PC_IMPORTANCE = {
    "PC1": 0.28, "PC2": 0.22, "PC3": 0.18, "PC4": 0.16, "PC5": 0.16,
}
XGB_PC_VARIANCE = {
    "PC1": 32.5, "PC2": 24.1, "PC3": 18.7, "PC4": 14.2, "PC5": 10.5,
}

PIPELINE_STEPS = [
    ("Tweet_Worldcup", "581 fichiers JSONL · ~1,16 M tweets"),
    ("MongoDB", "Import + collection tweets"),
    ("Agrégation", "users_aggregated.csv · 643 124 profils"),
    ("Labellisation Excel", "users_labeled_manual.csv"),
    ("ML", "StandardScaler → ACP → modèles"),
]

THEME = {
    "bg": "#F4F6F9",
    "surface": "#FFFFFF",
    "primary": "#1565C0",
    "primary_dark": "#0D47A1",
    "accent": "#00838F",
    "text": "#1A2332",
    "muted": "#5C6B7A",
    "border": "#DDE3EA",
    "normal": "#1565C0",
    "atypical": "#C62828",
    "success": "#2E7D32",
    "warning": "#EF6C00",
}

# Réexport pour compatibilité
from demo.team import ML_DIMENSIONS, TEAM_MEMBERS  # noqa: F401, E402
