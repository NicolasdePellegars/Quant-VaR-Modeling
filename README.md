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

Fast method but strongly dependent on the normality assumption

---

## 2.Historical VaR

Principle : directly use past data 

Steps :
-Comput past losses
- exxtract the 95 % quantile

No distribution assumption. However, the method depends entirely on past observations

---

## 3. Monte Carlo VaR

### Theorical Model

We assume that the asset price follows a **Geometric Brownian Motion (GBM)** :

$$
\frac{dS_t}{S_t} = \mu dt + \sigma dW_t
$$

#### Assumptions

- normally distributed returns   
- constant vol  
- no jump  
- independant increments  

---

#### Consequence

Log returns are normally distributed :

$$
\ln\left(\frac{S_T}{S_0}\right) \sim \mathcal{N}\left(\left(\mu - \frac{\sigma^2}{2}\right)T,\ \sigma^2 T\right)
$$

---

#### Formula used

$$
S_T = S_0 \exp\left(\left(\mu - \frac{\sigma^2}{2}\right)T + \sigma \sqrt{T} Z\right)
\quad \text{avec } Z \sim \mathcal{N}(0,1)
$$

In the code, me implicitly use $T = 1$ jour.

Futur prices are simulated using :

$$
S_{t+1} = S_t \exp\left(\mu - \frac{\sigma^2}{2} + \sigma Z\right)
$$

with $Z \sim \mathcal{N}(0,1)$

Then :

$$
L = \frac{S_t - S_{t+1}}{S_t}
$$

We generate $N$ scenarios.
We take the 95% quantile.

---

# Arbitrary choices 

Several choices directly affect the results : 

- Confidence level : **95 %**
- Number of Monte Carlo simulations : **5000**
- Estimation window size : **500 jours**  (amount of historical data used to compute VaR)
- Backtest period : **100 jours**
- One day horizon

These choices are not unique, different parameters would lead to different results.

We could have used a **99 %** VaR, Increase the backtest size... The number of Monte Carlo simulations was set to **5000** because the VaR was observed to stabilize around this value.

---

# 🔁 Backtesting

## Principle

At each date $t$:

1. We estimate the VaR using past data
2. We observe the actual loss on day $t+1$
3. We compare the two

$$
\text{Violation} = \mathbf{1}_{\{ \text{perte réelle} > \text{VaR} \}}
$$

---

## Mathematical Interpretation

If the VaR estimate is accurate: 

$$
\mathbb{P}(\text{violation}) = 1 - \alpha = 5\%
$$

Over N observations :

- expected number ≈ 5 % × N

---

## Financial interpretation 

- Too many violation → risk is underestimated 
- Too few violation → risk is overestimated
- Close to 5 % → the model is consistent with the expected violation rate 

---

# 🔎 Results 

- Parametric VaR : 1.8169 %
- Historical VaR : 1.6649 %
- Monte Carlo VaR : 1.9257 %

Violation rate during the backtesting :

- Historical : 4 %
- Parametric : 2 %
- Monte Carlo : 4 %

---

# Results Analysis

The three methods produce relatively similar VaR estimates.

Historical and Monte Carlo VaR both have a 4% violation rate, close to the theoretical 5% expected for a 95% VaR. Parametric VaR has a lower violation rate of 2%, suggesting that it was more conservative over the backtesting period.

These results should be interpreted carefully, as the backtest contains only 100 observations.

# Limitations

* Backtest based on only 100 observations
* Debatable Gaussian assumption
* Non-stationary market
* Sensitivity to parameters

---

# Conclusion

This project shows that :

- several VaR methods can be used
- their results strongly depend on the underlying assumptions
- backtesting is essential to evaluate a model

VaR is not an absolute measure of risk but a model dependant tool. 
