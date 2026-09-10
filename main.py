import pandas as pd 
import numpy as np 
import yfinance as yf 

from math import floor, sqrt, exp
from scipy.stats import norm 

df = yf.download("^GSPC", start="2016-02-12", interval="1d", auto_adjust=False) 
#auto_adjust = true : close est ajusté et on a pas de distinctions entre close et adjclose. 
#auto_adjust dividendes et split n'impactent pas les résultats du modèle


data0 = df["Adj Close"].dropna().sort_index().astype(float) #Si bug vérifier que Adj Close est bien dans la df, dropna (que df) pour sup NaN
data = data0.squeeze() #Permet de convertir df en série, ce qui facilite les calculs et évite erreurs de type

Rt = data.pct_change() #calcule le rendement simple = (Pt - Pt-1) / Pt-1 = (data - data.shift(1)) / data.shift(1)
rt = np.log(data / data.shift(1)).dropna() # Dropna Car schift décale de 1 le tableau donc rt[0] pas def !! 

mu = rt.mean()
sigma = rt.std()
#Estimateurs empirique esperance et variance 


VaR_parametrique = - (mu + sigma * norm.ppf(0.05)) #quantile de loi gaussienne, moins car perte > 0

print("La VaR paramétrique est : " , round(VaR_parametrique*100, 4), "%.")

#VaR historique : quantile emprique des rt On prend le plus quand rt telle que | rk, rk < rt | =5*n/100
n = len(rt)
rt_tri = rt.sort_values(ascending = True) 


VaR_historique = - rt_tri.iloc[floor(0.05*n)] #rt_tri = série pandas indexé par dates !! Iloc permet d'indexer par position (comme tableau)

print("La VaR historique est : ", round(VaR_historique*100,4), "%.")



# VAR MONTE CARLO

N = 5000 #nombre simulations 

# simuler N pertes potentielles (On a déjà nos log rendements)

# Tab[N] des prix S1. La perte est (S0 - S1) / S0 (on divise pour remettre en pourcentage de S0)


Tab =[]
S = data.iloc[-1]
for i in range (N) : #N arbitraire 
    z = np.random.normal(0,1)
    S_sim = S*exp( (mu - (sigma**2) /2) + sigma*z)  # Peut être que T = 1/252
    Tab.append((S - S_sim) / S) #
    # On simule un rendement logarithmique et on calcule le prix S avec S = S0 exp(rendement calculé)
Tab.sort()
Var_Monte_Carlo = - Tab[floor(0.05*N)]

print("La VaR Monte Carlo est ", round(Var_Monte_Carlo * 100,4), "%." )  



#BACKTEST

# Etape 1 : On commence par déterminer les paramètres 
taille = 500 #Le nombre de paramètres qu'on utilise pour calculer la VaR dans le backtest
n_backtest = 100 #Nombre de date sur lesquelles on teste la VaR 
n_sim = N #Le nombre de simulations Monte Carlo par date 

# Etape 2 : 
t0 = len(data) - n_backtest - 1 #La première date à la quelle on test
tinf= len(data) - 1   

dates = []

var_hist_list = []
var_param_list = []
var_mc_list = []

liste_perte = []

viol_hist_list = []
viol_param_list = []
viol_mc_list = []
 
np.random.seed(42) #PERMET QUE LES TIRAGES MONTE CARLO SOIENT IDENTIQUES 

#Boucle de BackTest 

for t in range(t0, t0 + 100) : 
    S_t = data.iloc[t]
    S_t1 = data.iloc[t+1]

    perte_reel = (S_t - S_t1) / S_t   

    #Maintenant on doit se donner les tableaux qui contiennent les données sur les rendements disponibles
    Rend_Passee = Rt.iloc[t - taille : t] 
    log_Rend_Passee = rt.iloc[t - taille : t] 

    #1 VaR historique 
    Perte_hist = -Rend_Passee 
    VaR_hist = np.quantile(Perte_hist,0.95) #Meilleure implémentation, np.quantile évite le tri

    #2 VaR paramétrique 
    mu_R = Rend_Passee.mean()
    sigma_r = Rend_Passee.std()

    VaR_param = - (mu_R + sigma_r * norm.ppf(0.05))

    #3 VaR Monte Carlo
    mu_log = log_Rend_Passee.mean()
    sigma_log = log_Rend_Passee.std()

    Z = np.random.normal(0, 1, n_sim)
    S_sim = S_t * np.exp((mu_log - 0.5 * sigma_log**2) + sigma_log * Z)

    Perte_sim = (S_t - S_sim) / S_t
    VaR_MC = np.quantile(Perte_sim, 0.95)

    #Violation de la VaR
    viol_hist = perte_reel > VaR_hist
    viol_param = perte_reel > VaR_param
    viol_mc = perte_reel > VaR_MC

    #Stockage des données dans un dataframe indexé par la date t+1 
    dates.append(data.index[t+1])
    
    var_hist_list.append(VaR_hist)
    var_param_list.append(VaR_param)
    var_mc_list.append(VaR_MC)

    liste_perte.append(perte_reel)

    viol_hist_list.append(viol_hist)
    viol_param_list.append(viol_param)
    viol_mc_list.append(viol_mc)


# 7) On met le résultat sous forme de dataframe

backtest_df = pd.DataFrame({
    "Date": dates,
    "Perte_reelle": liste_perte,
    "VaR_historique": var_hist_list,
    "VaR_parametrique": var_param_list,
    "VaR_MC": var_mc_list,
    "Violation_historique": viol_hist_list,
    "Violation_parametrique": viol_param_list,
    "Violation_MC": viol_mc_list
})

backtest_df = backtest_df.set_index("Date")


# Affichage du résultat 

def resume_backtest(df, col_violation, alpha):
    n = len(df)
    n_viol = int(df[col_violation].sum())
    freq = df[col_violation].mean()
    expected = 1 - alpha
    return {
        "Nombre de tests": n,
        "Nombre de violations": n_viol,
        "Frequence observee": freq,
        "Frequence theorique": expected
    }

resume_hist = resume_backtest(backtest_df, "Violation_historique", 0.95)
resume_param = resume_backtest(backtest_df, "Violation_parametrique", 0.95)
resume_mc = resume_backtest(backtest_df, "Violation_MC", 0.95)
print("===== Backtest VaR historique =====")
for k, v in resume_hist.items():
    if isinstance(v, float):
        print(f"{k:<22}: {v:.4f} ({100*v:.2f} %)")
    else:
        print(f"{k:<22}: {v}")

print("\n===== Backtest VaR paramétrique =====")
for k, v in resume_param.items():
    if isinstance(v, float):
        print(f"{k:<22}: {v:.4f} ({100*v:.2f} %)")
    else:
        print(f"{k:<22}: {v}")

print("\n===== Backtest VaR Monte Carlo =====")
for k, v in resume_mc.items():
    if isinstance(v, float):
        print(f"{k:<22}: {v:.4f} ({100*v:.2f} %)")
    else:
        print(f"{k:<22}: {v}")
