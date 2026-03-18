# 📊 Value at Risk (VaR) – S&P 500

Ce projet implémente trois méthodes de calcul de la **Value at Risk (VaR)** :

- VaR paramétrique  
- VaR historique  
- VaR Monte Carlo  

Un **backtest** est ensuite réalisé pour évaluer la qualité des modèles.

Code principal : `MonteCarlo.py`

---

# 🔎 Résultat du run

- VaR paramétrique : **1.8169 %**
- VaR historique : **1.6649 %**
- VaR Monte Carlo : **1.9257 %**

Backtest (100 jours) :

| Méthode | Violations | Fréquence |
|--------|----------|----------|
| Historique | 4 | 4 % |
| Paramétrique | 2 | 2 % |
| Monte Carlo | 4 | 4 % |
| Théorique | - | 5 % |

### Interprétation

- Les résultats sont **globalement cohérents**.
- Historique et Monte Carlo sont proches du **5 % attendu**.
- Paramétrique est **plus conservatrice**.
- Aucune méthode ne semble aberrante.

⚠️ Attention : 100 observations est un échantillon **faible**. Les conclusions restent limitées.

---

# 📌 Définition de la VaR

La VaR à 95 % représente la **perte maximale** que l’on ne dépasse pas avec 95 % de probabilité sur un jour.

Exemple :  
VaR = 2 % → il y a 5 % de chances de perdre **plus de 2 %** en un jour.

---

# ⚙️ Données

- Actif : S&P 500 (`^GSPC`)
- Période : depuis 2016
- Données : prix ajustés

On calcule :

- Rendements simples :  

\[
R_t = \frac{P_t - P_{t-1}}{P_{t-1}}
\]

- Log-rendements :  

\[
r_t = \log\left(\frac{P_t}{P_{t-1}}\right)
\]

---

# 📐 Méthodes de calcul

## 1. VaR paramétrique

Hypothèse : les rendements suivent une **loi normale**.

\[
\text{VaR} = -(\mu + \sigma z_{0.05})
\]

- \(\mu\) : moyenne empirique  
- \(\sigma\) : écart-type  
- \(z_{0.05}\) : quantile gaussien  

✔️ Simple  
❌ Hypothèse forte

---

## 2. VaR historique

Principe : utiliser directement les données passées.

Étapes :
1. Trier les rendements
2. Prendre le quantile 5 %

✔️ Aucun modèle  
❌ Dépend du passé uniquement

---

## 3. VaR Monte Carlo

Principe : simuler des scénarios futurs.

Modèle utilisé :

\[
S_{t+1} = S_t \exp\left(\mu - \frac{\sigma^2}{2} + \sigma Z\right)
\]

avec \(Z \sim \mathcal{N}(0,1)\)

Étapes :
1. Simuler \(N\) prix futurs  
2. Calculer les pertes :
\[
L = \frac{S_t - S_{t+1}}{S_t}
\]
3. Prendre le quantile 95 %

✔️ Flexible  
❌ Dépend du modèle

---

# ⚠️ Choix arbitraires

Certains choix ne sont pas uniques :

- Niveau de confiance : **95 %**
- Nombre de simulations : **5000**
- Fenêtre de calibration : **500 jours**
- Taille du backtest : **100 jours**
- Hypothèse gaussienne
- Utilisation des log-rendements

Ces choix influencent les résultats.

---

# 🔁 Backtest

## Principe

On teste si la VaR est cohérente avec la réalité.

À chaque date \(t\) :

1. On calcule la VaR avec les données passées
2. On observe la perte réelle au jour \(t+1\)
3. On vérifie :

\[
\text{Violation} = \mathbf{1}_{\{ \text{perte réelle} > \text{VaR} \}}
\]

---

## Fréquence de violation

Si la VaR est correcte :

\[
\mathbb{P}(\text{violation}) = 1 - \alpha = 5\%
\]

On compare :

- fréquence observée  
- fréquence théorique  

---

## Interprétation

- Trop de violations → VaR **sous-estime** le risque  
- Pas assez → VaR **surestime** le risque  
- Proche de 5 % → modèle **bien calibré**

---

# 📊 Conclusion

- Les trois méthodes donnent des résultats proches.
- Monte Carlo est la plus prudente.
- Paramétrique est conservatrice.
- Historique est simple mais efficace.

👉 Aucun modèle n’est parfait.  
👉 Le choix dépend du contexte et des hypothèses.
