import bisect
import numpy as np

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
    while old_fit < cur_fit and n <= 20:
        old_fit = cur_fit

        coeffs = np.polyfit(x, y, n)

        # Find r^2 to determine fit
        p = np.poly1d(coeffs)
        yhat = p(x)                        
        ybar = np.sum(y)/len(y)        
        ssreg = np.sum((yhat-ybar)**2)   
        sstot = np.sum((y - ybar)**2) 
        cur_fit = ssreg / sstot
        n += 1

    coeffs = np.polyfit(x, y, n-1)
    results['polynomial'] = coeffs.tolist()
    results['determination'] = old_fit

    print(n-1)
    poly = np.poly1d(coeffs)
    nx = [_ for _ in range(l, r+1)]
    ny = poly(nx)

    points = []
    for i in range(len(nx)):
        # if l <= nx[i] <= r and d <= ny[i] <= u:
        points.append((nx[i], ny[i]))
    results['points'] = points
    return results