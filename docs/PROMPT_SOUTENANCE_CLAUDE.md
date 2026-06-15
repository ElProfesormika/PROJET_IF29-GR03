# Prompt Claude — Slides de soutenance IF29 Groupe 3

> **Comment utiliser ce fichier**
> 1. Ouvrir Claude (claude.ai ou l'application).
> 2. Copier **tout le bloc « PROMPT À COLLER DANS CLAUDE »** (section 2) dans une nouvelle conversation.
> 3. Les champs durée/style restent à ajuster si besoin (noms et rôles déjà renseignés).
> 4. Demander ensuite à Claude : *« Génère les slides au format Markdown, une slide par section `---` »* ou *« Exporte en structure PowerPoint slide par slide »*.
> 5. Optionnel : demander une version **10 min** ou **15 min** en précisant la durée.

---

## 1. Contexte rapide du projet (référence)

| Élément | Valeur |
|---------|--------|
| **Cours** | IF29 — Intelligence des données |
| **Équipe** | Groupe 3 — 5 membres (voir `docs/EQUIPE_ROLES.md`) |
| **Sujet** | Détection de profils atypiques sur X (Twitter) |
| **Volume** | 643 124 profils · ~1,16 M tweets (Tweet_Worldcup) |
| **Approche 1** | Non supervisée : K-Means vs Isolation Forest → **Isolation Forest** |
| **Approche 2** | Supervisée : SVM vs XGBoost → **XGBoost** |
| **Dépôt GitHub** | https://github.com/ElProfesormika/PROJET_IF29-GR03 |

---

## 2. PROMPT À COLLER DANS CLAUDE

```
Tu es un expert en présentations académiques (soutenance de projet universitaire en data science / ML).
Génère une présentation de soutenance ORALE, claire, professionnelle et structurée, en FRANÇAIS.

---

## CONSIGNES DE FORMAT

- Durée cible : **15 minutes**
- Nombre de slides visé : **18 à 22 slides**
- Public : jury universitaire (professeur IF29 + éventuellement pairs)
- Ton : académique mais accessible, pas de jargon inutile
- Style visuel souhaité : **sobre, bleu marine / teal, peu de texte par slide, sans emojis**
- Format de sortie : Markdown avec séparateur `---` entre chaque slide
- Pour chaque slide, indiquer :
  - **Titre**
  - **Contenu** (puces courtes, max 5 par slide)
  - **Notes orateur** (2-3 phrases à dire à l'oral)
  - **Visuel suggéré** (graphique, schéma, tableau — décrire ce qu'il faut montrer)

---

## ÉQUIPE — Groupe 3 (5 membres)

### Correspondance — Cinq dimensions du modèle ML

| Dimension ML | Rôle | Membre |
|--------------|------|--------|
| Données d'entrée | Data Engineer / Data Cleaner | **Housseni YABRE** |
| Paramètres d'entrée | Data Analyst / Feature Engineer | **Vanelle Leita FOTSO AKOUDOUM** |
| Métriques d'état du modèle | Data Scientist (non supervisé) | **Samella LEUKOUO** |
| Sorties cibles / Résultats | ML Engineer (supervisé) | **Dorcas ADRAKE** |
| Politique de gestion du modèle | ML Project Manager / CDO | **Ace ANALLA** |

### Rôle de chaque membre en soutenance (~15 min)

| Ordre | Membre | Partie présentée | Durée |
|-------|--------|------------------|-------|
| 1 | **Housseni YABRE** | Introduction, contexte, pipeline MongoDB (JSON → profils) | ~2 min |
| 2 | **Vanelle Leita FOTSO AKOUDOUM** | EDA, features, labellisation Excel (4 critères) | ~3 min |
| 3 | **Samella LEUKOUO** | Non supervisé — K-Means vs Isolation Forest | ~3 min |
| 4 | **Dorcas ADRAKE** | Supervisé — SVM vs XGBoost, circularité | ~4 min |
| 5 | **Ace ANALLA** | Synthèse, limites, recommandations, conclusion | ~3 min |

### Fiches détaillées (L4)

**Membre 1 — Housseni YABRE** (Data Engineer / Data Cleaner)
- Données d'entrée : extraction JSON Tweet_Worldcup, nettoyage, agrégation MongoDB, `users_aggregated.csv`

**Membre 2 — Vanelle Leita FOTSO AKOUDOUM** (Data Analyst / Feature Engineer)
- Paramètres d'entrée : EDA, 16 features, corrélations, labellisation, `Groupe3_Analyse_Exploratoire.ipynb`

**Membre 3 — Samella LEUKOUO** (Data Scientist)
- Métriques modèle non supervisé : K-Means k=7, Isolation Forest 5 %, ACP 7 comp., retenu IF

**Membre 4 — Dorcas ADRAKE** (ML Engineer / Data Scientist)
- Sorties supervisées : SVM vs XGBoost, ACP 5 comp., 8 features hors règles, F1 = 0,443

**Membre 5 — Ace ANALLA** (ML Project Manager / CDO)
- Politique modèle : coordination, synthèse, limites, portail démo, L4, conclusion

---

## CONTENU DU PROJET — À INTÉGRER DANS LES SLIDES

### Slide d'ouverture
- Titre : « Détection de profils atypiques sur X (Twitter) — Comparaison de méthodes de classification »
- Projet IF29 — Groupe 3
- **Équipe :** Housseni YABRE · Vanelle Leita FOTSO AKOUDOUM · Samella LEUKOUO · Dorcas ADRAKE · Ace ANALLA
- Date de soutenance

### Slide équipe et répartition des rôles (OBLIGATOIRE — L4)
- Tableau des 5 dimensions ML ↔ membre ↔ rôle
- Mentionner le portail démo Streamlit (`demo/app.py`) comme support de présentation
- Ordre de passage des 5 intervenants

### Problématique et objectif
- **Contexte** : sur les réseaux sociaux, certains comptes présentent des comportements atypiques (bots, spam, amplification, bursts d'activité).
- **Objectif du sujet IF29** : comparer **deux approches** de classification pour détecter ces profils :
  1. **Non supervisée** : sans labels → exploration
  2. **Supervisée** : avec labels → prédiction guidée
- **Question de recherche** : quelle méthode est la plus pertinente dans chaque contexte, et comment les résultats se comparent-ils ?

### Jeu de données
- Source : dataset **Tweet_Worldcup** (~1 161 999 tweets, 581 fichiers JSONL)
- Pipeline : tweets bruts → **MongoDB** → agrégation par utilisateur → profils
- **643 124 profils** agrégés, **21 variables** comportementales
- Hypothèse : on analyse uniquement l'**auteur du tweet** (`user`), pas `retweeted_status.user`
- Fichiers produits :
  - `users_aggregated.csv` (sans label)
  - `users_labeled_manual.csv` (+ `label`, + `anomaly_score`)

### Pipeline de préparation (Étape 1)
Schéma à illustrer :
```
raw/*.json → MongoDB (tweets) → agrégation → users_aggregated.csv → Excel → users_labeled_manual.csv
```
- Script : `scripts/import_local.sh` + `Export_CSV.py`
- Catégories de variables : profil social, activité, contenu, engagement (partiel), temporel

### Analyse exploratoire (EDA)
- Notebook : `Groupe3_Analyse_Exploratoire.ipynb`
- Observations clés :
  - Distributions très asymétriques (followers, friends, etc.)
  - Peu de valeurs manquantes
  - Engagement (`avg_favorites`, `avg_retweet_count`) quasi nul → collecte partielle
  - `log1p` utilisé **uniquement pour visualiser**, pas dans le pipeline ML
- **ACP pour le ML non supervisé** : seuil **75 % de variance** → **7 composantes** (~79 %)
  - Kaiser → 5 comp. · 70 % → 6 · **75 % → 7 (retenu)** · 80 % → 8

### Labellisation manuelle (Excel)
- Réalisée **uniquement sous Microsoft Excel** (filtres + inspection visuelle)
- **4 critères d'anomalie** — atypique si **≥ 2 critères sur 4** :

| # | Critère | Condition | Interprétation |
|---|---------|-----------|----------------|
| 1 | Amplification | retweet_ratio ≥ 0,8 | Retweet quasi systématique |
| 2 | Spam | avg_urls ≥ 1,5 OU avg_mentions ≥ 2 | Contenu surchargé |
| 3 | Burst | active_days = 1 ET nb_tweets ≥ 2 | Activité concentrée |
| 4 | Déséquilibre social | followers_friends_ratio ≥ 30 | Audience disproportionnée |

- Résultats :
  - Normal : 534 199 (83,1 %)
  - Atypique : 108 925 (16,9 %)
- Références : Ferrara et al. (2016), Chu et al. (2012), Varol et al. (2017)

### Méthodologie ML commune
Pipeline :
```
features → StandardScaler → ACP → modèles
```

| | Non supervisé | Supervisé |
|--|---------------|-----------|
| Features | 16 variables MongoDB | 8 hors règles Excel |
| ACP | **7 composantes** (~79 %) | **5 composantes** (100 %) |
| Labels | exclus à l'entraînement | `label` = cible |
| Modèles testés | K-Means, Isolation Forest | SVM, XGBoost |
| Retenu | **Isolation Forest** | **XGBoost** |

**Point important à dire à l'oral** : ACP 7 comp., ACP 5 comp. et k=7 K-Means sont **3 choix indépendants**.

8 features supervisées (hors règles Excel) :
`followers_count`, `friends_count`, `avg_tweet_length`, `avg_hashtags`, `avg_favorites`, `avg_retweet_count`, `verified`, `default_profile_image`

8 features exclues (liées aux règles) :
`retweet_ratio`, `avg_urls`, `avg_mentions`, `active_days`, `nb_tweets`, `followers_friends_ratio`, `nb_retweets`, `tweet_frequency`

### Approche non supervisée
- Notebook : `Groupe3_profils_atypiques_non_Sup.ipynb`
- **K-Means** (MiniBatchKMeans, k=7 clusters — choix par coude d'inertie) :
  - Clusters minoritaires (< 1 %) = atypiques
  - Résultat : **~3 500 profils (0,54 %)**
- **Isolation Forest** (contamination = 5 %) :
  - Résultat : **~32 141 profils (5,00 %)**
- **Méthode retenue : Isolation Forest**
  - Conçue pour la détection d'anomalies
  - Plus sensible sur 643 000 profils
  - Consensus K-Means + Iso Forest : ~3 498 profils

### Approche supervisée
- Notebook : `Groupe3_profils_atypiques_Sup.ipynb`
- Split train/test **80/20** stratifié
- **SVM** (LinearSVC, class_weight balanced) vs **XGBoost** (scale_pos_weight)
- Résultats (ACP 5 comp. + 8 features hors règles) :

| Métrique | SVM | XGBoost |
|----------|-----|---------|
| Accuracy | 55,9 % | **66,7 %** |
| F1 (Atypique) | 0,361 | **0,443** |
| Recall | 0,737 | **0,783** |
| Precision | 0,239 | **0,309** |
| ROC-AUC | 0,670 | **0,794** |

- **Méthode retenue : XGBoost** (meilleur F1 et ROC-AUC)

### Limite méthodologique — Circularité (slide importante)
- Les labels viennent de 4 règles Excel sur les mêmes variables
- Si on donne les **16 features** au modèle → XGBoost F1 ≈ **0,970** (annexe)
  → le modèle **recopie les règles**, pas une vérité terrain indépendante
- Évaluation **honnête retenue** : 8 features hors règles + ACP 5 comp. → F1 = 0,443
- Montrer honnêteté scientifique : on a identifié et corrigé ce biais

### Comparaison des deux approches retenues

| | Isolation Forest | XGBoost |
|--|------------------|---------|
| Labels requis | Non | Oui (Excel) |
| Features ML | 16 | 8 (hors règles) |
| ACP | 7 composantes | 5 composantes |
| Résultat | ~32 141 détectés (5 %) | F1 = 0,443 |
| Forces | Exploration sans annotation | Signal avec labels |
| Faiblesses | Contamination arbitraire (5 %) | Label corrélé aux règles |

### Conclusion et recommandations
1. **Isolation Forest** → phase d'**exploration** sans labels (détecte ~5 % de profils déviants)
2. **XGBoost** → une fois les labels définis, **sans réutiliser** les variables des règles Excel
3. Les deux approches sont **complémentaires**, pas concurrentes
4. Perspectives : validation terrain, autres jeux de données, deep learning, détection temps réel

### Slide de clôture
- Synthèse en 3 phrases
- Remerciements
- Questions ?

---

## SLIDES OBLIGATOIRES À NE PAS OUBLIER

1. Plan de la présentation
2. **Slide équipe et répartition des rôles (L4)**
3. Schéma du pipeline complet (données → ML → résultats)
4. Tableau des 4 règles de labellisation
5. Tableau comparatif SVM vs XGBoost
6. Slide « circularité » (limite + correction)
7. Slide conclusion avec recommandation pratique
8. Slide « Questions » avec noms des 5 membres

---

## QUESTIONS PROBABLES DU JURY (préparer 1 slide « annexe » ou notes)

1. **Pourquoi Isolation Forest plutôt que K-Means ?**
   → K-Means cherche des groupes compacts ; Isolation Forest isole les points « faciles à séparer » = anomalies. Sur 643k profils, IF détecte 5 % vs 0,54 % pour K-Means.

2. **Pourquoi 7 composantes ACP en non supervisé et 5 en supervisé ?**
   → 16 features → seuil 75 % variance = 7 comp. · 8 features → saturation à 100 % dès 5 comp. Ce sont des contextes différents.

3. **Pourquoi k=7 pour K-Means ?**
   → Méthode du coude sur l'inertie (nombre de **clusters**), indépendant du nombre de composantes ACP.

4. **Pourquoi F1 = 0,443 et pas 0,97 ?**
   → 0,97 = circularité (modèle recopie les règles Excel). 0,443 = évaluation honnête sans features des règles.

5. **Les labels Excel sont-ils fiables ?**
   → Validés manuellement, inspirés EDA + littérature. Limite reconnue : pas de vérité terrain externe.

6. **Pourquoi exclure certaines features en supervisé ?**
   → Éviter que le modèle apprenne par cœur les règles de labellisation plutôt que des patterns généralisables.

---

## DEMANDE FINALE À CLAUDE

Génère la présentation complète slide par slide en Markdown.
Ensuite, propose :
1. Une version « script oral » minute par minute pour **15 minutes**, avec **transitions nommées** entre Housseni, Vanelle, Samella, Dorcas et Ace
2. Une liste de graphiques à capturer depuis les notebooks (avec nom du notebook et section)
3. Une slide « backup » avec le tableau récapitulatif final

Graphiques à mentionner dans les slides :
- EDA : distributions, variance cumulée ACP (section 11)
- Non sup. : coude K-Means, barres détections, matrice de confusion vs labels
- Sup. : barres F1 SVM vs XGBoost, courbes ROC, matrice de confusion
- Final : synthèse visuelle 2 graphiques (`Groupe3_profils_atypiques_Final.ipynb`)
```

---

## 3. Prompts de suivi (après la première génération)

Copier l'un de ces messages **dans la même conversation Claude** selon le besoin :

### Version plus courte (8 slides)
```
Raccourcis la présentation à 8 slides maximum pour une soutenance de 5 minutes.
Garde : problématique, données, labellisation, méthodo, résultats non sup., résultats sup., circularité, conclusion.
```

### Version PowerPoint
```
Transforme chaque slide Markdown en instructions pour PowerPoint :
- mise en page (titre, corps, footer)
- texte exact à copier
- description détaillée du visuel à créer
```

### Script oral détaillé
```
Écris le script oral complet slide par slide pour une présentation de **15 minutes**.
Indique le timing et l'intervenant (Housseni YABRE, Vanelle Leita FOTSO AKOUDOUM, Samella LEUKOUO, Dorcas ADRAKE, Ace ANALLA).
```

### Slide circularité (approfondie)
```
Crée 2 slides dédiées à la circularité label/features :
1. Explication du problème avec exemple chiffré (F1 0,97 vs 0,443)
2. Comment nous l'avons corrigé (8 features exclues)
Ton pédagogique pour le jury.
```

### Q&A jury
```
Simule 10 questions difficiles du jury avec des réponses courtes (30 secondes chacune) basées sur le projet IF29 Groupe 3.
```

---

## 4. Graphiques à exporter depuis les notebooks

| Slide suggérée | Notebook | Contenu |
|----------------|----------|---------|
| Distributions | `Groupe3_Analyse_Exploratoire.ipynb` | Histogrammes variables clés |
| ACP variance | `Groupe3_Analyse_Exploratoire.ipynb` | Scree plot + seuil 75 % |
| Coude K-Means | `Groupe3_profils_atypiques_non_Sup.ipynb` | Inertie vs k |
| Détections non sup. | `Groupe3_profils_atypiques_non_Sup.ipynb` | Barres K-Means / Iso Forest |
| SVM vs XGBoost | `Groupe3_profils_atypiques_Sup.ipynb` | Barres métriques + ROC |
| Circularité | `Groupe3_profils_atypiques_Sup.ipynb` | Section 8 annexe |
| Synthèse finale | `Groupe3_profils_atypiques_Final.ipynb` | 2 graphiques côte à côte |

---

## 5. Chiffres clés à retenir (anti-piège)

| Chiffre | Signification |
|---------|---------------|
| 643 124 | Nombre de profils |
| 16,9 % | Part de profils atypiques (labels) |
| 7 | Composantes ACP (non supervisé) |
| 5 | Composantes ACP (supervisé) |
| k = 7 | Clusters K-Means (≠ 7 composantes ACP) |
| ~3 500 | Atypiques K-Means (0,54 %) |
| ~32 141 | Atypiques Isolation Forest (5 %) |
| F1 = 0,443 | XGBoost (évaluation honnête) |
| F1 ≈ 0,970 | XGBoost avec 16 features (circularité) |
| ROC-AUC = 0,794 | XGBoost retenu |

---

*Projet IF29 — Groupe 3 — Fichier prompt soutenance*
