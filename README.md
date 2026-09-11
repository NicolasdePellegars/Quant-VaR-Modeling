# Value at Risk (VaR) – S&P 500

The project implements tree methods to compute **Value at Risk (VaR)** supported by a backtest **backtest**.

There are two objectives :
- to estimate the risk of a one-day loss 
- to evaluate the quality of the VaR estimates using backtesting

---

# Data

- Asset : S&P 500 (easily adjustable)
- Source : Yahoo Finance
- Data used : adjusted prices (to make historical prices comparable over time to avoid treating events such as dividends or stock splits as actual market losses)

We compute :

- Simple returns :

$$R_t = \frac{P_t - P_{t-1}}{P_{t-1}}$$

- Log returns :

$$r_t = \log\left(\frac{P_t}{P_{t-1}}\right)$$

Log returns are used for the Monte Carlo method.

---

# VaR Methods

## 1. Parametric VaR 

Assumption : returns follow a normal distribution .

$$
\text{VaR} = -(\mu + \sigma z_{0.05})
$$

- empirical estimation of $\mu$ and $\sigma$
- Gaussian quantile

Méthode rapide mais dépend fortement de l’hypothèse de normalité.

---

## 2. VaR historique

Principe : utiliser directement les données passées.

Étapes :
- calcul des pertes passées
- extraction du quantile 95 %

 Pas d’hypothèse de loi  
 Mais dépend entièrement du passé

---

## 3. VaR Monte Carlo

### 📐 Modèle théorique

On suppose que le prix suit un **mouvement brownien géométrique (GBM)** :

$$
\frac{dS_t}{S_t} = \mu dt + \sigma dW_t
$$

#### Hypothèses

- rendements gaussiens  
- volatilité constante  
- pas de sauts  
- indépendance des incréments  

---

#### Conséquence

Les log-rendements sont normaux :

$$
\ln\left(\frac{S_T}{S_0}\right) \sim \mathcal{N}\left(\left(\mu - \frac{\sigma^2}{2}\right)T,\ \sigma^2 T\right)
$$

---

#### Formule utilisée

$$
S_T = S_0 \exp\left(\left(\mu - \frac{\sigma^2}{2}\right)T + \sigma \sqrt{T} Z\right)
\quad \text{avec } Z \sim \mathcal{N}(0,1)
$$

Dans le code, on prend implicitement $T = 1$ jour.

On simule des prix futurs via :

$$
S_{t+1} = S_t \exp\left(\mu - \frac{\sigma^2}{2} + \sigma Z\right)
$$

avec $Z \sim \mathcal{N}(0,1)$

Puis :

$$
L = \frac{S_t - S_{t+1}}{S_t}
$$

On génère N scénarios  
On prend le quantile 95 %

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

Ces choix ne sont pas uniques  
D’autres paramètres donneraient des résultats différents  
Ils ne changent pas la cohérence du modèle. 

On aurait pu prendre la VaR à **99 %**, augmenter la taille du backtest... Le nombre de simulations de Monte Carlo a été fixé à **5000** car une stabilisation de la VaR a été observée aux alentours de cette valeur. 

---

# 🔁 Backtest

## Principe

À chaque date t :

1. On estime la VaR avec les données passées
2. On observe la perte réelle au jour t+1
3. On compare

$$
\text{Violation} = \mathbf{1}_{\{ \text{perte réelle} > \text{VaR} \}}
$$

---

## Interprétation mathématique

Si la VaR est correcte :

$$
\mathbb{P}(\text{violation}) = 1 - \alpha = 5\%
$$

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

---

# 📊 Analyse des résultats

Les trois méthodes donnent des niveaux de VaR proches, mais leurs différences permettent d’interpréter la structure du risque.

- La VaR Monte Carlo est la plus élevée (1.9257 %).  
Cela suggère que la volatilité estimée est significative et que le modèle gaussien appliqué aux log-rendements génère des scénarios extrêmes plus marqués.  
Cela peut être cohérent avec une période incluant des phases de forte incertitude (ex : crises, chocs macro, hausse des taux).

- La VaR historique est plus faible (1.6649 %).  
Cela signifie que les pertes extrêmes observées dans le passé récent sont moins sévères que celles générées par le modèle.  
On peut en déduire que la fenêtre historique utilisée ne contient pas suffisamment d’événements extrêmes, ou que les chocs passés sont moins violents que ceux implicites dans la volatilité actuelle.

- La VaR paramétrique est intermédiaire mais avec seulement 2 % de violations.  
Elle semble surestimer le risque dans le backtest.  
Cela peut indiquer que l’hypothèse gaussienne lisse les données et attribue trop de poids à la volatilité moyenne, sans bien capturer la dynamique réelle des queues de distribution.

---

## Lecture en termes de structure de marché

Ces résultats peuvent être interprétés comme suit :

- L’écart entre VaR historique et Monte Carlo suggère une possible **instabilité récente du marché**.  
Le modèle (via σ) intègre une volatilité élevée, mais celle-ci ne s’est pas encore traduite par suffisamment de pertes extrêmes dans les données historiques.

- Le faible nombre de violations pour la VaR paramétrique peut indiquer que :  
  soit le marché a été relativement calme sur la période de backtest,  
  soit la distribution réelle des rendements est moins extrême que la gaussienne sur cet intervalle.

- Le fait que Monte Carlo et historique soient proches en fréquence de violation (4 %) suggère que malgré leurs différences de construction, ces deux approches capturent relativement bien le risque empirique sur cette période.

---

## Interprétation économique

On peut formuler l’hypothèse suivante :

Le marché présente une volatilité élevée (captée par σ),  
mais sans occurrence récente de chocs extrêmes équivalents dans la fenêtre historique.

Cela correspond typiquement à des phases :

- post-crise (volatilité encore élevée mais marché stabilisé)
- ou périodes d’incertitude macro (inflation, taux, géopolitique)

---

En résumé :

- Historique → dépend du passé observé  
- Paramétrique → dépend de la structure du modèle  
- Monte Carlo → dépend de la volatilité estimée  

Les différences entre ces méthodes donnent une information sur la **forme de la distribution des rendements et l’état du marché**.

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

La VaR n’est pas une vérité absolue  
C’est un outil dépendant du modèle
