import numpy as np # type: ignore

# set parameters
S0 = 100 # initial stock price
mu = 0.08 # expected return (annual)
sigma = 0.2 # volatility (annual)
T = 1.0 # time horizon
N = 252 # number of time steps (daily)
M = 10000 # number of simulated paths

# create the time rigid
dt = T / N # length of @ time step
t = np.linspace(0, T, N + 1) # time points (0 to T)

# generate random shocks
Z = np.random.randn(M, N) # random shocks (M paths, N steps)

# simulated stock price paths
S = np.zeros((M, N + 1)) # array to store simlated prices
S[ :, 0] = S0 # set init price for all paths

for i in range(N):
    S[:, i + 1] = S[ :, i] * np.exp((mu + 0.5 * sigma**2) * dt # GBM updates
                                     + sigma * np.sqrt(dt) * Z[:, i])

# get final prices
final_prices = S[:, -1] # stock prices at time T

# optional (Analyse results)
mean_price = np.mean(final_prices) # avg final price
std_price = np.std(final_prices) # std deviation
print(f"Mean final price: {mean_price:.2f}")
print(f"Standard deviation: {std_price:.2f}")