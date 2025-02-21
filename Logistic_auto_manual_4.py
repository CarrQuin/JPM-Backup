import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# --- Einstellungen ---
file_path = r"Installation.xlsx"  # Pfad zur Originaldatei
sheet = "Global Top5" #sheet name
data_cols = "A, I"                          # Spalten, z. B. A: Jahr, I: beobachtete Werte
manual_cutoff_year = 2023                   # Jahr, bis zu dem Originaldaten genutzt werden
transition_width = 1                        # Übergangsbreite (in Jahren) für das Blending

# Weitere Einstellungen
preset_year = 2035
end_year = 2050  # Ende der Prognose

# Parameter für den automatischen Fit
values_coeff_max = 10   # Multiplikator für K
growth_rate_min = 0.01  # untere Schranke für b
preset_year_max = 2040  # obere Schranke für x0

# Manuelle logistische Modellparameter
manual_K = 315
manual_b = 0.18
manual_x0 = 2033

# --- Funktion zur Berechnung der logistischen Wachstumskurve ---
def logistic_growth(x, K, b, x0):
    return K / (1 + np.exp(-b * (x - x0)))

# --- Daten einlesen ---
data = pd.read_excel(file_path, header=0, sheet_name=sheet, usecols=data_cols)
data.dropna(inplace=True)
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
        p0=[max(values) * 1, growth_rate_min, preset_year],
        bounds=([max(values) * 0.6, growth_rate_min, preset_year],
                [max(values) * 7.3, 1.5, preset_year_max]),
        maxfev=10000
    )
    print(f"Logistische Parameter (auto fit): K = {logistic_params[0]:.2f}, b = {logistic_params[1]:.5f}, x0 = {int(logistic_params[2])}")
except RuntimeError as e:
    print(f"Logistische Modellanpassung fehlgeschlagen: {e}")
    logistic_params = None

# --- Erzeuge einen vollständigen Jahresbereich ---
all_years = np.arange(min(years), end_year + 1)

# --- Definition der automatischen Piecewise-Blended-Funktion ---
# Hier wird sichergestellt, dass für x <= manual_cutoff_year der Wert exakt aus den Originaldaten (mittels Interpolation) kommt.
if logistic_params is not None:
    def auto_piecewise_blended(x):
        if x <= manual_cutoff_year:
            return np.interp(x, years, values)
        elif x > manual_cutoff_year + transition_width:
            return logistic_growth(x, *logistic_params)
        else:
            # Blending im Übergangsbereich
            weight = (x - manual_cutoff_year) / transition_width
            observed = np.interp(x, years, values)
            logistic_val = logistic_growth(x, *logistic_params)
            return (1 - weight) * observed + weight * logistic_val

    vec_auto_piecewise = np.vectorize(auto_piecewise_blended)
    auto_piecewise_values = vec_auto_piecewise(all_years)
else:
    # Falls der Fit fehlschlägt, nutzen wir für die automatische Kurve die Originaldaten
    auto_piecewise_values = np.interp(all_years, years, values)

# --- Definition der manuellen Piecewise-Blended-Funktion ---
def manual_piecewise_blended(x):
    if x <= manual_cutoff_year:
        # Exakte Übernahme der Originaldaten (bei fehlendem exaktem x erfolgt Interpolation)
        return np.interp(x, years, values)
    elif x > manual_cutoff_year + transition_width:
        return logistic_growth(x, manual_K, manual_b, manual_x0)
    else:
        # Blending: Gewicht steigt linear von 0 bis 1 im Übergangsbereich
        weight = (x - manual_cutoff_year) / transition_width
        observed = np.interp(x, years, values)
        logistic_val = logistic_growth(x, manual_K, manual_b, manual_x0)
        return (1 - weight) * observed + weight * logistic_val

vec_manual_piecewise = np.vectorize(manual_piecewise_blended)
manual_piecewise_values = vec_manual_piecewise(all_years)

# --- Neue DataFrame mit vollständigem Jahresbereich und Prognosewerten ---
df_output = pd.DataFrame({
    year_col: all_years,
    'Auto_Piecewise_Blended': auto_piecewise_values,
    'Manual_Piecewise_Blended': manual_piecewise_values
})

# --- Ausgabe der aktualisierten Datei ---
output_file = f"{data.columns[1]}.xlsx"
df_output.to_excel(output_file, index=False)
print(f"Neue Daten wurden in {output_file} gespeichert.")

# --- Plot ---
plt.figure(num="auto vs manual", figsize=(10, 6))
plt.scatter(years, values, color="black", label="Originaldaten")
plt.plot(all_years, auto_piecewise_values, linestyle="--", color="blue", label="Worstcase scenario (auto)")
plt.plot(all_years, manual_piecewise_values, linestyle="--", color="red", label="Bestcase scenario (manual)")
plt.gcf().set_tight_layout(True)
plt.xlabel("Jahr")
plt.ylabel(value_col)
plt.legend()
plt.grid(True)
plt.show()
