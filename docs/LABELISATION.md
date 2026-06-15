# Labellisation manuelle des profils atypiques

Document associé au projet IF29 — *Comparaison de deux méthodes de classification pour la détection de profils atypiques sur X (Twitter)*.

---

## 1. Contexte

Le pipeline MongoDB (Étape 1) produit `users_aggregated.csv` : 643 124 profils, 21 variables, **sans label**. Ce fichier est exploitable en non supervisé, mais le modèle supervisé (SVM / XGBoost) nécessite une variable cible.

Une **labellisation manuelle** a été réalisée par l'équipe pour enrichir le jeu de données et produire `users_labeled_manual.csv`.

Conformément au sujet IF29, les labels ont été **définis et validés manuellement** à partir de l'analyse exploratoire (`Groupe3_Analyse_Exploratoire.ipynb`) et de la littérature sur les bots Twitter (Ferrara et al., 2016 ; Chu et al., 2012 ; Varol et al., 2017).

> **Important :** la labellisation a été effectuée **uniquement sous Microsoft Excel** (filtres, tri, inspection visuelle). Aucun script Python n'a été utilisé pour générer les labels.

---

## 2. Relation entre les fichiers

```
users_aggregated.csv  ->  labellisation Excel  ->  users_labeled_manual.csv
     (sans label)            (manuel)               (+ label, + anomaly_score)
```

**`users_labeled_manual.csv`** est le **même fichier** que `users_aggregated.csv`, enrichi de deux colonnes après labellisation. Les 643 124 profils et les 21 variables d'origine sont identiques.

| Fichier | Rôle |
|---------|------|
| `users_aggregated.csv` | Archive pipeline MongoDB — export avant labellisation |
| `users_labeled_manual.csv` | Fichier ML commun — non supervisé et supervisé |

---

## 3. Processus de labellisation (Excel)

### Étape 1 — Export

Ouverture de `users_aggregated.csv` (643 124 lignes) dans **Microsoft Excel**.

### Étape 2 — Filtres et inspection

Pour chaque critère d'anomalie identifié lors de l'EDA, application d'un **filtre Excel** et inspection visuelle des profils concernés :

| # | Filtre Excel | Interprétation |
|---|--------------|----------------|
| 1 | `retweet_ratio >= 0,8` | Amplification — compte qui retweete quasi systématiquement |
| 2 | `avg_urls >= 1,5` **OU** `avg_mentions >= 2` | Spam — contenu surchargé (liens, mentions) |
| 3 | `active_days = 1` **ET** `nb_tweets >= 2` | Burst d'activité — plusieurs tweets en un seul jour |
| 4 | `followers_friends_ratio >= 30` | Déséquilibre social — audience disproportionnée |

### Étape 3 — Score et label

Pour chaque profil, comptage **manuel** du nombre de critères remplis (`anomaly_score`, de 0 à 4) :

| `anomaly_score` | Signification | Label |
|-----------------|---------------|-------|
| 0 | Aucun critère rempli | Normal (`0`) |
| 1 | Un seul critère rempli | Normal (`0`) |
| 2, 3 ou 4 | Deux critères ou plus remplis | Atypique (`1`) |

**Règle finale :** un profil est **atypique** s'il cumule **au moins 2 critères sur 4**.

### Étape 4 — Validation et export

Validation collective des seuils par l'équipe, puis export en CSV : `users_labeled_manual.csv`.

---

## 4. Résultats de la labellisation

| Classe | Nombre | Proportion |
|--------|--------|------------|
| Normal (`label = 0`) | 534 199 | 83,1 % |
| Atypique (`label = 1`) | 108 925 | 16,9 % |

| `anomaly_score` | Profils |
|-----------------|---------|
| 0 | 147 681 |
| 1 | 386 518 |
| 2 | 103 247 |
| 3 | 5 600 |
| 4 | 78 |

---

## 5. Justification des seuils

Les seuils ont été choisis à partir de :

1. **L'analyse exploratoire** — percentiles, outliers, comparaison des distributions
2. **La littérature scientifique** — indicateurs de bots et comptes automatisés
3. **La validation manuelle Excel** — inspection des profils filtrés pour confirmer la pertinence

---

## 6. Utilisation selon l'approche ML

Les deux approches utilisent **`users_labeled_manual.csv`**, avec un rôle différent pour les colonnes de labellisation :

| Colonne | Non supervisé | Supervisé |
|---------|---------------|-----------|
| 16 features MongoDB | Entrée ML | Partiellement (8 hors règles Excel) |
| `label` | Exclu en entrée — évaluation a posteriori | Variable cible |
| `anomaly_score` | Exclu | Exclu |

**Pipeline :** `StandardScaler` -> ACP -> modèles.

**Non supervisé :** 16 features, ACP **7 composantes** (seuil 75 % ~ 79 %), labels exclus à l'entraînement.

**Supervisé :** 8 features hors règles Excel, ACP **5 composantes** (saturation 100 % sur 8 features) (`followers_count`, `friends_count`, `avg_tweet_length`, `avg_hashtags`, `avg_favorites`, `avg_retweet_count`, `verified`, `default_profile_image`). SVM et XGBoost sur l'espace ACP.

---

## 7. Précautions méthodologiques

### Fuite d'information

`anomaly_score` et `label` **ne doivent pas être utilisés comme features** d'entrée.

### Circularité label / features (supervisé)

Les labels découlent de 4 règles sur les mêmes variables comportementales. Si le modèle reçoit ces features (`retweet_ratio`, `avg_urls`, etc.), XGBoost obtient F1 ~ 0,970 (16 features + ACP 7 comp.) : il reproduit les règles Excel, pas une vérité terrain indépendante.

L'évaluation retenue **exclut les 8 features impliquées dans les règles** (voir `Groupe3_profils_atypiques_Sup.ipynb`, section 8 annexe).

---

## 8. Fichiers et notebooks associés

| Fichier / notebook | Description |
|--------------------|-------------|
| `users_aggregated.csv` | Données agrégées MongoDB, sans label |
| `users_labeled_manual.csv` | Données enrichies — fichier ML commun |
| `Groupe3_Labelisation.ipynb` | Synthèse markdown du processus |
| `Groupe3_Analyse_Exploratoire.ipynb` | EDA ayant motivé les seuils |
| `Groupe3_profils_atypiques_non_Sup.ipynb` | K-Means + Isolation Forest |
| `Groupe3_profils_atypiques_Sup.ipynb` | SVM + XGBoost |
| `README.md` | Documentation générale du projet |
