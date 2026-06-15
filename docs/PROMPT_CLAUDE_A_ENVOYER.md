
---

```
Tu es un expert en présentations académiques (soutenance de projet universitaire en data science / ML).
Génère une présentation de soutenance ORALE, claire, professionnelle et structurée, en FRANÇAIS.

## CONSIGNES DE FORMAT

- Nombre de slides visé : 18 à 22
- Public : jury universitaire (professeur IF29)
- Ton : académique mais accessible
- Style : sobre, bleu marine / teal, peu de texte par slide, sans emojis
- Format de sortie : Markdown avec séparateur --- entre chaque slide
- Pour chaque slide indiquer :
  - Titre
  - Contenu (puces courtes, max 5 par slide)
  - Notes orateur (2-3 phrases)
  - Visuel suggéré (graphique, schéma ou tableau)

## ÉQUIPE — Groupe 3

| Dimension ML | Rôle | Membre |
|--------------|------|--------|
| Données d'entrée | Data Engineer / Data Cleaner | Housseni YABRE |
| Paramètres d'entrée | Data Analyst / Feature Engineer | Vanelle Leita FOTSO AKOUDOUM |
| Métriques d'état du modèle | Data Scientist (non supervisé) | Samella LEUKOUO |
| Sorties cibles / Résultats | ML Engineer (supervisé) | Dorcas ADRAKE |
| Politique de gestion du modèle | ML Project Manager / CDO | Ace ANALLA |

Partie présentée par membre :
- Housseni YABRE : introduction, contexte, pipeline MongoDB (JSON → profils)
- Vanelle Leita FOTSO AKOUDOUM : EDA, features, labellisation Excel
- Samella LEUKOUO : non supervisé — K-Means vs Isolation Forest
- Dorcas ADRAKE : supervisé — SVM vs XGBoost, circularité
- Ace ANALLA : synthèse, limites, démo Streamlit, conclusion

Dépôt GitHub : https://github.com/ElProfesormika/PROJET_IF29-GR03
Portail démo : demo/app.py (Streamlit)

## CONTENU DU PROJET

Titre : Détection de profils atypiques sur X (Twitter) — Comparaison de méthodes de classification
Cours : IF29 — Intelligence des données — Groupe 3

Problématique :
- Comptes atypiques sur Twitter (bots, spam, amplification, bursts d'activité)
- Comparer deux approches : non supervisée (sans labels) et supervisée (avec labels)

Données :
- Dataset Tweet_Worldcup : ~1 161 999 tweets, 581 fichiers JSONL
- Pipeline : tweets bruts → MongoDB → agrégation → 643 124 profils, 21 variables
- Hypothèse : auteur du tweet uniquement (user), pas retweeted_status.user
- users_aggregated.csv (sans label) → labellisation Excel → users_labeled_manual.csv

Pipeline :
raw/*.json → MongoDB → agrégation → users_aggregated.csv → Excel → users_labeled_manual.csv
Scripts : scripts/import_local.sh, Export_CSV.py

EDA (Groupe3_Analyse_Exploratoire.ipynb) :
- Distributions asymétriques, peu de valeurs manquantes
- log1p = visualisation uniquement ; StandardScaler seul en ML
- ACP non supervisé : seuil 75 % → 7 composantes (~79 %)

Labellisation Excel (atypique si ≥ 2 critères sur 4) :
1. retweet_ratio ≥ 0,8 — Amplification
2. avg_urls ≥ 1,5 OU avg_mentions ≥ 2 — Spam
3. active_days = 1 ET nb_tweets ≥ 2 — Burst
4. followers_friends_ratio ≥ 30 — Déséquilibre social
Résultat : 534 199 normal (83,1 %) · 108 925 atypique (16,9 %)

Pipeline ML : features → StandardScaler → ACP → modèles

| | Non supervisé | Supervisé |
|--|---------------|-----------|
| Features | 16 MongoDB | 8 hors règles Excel |
| ACP | 7 composantes (~79 %) | 5 composantes (100 %) |
| Modèles | K-Means, Isolation Forest | SVM, XGBoost |
| Retenu | Isolation Forest | XGBoost |

Important : ACP 7 comp., ACP 5 comp. et k=7 K-Means sont 3 choix indépendants.

8 features supervisées : followers_count, friends_count, avg_tweet_length, avg_hashtags, avg_favorites, avg_retweet_count, verified, default_profile_image

Non supervisé (Groupe3_profils_atypiques_non_Sup.ipynb) :
- K-Means k=7 : ~3 500 profils (0,54 %)
- Isolation Forest 5 % : ~32 141 profils (5,00 %) — RETENU
- Consensus : ~3 498 profils

Supervisé (Groupe3_profils_atypiques_Sup.ipynb) — split 80/20 :

| Métrique | SVM | XGBoost |
|----------|-----|---------|
| Accuracy | 55,9 % | 66,7 % |
| F1 | 0,361 | 0,443 |
| Recall | 0,737 | 0,783 |
| Precision | 0,239 | 0,309 |
| ROC-AUC | 0,670 | 0,794 |

Circularité : avec 16 features → F1 ~ 0,970 (recopie règles Excel). Évaluation retenue : 8 features hors règles → F1 = 0,443.

Conclusion :
- Isolation Forest pour l'exploration sans labels
- XGBoost avec labels, sans variables des règles Excel
- Deux approches complémentaires

## SLIDES OBLIGATOIRES

1. Plan de la présentation
2. Slide équipe et répartition des rôles (L4)
3. Schéma pipeline complet
4. Tableau 4 règles labellisation
5. Tableau SVM vs XGBoost
6. Slide circularité
7. Conclusion et recommandations
8. Slide démo Streamlit + lien GitHub
9. Questions

## GRAPHIQUES À PRÉVOIR DANS LES SLIDES

- EDA : distributions, variance cumulée ACP
- Non sup. : coude K-Means, barres détections, matrices confusion
- Sup. : barres F1, courbes ROC, matrices confusion
- Final : synthèse 2 graphiques (Groupe3_profils_atypiques_Final.ipynb)
- Portail démo Streamlit (captures demo/app.py)

## DEMANDE FINALE

Génère la présentation complète slide par SLIDE
Ajoute une slide annexe « Questions jury » avec réponses courtes sur :
- Isolation Forest vs K-Means
- ACP 7 vs 5 composantes
- k=7 K-Means vs 7 composantes ACP
- F1 0,443 vs 0,970 (circularité)
- Fiabilité labels Excel
- Exclusion features supervisées
```
