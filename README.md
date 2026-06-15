# IF29 — Détection de profils atypiques sur X (Twitter)

**Projet Groupe 3** — Comparaison de deux méthodes de classification (non supervisée et supervisée)

---

## Contexte

Ce projet compare deux approches de détection de profils atypiques sur **643 124 profils Twitter** agrégés depuis **~1,16 million de tweets** (`Tweet_Worldcup`).

| Approche | Algorithmes comparés | Retenue |
|----------|---------------------|---------|
| **Non supervisée** | K-Means vs Isolation Forest | **Isolation Forest** |
| **Supervisée** | SVM vs XGBoost | **XGBoost** |

---

## Pipeline ML commun

```
features  ->  StandardScaler  ->  ACP  ->  modèles
```

**ACP non supervisée (16 features) :** seuil **75 %** = **7 composantes** (~79 %).

**ACP supervisée (8 features) :** saturation **100 %** = **5 composantes**.

| Critère | Composantes |
|---------|-------------|
| Kaiser (valeur propre > 1) | 5 |
| Seuil 70 % | 6 |
| **Seuil 75 % (retenu, non sup.)** | **7** |
| Seuil 80 % | 8 |

**Important :** ACP 7 comp. (non sup.), ACP 5 comp. (sup.) et **k=7** K-Means (clusters) sont trois décisions **indépendantes**.

| Étape | Non supervisé | Supervisé |
|-------|---------------|-----------|
| Features | 16 variables MongoDB | 8 variables (hors règles Excel) |
| Normalisation | `StandardScaler` | `StandardScaler` (fit train) |
| ACP | 7 composantes (~79 %) | 5 composantes (100 %, 8 feat.) |
| Modèles | K-Means, Isolation Forest | SVM, XGBoost |

---

## Étape 1 — Préparation des données (MongoDB)

Avant toute modélisation ML, un **pipeline de préparation et d'agrégation** transforme les tweets bruts (niveau tweet) en profils utilisateurs (niveau agrégé).

### Données d'entrée

| | |
|--|--|
| **Source** | Dataset `Tweet_Worldcup` (`raw/` — 581 fichiers JSONL) |
| **Volume** | ~1 161 999 tweets |
| **Stockage** | MongoDB — collection `tweets` |
| **Granularité** | 1 document = 1 tweet |

> **Hypothèse fondamentale :** l'analyse porte **uniquement sur l'auteur du tweet observé** (`user`). Les informations de `retweeted_status.user` ne sont **pas** utilisées.

### Import MongoDB

```bash
bash scripts/import_local.sh
```

```
raw/*.json  ->  MongoDB (tweets)  ->  agrégation  ->  users_aggregated.csv
```

### Variables agrégées (21 colonnes)

| Catégorie | Variables |
|-----------|-----------|
| **Profil social** | `followers_count`, `friends_count`, `followers_friends_ratio`, `verified`, `default_profile_image`, `profile_lang` |
| **Activité** | `nb_tweets`, `nb_retweets`, `retweet_ratio` |
| **Contenu** | `avg_tweet_length`, `avg_hashtags`, `avg_urls`, `avg_mentions` |
| **Engagement** | `avg_favorites`, `avg_retweet_count` *(nulles — collecte partielle)* |
| **Temporel** | `first_tweet_date`, `last_tweet_date`, `active_days`, `tweet_frequency` |

---

## Jeu de données ML

```
users_aggregated.csv       ->  labellisation Excel  ->  users_labeled_manual.csv
     (sans label)                  (manuel)              (+ label, + anomaly_score)
```

| Approche | Fichier | Labels en entrée |
|----------|---------|------------------|
| **Non supervisée** | `users_labeled_manual.csv` | Non — 16 features ; `label` pour évaluation |
| **Supervisée** | `users_labeled_manual.csv` | Oui — 8 features hors règles ; `label` = cible |

---

## Structure du dépôt

```
IF29/
├── README.md
├── README_data.md
├── requirements.txt
├── docs/LABELISATION.md
├── scripts/import_local.sh
├── raw/
├── users_aggregated.csv
├── users_labeled_manual.csv
├── Groupe3_Analyse_Exploratoire.ipynb
├── Groupe3_Labelisation.ipynb
├── Groupe3_profils_atypiques_non_Sup.ipynb
├── Groupe3_profils_atypiques_Sup.ipynb
└── Groupe3_profils_atypiques_Final.ipynb
```

---

## Installation

```bash
cd IF29
python3 -m venv venv_if29
source venv_if29/bin/activate
pip install -r requirements.txt
```

---

## Utilisation

```bash
jupyter notebook Groupe3_Analyse_Exploratoire.ipynb
jupyter notebook Groupe3_Labelisation.ipynb
jupyter notebook Groupe3_profils_atypiques_non_Sup.ipynb
jupyter notebook Groupe3_profils_atypiques_Sup.ipynb
jupyter notebook Groupe3_profils_atypiques_Final.ipynb
```

---

## Labellisation manuelle

Labels créés **sous Excel** (filtres, inspection visuelle). Atypique si **>= 2 critères sur 4** :

| # | Règle | Condition |
|---|-------|-----------|
| 1 | Amplification | `retweet_ratio >= 0,8` |
| 2 | Spam | `avg_urls >= 1,5` OU `avg_mentions >= 2` |
| 3 | Activité concentrée | `active_days = 1` ET `nb_tweets >= 2` |
| 4 | Déséquilibre social | `followers_friends_ratio >= 30` |

Détails : [`docs/LABELISATION.md`](docs/LABELISATION.md)

---

## Résultats

### Non supervisé — Isolation Forest retenu

| Méthode | Atypiques | % |
|---------|-----------|---|
| K-Means | ~3 500 | 0,54 % |
| **Isolation Forest** | **~32 141** | **5,00 %** |

### Supervisé — XGBoost retenu (ACP 5 comp. + 8 features hors règles)

| Métrique | SVM | **XGBoost** |
|----------|-----|-------------|
| F1 (Atypique) | 0,361 | **0,443** |
| ROC-AUC | 0,670 | **0,794** |

**Précaution :** avec les 16 features + ACP 7 comp. (annexe), F1 ~ 0,970 (circularité). Évaluation retenue : 8 features + ACP 5 comp. Voir section 8 de `Groupe3_profils_atypiques_Sup.ipynb`.

---

## Livrables IF29

| Livrable | Support |
|----------|---------|
| L1 Rapport | Notebooks + `docs/LABELISATION.md` |
| L2 Code | Ce dépôt + README |
| L3 Soutenance | `Groupe3_profils_atypiques_Final.ipynb` |
| L4 Rôles | À compléter par l'équipe |

---

## Bibliographie

- Ferrara, E. et al. (2016). *The rise of social bots.* Communications of the ACM, 59(7), 96-104.
- Chu, Z. et al. (2012). *Detecting automation of Twitter accounts.* IEEE TDSC, 9(6), 811-824.
- Varol, O. et al. (2017). *Online human-bot interactions.* ICWSM, 280-289.

---

*Projet IF29 — Groupe 3*
