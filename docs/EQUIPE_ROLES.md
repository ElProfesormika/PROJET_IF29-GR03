# Répartition des rôles — IF29 Groupe 3 (L4)

Document associé au livrable **L4** du projet IF29.

---

## Synthèse — Cinq dimensions du modèle ML

| Dimension du modèle ML | Rôle | Membre |
|------------------------|------|--------|
| Données d'entrée | Data Engineer / Data Cleaner | **Housseni YABRE** |
| Paramètres d'entrée | Data Analyst / Feature Engineer | **Vanelle Leita FOTSO AKOUDOUM** |
| Métriques d'état du modèle | Data Scientist (non supervisé) | **Samella LEUKOUO** |
| Sorties cibles / Résultats | ML Engineer (supervisé) | **Dorcas ADRAKE** |
| Politique de gestion du modèle | ML Project Manager / CDO | **Ace ANALLA** |

---

## Membre 1 — Housseni YABRE

**Responsabilité principale :** Données d'entrée

**Rôles :** Data Engineer · Data Cleaner

**Tâches réalisées :**
- Extraction des données à partir des fichiers JSON du dataset Tweet_Worldcup
- Compréhension et documentation de la structure des données Twitter
- Nettoyage : valeurs manquantes, doublons, incohérences
- Structuration tweets / utilisateurs et agrégation par profil
- Mise en place du stockage MongoDB et export `users_aggregated.csv`

**Livrables :** `scripts/import_local.sh`, `Export_CSV.py`, `users_aggregated.csv`

**Soutenance :** Introduction, contexte et pipeline MongoDB

---

## Membre 2 — Vanelle Leita FOTSO AKOUDOUM

**Responsabilité principale :** Paramètres d'entrée

**Rôles :** Data Analyst · Feature Engineer

**Tâches réalisées :**
- Analyse exploratoire (statistiques, distributions, corrélations)
- Conception des 16 variables explicatives agrégées
- Définition d'attributs comportementaux, contenu et graphe social
- Normalisation et justification des features (littérature Ferrara, Chu, Varol)
- Documentation de la labellisation Excel

**Livrables :** `Groupe3_Analyse_Exploratoire.ipynb`, `Groupe3_Labelisation.ipynb`, `docs/LABELISATION.md`

**Soutenance :** EDA, features et labellisation

---

## Membre 3 — Samella LEUKOUO

**Responsabilité principale :** Métriques d'état du modèle non supervisé

**Rôle :** Data Scientist

**Tâches réalisées :**
- Implémentation K-Means (MiniBatchKMeans, k=7) et Isolation Forest
- Choix des hyperparamètres (coude d'inertie, contamination 5 %)
- ACP 7 composantes et évaluation vs labels manuels
- Visualisation et interprétation des clusters
- Retenu : **Isolation Forest** (~32 141 profils, 5 %)

**Livrables :** `Groupe3_profils_atypiques_non_Sup.ipynb`

**Soutenance :** Approche non supervisée

---

## Membre 4 — Dorcas ADRAKE

**Responsabilité principale :** Sorties cibles et résultats supervisés

**Rôles :** Machine Learning Engineer · Data Scientist

**Tâches réalisées :**
- Implémentation SVM (LinearSVC) et XGBoost
- Split train/test 80/20, ACP 5 composantes, 8 features hors règles Excel
- Évaluation : accuracy, F1, recall, precision, ROC-AUC, matrices de confusion
- Analyse de la circularité label/features (annexe)
- Retenu : **XGBoost** (F1 = 0,443, ROC-AUC = 0,794)

**Livrables :** `Groupe3_profils_atypiques_Sup.ipynb`

**Soutenance :** Approche supervisée et circularité

---

## Membre 5 — Ace ANALLA

**Responsabilité principale :** Politique de gestion du modèle et coordination

**Rôles :** ML Project Manager · Chief Data Officer

**Tâches réalisées :**
- Coordination globale et cohérence méthodologique
- Supervision des choix techniques et validation des hypothèses
- Comparaison globale supervisée vs non supervisée
- Identification des limites, biais et risques de labellisation
- Rédaction L4, portail démo Streamlit, prompt soutenance, conclusion

**Livrables :** `Groupe3_profils_atypiques_Final.ipynb`, `demo/`, `docs/PROMPT_SOUTENANCE_CLAUDE.md`, ce document

**Soutenance :** Synthèse, limites, recommandations et conclusion

---

*Projet IF29 — Groupe 3*
