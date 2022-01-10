import bisect
import numpy as np
import sympy as sy
import math

polynomialfit = np.polynomial.polynomial.Polynomial.fit
"""
Polyfit(x, y, l, r)
x - A list of x-coords
y - A list of y-coords
Returns a dict with 3 items representing the line of best fit
polynomial - coefficients for the LOBF
determination - the coefficient of determination
points - a list of points to plot
"""
def polyfit(x, y, l, r):
    results = {}

    old_fit = -1
    cur_fit = 0
    n=1
    while old_fit < cur_fit and n <= min(len(x)-1,20):
        old_fit = cur_fit

        data = polynomialfit(x, y, n, [l,r])
        coeffs = data.convert().coef

        # Find r^2 to determine fit
        p = np.poly1d(coeffs)
        yhat = p(x)                        
        ybar = np.sum(y)/len(y)        
        ssreg = np.sum((yhat-ybar)**2)   
        sstot = np.sum((y - ybar)**2) 
        cur_fit = ssreg / sstot
        n += 1

    data = polynomialfit(x, y, n-1, [l,r])
    coeffs = data.convert().coef
    results['polynomial'] = coeffs
    results['determination'] = old_fit

    print(n-1)
    poly = np.poly1d(coeffs[::-1])
    nx = [_ for _ in range(l, r+1)]
    ny = poly(nx)

    points = []
    for i in range(len(nx)):
        # if l <= nx[i] <= r and d <= ny[i] <= u:
        points.append((nx[i], ny[i]))
    results['points'] = points
    return results

def arclength(l, r, coeffs):
    # Taking the derivative of the polynomial
    deriv = [coeffs[i]*i for i in range(1, len(coeffs))] 
    poly = np.poly1d(deriv[::-1])

    # print(deriv)
    # Arc length function
    def f(x):
        nx = x
        for i in range(len(nx)):
            # print(1+poly(nx[i])**2)
            nx[i] = math.sqrt(1+poly(nx[i])**2)
        return nx

    # Riemann Sum to approximate integration on the arc length function
    N = 10000
    dx = (r-l)/N
    x_midpoint = np.linspace(dx/2, r - dx/2, N)
    riemann_sum = np.sum(f(x_midpoint) * dx)

    return riemann_sum 