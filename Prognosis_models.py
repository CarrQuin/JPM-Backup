"""
Date: 15.01.2025
Description: This script is used to predict the future trend about PV market based on historical data.
The script reads the data from an Excel file, fits different growth models to the data, and generates
predictions for the future years. The different models are uesd and could add or remove the models
by changing the model options. The script also saves the result to a CSV file and plots the predictions.
Author: Kaiyu Qian
"""
import numpy as np
import pandas as pd
import Confidence_intervals as ci
from scipy.optimize import curve_fit
# ------------------------------------------------------------
# Set the file path and data columns
file_path = r"Prognosis-Datasource.xlsx" #in the same folder
data_cols = "A, E" #should be the columns of years and values

# Set the save result option
save_result = True

# Set the model options
include_logistic = True
include_gompertz = False
include_gaussian = False
include_exponential = False
include_power_law = False

# Set the preset years
preset_year = 2026 # The year where the growth rate is the highest
preset_year_max = 2035 # The maximum year for the preset year
values_coeff_max = 10 # The maximum coefficient for the values
end_year = 2050 # The end year for the prediction

# Set the confidence interval in percentage [%]
covariance_level = 75 # 0-100
covariance_model = "t" # "z" or "t"

#------------------------------------------------------------
# Read the data from the Excel file
data = pd.read_excel(file_path, header=0, usecols=data_cols)
data.dropna( inplace=True)
years = data.iloc[:,0].astype(int).tolist()
values = data.iloc[:,1].astype(float).tolist()

# Normalize the years
future_years = np.arange(np.min(years) - 1, end_year + 1)

# Initialize the predictions
logistic_predictions = None
gompertz_predictions = None
gaussian_predictions = None
exponential_predictions = None
power_law_predictions = None

#------------------------------------------------------------
# The Logistic Growth Model
def logistic_growth(x, K, b, x0):
    """return : array_like"""
    return K / (1 + np.exp(-b * (x - x0)))

if include_logistic:
    # Fit the Logistic model to the data
    try:
        logistic_params, logistic_covariance = curve_fit(
            logistic_growth, years, values, 
            p0=[max(values)*3, 0.1, preset_year], # !!! The hardest part is to find the right initial parameters
            bounds=([max(values)*1, 0, np.min(years)], [max(values)*values_coeff_max, 5, preset_year_max]), 
            maxfev=10000
        )
        print(f"\nLogistic parameters: \nK={logistic_params[0]:.2f}, \nb={logistic_params[1]:.5f}, \nx0={int(logistic_params[2])}")
    except RuntimeError as e:
        print(f"Logistic model fitting failed: {e}")
        logistic_params = None

    if logistic_params is not None:
        logistic_predictions = logistic_growth(future_years, *logistic_params)
        logistic_params_lower, logistic_params_upper = ci.covariance_params(
            covariance_level, years, logistic_params, logistic_covariance, covariance_model)
        covariance_years = np.arange(np.max(years), end_year + 1)
        logistic_prediced_lower = logistic_growth(covariance_years, *logistic_params_lower)
        logistic_perdiced_upper = logistic_growth(covariance_years, *logistic_params_upper)

# ------------------------------------------------------------
# The Gompertz Growth Model
def gompertz_growth(x, K, b, x0):
    """return : array_like"""
    return K * np.exp(-np.exp(-b * (x - x0)))

if include_gompertz:
    # Fit the Gompertz model to the data
    try:
        gompertz_params, gompertz_covariance = curve_fit(
            gompertz_growth, years, values, 
            p0=[max(values)*3, 0.1, preset_year], # !!! The hardest part is to find the right initial parameters
            bounds=([max(values)*1, 0, np.min(years)], [max(values)*values_coeff_max, 5, preset_year_max]), 
            maxfev=10000
        )
        print(f"\nGompertz parameters: \nK={gompertz_params[0]:.2f}, \nb={gompertz_params[1]:.5f}, \nx0={int(gompertz_params[2])}")
    except RuntimeError as e:
        print(f"Gompertz model fitting failed: {e}")
        gompertz_params = None

    if gompertz_params is not None:
        gompertz_predictions = gompertz_growth(future_years, *gompertz_params)
        

# ------------------------------------------------------------
# The Gaussian Growth Model
def gaussian_growth(x, A, c1, c2, u):
    """return : array_like"""
    # return A * np.exp(-0.5 * ((x - u) / c1)**2)
    return np.where(x < u,
        A * np.exp(-0.5 * ((x - u) / c1)**2), 
        A * np.exp(-0.5 * ((x - u) / c2)**2))

if include_gaussian: 
    try:
        gaussian_params, gaussian_covariance = curve_fit(
            gaussian_growth, years, values, 
            p0=[max(values)*0.5, 0.5,1, preset_year], 
            # bounds=([max(value)*0.1, 0,0, np.min(years)], [max(value)*1.5,np.inf, 10, 2035]), 
            maxfev=10000
        )
        print(f"\nGaussian parameters: \nA={gaussian_params[0]:.2f}, \nc1={gaussian_params[1]:.2f}, \nc2={gaussian_params[2]:.2f}, \nu={gaussian_params[3]:.2f}")
    except RuntimeError as e:
        print(f"Gaussian model fitting failed: {e}")
        gaussian_params = None

    if gaussian_params is not None:
        gaussian_predictions = gaussian_growth(future_years, *gaussian_params)

# ------------------------------------------------------------
# The Exponential Growth Model
def exponential_growth(x, c, l, a):
    """return : array_like"""
    return c * (1 - np.exp(-((x/l)**a)))

if include_exponential:
    try:
        # Normalize the years
        normalized_years_exp = (np.array(years) - np.min(years)) / (np.max(years) - np.min(years))
        future_normalized_years_exp = (future_years - np.min(years)) / (np.max(years) - np.min(years))
        normalized_preset_year_max_exp = (preset_year_max - np.min(years)) / (np.max(years) - np.min(years))
        
        exponential_params, exponential_covariance = curve_fit(
            exponential_growth, normalized_years_exp, values, 
            p0=[np.max(values)*1.5, 0.5, 1], 
            bounds=([max(values)*1, 0, 0], [max(values)*values_coeff_max, normalized_preset_year_max_exp, np.inf]), 
            maxfev=10000
        )
        exp_preset_year = int(exponential_params[1]*(np.max(years)-np.min(years))+np.min(years))
        print(f"\nExponential parameters: \nc={exponential_params[0]:.2f}, \nl={exponential_params[1]:.2f}, \na={exponential_params[2]:.5f}")
    except RuntimeError as e:
        print(f"Exponential model fitting failed: {e}")
        exponential_params = None

    if exponential_params is not None:
        exponential_predictions = exponential_growth(future_normalized_years_exp, *exponential_params)

# -----------------------------------------------------------
# The Power Law Growth Model
def power_law(x, a, b):
    """return : array_like"""
    return a * (x**b)

if include_power_law:
    try:
        normalized_years = np.array(years) - np.min(years)
        future_normalized_years = future_years - np.min(years)
        power_law_params, power_law_covariance = curve_fit(
            power_law, normalized_years, values, 
            p0=[1, 0.01], 
            bounds=([0, 0], [np.inf, np.inf]), 
            maxfev=10000
        )
        print(f"\nPower Law parameters: \na={power_law_params[0]:.2f}, \nb={power_law_params[1]:.5f}")
    except RuntimeError as e:
        print(f"Power Law model fitting failed: {e}")
        power_law_params = None

    if power_law_params is not None and include_power_law:
        power_law_predictions = power_law(future_normalized_years, *power_law_params)

#------------------------------------------------------------


    
    
#------------------------------------------------------------
# Save the result to a CSV file
if save_result:
    predictions = pd.DataFrame({
        "Year": future_years,
        "Logistic": logistic_predictions,
        "Gompertz": gompertz_predictions,
        "Gaussian": gaussian_predictions,
        "Exponential": exponential_predictions,
        "Power Law": power_law_predictions
    })
    predictions.to_csv("Prognoses-Result.csv", index=False)
    print(f"\nPrognoses result has been saved to 'Prognoses-Result.csv'")
    
    covariance = pd.DataFrame({
        "Year": future_years[-len(logistic_prediced_lower):],
        "Logistic Lower": logistic_prediced_lower,
        "Logistic exact": logistic_predictions[-len(logistic_prediced_lower):],
        "Logistic Upper": logistic_perdiced_upper
    })
    covariance.to_csv("Prognoses-Covariance.csv", index=False)
    print(f"\nPrognoses covariance has been saved to 'Prognoses-Covariance.csv'")

# Print the parameters
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    plt.figure(num=f"comparison different prognoses up to {int(future_years[-1])}", figsize=(10, 6))
    plt.scatter(years, values, color="black", label="Original Data")
    if logistic_predictions is not None: 
        plt.plot(future_years, logistic_predictions, linestyle="--", color="blue", label="Logistic Growth Model")
        plt.axvline(x=logistic_params[2], linestyle="-", color="blue", label="G Preset Year")
        plt.fill_between(covariance_years, logistic_prediced_lower, logistic_perdiced_upper, color="blue", alpha=0.2, label=f"Confidence Interval ({covariance_model}) {covariance_level}%")
    if gompertz_predictions is not None: 
        plt.plot(future_years, gompertz_predictions, linestyle="--", color="green", label="Gompertz Growth Model")
        plt.axvline(x=gompertz_params[2], linestyle="-", color="green", label="G Preset Year")
    if gaussian_predictions is not None:
        plt.plot(future_years, gaussian_predictions, linestyle="--", color="purple", label="Gaussian Growth Model")
    if exponential_predictions is not None:
        plt.plot(future_years, exponential_predictions, linestyle="--", color="magenta", label="Exponential Growth Model")
        plt.axvline(x=exp_preset_year, linestyle="-", color="magenta", label=f"G Preset Year {exp_preset_year}")
    if power_law_predictions is not None:
        plt.plot(future_years, power_law_predictions, linestyle=":", color="orange", label="Power Law Growth Model")
    plt.gcf().set_tight_layout(True)
    plt.title(f"The different prognoses up to {int(future_years[-1])}")
    # plt.xlabel(data.columns[0])
    plt.ylabel(data.columns[1])
    plt.legend()
    plt.grid(True)
    plt.show()
