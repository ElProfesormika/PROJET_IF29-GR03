"""Constantes et métriques du projet IF29 — Groupe 3 (aucun import demo.*)."""

# 21 colonnes MongoDB → 16 features ML (après EDA)
VARIABLES_AGGREGATED_COUNT = 21
FEATURES_ML_COUNT = 16

VARIABLES_AGGREGATED_21 = [
    "user_id", "screen_name", "verified", "profile_lang", "default_profile_image",
    "followers_count", "friends_count", "followers_friends_ratio",
    "nb_tweets", "nb_retweets", "retweet_ratio",
    "avg_tweet_length", "avg_hashtags", "avg_urls", "avg_mentions",
    "avg_favorites", "avg_retweet_count",
    "first_tweet_date", "last_tweet_date", "active_days", "tweet_frequency",
]

FEATURES_EXCLUDED_FROM_ML = [
    "user_id", "screen_name", "profile_lang",
    "first_tweet_date", "last_tweet_date",
]

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
        "summary": "Distributions, corrélations, réduction 21 → 16 variables pour le ML.",
        "highlights": [
            "643 124 profils — source : users_aggregated.csv (sans labels)",
            "21 variables agrégées → 16 features ML retenues après EDA",
            "Corrélations en % · describe sur le jeu complet",
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
            "K-Means k=7 : ~3 498 profils (0,54 %)",
            "Isolation Forest (auto) : ~42 987 profils",
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
            "Isolation Forest (contamination auto) : ~42 987 profils",
            "XGBoost F1 = 0,443 · ROC-AUC = 0,794",
            "Rapport L1 : docs/RAPPORT_PROJET.md",
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
    "K-Means": {"count": 3_498, "pct": 0.54},
    "Isolation Forest": {"count": 42_987, "pct": 6.68},
    "Consensus": {"count": 3_498, "pct": 0.54},
    "Iso Forest seul": {"count": 39_489, "pct": 6.14},
    "K-Means seul": {"count": 0, "pct": 0.00},
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

# Matrices de confusion (jeu complet 643 124 profils sauf SVM/XGB = test 20 %)
CM_SVM = [[55_875, 51_012], [5_717, 16_021]]
CM_XGB = [[68_824, 38_063], [4_717, 17_021]]
CM_KM_VS_IF = [[600_137, 39_489], [0, 3_498]]
CM_KM_VS_LABELS = [[530_995, 3_204], [108_631, 294]]
CM_IF_VS_LABELS = [[500_466, 33_733], [99_671, 9_254]]


def cm_to_metrics(cm):
    """Métriques binaires depuis une matrice [[TN, FP], [FN, TP]]."""
    tn, fp = cm[0]
    fn, tp = cm[1]
    total = tn + fp + fn + tp
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    accuracy = (tn + tp) / total if total else 0.0
    return {
        "Precision": round(precision, 3),
        "Recall": round(recall, 3),
        "F1": round(f1, 3),
        "Accuracy": round(accuracy, 3),
    }


IF_VS_LABELS_METRICS = cm_to_metrics(CM_IF_VS_LABELS)
KM_VS_LABELS_METRICS = cm_to_metrics(CM_KM_VS_LABELS)

XGB_PC_IMPORTANCE = {
    "PC1": 0.28, "PC2": 0.22, "PC3": 0.18, "PC4": 0.16, "PC5": 0.16,
}
XGB_PC_VARIANCE = {
    "PC1": 32.5, "PC2": 24.1, "PC3": 18.7, "PC4": 14.2, "PC5": 10.5,
}

PIPELINE_STEPS = [
    ("Tweet_Worldcup", "581 fichiers JSONL · ~1,16 M tweets"),
    ("MongoDB + Agrégation", "→ `users_aggregated.csv` · 643 124 profils · **21 variables** · sans label"),
    ("Analyse exploratoire", "Sur `users_aggregated.csv` · describe · corrélations % · **21 → 16 features**"),
    ("Labellisation Excel", "→ `users_labeled_manual.csv` · + `label` · + `anomaly_score`"),
    ("Modélisation ML", "`users_labeled_manual.csv` · StandardScaler → ACP → modèles"),
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

__all__ = [
    "ANOMALY_SCORE_DIST",
    "CM_IF_VS_LABELS",
    "CM_KM_VS_IF",
    "CM_KM_VS_LABELS",
    "CM_SVM",
    "CM_XGB",
    "EDA_NUMERIC",
    "FEATURES_16",
    "FEATURES_EXCLUDED_FROM_ML",
    "FEATURES_ML",
    "FEATURES_ML_COUNT",
    "IF_VS_LABELS_METRICS",
    "KM_VS_LABELS_METRICS",
    "LABEL_COMPARE_COLS",
    "LABEL_RULES",
    "NOTEBOOKS",
    "PIPELINE_STEPS",
    "PROJECT",
    "RESULTS_SUPERVISED",
    "RESULTS_UNSUPERVISED",
    "THEME",
    "VARIABLES_AGGREGATED_21",
    "VARIABLES_AGGREGATED_COUNT",
    "XGB_PC_IMPORTANCE",
    "XGB_PC_VARIANCE",
    "cm_to_metrics",
]
