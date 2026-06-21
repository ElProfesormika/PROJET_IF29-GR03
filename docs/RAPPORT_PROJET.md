# Rapport de projet IF29 — Détection de profils atypiques sur X (Twitter)

**Cours :** IF29 — Traitement de données (Data Analytics)  
**Équipe :** Groupe 3  
**Membres :** Housseni YABRE · Vanelle Leita FOTSO AKOUDOUM · Samella LEUKOUO · Dorcas ADRAKE · Ace ANALLA  
**Date :** Juin 2026  
**Dépôt :** [GitHub — PROJET_IF29-GR03](https://github.com/ElProfesormika/PROJET_IF29-GR03)

---

## Table des matières

1. [Introduction](#1-introduction)
2. [Contexte et problématique](#2-contexte-et-problématique)
3. [Description des données](#3-description-des-données)
4. [Méthodologie](#4-méthodologie)
5. [Résultats](#5-résultats)
6. [Discussion et analyse comparative](#6-discussion-et-analyse-comparative)
7. [Limites du projet](#7-limites-du-projet)
8. [Conclusion et recommandations](#8-conclusion-et-recommandations)
9. [Bibliographie](#9-bibliographie)
10. [Annexes](#10-annexes)

---

## 1. Introduction

### 1.1 Objectif du projet

Ce projet s'inscrit dans le cadre du cours **IF29 — Traitement de données** et répond à l'énoncé suivant : *comparer deux approches de classification appliquées à la détection de profils « atypiques » sur Twitter*, l'une **non supervisée**, l'autre **supervisée**.

Notre équipe a choisi d'étudier **643 124 profils Twitter** agrégés à partir d'environ **1,16 million de tweets** collectés pendant la Coupe du Monde 2018 (`Tweet_Worldcup`). L'objectif n'est pas de produire un système de production prêt à l'emploi, mais de **construire, comparer et documenter** une démarche analytique reproductible, en explicitant les choix méthodologiques, les compromis et les limites.

### 1.2 Définition retenue de « profil atypique »

Un profil atypique est un compte dont les **caractéristiques statistiques ou comportementales s'écartent significativement** de la population moyenne observée dans le corpus. Cette définition s'appuie sur :

- La littérature sur les **bots**, **spammeurs** et comptes automatisés (Ferrara et al., 2016 ; Chu et al., 2012 ; Varol et al., 2017) ;
- L'**analyse exploratoire** de nos données (distributions asymétriques, outliers sur le ratio followers/friends, amplification par retweets) ;
- Une **labellisation manuelle** sous Excel, fondée sur quatre critères comportementaux cumulables.

Nous ne prétendons pas disposer d'une vérité terrain absolue : les labels sont des **proxies opérationnels** permettant d'évaluer a posteriori les modèles non supervisés et d'entraîner les modèles supervisés.

### 1.3 Approche globale

| Dimension | Non supervisée | Supervisée |
|-----------|----------------|------------|
| Algorithmes comparés | K-Means vs **Isolation Forest** | SVM vs **XGBoost** |
| Modèle retenu | **Isolation Forest** | **XGBoost** |
| Labels en entrée | Non | Oui (`label`) |
| Features ML | 16 variables MongoDB | 8 variables hors règles Excel |
| Réduction dimension | ACP — 7 composantes (~79 %) | ACP — 5 composantes (100 %) |

Les deux approches retenues sont **complémentaires** : Isolation Forest pour l'exploration initiale sans annotation ; XGBoost pour la classification une fois les labels définis.

### 1.4 Livrables produits

| Livrable IF29 | Support dans ce dépôt |
|---------------|----------------------|
| **L1 — Rapport** | Ce document + notebooks + `docs/LABELISATION.md` |
| **L2 — Code documenté** | Dépôt GitHub, README, notebooks commentés |
| **L3 — Soutenance** | `Groupe3_profils_atypiques_Final.ipynb`, `docs/PROMPT_SOUTENANCE_CLAUDE.md`, portail `demo/app.py` |
| **L4 — Rôles équipe** | `docs/EQUIPE_ROLES.md` |

---

## 2. Contexte et problématique

### 2.1 Enjeu de la détection de profils atypiques

Sur les réseaux sociaux, une fraction non négligeable de comptes présente des comportements automatisés ou coordonnés : amplification de contenus (retweets massifs), spam (URLs et mentions excessives), activité concentrée sur une courte période, ou audiences artificiellement gonflées (ratio followers/friends extrême). Identifier ces profils est un enjeu pour :

- La **modération de contenu** et la lutte contre la désinformation ;
- La **qualité des analyses** de corpus (biais si bots non filtrés) ;
- La **compréhension des dynamiques** informationnelles lors d'événements massifs (ici, la Coupe du Monde).

### 2.2 Question de recherche

> *Comment comparer rigoureusement une approche non supervisée (sans labels) et une approche supervisée (avec labels) pour la détection de profils atypiques sur un grand corpus Twitter, et quels modèles retenir dans chaque famille ?*

Sous-questions :

1. Quels **indicateurs comportementaux** extraire des tweets bruts ?
2. Comment **labelliser** des profils en l'absence de ground truth officielle ?
3. Quels **algorithmes** choisir et comment **évaluer** leur concordance ?
4. Comment **éviter la circularité** entre règles de labellisation et features supervisées ?

### 2.3 Hypothèses de travail

1. Les variables agrégées au niveau **profil** (followers, activité, contenu) suffisent à discriminer une partie des comportements atypiques.
2. Une **ACP** préalable réduit la redondance entre features corrélées.
3. **Isolation Forest** détectera plus de profils déviants que K-Means sur un dataset massif et asymétrique.
4. **XGBoost** surpassera un SVM linéaire grâce à sa capacité non linéaire, sous réserve d'une évaluation **sans features des règles Excel**.

---

## 3. Description des données

### 3.1 Source et volume

| Élément | Valeur |
|---------|--------|
| Dataset source | `Tweet_Worldcup` |
| Fichiers bruts | 581 fichiers JSONL (`raw/`) |
| Tweets | ~1 161 999 |
| Profils agrégés | 643 124 |
| Période | Juin 2018 (Coupe du Monde) |
| Stockage intermédiaire | MongoDB — collection `tweets` |
| Export final | `users_aggregated.csv` puis `users_labeled_manual.csv` |

**Hypothèse fondamentale :** l'analyse porte uniquement sur l'**auteur du tweet observé** (`user`). Les métadonnées de `retweeted_status.user` ne sont pas utilisées.

### 3.2 Pipeline de préparation (Étape 1)

```
raw/*.json  →  MongoDB (tweets)  →  agrégation par user_id  →  users_aggregated.csv
```

**Scripts :** `scripts/import_local.sh`, `Export_CSV.py`

L'agrégation produit **21 variables** par profil :

| Catégorie | Variables |
|-----------|-----------|
| **Identifiants** | `user_id`, `screen_name` |
| **Profil social** | `followers_count`, `friends_count`, `followers_friends_ratio`, `verified`, `default_profile_image`, `profile_lang` |
| **Activité** | `nb_tweets`, `nb_retweets`, `retweet_ratio` |
| **Contenu** | `avg_tweet_length`, `avg_hashtags`, `avg_urls`, `avg_mentions` |
| **Engagement** | `avg_favorites`, `avg_retweet_count` *(souvent nulles — collecte partielle)* |
| **Temporel** | `first_tweet_date`, `last_tweet_date`, `active_days`, `tweet_frequency` |

### 3.3 Réduction des variables (EDA)

L'analyse exploratoire (`Groupe3_Analyse_Exploratoire.ipynb`) sur `users_aggregated.csv` (**sans labels**) a conduit à exclure **5 variables** du ML :

| Variable exclue | Justification |
|-----------------|---------------|
| `user_id`, `screen_name` | Identifiants — pas de valeur prédictive |
| `profile_lang` | Catégorielle peu informative dans ce contexte |
| `first_tweet_date`, `last_tweet_date` | Redondantes avec `active_days` / `tweet_frequency` |

**16 features ML** retenues pour la modélisation non supervisée.

### 3.4 Caractéristiques statistiques du jeu

- **Peu ou pas de valeurs manquantes** sur le jeu agrégé — exploitable directement après normalisation.
- **Distributions fortement asymétriques** (queues longues) : médiane << moyenne sur `followers_count`, `nb_tweets`, etc.
- **Présence d'outliers** confirmée par boxplots tronqués au 95e percentile.
- **Corrélations notables** : par exemple entre `nb_tweets` et `retweet_ratio`, justifiant l'ACP en modélisation.

### 3.5 Labellisation manuelle

Après l'EDA, une labellisation **sous Microsoft Excel** (filtres, tri, inspection visuelle) produit `users_labeled_manual.csv` (+2 colonnes : `label`, `anomaly_score`).

**Quatre critères d'anomalie :**

| # | Règle | Condition | Interprétation |
|---|-------|-----------|----------------|
| 1 | Amplification | `retweet_ratio ≥ 0,8` | Compte qui retweete quasi systématiquement |
| 2 | Spam | `avg_urls ≥ 1,5` OU `avg_mentions ≥ 2` | Contenu surchargé |
| 3 | Burst | `active_days = 1` ET `nb_tweets ≥ 2` | Activité concentrée |
| 4 | Déséquilibre social | `followers_friends_ratio ≥ 30` | Audience disproportionnée |

**Règle finale :** atypique si **≥ 2 critères sur 4** (`anomaly_score ≥ 2`).

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

Détails complets : [`docs/LABELISATION.md`](LABELISATION.md)

### 3.6 Description détaillée des 16 features ML

Chaque feature agrégée capture une facette du comportement du profil, en lien avec la littérature sur la détection de bots et comptes automatisés :

| Feature | Type | Description | Lien littérature |
|---------|------|-------------|------------------|
| `followers_count` | Numérique | Nombre d'abonnés au profil | Indicateur de visibilité / crédibilité perçue |
| `friends_count` | Numérique | Nombre de comptes suivis | Comptes bots suivent souvent massivement |
| `followers_friends_ratio` | Numérique | Ratio followers / friends | Déséquilibre social (Chu et al., 2012) |
| `nb_tweets` | Numérique | Tweets dans le corpus | Volume d'activité |
| `nb_retweets` | Numérique | Retweets émis | Comportement d'amplification |
| `retweet_ratio` | Numérique | Part de retweets dans l'activité | Signal d'automatisation (Ferrara et al., 2016) |
| `avg_tweet_length` | Numérique | Longueur moyenne des tweets | Contenu original vs minimal |
| `avg_hashtags` | Numérique | Hashtags moyens par tweet | Stratégie de visibilité |
| `avg_urls` | Numérique | URLs moyennes par tweet | Spam / redirection (Varol et al., 2017) |
| `avg_mentions` | Numérique | Mentions moyennes par tweet | Comportement de spam |
| `avg_favorites` | Numérique | Favoris moyens reçus | Engagement (données partielles) |
| `avg_retweet_count` | Numérique | Retweets moyens reçus | Portée (données partielles) |
| `active_days` | Numérique | Jours distincts d'activité | Régularité vs burst |
| `tweet_frequency` | Numérique | Tweets par jour actif | Intensité temporelle |
| `verified` | Binaire | Compte certifié | Signal de légitimité |
| `default_profile_image` | Binaire | Avatar par défaut | Comptes jetables / non personnalisés |

### 3.7 Qualité et intégrité des données

**Valeurs manquantes :** le pipeline MongoDB produit un jeu agrégé quasi-complet. Les colonnes `avg_favorites` et `avg_retweet_count` sont fréquemment nulles en raison d'une **collecte partielle** des métriques d'engagement dans le corpus source — elles sont conservées car informatives lorsqu'elles sont présentes, mais leur interprétation doit être nuancée.

**Doublons :** l'agrégation par `user_id` garantit un profil unique par utilisateur.

**Cohérence temporelle :** les dates `first_tweet_date` et `last_tweet_date` sont cohérentes avec `active_days` ; ces dates brutes sont exclues du ML au profit de variables dérivées plus compactes.

**Biais d'échantillonnage :** le corpus est limité aux tweets contenant des mots-clés liés à la Coupe du Monde — les profils très actifs sur le football y sont sur-représentés par rapport à une population Twitter générale.

---

## 4. Méthodologie

### 4.1 Pipeline ML commun

```
features  →  StandardScaler  →  ACP  →  modèle(s)
```

Ce pipeline est appliqué aux deux approches, avec des paramètres distincts selon le contexte.

### 4.2 Analyse en composantes principales (ACP)

| Contexte | Features | Composantes | Variance expliquée | Justification |
|----------|----------|-------------|---------------------|---------------|
| Non supervisé | 16 | **7** | ~79 % | Seuil 75 % de variance cumulée (EDA section 11) |
| Supervisé | 8 | **5** | 100 % | Saturation — 8 features → max 8 composantes, 5 suffisent |

**Important :** ACP 7 comp. (non sup.), ACP 5 comp. (sup.) et **k=7** K-Means sont **trois décisions indépendantes**.

Critères Kaiser et seuils multiples testés :

| Critère | Composantes |
|---------|-------------|
| Kaiser (valeur propre > 1) | 5 |
| Seuil 70 % | 6 |
| **Seuil 75 % (retenu, non sup.)** | **7** |
| Seuil 80 % | 8 |

### 4.3 Approche non supervisée

**Notebook :** `Groupe3_profils_atypiques_non_Sup.ipynb`

**Entrée :** 16 features de `users_labeled_manual.csv`. Colonnes `label` et `anomaly_score` **exclues** à l'entraînement — utilisées uniquement pour l'évaluation a posteriori.

#### 4.3.1 K-Means (MiniBatchKMeans)

- **k = 7** clusters, choisi par la méthode du coude sur l'inertie (k ∈ [2, 10]).
- `batch_size = 10 000`, `n_init = 10`, `random_state = 42`.
- **Règle d'atypicité :** profils appartenant à un cluster représentant **< 1 %** du dataset.
- **Rôle :** baseline de clustering du cours — cherche des groupes compacts, pas des anomalies isolées.

#### 4.3.2 Isolation Forest

- `n_estimators = 100`, **`contamination = 'auto'`**, `random_state = 42`.
- **`contamination = 'auto'`** : le seuil de décision est déterminé automatiquement à partir des scores d'anomalie (approche originale Liu et al., 2008), sans imposer un pourcentage fixe de la population.
- Labels internes : **-1** = anomalie, **+1** = normal.
- **Rôle :** détection d'anomalies — isole les points « faciles à séparer » par des partitions aléatoires.

#### 4.3.3 Critères de comparaison K-Means vs Isolation Forest

| Critère | K-Means | Isolation Forest |
|---------|---------|------------------|
| Objectif | Segmentation | Détection d'anomalies |
| Sensibilité | Faible (~0,5 %) | Élevée (~6,7 %) |
| Volume détecté | ~3 498 profils | ~42 987 profils |
| Concordance | Consensus ~3 498 | IF seul ~39 489 |
| vs labels Excel | Rappel très faible | Rappel modéré, plus de FP |

**Modèle retenu : Isolation Forest** — conçu pour la détection d'anomalies, plus adapté à l'exploration initiale sans labels.

### 4.4 Approche supervisée

**Notebook :** `Groupe3_profils_atypiques_Sup.ipynb`

#### 4.4.1 Features hors règles Excel (anti-circularité)

Les labels découlent de règles sur `retweet_ratio`, `avg_urls`, `avg_mentions`, `active_days`, `nb_tweets`, `followers_friends_ratio`. Si le modèle reçoit ces variables, il **recopie les règles** (F1 ~ 0,970 avec 16 features).

**8 features retenues :**

`followers_count`, `friends_count`, `avg_tweet_length`, `avg_hashtags`, `avg_favorites`, `avg_retweet_count`, `verified`, `default_profile_image`

#### 4.4.2 Protocole d'entraînement

- Split **train/test 80/20 stratifié** sur `label`.
- Pipeline : `StandardScaler` (fit sur train) → **ACP 5 comp.** → modèle.
- **SVM :** `LinearSVC`, `class_weight='balanced'`.
- **XGBoost :** `scale_pos_weight` pour le déséquilibre des classes.

#### 4.4.3 Justification du SVM linéaire (pas de noyau RBF)

Un SVM à noyau RBF a un coût **O(n²)** — impraticable sur 514 000 lignes d'entraînement. Le noyau RBF a été testé en annexe sur sous-échantillon (`Groupe3_SVM_Noyaux_Annexe.ipynb`) ; le SVM linéaire reste la baseline scalable retenue.

**Modèle retenu : XGBoost** — meilleur F1 et ROC-AUC sur l'évaluation honnête.

### 4.5 Méthodologie de comparaison supervisé vs non supervisé

Les deux approches ne partagent pas la même métrique native :

| Approche | Métrique principale | Évaluation vs labels |
|----------|--------------------|-----------------------|
| Non supervisée | Nombre / % de profils détectés | Matrice de confusion, P/R/F1 a posteriori |
| Supervisée | F1, ROC-AUC sur jeu test | Directe |

**Stratégie comparative :**

1. **Complémentarité fonctionnelle** : IF explore sans labels ; XGBoost classifie avec labels.
2. **Concordance partielle** : mesurer le chevauchement IF ↔ labels Excel (rappel ~8,5 %, précision ~21,5 %).
3. **Rigueur méthodologique** : traitement explicite de la circularité supervisée.
4. **Robustesse** : consensus K-Means ∩ IF (~3 498 profils) comme noyau d'anomalies.

### 4.6 Normalisation et prétraitement

**StandardScaler** (moyenne 0, variance 1) est appliqué à l'ensemble des features numériques avant l'ACP. Ce choix est motivé par :

- L'**hétérogénéité des échelles** : `followers_count` peut atteindre des dizaines de millions tandis que `avg_hashtags` reste proche de 0-5 ;
- La **sensibilité de l'ACP** aux variables de grande variance — sans scaling, `followers_count` dominerait les composantes ;
- La **compatibilité** avec SVM (sensible à la mise à l'échelle) et Isolation Forest (partitionne l'espace des features).

Les variables binaires `verified` et `default_profile_image` sont castées en entiers (0/1) avant scaling.

**Pas de transformation logarithmique en ML :** l'EDA utilise `log1p` uniquement pour la visualisation des distributions asymétriques ; la modélisation utilise les valeurs brutes après StandardScaler.

### 4.7 Politique de gestion du modèle (L4)

| Aspect | Décision retenue |
|--------|------------------|
| **Données d'entrée** | `users_labeled_manual.csv` — fichier unique, traçabilité MongoDB → CSV |
| **Paramètres d'entrée** | Hyperparamètres documentés dans les notebooks ; `random_state=42` pour reproductibilité |
| **Sorties** | Profils flaggés (IF : -1/+1 ; XGBoost : probabilité + classe) |
| **Métriques de suivi** | Non sup. : volume détecté, P/R/F1 vs labels ; Sup. : F1, AUC sur test |
| **Réentraînement** | Non automatisé — réentraînement manuel si nouveau corpus ou nouvelles règles |
| **Gouvernance** | Labels Excel = proxy métier ; pas de déploiement production sans validation experte |
| **Versioning** | Dépôt GitHub ; notebooks comme source de vérité des pipelines |

---

## 5. Résultats

### 5.1 Résultats non supervisés

Configuration : 16 features → StandardScaler → ACP 7 comp. (~79 % variance)

| Méthode | Profils détectés | % du jeu |
|---------|------------------|----------|
| K-Means (k=7, clusters < 1 %) | 3 498 | 0,54 % |
| **Isolation Forest (contamination auto)** | **42 987** | **6,68 %** |
| Consensus (K-Means ∩ IF) | 3 498 | 0,54 % |
| IF seul (hors consensus) | 39 489 | 6,14 % |
| K-Means seul | 0 | 0,00 % |

#### Isolation Forest vs labels Excel

| | Prédit Normal | Prédit Atypique |
|--|---------------|-----------------|
| **Label Normal** | 500 466 | 33 733 |
| **Label Atypique** | 99 671 | 9 254 |

| Métrique | Valeur |
|----------|--------|
| Précision | 0,215 |
| Rappel | 0,085 |
| F1 | 0,122 |
| Accuracy | 0,793 |

#### K-Means vs labels Excel

| Métrique | Valeur |
|----------|--------|
| Précision | 0,084 |
| Rappel | 0,003 |
| F1 | 0,005 |

Le K-Means isole un **noyau très compact** de profils extrêmes ; Isolation Forest **élargit significativement** la détection.

### 5.2 Résultats supervisés

Configuration : 8 features hors règles → StandardScaler → ACP 5 comp. → modèle  
Jeu test : 128 625 profils (20 %)

| Métrique | SVM | **XGBoost** |
|----------|-----|-------------|
| Accuracy | 0,559 | **0,667** |
| F1 (Atypique) | 0,361 | **0,443** |
| Recall | 0,737 | **0,783** |
| Precision | 0,239 | **0,309** |
| ROC-AUC | 0,670 | **0,794** |

#### Matrices de confusion (jeu test)

**SVM :**

| | Prédit 0 | Prédit 1 |
|--|----------|----------|
| Réel 0 | 55 875 | 51 012 |
| Réel 1 | 5 717 | 16 021 |

**XGBoost :**

| | Prédit 0 | Prédit 1 |
|--|----------|----------|
| Réel 0 | 68 824 | 38 063 |
| Réel 1 | 4 717 | 17 021 |

#### Importance des composantes (XGBoost)

PC1 et PC2 dominent l'importance — le modèle s'appuie principalement sur les directions de plus grande variance après ACP.

### 5.3 Annexe — Circularité (16 features)

Avec les **16 features + ACP 7 comp.**, XGBoost atteint F1 ~ **0,970** : le modèle reproduit les règles Excel, pas une généralisation indépendante. Cette configuration est documentée en annexe mais **non retenue** pour l'évaluation finale.

### 5.4 Synthèse comparative

| | Isolation Forest | XGBoost |
|--|------------------|---------|
| Labels requis | Non | Oui |
| Features | 16 | 8 (hors règles) |
| ACP | 7 comp. | 5 comp. |
| Résultat clé | 42 987 profils (6,68 %) | F1 = 0,443 · AUC = 0,794 |
| Usage recommandé | Exploration initiale | Classification avec labels |

---

## 6. Discussion et analyse comparative

### 6.1 Apports de l'approche non supervisée

**Isolation Forest** permet de parcourir **643 124 profils sans annotation préalable**, en signalant ~6,7 % de profils aux scores d'anomalie élevés. C'est particulièrement utile en phase d'exploration, lorsque les critères d'atypicité ne sont pas encore formalisés.

Le passage de `contamination = 0,05` (fixe) à **`contamination = 'auto'`** supprime un degré d'arbitraire : le seuil est inféré des données plutôt qu'imposé. Sur notre jeu, cela porte la détection de 32 141 (5,00 %) à **42 987 (6,68 %)** profils — cohérent avec une population réellement plus « contaminée » que 5 % selon les scores d'isolation.

Le **consensus K-Means ∩ IF** (~3 498 profils) constitue un noyau robuste : les deux méthodes s'accordent sur ces profils extrêmes, renforçant la confiance dans leur caractère atypique.

### 6.2 Apports de l'approche supervisée

**XGBoost** exploite les labels pour atteindre un **F1 = 0,443** et un **ROC-AUC = 0,794** — performances modestes mais **scientifiquement honnêtes**, car évaluées sans les features directement liées aux règles Excel.

Le rappel élevé (0,783) indique une bonne **couverture des atypiques** ; la précision plus faible (0,309) traduit de nombreux faux positifs — attendu compte tenu du chevauchement partiel des classes en espace ACP.

### 6.3 Complémentarité des deux approches

```
Phase 1 — Exploration     : Isolation Forest (sans labels)
Phase 2 — Formalisation   : Labellisation Excel (critères métier)
Phase 3 — Classification  : XGBoost (avec labels, sans circularité)
```

Les deux approches ne s'opposent pas : elles couvrent des **étapes différentes** du cycle de détection. L'IF ouvre l'exploration ; XGBoost discrimine une fois les labels disponibles.

### 6.4 Interprétation des écarts IF ↔ labels

Le faible rappel de l'IF vs labels Excel (8,5 %) s'explique par :

1. **Définitions différentes** : l'IF détecte des outliers statistiques multidimensionnels ; les règles Excel ciblent des comportements spécifiques (retweet, spam, burst).
2. **Seuil auto** : l'IF ne cherche pas à reproduire les 16,9 % de labels atypiques.
3. **Chevauchement partiel en ACP 2D** : normal et atypique se superposent — la séparation n'est pas triviale.

### 6.5 Analyse des profils consensus (K-Means ∩ IF)

Les **3 498 profils** détectés par les deux méthodes présentent en moyenne des valeurs extrêmes sur :

- `retweet_ratio` élevé (amplification quasi-systématique) ;
- `followers_friends_ratio` disproportionné (audiences gonflées ou comptes asymétriques) ;
- `avg_urls` et `avg_mentions` au-dessus de la médiane populationnelle.

Ce noyau constitue le **signal le plus robuste** du projet : deux algorithmes aux philosophies différentes (clustering vs isolation) convergent sur les mêmes profils. En revanche, les **39 489 profils détectés uniquement par l'IF** représentent des anomalies « diffuses » — profils statistiquement isolés qui ne satisfont pas forcément les critères Excel (ex. combinaison atypique de followers et longueur de tweets sans retweet excessif).

### 6.6 Leçons apprises

| Enseignement | Détail |
|--------------|--------|
| Ordre pipeline | EDA **avant** labellisation — évite le biais de conception des features |
| Circularité | Exclure les features des règles de label en supervisé — F1 passe de 0,97 à 0,44 |
| Contamination IF | `auto` plus justifiable qu'un 5 % arbitraire — +33 % de détections |
| Échelle | MiniBatchKMeans et LinearSVC permettent 643 k profils ; noyaux RBF non |
| Complémentarité | Non sup. et sup. répondent à des questions différentes — les confronter directement en F1 est incomplet |

### 6.7 Pistes d'amélioration

1. **Validation experte** : audit manuel de 500 profils IF pour estimer la précision réelle.
2. **Features textuelles** : TF-IDF, embeddings sur le contenu des tweets.
3. **Graphe social** : features de voisinage (followers communs, patterns de retweet).
4. **Semi-supervisé** : utiliser les labels sur un sous-ensemble pour affiner l'IF.
5. **Autres corpus** : généraliser au-delà du biais World Cup.
6. **Validation croisée** : k-fold stratifié sur le supervisé ; bootstrap sur échantillons IF.

---

## 7. Limites du projet

### 7.1 Limites des données

- **Biais thématique et temporel** : corpus World Cup 2018 — généralisation limitée à d'autres contextes.
- **Collecte partielle** : `avg_favorites` et `avg_retweet_count` souvent nulles.
- **Granularité profil** : un utilisateur actif pendant l'événement peut sembler atypique sans l'être structurellement.

### 7.2 Limites de la labellisation

- Labels **subjectifs**, non validés par un expert externe ou une vérité terrain.
- Règles Excel **corrélées aux features** — risque de circularité (traité explicitement en supervisé).
- Seuil « ≥ 2 critères sur 4 » arbitraire mais documenté et justifié par l'EDA.

### 7.3 Limites des modèles

- **IF `contamination = auto`** : le pourcentage détecté (6,68 %) n'est pas contrôlé explicitement ; il dépend de la distribution des scores.
- **K-Means** : sous-détecte massivement vs labels ; sensible au choix de k et au seuil 1 %.
- **XGBoost F1 modeste** : sans features des règles, la séparation reste difficile.
- **Pas de validation croisée** sur le non supervisé (coût computationnel sur 643 k profils).

### 7.4 Limites organisationnelles

- Pas de déploiement en production ni de politique de réentraînement automatisé.
- Évaluation qualitative des profils détectés limitée (pas d'audit manuel exhaustif des 42 987 profils IF).

---

## 8. Conclusion et recommandations

### 8.1 Conclusion

Ce projet démontre une **méthodologie complète et reproductible** pour comparer détection non supervisée et classification supervisée de profils atypiques Twitter :

1. **Pipeline de données** : JSON → MongoDB → agrégation → 643 124 profils, 21 → 16 features.
2. **Labellisation argumentée** : 4 critères inspirés de l'EDA et de la littérature, 16,9 % d'atypiques.
3. **Non supervisé retenu : Isolation Forest** (`contamination = auto`) — 42 987 profils (6,68 %) pour l'exploration.
4. **Supervisé retenu : XGBoost** — F1 = 0,443, ROC-AUC = 0,794, évaluation sans circularité.
5. **Contribution méthodologique** : traitement explicite de la circularité label/features, comparaison rigoureuse des approches.

### 8.2 Recommandations

| Contexte | Recommandation |
|----------|----------------|
| Exploration initiale | Isolation Forest sur l'ensemble, sans labels |
| Formalisation des critères | Labellisation experte sur échantillon des profils IF |
| Classification | XGBoost avec features hors règles de labellisation |
| Validation | Audit manuel d'un échantillon des profils consensus |
| Perspectives | Autres corpus, validation croisée, deep learning sur contenu textuel |

---

## 9. Bibliographie

- Chu, Z., Gianvecchio, S., Wang, H., & Jajodia, S. (2012). *Detecting automation of Twitter accounts: Are you a human, bot, or cyborg?* IEEE Transactions on Dependable and Secure Computing, 9(6), 811-824.
- Ferrara, E., Varol, O., Davis, C., Menczer, F., & Flammini, A. (2016). *The rise of social bots.* Communications of the ACM, 59(7), 96-104.
- Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). *Isolation Forest.* ICDM, 413-422.
- Varol, O., Ferrara, E., Davis, C. A., Menczer, F., & Flammini, A. (2017). *Online human-bot interactions: Detection, estimation, and characterization.* Proceedings of ICWSM, 280-289.

---

## 10. Annexes

### Annexe A — Répartition des rôles (L4)

Voir [`docs/EQUIPE_ROLES.md`](EQUIPE_ROLES.md) pour le détail par membre et les cinq dimensions du modèle ML :

| Dimension ML | Rôle | Membre |
|--------------|------|--------|
| Données d'entrée | Data Engineer | Housseni YABRE |
| Paramètres d'entrée | Data Analyst | Vanelle Leita FOTSO AKOUDOUM |
| Métriques d'état du modèle | Data Scientist (non sup.) | Samella LEUKOUO |
| Sorties cibles / Résultats | ML Engineer (sup.) | Dorcas ADRAKE |
| Politique de gestion du modèle | ML Project Manager / CDO | Ace ANALLA |

### Annexe B — Notebooks du projet

| Notebook | Contenu |
|----------|---------|
| `Groupe3_Analyse_Exploratoire.ipynb` | EDA, corrélations, réduction 21 → 16 features |
| `Groupe3_Labelisation.ipynb` | Documentation du processus Excel |
| `Groupe3_profils_atypiques_non_Sup.ipynb` | K-Means vs Isolation Forest |
| `Groupe3_profils_atypiques_Sup.ipynb` | SVM vs XGBoost, annexe circularité |
| `Groupe3_profils_atypiques_Final.ipynb` | Synthèse soutenance |
| `Groupe3_SVM_Noyaux_Annexe.ipynb` | Comparaison noyaux SVM (sous-échantillon) |

### Annexe C — Installation et reproduction

```bash
cd IF29
python3 -m venv venv_if29
source venv_if29/bin/activate
pip install -r requirements.txt
jupyter notebook Groupe3_profils_atypiques_non_Sup.ipynb
```

Portail de démonstration : `bash scripts/run_demo.sh` → http://localhost:8501

### Annexe D — Matrice K-Means vs Isolation Forest

| | IF Normal | IF Atypique |
|--|-----------|-------------|
| **KM Normal** | 600 137 | 39 489 |
| **KM Atypique** | 0 | 3 498 |

### Annexe E — Détail du pipeline MongoDB

Le script `scripts/import_local.sh` importe les 581 fichiers JSONL dans MongoDB. L'agrégation par `user_id` calcule pour chaque profil :

- Comptages (`nb_tweets`, `nb_retweets`) ;
- Moyennes (`avg_*`) sur les tweets du profil ;
- Ratios dérivés (`retweet_ratio`, `followers_friends_ratio`, `tweet_frequency`) ;
- Métadonnées profil (`verified`, `default_profile_image`, etc.).

L'export `Export_CSV.py` produit `users_aggregated.csv` depuis la collection MongoDB `users_aggregated`.

### Annexe F — État des features supervisées exclues

Les 8 features **exclues** du supervisé honnête sont précisément celles impliquées dans les règles Excel :

| Feature exclue | Règle Excel associée |
|----------------|---------------------|
| `retweet_ratio` | Règle 1 — Amplification |
| `avg_urls` | Règle 2 — Spam |
| `avg_mentions` | Règle 2 — Spam |
| `active_days` | Règle 3 — Burst |
| `nb_tweets` | Règle 3 — Burst |
| `followers_friends_ratio` | Règle 4 — Déséquilibre social |
| `nb_retweets` | Corollaire de retweet_ratio |
| `tweet_frequency` | Corollaire de active_days / nb_tweets |

### Annexe G — Comparaison contamination fixe vs auto

| Paramètre | `contamination = 0,05` | `contamination = 'auto'` |
|-----------|------------------------|--------------------------|
| Profils détectés | 32 141 | 42 987 |
| % du jeu | 5,00 % | 6,68 % |
| Justification | Hypothèse arbitraire | Seuil inféré des scores (Liu et al., 2008) |
| IF seul (hors KM) | 28 643 | 39 489 |
| Rappel vs labels | ~7,5 % | ~8,5 % |

Le mode `auto` détecte environ **10 846 profils supplémentaires** (+33,7 %), avec une légère amélioration du rappel vis-à-vis des labels Excel, tout en conservant le même noyau consensus avec K-Means (3 498 profils).

### Annexe H — Portail de démonstration (L3)

Le portail Streamlit (`demo/app.py`) centralise pour la soutenance :

- Pipeline de données et schéma MongoDB ;
- Visualisations EDA (distributions, corrélations, boxplots) ;
- Labellisation et distribution des scores ;
- Résultats non supervisés et supervisés ;
- Synthèse comparative et fiches équipe (L4).

Lancement : `bash scripts/run_demo.sh` → http://localhost:8501

---

*Fin du rapport — Projet IF29 Groupe 3 — Juin 2026*
