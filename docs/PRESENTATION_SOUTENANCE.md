# Présentation soutenance — IF29 Groupe 3

**16 slides** + démonstration live du portail Streamlit (`demo/app.py`)

Style : sobre, bleu marine / teal, peu de texte par slide, sans emojis.

---

## Slide 1 — Page de titre

**Titre :** Détection de profils atypiques sur X (Twitter)  
**Sous-titre :** Comparaison non supervisée et supervisée — IF29 Groupe 3

**Contenu :**
- Intelligence des données — Groupe 3
- 643 124 profils · ~1,16 M tweets
- GitHub : https://github.com/ElProfesormika/PROJET_IF29-GR03

**Notes orateur :**  
Nous présentons notre travail de détection de comptes atypiques sur Twitter, puis une démonstration live du portail web.

**Visuel suggéré :** Fond bleu marine / teal, noms des 5 membres.

---

## Slide 2 — Plan

**Titre :** Plan de la présentation

**Contenu :**
1. Contexte, données et pipeline
2. EDA et labellisation
3. Approche non supervisée
4. Approche supervisée et circularité
5. Synthèse et limites
6. **Démonstration live** — portail Streamlit

**Notes orateur :**  
Les slides couvrent la méthodologie et les résultats. Nous terminons par une démo interactive du portail web.

**Visuel suggéré :** Liste numérotée, dernière étape mise en avant (« Démo live »).

---

## Slide 3 — Contexte et problématique

**Titre :** Pourquoi détecter des profils atypiques ?

**Contenu :**
- Comptes suspects : bots, spam, amplification, bursts d'activité
- Question : les détecter **sans labels**, puis **avec labels** ?
- Deux approches comparées sur le même pipeline de features
- Méthodes du cours : ACP, K-Means, SVM — complétées par Isolation Forest et XGBoost

**Notes orateur :**  
Notre problématique est double : explorer les anomalies sans annotation, puis classifier une fois les labels définis.

**Visuel suggéré :** Schéma normal vs atypique (4 axes).

---

## Slide 4 — Équipe et rôles (L4)

**Titre :** Équipe — Cinq dimensions du modèle ML

**Contenu :**

| Dimension | Membre | Partie soutenance |
|-----------|--------|-------------------|
| Données d'entrée | Housseni YABRE | Pipeline MongoDB |
| Paramètres d'entrée | Vanelle FOTSO AKOUDOUM | EDA + labellisation |
| Métriques non sup. | Samella LEUKOUO | K-Means vs Isolation Forest |
| Résultats supervisés | Dorcas ADRAKE | SVM vs XGBoost |
| Gestion du modèle | Ace ANALLA | Synthèse + démo |

**Notes orateur :**  
Chaque membre couvre une dimension du cycle de vie ML, de l'ingestion à la synthèse.

**Visuel suggéré :** Tableau L4.

---

## Slide 5 — Données et pipeline d'ingestion

**Titre :** Dataset et pipeline de bout en bout

**Contenu :**
- Tweet_Worldcup : ~1,16 M tweets · 581 JSONL → **643 124 profils**, 21 variables
- Hypothèse : auteur = `user` uniquement
- Pipeline :
  ```
  raw/*.json → MongoDB → users_aggregated.csv → Excel → users_labeled_manual.csv
  ```
- Scripts : `import_local.sh`, `Export_CSV.py`

**Notes orateur :**  
Housseni a construit le pipeline d'agrégation. Vanelle a ensuite labellisé les profils sous Excel.

**Visuel suggéré :** Schéma horizontal du pipeline (reprendre `pipeline_flow` de la démo).

---

## Slide 6 — EDA et labellisation

**Titre :** Analyse exploratoire et définition des labels

**Contenu :**
- Distributions asymétriques · peu de valeurs manquantes
- `log1p` = visualisation seule · `StandardScaler` en ML
- **16 features** agrégées (comportement, contenu, réseau social)
- **Atypique si ≥ 2 critères sur 4 :**

| # | Critère | Condition |
|---|---------|-----------|
| 1 | Amplification | `retweet_ratio ≥ 0,8` |
| 2 | Spam | `avg_urls ≥ 1,5` OU `avg_mentions ≥ 2` |
| 3 | Burst | `active_days = 1` ET `nb_tweets ≥ 2` |
| 4 | Déséquilibre | `followers_friends_ratio ≥ 30` |

**Résultat :** 83,1 % normal · **16,9 % atypique** (108 925 profils)

**Notes orateur :**  
L'EDA a orienté nos features et règles. La labellisation manuelle sous Excel donne environ 17 % de profils atypiques.

**Visuel suggéré :** Camembert normal/atypique + tableau des 4 règles.

---

## Slide 7 — Pipeline ML et ACP

**Titre :** Préparation des modèles

**Contenu :**
- Pipeline commun : `features → StandardScaler → ACP → modèle`
- Split supervisé : 80/20 stratifié

| | Non supervisé | Supervisé |
|--|---------------|-----------|
| Features | 16 MongoDB | 8 hors règles Excel |
| ACP | **7 comp.** (~79 %) | **5 comp.** (100 %) |
| Modèles | K-Means, Isolation Forest | SVM, XGBoost |

**Point clé :** ACP 7 comp., ACP 5 comp. et k=7 K-Means = **3 choix indépendants**

**Notes orateur :**  
L'ACP réduit la redondance entre variables. Les nombres de composantes diffèrent selon le contexte, sans lien avec k=7 de K-Means.

**Visuel suggéré :** Schéma 4 blocs + courbe variance cumulée ACP.

---

## Slide 8 — Non supervisé : K-Means vs Isolation Forest

**Titre :** Détection sans labels — résultats

**Contenu :**
- **K-Means** (k=7) : baseline cours — segmentation en clusters
- **Isolation Forest** (5 %) : détection d'anomalies — **retenu**
- Entrée : 16 features + ACP 7 comp.

| Méthode | Détectés | % |
|---------|----------|---|
| K-Means | ~3 500 | 0,54 % |
| **Isolation Forest** | **~32 141** | **5,00 %** |
| Consensus | ~3 498 | 0,54 % |

**Notes orateur :**  
K-Means sous-détecte les atypiques. Isolation Forest est plus sensible et adapté à l'exploration initiale sans labels.

**Visuel suggéré :** Barres comparatives + courbe du coude K-Means.

---

## Slide 9 — Supervisé : méthodologie

**Titre :** Classification avec labels

**Contenu :**
- **8 features hors règles Excel** (éviter la circularité)
- ACP 5 composantes · split 80/20
- **SVM** : `LinearSVC`, scalable sur 514 k lignes train
- **XGBoost** : frontière non linéaire, `scale_pos_weight`
- Pas de SVM à noyau : coût O(n²), impraticable à cette échelle

**Features retenues :** `followers_count`, `friends_count`, `avg_tweet_length`, `avg_hashtags`, `avg_favorites`, `avg_retweet_count`, `verified`, `default_profile_image`

**Notes orateur :**  
Nous comparons le SVM linéaire du cours à XGBoost. Le noyau RBF a été testé en annexe uniquement sur sous-échantillon — non applicable sur l'ensemble.

**Visuel suggéré :** Liste des 8 features + scatter ACP 2D (chevauchement des classes).

---

## Slide 10 — Résultats : SVM vs XGBoost

**Titre :** Tableau comparatif supervisé

**Contenu :**

| Métrique | SVM | **XGBoost** |
|----------|-----|-------------|
| Accuracy | 55,9 % | **66,7 %** |
| F1 | 0,361 | **0,443** |
| Recall | 0,737 | **0,783** |
| Precision | 0,239 | **0,309** |
| ROC-AUC | 0,670 | **0,794** |

**Retenu : XGBoost** — meilleur sur toutes les métriques

**Notes orateur :**  
XGBoost améliore le F1 et l'AUC tout en gardant un rappel élevé. C'est notre modèle supervisé retenu.

**Visuel suggéré :** Barres F1 + courbes ROC.

---

## Slide 11 — Circularité méthodologique

**Titre :** Pourquoi exclure 8 features ?

**Contenu :**
- Labels Excel construits à partir de variables présentes dans les 16 features
- Avec **16 features** → F1 ~ **0,970** : le modèle recopie les règles
- Avec **8 features hors règles** → F1 = **0,443** : évaluation honnête
- F1 modeste mais **scientifiquement rigoureux**

**Notes orateur :**  
Un F1 de 0,97 serait trompeur. Nous avons volontairement retiré les variables liées aux règles Excel pour mesurer une vraie capacité de généralisation.

**Visuel suggéré :** Barres F1 : 0,970 vs 0,443 (slide `circularite` de la démo).

---

## Slide 12 — Synthèse

**Titre :** Deux approches complémentaires

**Contenu :**

| | Isolation Forest | XGBoost |
|--|------------------|---------|
| Labels | Non requis | Oui |
| Usage | Exploration initiale | Classification |
| Résultat | ~32 141 profils (5 %) | F1 = 0,443 · AUC = 0,794 |

1. **IF** en amont — sans annotation manuelle  
2. **XGBoost** ensuite — avec labels, sans circularité

**Notes orateur :**  
Les deux approches ne s'opposent pas : elles couvrent le cycle complet, de l'exploration à la classification.

**Visuel suggéré :** Graphiques de synthèse (`Groupe3_profils_atypiques_Final.ipynb`).

---

## Slide 13 — Limites

**Titre :** Limites et perspectives

**Contenu :**
- Labels Excel subjectifs, non validés par un expert externe
- F1 supervisé modeste : séparation difficile sans features des règles
- Biais dataset World Cup (temporel, thématique)
- Contamination IF fixée à 5 % (choix arbitraire)
- Perspectives : validation experte, autres corpus Twitter

**Notes orateur :**  
Nous assumons ces limites. Le projet démontre une démarche rigoureuse plus qu'une solution de production.

**Visuel suggéré :** Liste sobre.

---

## Slide 14 — Conclusion

**Titre :** Conclusion

**Contenu :**
- Pipeline complet : JSON → MongoDB → profils → labels → ML
- **Isolation Forest** : exploration sans labels
- **XGBoost** : classification supervisée honnête
- Méthodes du cours + compléments adaptés au problème
- Livrables : 5 notebooks · documentation L4 · portail web

**Notes orateur :**  
Notre contribution principale est la comparaison rigoureuse de deux familles de méthodes, avec un traitement explicite de la circularité.

**Visuel suggéré :** Schéma récapitulatif pipeline.

---

## Slide 15 — Transition démo live

**Titre :** Démonstration — Portail Streamlit

**Contenu :**
- Interface web : `demo/app.py`
- Lancement : `bash scripts/run_demo.sh`
- Navigation : Accueil · Pipeline · EDA · Labellisation · ML · Synthèse · Notebooks
- Chaque graphique = interprétation intégrée
- **→ Démonstration live maintenant**

**Notes orateur :**  
Ace lance la démo. Parcourir 3-4 sections clés : pipeline, labellisation, résultats ML, circularité. Le jury peut poser des questions en naviguant.

**Visuel suggéré :** Capture d'écran page d'accueil Streamlit.

---

## Slide 16 — Questions

**Titre :** Merci — Questions ?

**Contenu :**
- GitHub : https://github.com/ElProfesormika/PROJET_IF29-GR03
- Annexe orale possible :
  - IF vs K-Means → anomalies vs clusters
  - ACP 7 vs 5 → contextes différents
  - F1 0,443 vs 0,970 → circularité
  - Labels Excel → subjectifs mais reproductibles

**Notes orateur :**  
Après la démo, nous répondons aux questions. L'annexe FAQ est dans la documentation si besoin.

**Visuel suggéré :** Slide sobre, lien GitHub.

---

## Répartition orale suggérée (hors démo)

| Membre | Slides | ~durée |
|--------|--------|--------|
| Housseni YABRE | 3, 5 | ~2 min |
| Vanelle FOTSO AKOUDOUM | 6, 7 (partie EDA) | ~2 min |
| Samella LEUKOUO | 7 (ACP), 8 | ~2 min |
| Dorcas ADRAKE | 9, 10, 11 | ~3 min |
| Ace ANALLA | 12, 13, 14, 15 + **démo live** | ~5-6 min |

**Total slides : 16** · **Démo live : ~5 min** après la slide 15.

---

## Parcours démo Streamlit recommandé

1. **Accueil** — chiffres clés du projet
2. **Pipeline** — schéma ingestion → ML
3. **Labellisation** — 4 règles + distribution labels
4. **Non supervisé** — K-Means vs Isolation Forest
5. **Supervisé** — SVM vs XGBoost + ROC
6. **Synthèse** — circularité + conclusion

Lancement :

```bash
bash scripts/run_demo.sh
# http://localhost:8501
```

---

## Annexe — Questions jury (non présentée sauf demande)

**Isolation Forest vs K-Means ?**  
K-Means segmente ; IF détecte des anomalies. IF est plus adapté car les atypiques sont rares et dispersés. K-Means sous-détecte (0,54 % vs 17 % de labels).

**ACP 7 comp. vs 5 comp. ?**  
16 features (non sup.) → seuil 75 % → 7 comp. (~79 %). 8 features (sup.) → saturation à 5 comp. (100 %). Deux contextes, deux choix.

**k=7 K-Means vs 7 composantes ACP ?**  
Trois choix **indépendants** : k=7 vient du coude d'inertie, 7 comp. ACP du seuil de variance, 5 comp. supervisé de la saturation.

**F1 0,443 vs 0,970 ?**  
0,970 = circularité (16 features incluent les règles Excel). 0,443 = évaluation honnête sans ces variables.

**Fiabilité des labels Excel ?**  
Labels manuels, reproductibles, mais subjectifs. Non validés par un expert. Limite assumée.

**Pourquoi exclure 8 features supervisées ?**  
Elles servent directement aux règles de labellisation. Les inclure ferait apprendre les règles au modèle, pas un comportement généralisable.

**Pourquoi pas de SVM à noyau ?**  
Coût O(n²) incompatible avec 514 k lignes d'entraînement. Testé en annexe (`Groupe3_SVM_Noyaux_Annexe.ipynb`) sur sous-échantillon uniquement.
