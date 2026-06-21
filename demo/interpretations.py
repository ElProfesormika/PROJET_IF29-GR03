"""Interprétations concises affichées sous chaque graphique."""

INTERP = {
    "pipeline_flow": (
        "1) Agrégation MongoDB → users_aggregated.csv (21 variables, sans label). "
        "2) EDA sur ce fichier → justification de 16 features ML. "
        "3) Labellisation Excel → users_labeled_manual.csv (+ label, + anomaly_score). "
        "4) Modélisation ML sur le fichier labellisé."
    ),
    "acp_comparison": (
        "Le non supervisé retient 7 composantes (seuil 75 % sur 16 features). "
        "Le supervisé retient 5 composantes (saturation à 100 % sur 8 features). "
        "Le k=7 de K-Means est un choix de clusters indépendant."
    ),
    "synthesis_final": (
        "Conclusion globale : sur 643 124 profils, Isolation Forest (contamination auto, ~6,7 % détectés, sans labels) "
        "et XGBoost (F1 = 0,443, AUC = 0,794, avec labels) sont complémentaires — "
        "exploration d'abord, classification ensuite. La comparaison rigoureuse et le traitement "
        "de la circularité constituent la contribution principale du projet."
    ),
    "retained_models": (
        "Isolation Forest explore ~6,7 % de profils déviants sans annotation (seuil auto). "
        "XGBoost classifie avec les labels Excel (F1 = 0,443, AUC = 0,794). "
        "Les deux répondent à la problématique par des angles différents."
    ),
    "label_distribution": (
        "Environ 17 % des profils sont atypiques selon la labellisation Excel. "
        "Le déséquilibre des classes est pris en compte dans les modèles supervisés "
        "(class_weight, scale_pos_weight)."
    ),
    "missing_values": (
        "Peu ou pas de valeurs manquantes : le jeu de données agrégé MongoDB "
        "est exploitable directement sans imputation."
    ),
    "describe_aggregated": (
        "Statistiques calculées sur l'intégralité des 643 124 profils "
        "(users_aggregated.csv), avant labellisation. "
        "Les distributions asymétriques (médiane << moyenne) confirment la présence de profils extrêmes."
    ),
    "distributions_grid": (
        "Les variables sont fortement asymétriques (queues longues). "
        "log1p sert uniquement à visualiser ; le ML utilise StandardScaler sans transformation log."
    ),
    "scatter_followers": (
        "La majorité des profils combine peu de followers et une activité modérée. "
        "Quelques profils extrêmes concentrent beaucoup de followers ou de tweets."
    ),
    "boxplots": (
        "Les boxplots tronqués au 95e percentile confirment la présence d'outliers "
        "sur followers, friends et métriques d'activité."
    ),
    "correlation": (
        "Corrélations exprimées en pourcentage (coefficient × 100). "
        "Certaines variables sont fortement liées (ex. nb_tweets / retweet_ratio) : "
        "l'ACP réduira cette redondance en modélisation."
    ),
    "features_reduced": (
        "users_aggregated.csv : 21 colonnes MongoDB. L'EDA en exclut 5 "
        "(identifiants, langue, dates brutes) → 16 features ML. "
        "La labellisation Excel produit ensuite users_labeled_manual.csv."
    ),
    "normal_vs_atypical": (
        "Les profils atypiques se distinguent sur retweet_ratio, avg_urls et avg_mentions, "
        "ce qui justifie les critères de labellisation retenus."
    ),
    "pca_scree": (
        "La variance cumulée dépasse 75 % à 7 composantes (~79 %). "
        "Au-delà, le gain marginal par composante supplémentaire diminue."
    ),
    "pca_scatter_2d": (
        "Normal et atypique se chevauchent partiellement en 2D : "
        "la séparation n'est pas linéaire, d'où l'intérêt de modèles non linéaires (XGBoost, Isolation Forest)."
    ),
    "anomaly_score": (
        "La majorité des profils cumule 0 ou 1 critère (normal). "
        "Le seuil label = 2 transforme ~17 % des profils en atypiques."
    ),
    "kmeans_elbow": (
        "L'inertie diminue avec k ; k=7 est retenu au coude comme compromis "
        "entre granularité et interprétabilité des clusters."
    ),
    "cluster_distribution": (
        "K-Means produit des clusters très déséquilibrés. "
        "Les clusters minoritaires (< 1 % des profils) sont interprétés comme atypiques."
    ),
    "isolation_forest_bar": (
        "Avec contamination = auto, Isolation Forest isole ~42 987 profils "
        "sans utiliser les labels — le seuil est déterminé par les scores d'anomalie."
    ),
    "unsupervised_comparison": (
        "K-Means et Isolation Forest ne détectent pas les mêmes profils. "
        "Le consensus (~3 498) forme un noyau d'anomalies robuste ; "
        "Isolation Forest étend la détection à ~39 489 profils supplémentaires."
    ),
    "cm_km_vs_if": (
        "Peu de profils sont flaggés atypiques par K-Means seul. "
        "Isolation Forest capture un volume bien plus large, "
        "confirmant sa sensibilité supérieure sur ce dataset."
    ),
    "cm_km_vs_labels": (
        "K-Means sous-détecte les atypiques par rapport aux labels Excel "
        "(rappel faible) : il cible un noyau très compact de profils extrêmes."
    ),
    "cm_if_vs_labels": (
        "Isolation Forest améliore le rappel mais génère plus de faux positifs "
        "que K-Means, cohérent avec contamination = auto (~6,7 % détectés)."
    ),
    "acp_supervised": (
        "Avec seulement 8 features, 5 composantes suffisent à capturer 100 % de la variance. "
        "PC6 et PC7 n'apportent aucune information supplémentaire."
    ),
    "xgb_importance": (
        "PC1 et PC2 dominent l'importance XGBoost : le modèle s'appuie surtout "
        "sur les directions de plus grande variance après ACP."
    ),
    "supervised_metrics": (
        "XGBoost est meilleur sur toutes les métriques clés. "
        "Le F1 modéré (0,443) reflète une évaluation honnête sans features des règles Excel."
    ),
    "cm_svm": (
        "Le SVM privilégie le rappel (0,737) au détriment de la précision (0,239) : "
        "il détecte beaucoup d'atypiques mais avec de nombreux faux positifs."
    ),
    "cm_xgb": (
        "XGBoost améliore précision et F1 par rapport au SVM. "
        "Le rappel reste élevé (0,783), signe d'une bonne couverture des atypiques."
    ),
    "roc_curves": (
        "Plus la courbe est proche du coin supérieur gauche, meilleur est le modèle. "
        "XGBoost (AUC = 0,794) discrimine mieux les classes que le SVM (AUC = 0,670)."
    ),
    "circularite": (
        "Avec les 16 features, XGBoost recopie les règles Excel (F1 ~ 0,97). "
        "En excluant les 8 features liées aux règles, le F1 tombe à 0,443 : "
        "c'est l'évaluation scientifique retenue."
    ),
}
