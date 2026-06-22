"""Équipe et répartition des rôles — IF29 Groupe 3."""

ML_DIMENSIONS = [
    ("Données d'entrée", "Data Engineer", "Housseni YABRE"),
    ("Paramètres d'entrée", "Data Analyst / Feature Engineer", "Vanelle Leita FOTSO AKOUDOUM"),
    ("Métriques d'état du modèle", "Data Scientist (non supervisé)", "Samella LEUKOUO"),
    ("Sorties cibles / Résultats", "ML Engineer (supervisé)", "Dorcas ADRAKE"),
    ("Politique de gestion du modèle", "ML Project Manager / CDO", "Ace ANALLA"),
]

TEAM_MEMBERS = [
    {
        "id": 1,
        "name": "Housseni YABRE",
        "roles": ["Data Engineer", "Data Cleaner"],
        "ml_dimension": "Données d'entrée",
        "soutenance": "Introduction, contexte et pipeline MongoDB (données brutes → profils agrégés)",
        "deliverables": ["scripts/import_local.sh", "scripts/aggregated.sh", "Export_CSV.py", "users_aggregated.csv"],
        "tasks": [
            "Extraction des données JSON (dataset Tweet_Worldcup)",
            "Documentation de la structure des données Twitter",
            "Nettoyage : valeurs manquantes, doublons, incohérences",
            "Séparation tweets / utilisateurs et agrégation par profil",
            "Stockage final MongoDB et export CSV",
        ],
    },
    {
        "id": 2,
        "name": "Vanelle Leita FOTSO AKOUDOUM",
        "roles": ["Data Analyst", "Feature Engineer"],
        "ml_dimension": "Paramètres d'entrée",
        "soutenance": "Analyse exploratoire, features et labellisation Excel",
        "deliverables": [
            "Groupe3_Analyse_Exploratoire.ipynb",
            "Groupe3_Labelisation.ipynb",
            "docs/LABELISATION.md",
        ],
        "tasks": [
            "Analyse exploratoire (statistiques, distributions, corrélations)",
            "Conception des 16 variables explicatives agrégées",
            "Attributs comportementaux, contenu et graphe social",
            "Normalisation et justification des features (littérature)",
            "Participation à la définition des critères de labellisation",
        ],
    },
    {
        "id": 3,
        "name": "Samella LEUKOUO",
        "roles": ["Data Scientist"],
        "ml_dimension": "Métriques d'état du modèle (non supervisé)",
        "soutenance": "Approche non supervisée — K-Means vs Isolation Forest",
        "deliverables": ["Groupe3_profils_atypiques_non_Sup.ipynb"],
        "tasks": [
            "Implémentation K-Means (MiniBatchKMeans, k=7) et Isolation Forest",
            "Choix hyperparamètres et justification (coude, contamination auto)",
            "ACP 7 composantes, évaluation vs labels manuels",
            "Visualisation clusters et comparaison des méthodes",
            "Retenu : Isolation Forest (~42 987 profils, 6,68 %)",
        ],
    },
    {
        "id": 4,
        "name": "Dorcas ADRAKE",
        "roles": ["Machine Learning Engineer", "Data Scientist"],
        "ml_dimension": "Sorties cibles / Résultats (supervisé)",
        "soutenance": "Approche supervisée — SVM vs XGBoost et circularité",
        "deliverables": ["Groupe3_profils_atypiques_Sup.ipynb"],
        "tasks": [
            "Implémentation SVM (LinearSVC) et XGBoost",
            "Split train/test 80/20, ACP 5 composantes, 8 features hors règles",
            "Évaluation : accuracy, F1, recall, precision, ROC-AUC",
            "Analyse circularité label/features (annexe F1 ~ 0,97 vs 0,443)",
            "Retenu : XGBoost (F1 = 0,443, ROC-AUC = 0,794)",
        ],
    },
    {
        "id": 5,
        "name": "Ace ANALLA",
        "roles": ["ML Project Manager", "Chief Data Officer"],
        "ml_dimension": "Politique de gestion du modèle",
        "soutenance": "Synthèse, limites, recommandations et conclusion",
        "deliverables": [
            "Groupe3_profils_atypiques_Final.ipynb",
            "docs/RAPPORT_PROJET.md",
            "docs/PROMPT_SOUTENANCE_CLAUDE.md",
            "demo/app.py",
            "docs/EQUIPE_ROLES.md",
        ],
        "tasks": [
            "Coordination globale et cohérence méthodologique",
            "Validation des choix techniques et des hypothèses",
            "Comparaison supervisée vs non supervisée",
            "Identification limites, biais et risques de labellisation",
            "Rédaction rapport L1, portail démo et préparation soutenance",
        ],
    },
]

PRESENTATION_ORDER = [
    {"ordre": 1, "intervenant": "Housseni YABRE", "partie": "Introduction + pipeline données", "duree": "~2 min"},
    {"ordre": 2, "intervenant": "Vanelle Leita FOTSO AKOUDOUM", "partie": "EDA + labellisation", "duree": "~3 min"},
    {"ordre": 3, "intervenant": "Samella LEUKOUO", "partie": "Non supervisé (K-Means / Isolation Forest)", "duree": "~3 min"},
    {"ordre": 4, "intervenant": "Dorcas ADRAKE", "partie": "Supervisé (SVM / XGBoost) + circularité", "duree": "~4 min"},
    {"ordre": 5, "intervenant": "Ace ANALLA", "partie": "Synthèse, limites, conclusion", "duree": "~3 min"},
]
