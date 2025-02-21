import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# --- Einstellungen ---
file_path = r"Installation.xlsx"  # Pfad zur Originaldatei
sheet = "Global Top5"                     # Blattname
data_cols = "A, G"                          # Spalten, z. B. A: Jahr, E: beobachtete Werte
manual_cutoff_year = 2023                   # Jahr, bis zu dem Originaldaten genutzt werden
transition_width = 0                        # Übergangsbreite (in Jahren) für das Blending

# Weitere Einstellungen
preset_year = 2024
end_year = 2051  # Endjahr für die Prognose
jump = 11        # Anzahl der Jahre, die übersprungen werden
# Parameter für den automatischen Fit
values_coeff_max = 5   # Multiplikator für K
growth_rate_min = 0.15  # untere Schranke für b
preset_year_max = 2035  # obere Schranke für x0

# Manuelle logistische Modellparameter
manual_K = 360
manual_b = 0.27
manual_x0 = 2023

# --- Funktion zur Berechnung der logistischen Wachstumskurve ---
def logistic_growth(x, K, b, x0):
    return K / (1 + np.exp(-b * (x - x0)))

# --- Daten einlesen ---
data = pd.read_excel(file_path, sheet_name=sheet, header=0, usecols=data_cols)
data.dropna(inplace=True)
# data = data.iloc[jump:]
# Annahme: Die erste Spalte enthält die Jahre, die zweite die beobachteten Werte
year_col = data.columns[0]
value_col = data.columns[1]

# Konvertierung der Spalten (falls notwendig)
data[year_col] = data[year_col].astype(int)
data[value_col] = data[value_col].astype(float)

# Für den Fit benötigen wir Listen bzw. Arrays:
years = data[year_col].tolist()
values = data[value_col].tolist()

# --- Automatischer Fit des logistischen Modells ---
try:
    logistic_params, covariance = curve_fit(
        logistic_growth, years, values,
        p0=[max(values) * (values_coeff_max / 3), growth_rate_min, preset_year],
        bounds=([max(values) * (values_coeff_max / 10), growth_rate_min, min(years)],
            [max(values) * values_coeff_max, 2, preset_year_max]),
        maxfev=10000
    )
    print(f"Logistische Parameter (auto fit): K = {logistic_params[0]:.2f}, b = {logistic_params[1]:.5f}, x0 = {int(logistic_params[2])}")
except RuntimeError as e:
    print(f"Logistische Modellanpassung fehlgeschlagen: {e}")
    logistic_params = None

# --- Erzeuge einen vollständigen Jahresbereich ---
all_years = np.arange(min(years), end_year + 1)

# --- Berechnung der automatischen logistischen Prognose für jeden Jahr im Bereich ---
if logistic_params is not None:
    logistic_auto_values = logistic_growth(all_years, *logistic_params)
else:
    logistic_auto_values = np.full_like(all_years, np.nan, dtype=float)

# --- Definition der manuellen Piecewise-Blended-Funktion ---
def manual_piecewise_blended(x):
    if x <= manual_cutoff_year:
        # Falls x nicht exakt in den Originaljahren vorhanden ist, erfolgt die Interpolation
        return np.interp(x, years, values)
    elif x > manual_cutoff_year + transition_width:
        return logistic_growth(x, manual_K, manual_b, manual_x0)
    else:
        # Blending: Gewicht steigt linear von 0 bis 1 im Übergangsbereich
        weight = (x - manual_cutoff_year) / transition_width
        observed = np.interp(x, years, values)
        logistic_val = logistic_growth(x, manual_K, manual_b, manual_x0)
        return (1 - weight) * observed + weight * logistic_val

# Vektorisiere die Funktion, um sie auf den gesamten Jahresbereich anzuwenden
vec_manual_piecewise_blended = np.vectorize(manual_piecewise_blended)
manual_piecewise_values = vec_manual_piecewise_blended(all_years)

# --- Neue DataFrame mit vollständigem Jahresbereich und Prognosewerten ---
df_output = pd.DataFrame({
    year_col: all_years,
    'Logistic_auto': logistic_auto_values,
    'Manual_Piecewise_Blended': manual_piecewise_values
})

# --- Ausgabe der aktualisierten Datei ---
# output_file = "Prognosis-Datasource_1_updated.xlsx"
# df_output.to_excel(output_file, sheet, index=False)
# print(f"Neue Daten wurden in {output_file} gespeichert.")

# --- Plot ---
plt.figure(num="auto vs manual", figsize=(10, 6))
plt.scatter(years, values, color="black", label="Originaldaten")
if logistic_params is not None:
    plt.plot(all_years, logistic_auto_values, linestyle="--", color="blue", label="Logistic auto")
plt.plot(all_years, manual_piecewise_values, linestyle="--", color="red", label="Manuell (Piecewise mit Blending)")
plt.gcf().set_tight_layout(True)
plt.xlabel("Jahr")
plt.ylabel(value_col)
plt.legend()
plt.grid(True)
plt.show()
