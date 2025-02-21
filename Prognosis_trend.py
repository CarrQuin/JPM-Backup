"""
Date: 24.01.2025
Description: Show the trend of Periode.
Author: Kaiyu Qian
"""
import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
file_path = r"Prognosis-Datasource.xlsx"
data = pd.read_excel(
    file_path, usecols="A, E", header=0
    )
data.columns = ["Years", "Values"]
data.dropna(subset=["Years", "Values"], inplace=True)
data.set_index("Years", inplace=True)
data.astype(float)
seasonal_decompose(data, model='additive', period=10).plot()
plt.show()
