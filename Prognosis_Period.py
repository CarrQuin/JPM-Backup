import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy.optimize import curve_fit

# read Excel file
data = pd.read_excel(r"Prognosis-Datasource.xlsx", usecols="A, E", header=0)
data.dropna( inplace=True)
years = data.iloc[:,0].astype(int).tolist()
values = data.iloc[:,1].astype(float).tolist()
data.set_index("Jahr", inplace=True)

# Normalization the years
preset_years = 2020
future_years = np.arange(np.min(years)-1, 2051)

# Decompose the data
result = seasonal_decompose(data, model='additive', period=5)
trend_part = result.trend
seasonal_part = result.seasonal
residual_part = result.resid

# Filter out missing values
valid_indices = ~trend_part.isna()
filtered_years = np.array(years)[valid_indices]
filtered_trend = trend_part[valid_indices].values

valid_seasonal = ~seasonal_part.isna()
filtered_seasonal_years = np.array(years)[valid_seasonal]
filtered_seasonal = seasonal_part[valid_seasonal].values

# Trend model
def logistic_model(x, K, b, x0):
    return K / (1 + np.exp(-b * (x - x0)))

logistic_params, _ = curve_fit(
    logistic_model, filtered_years, filtered_trend, 
    p0=[np.max(filtered_trend)*0.5, 0.01, preset_years],
    bounds=([np.max(filtered_trend)*0.1, 0, 0], [np.max(filtered_trend)*10, np.inf, 2035]),
    maxfev=10000
)

logistic_predictions = logistic_model(future_years, *logistic_params)

# Seasonal model
def sin_model(t, A0, k, f, phi):
    return (A0 * np.exp(k*t)) * np.sin(2 * np.pi * f * t + phi)

periodic_params, _ = curve_fit(
    sin_model, filtered_seasonal_years, filtered_seasonal,
    p0=[np.max(filtered_seasonal)*0.5, 0.01, 1/20, 0],
    bounds=([np.max(filtered_seasonal)*0.1, 0, 0, -np.pi], [np.max(filtered_seasonal)*10, np.inf, 20, np.pi]),
    maxfev=10000
    )

seasonal_pred = sin_model(future_years, *periodic_params)

# Future prediction
future_pred = logistic_predictions + seasonal_pred

# Plot the data
plt.figure(num=f"Prognosis up to {int(future_years[-1])}", figsize=(16, 9))
plt.scatter(years, values, color="black", label="Actual Data")
plt.plot(future_years, future_pred, label="Prediction")
plt.gcf().set_tight_layout(True)
plt.title(f"Prognosis up to {int(future_years[-1])}")
plt.legend()
plt.show()
