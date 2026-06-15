# Dataset utilisateurs — Projet IF29 Groupe 3

Documentation complémentaire : [`README.md`](README.md) · [`docs/LABELISATION.md`](docs/LABELISATION.md)

---

## Fichiers de données

| Fichier | Lignes | Colonnes | Description |
|---------|--------|----------|-------------|
| `users_aggregated.csv` | 643 124 | 21 | Profils agrégés MongoDB, sans label |
| `users_labeled_manual.csv` | 643 124 | 23 | Même données + `label` + `anomaly_score` |
| `raw/` | ~1,16 M tweets | — | 581 fichiers JSONL (`Tweet_Worldcup`) |

---

## Notebooks

| Notebook | Rôle | Données | ACP |
|----------|------|---------|-----|
| `Groupe3_Analyse_Exploratoire.ipynb` | EDA | agrégé + labelisé | 7 comp. (16 feat.) |
| `Groupe3_Labelisation.ipynb` | Doc labels | — | — |
| `Groupe3_profils_atypiques_non_Sup.ipynb` | K-Means / Iso. Forest | labelisé | **7 comp.** |
| `Groupe3_profils_atypiques_Sup.ipynb` | SVM / XGBoost | labelisé | **5 comp.** |
| `Groupe3_profils_atypiques_Final.ipynb` | Synthèse | — | — |

---

## Pipeline ML

```
features  ->  StandardScaler  ->  ACP  ->  modèles
```

| Approche | Features | ACP | Labels |
|----------|----------|-----|--------|
| Non supervisé | 16 MongoDB | 7 (~79 %) | exclus |
| Supervisé | 8 hors règles Excel | 5 (100 %) | `label` = cible |

**Trois choix indépendants :** ACP 7 comp. · ACP 5 comp. · k=7 K-Means (clusters).

---

## 8 features supervisées (hors règles Excel)

`followers_count`, `friends_count`, `avg_tweet_length`, `avg_hashtags`, `avg_favorites`, `avg_retweet_count`, `verified`, `default_profile_image`

**Exclues :** `retweet_ratio`, `avg_urls`, `avg_mentions`, `active_days`, `nb_tweets`, `followers_friends_ratio`, `nb_retweets`, `tweet_frequency`
