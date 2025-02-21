"""
Date: 29.01.2025
Description: This module contains a class for the mixed model of growth and cycle. 
                It can be used to fit the model to data and make predictions with some kind of periodicity.
Author: Kaiyu Qian
"""
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

class GrowthCycleModel:

    def __init__(self):
        self.params = None
        self.covariance = None
        
    def model_function(self, t, L, k, t0, A, T, phi, w):
        """
        Mixed model of growth and cycle
        Parameters:
        L: Saturation value
        k: Growth rate
        t0: Midpoint of growth
        A: Amplitude of cycle
        T: Period of cycle
        phi: Phase of cycle
        w: Weight parameter of cycle
        """
        # Logistic growth model
        growth = L / (1 + np.exp(-k * (t - t0)))
        
        # Cycle model
        current_ratio = growth / L
        max_available_amplitude = np.minimum(growth, L - growth)
        amplitude_factor = current_ratio ** w
        actual_amplitude = np.minimum(A * L, max_available_amplitude)
        cycle = actual_amplitude * amplitude_factor * np.sin(2 * np.pi * t / T + phi)
        
        return growth + cycle
    
    def fit(self, t_data, y_data, p0=None):
        """
        Fit the mixed growth-cycle model to the data
        Parameters:
        t_data: Time points
        y_data: Values
        p0: Initial parameters
        fixed_params: Fixed parameters
        """
        if p0 is None:
            # Use some default values for initial parameters
            L = np.max(y_data) * 0.5
            k = 0.01 
            t0 = np.mean(t_data) - 1 
            A = 0.01
            T = 53 
            phi = 0 
            w = 1 
            p0 = [L, k, t0, A, T, phi, w]
        
        # Fit the model to the data
        self.params, self.covariance = curve_fit(
            self.model_function, t_data, y_data,
            p0=p0,
            bounds=([0, 0, min(t_data), 0, 0, -np.pi, 0],
                    [np.inf, np.inf, max(t_data) + 15, 1, np.inf, np.pi, np.inf]),
            maxfev=10000
        )
        
        return self
    
    def adjust_parameters(self, **kwargs):
        """
        Adjust the model parameters
        Example:
        model.adjust_parameters(T=4, A=0.1, w=3)
        """
        if self.params is None:
            raise ValueError("The model has not been fitted yet")
        
        param_names = ['L', 'k', 't0', 'A', 'T', 'phi', 'w']
        for name, value in kwargs.items():
            if name in param_names:
                idx = param_names.index(name)
                self.params[idx] = value
            else:
                raise ValueError(f"Unknown Parameter: {name}")
    
    def predict(self, t):
        """ Predict using the recent parameters """
        if self.params is None:
            raise ValueError("The model has not been fitted yet")
        return self.model_function(t, *self.params)
    
    def plot_fit_and_prediction(self, t_data, y_data, t_future=None, show_components=True):
        """
        Plot the fitting and prediction results
        Parameters:
        t_future: Time points for future prediction
        show_components: Whether to show the growth and cycle components
        """
        if t_future is None:
            t_future = np.linspace(min(t_data), max(t_data) + 10, 1000)
        else:
            t_future = np.linspace(min(t_data), t_future + 1, 1000)
            
        # Print the model parameters and R2 score
        y_fitted = self.predict(t_data)
        r2 = r2_score(y_data, y_fitted)
        print("\nParemeter values:")
        print(f"Saturation value (L): {self.params[0]:.2f}")
        print(f"Growth rate (k): {self.params[1]:.4f}")
        print(f"Midpoint of growth (t0): {self.params[2]:.2f}")
        print(f"Amplitude of cycle (A): {self.params[3]:.4f}")
        print(f"Period of cycle (T): {self.params[4]:.2f}")
        print(f"Phase of cycle (phi): {self.params[5]:.2f}")
        print(f"Weight parameter of cycle (w): {self.params[6]:.2f}")
        print(f"R2: {r2:.4f}")
        
        plt.figure(figsize=(10, 6))
        plt.scatter(t_data, y_data, color='blue', label='Actual data')
        y_pred = self.predict(t_future)
        plt.plot(t_future, y_pred, 'r-', label='Predicted data')
        
        if show_components:
            # Plot the growth and cycle components
            growth = self.params[0] / (1 + np.exp(-self.params[1] * (t_future - self.params[2])))
            plt.plot(t_future, growth, 'g--', label='Trend component')
            
            # Cycle component
            current_ratio = growth / self.params[0]
            amplitude_factor = current_ratio ** self.params[6]
            envelope_up = growth + self.params[3] * amplitude_factor
            envelope_down = growth - self.params[3] * amplitude_factor
            plt.fill_between(t_future, envelope_down, envelope_up, alpha=0.2, color='gray',
                           label='Periodic cycle')
        
        # plt.xlabel('Year')
        # plt.ylabel('Value')
        plt.title(f'The prognoses of the mixed model up to {int(max(t_future)-1)}')
        plt.gcf().set_tight_layout(True)
        plt.legend()
        plt.grid(True)
        plt.show()
        
if __name__ == "__main__":
    import pandas as pd
    data = pd.read_excel(r"Prognosis-Datasource.xlsx", header=0, usecols="A, B")
    data.dropna( inplace=True)
    years = np.array(data.iloc[:,0].astype(int).tolist())
    values = np.array(data.iloc[:,1].astype(float).tolist())
    
    model = GrowthCycleModel()
    model.fit(years, values)
    model.adjust_parameters(T=15,L=1100, A=0.6, w=3)
    model.plot_fit_and_prediction(years, values, t_future=2050)