# 📊 Value at Risk (VaR) – S&P 500

Ce projet implémente trois méthodes de calcul de la **Value at Risk (VaR)** et un **backtest rigoureux**.

L’objectif est double :
- estimer le risque de perte à 1 jour
- vérifier si les modèles sont bien calibrés

---

# 📊 Données

- Actif : S&P 500 (Très aisément modifiable)
- Source : Yahoo Finance
- Donnée utilisée : prix ajusté

On construit :

- Rendement simple :
\[
R_t = \frac{P_t - P_{t-1}}{P_{t-1}}
\]

- Log-rendement :
\[
r_t = \log\left(\frac{P_t}{P_{t-1}}\right)
\]

👉 Les log-rendements sont utilisés pour Monte Carlo.

---

# 📐 Méthodes de VaR

## 1. VaR paramétrique

Hypothèse : les rendements suivent une loi normale.

\[
\text{VaR} = -(\mu + \sigma z_{0.05})
\]

- estimation empirique de \(\mu\) et \(\sigma\)
- quantile gaussien

👉 Méthode rapide mais dépend fortement de l’hypothèse de normalité.

---

## 2. VaR historique

Principe : utiliser directement les données passées.

Étapes :
- calcul des pertes passées
- extraction du quantile 95 %

👉 Pas d’hypothèse de loi  
👉 Mais dépend entièrement du passé

---

## 3. VaR Monte Carlo

### 📐 Modèle théorique

On suppose que le prix suit un **mouvement brownien géométrique (GBM)** :

\[
\frac{dS_t}{S_t} = \mu dt + \sigma dW_t
\]

#### Hypothèses

- rendements gaussiens  
- volatilité constante  
- pas de sauts  
- indépendance des incréments  

---

#### Conséquence

Les log-rendements sont normaux :

\[
\ln\left(\frac{S_T}{S_0}\right) \sim \mathcal{N}\left(\left(\mu - \frac{\sigma^2}{2}\right)T,\ \sigma^2 T\right)
\]

---

#### Formule utilisée

\[
S_T = S_0 \exp\left(\left(\mu - \frac{\sigma^2}{2}\right)T + \sigma \sqrt{T} Z\right)
\quad \text{avec } Z \sim \mathcal{N}(0,1)
\]

👉 Dans le code, on prend implicitement \(T = 1\) jour.

On simule des prix futurs via :

\[
S_{t+1} = S_t \exp\left(\mu - \frac{\sigma^2}{2} + \sigma Z\right)
\]

avec \(Z \sim \mathcal{N}(0,1)\)

Puis :

\[
L = \frac{S_t - S_{t+1}}{S_t}
\]

👉 On génère N scénarios  
👉 On prend le quantile 95 %

---

# ⚠️ Choix arbitraires (IMPORTANT)

Plusieurs choix influencent directement les résultats :

- Niveau de confiance : **95 %**
- Nombre de simulations Monte Carlo : **5000**
- Taille de la fenêtre d’estimation : **500 jours**
- Taille du backtest : **100 jours**
- Modèle gaussien pour les rendements
- Utilisation des log-rendements
- Horizon fixé implicitement à 1 jour

👉 Ces choix ne sont pas uniques  
👉 D’autres paramètres donneraient des résultats différents 
👉 Ils ne changent pas la cohérence du modèle. 

On aurait pu prendre la VaR à **99 %**, augmenter la taille du backtest... Le nombre de simulations de Monte Carlo a été fixé à **5000** car une stabilisation de la VaR a été observée aux alentours de cette valeur. 

---

# 🔁 Backtest (partie centrale du projet)

## Principe

À chaque date t :

1. On estime la VaR avec les données passées
2. On observe la perte réelle au jour t+1
3. On compare

\[
\text{Violation} = \mathbf{1}_{\{ \text{perte réelle} > \text{VaR} \}}
\]

---

## Interprétation mathématique

Si la VaR est correcte :

\[
\mathbb{P}(\text{violation}) = 1 - \alpha = 5\%
\]

Sur N observations :

- nombre attendu ≈ 5 % × N

---

## Interprétation financière

- Trop de violations → risque sous-estimé
- Trop peu → modèle trop conservateur
- Proche de 5 % → modèle cohérent

---

# 🔎 Résultats obtenus

- VaR paramétrique : 1.8169 %
- VaR historique : 1.6649 %
- VaR Monte Carlo : 1.9257 %

Backtest :

- Historique : 4 %
- Paramétrique : 2 %
- Monte Carlo : 4 %
- Théorique : 5 %

---

# 📊 Analyse des résultats

- Les trois méthodes sont cohérentes en ordre de grandeur
- Monte Carlo donne la VaR la plus élevée → plus prudente
- Paramétrique donne peu de violations → surestime légèrement le risque
- Historique est bien calibrée sur cet échantillon

👉 Aucun modèle ne domine clairement

---

# ⚠️ Limites

- Backtest sur seulement 100 observations
- Hypothèse gaussienne discutable
- Marché non stationnaire
- Sensibilité aux paramètres

---

# 📌 Conclusion

Ce projet montre que :

- plusieurs méthodes de VaR existent
- leurs résultats dépendent fortement des hypothèses
- le backtest est essentiel pour valider un modèle

👉 La VaR n’est pas une vérité absolue  
👉 C’est un outil dépendant du modèle
