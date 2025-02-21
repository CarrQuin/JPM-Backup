"""
Date: 11.02.2025
Description: This module contains functions for calculating confidence intervals.
Author: Kaiyu Qian
"""
import numpy as np
from scipy import stats, optimize

def covariance_params(covariance_level, years, model_params, covariance, z_t):
    """
    Parameters:
        covariance_level: int, in precentage[0, 100]
        years: list, 
        model_params: array_like,
        covariance: array_like,
        z_t: str, "z" or "t"
    Return:
        array_like, array_like
    """
    alpha = 1 - covariance_level / 100
    perr = np.sqrt(np.diag(covariance))
    if z_t == "z":
        z_value = stats.norm.ppf(0.5 + alpha / 2)
        z_confidence = z_value * perr
        lower_z_params = model_params - z_confidence
        upper_z_params = model_params + z_confidence
        return lower_z_params, upper_z_params
    elif z_t == "t":
        t_value = stats.t.ppf(0.5 + alpha / 2, len(years) - 1)
        t_confidence = t_value * perr
        lower_t_params = model_params - t_confidence
        upper_t_params = model_params + t_confidence
        return lower_t_params, upper_t_params
    else:
        return None, None

def covariance_matrix(model, x, y, params, eps=1e-9):
    """
    Parameters:
        model: model function
        x: array_like
        y: array_like
        params: list or array_like
        eps: float
    Return:
        pcov: 2-D array
    """
    N = len(x)
    M = len(params)
    J = np.zeros((N, M))
    for i in range(N):
        J[i,:] = optimize.approx_fprime(params, lambda p: model(x[i], *p), eps)
        
    residuals = y - model(x, *params)
    MSE = np.sum(residuals**2) / (N - M)
    try:
        pcov = MSE * np.linalg.inv(J.T @ J)
    except np.linalg.LinAlgError:
        pcov = np.full((M, M), np.nan)
    return pcov
