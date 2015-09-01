from scipy.optimize import curve_fit
import numpy as np


def chisqr(y, ymod, sigma=None):
    if sigma == None:
        sigma = np.zeros(len(y)) + 1.0
    chi2 = sum(((y - ymod) / sigma) ** 2)
    return chi2


def degrees_of_freedom(y, params):
    return len(y) - len(params)


def fit_func(func, x, y, sigma=None):
    """
    uses curve_fit to fit a function to a set of data, then also calculates the chi2 and numbers of degrees of freedom
    dof
    func is the function definition according to the curve_fit specification
    func should be of the form f(x,params) where x is the independent variable and params the parameter array
    """
    popt, pcov = curve_fit(func, x, y, sigma=sigma)
    ymod = func(x, *popt)  # calculate the function values using the optimized parameters popt
    chi2 = chisqr(y, ymod, sigma=sigma)
    dof = degrees_of_freedom(y, popt)
    return popt, pcov, chi2, dof
