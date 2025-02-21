import numpy as np
import pandas as pd
import Prognosis_models as pg1 # bad style, but it is just working


#read the results of the models
data_logistic = pg1.logistic_predictions

# calculate the growth rates
growth_rate_logistic = np.diff(data_logistic) / data_logistic[:-1]

# Save the growth rates in a CSV file
growth_rates = pd.DataFrame(
    {
        "Year": pg1.future_years[1:],
        "Logistic": growth_rate_logistic,
    }
)
growth_rates.to_csv("growth_rates.csv", index=False)
print("Growth rates saved to 'growth_rates.csv'")

# plot the growth rates
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    plt.subplots(figsize=(10, 6), num=f"Growth rates up to {int(pg1.future_years[-1])}")
    plt.plot(pg1.future_years[1:], growth_rate_logistic, label="Logistic", color="blue")
    plt.title("Logistic Growth Model")
    plt.grid(True)
    plt.tight_layout()
    plt.gcf().set_tight_layout(True)
    # plt.title(f"Growth ratesup to {int(pg1.future_years[-1])}")
    plt.legend()
    plt.show()
    