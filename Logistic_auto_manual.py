"""
Date: 18.02.2025
Description: Show the difference between the auto and manual logistic models.
Author: Kaiyu Qian
"""
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import Confidence_intervals as ci

# Location of the data
file = r"Installation.xlsx" #in the same folder
sheet = "Global Top5" #sheet name
cols = "A, M" #should be the columns of years and values

# The end year of the Prognose
end_year = 2051

# Auto logistic model
show_auto = True
values_coeff_max = 3 # k max
growth_rate_min = 0.1 # b min
preset_year = 2018 # x0 preset year
preset_year_limits = 5 # the limits of the preset year

# Manual logistic model
show_maual = False
k_m = 390
b_m = 0.215
x0_m = 2029

# Covariance
show_covariance = False
covariance_level = 75 # in percentage [0,100] %
covariance_mode = "t" # "z" or "t"

# Read the data
data = pd.read_excel(file, header=0, usecols=cols, sheet_name=sheet)
data.dropna( inplace=True)
years = data.iloc[:,0].astype(int).tolist()
values = data.iloc[:,1].astype(float).tolist()

# Logistic function
def logistic_growth(x, k, b, x0):
    """
    Parameters
        x: int
        k: float
        b: float
        x0: int
    Return
        float
    """
    return k / (1 + np.exp(-b * (x - x0)))

logistic_params = None
future_years = np.arange(np.min(years) - 1, end_year + 1)
covariance_years = np.arange(np.max(years), end_year + 1)

try:
    logistic_params, covariance_auto = curve_fit(
        logistic_growth, years, values, 
        p0=[max(values)*1, growth_rate_min, preset_year], 
        bounds=([max(values)*1, growth_rate_min, preset_year-preset_year_limits], 
                [max(values)*values_coeff_max, 2, preset_year+preset_year_limits]), 
        maxfev=10000
    )
    print(f"\nLogistic parameters: \nK={logistic_params[0]:.2f}, \nb={logistic_params[1]:.5f}, \nx0={int(logistic_params[2])}")
except RuntimeError as e:
    print(f"Logistic model fitting failed: {e}")
    logistic_params = None
        
if logistic_params is not None and show_auto:
    logistic_predictions_auto = logistic_growth(future_years, *logistic_params)
    auto_params_lower, auto_params_upper = ci.covariance_params(
        covariance_level, years, logistic_params, covariance_auto, covariance_mode)
    auto_prediced_lower = logistic_growth(covariance_years, *auto_params_lower)
    auto_prediced_upper = logistic_growth(covariance_years, *auto_params_upper)
if show_maual:
    logistic_predictions_manual = logistic_growth(future_years, k_m, b_m, x0_m)
    covariance_manual = ci.covariance_matrix(logistic_growth, np.array(years), values, [k_m, b_m, x0_m])
    manual_params_lower, manual_params_upper = ci.covariance_params(
        covariance_level, years, [k_m, b_m, x0_m], covariance_manual, covariance_mode)
    manual_prediced_lower = logistic_growth(covariance_years, *manual_params_lower)
    manual_prediced_upper = logistic_growth(covariance_years, *manual_params_upper)

if __name__ == "__main__":
    plt.figure(num="auto and manual ", figsize=(10, 6))
    plt.scatter(years, values, color="black", label="Original Data")
    if show_auto:
        plt.plot(future_years, logistic_predictions_auto, linestyle="--", color="blue", label="Logistic auto")
        if show_covariance:
            plt.fill_between(covariance_years, auto_prediced_lower, auto_prediced_upper, color="blue", alpha=0.2)
        plt.axvline(x=logistic_params[2], linestyle="-", color="blue", label=f"preset year: {int(logistic_params[2])}")
    if show_maual: 
        plt.plot(future_years, logistic_predictions_manual, linestyle="--", color="red", label="Logistic maunual")
        if show_covariance:
            plt.fill_between(covariance_years, manual_prediced_lower, manual_prediced_upper, color="red", alpha=0.2)
        plt.axvline(x=x0_m, linestyle="-", color="red", label=f"preset year: {x0_m}")
    plt.gcf().set_tight_layout(True)
    plt.ylabel(data.columns[1])
    plt.legend()
    plt.grid(True)
    plt.show()