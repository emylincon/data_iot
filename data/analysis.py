import operator

import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
dic = {}

fr = open('data.txt', 'r')
f1 = fr.readlines()
for i in f1:
    a = i.split()
    dic[a[0]] = a[1:]

fr.close()
mem = [float(i[0:-1]) for i in dic['mem'][1:-1]]
cpu = [float(i[0:-1]) for i in dic['cpu'][1:-1]]
store = [float(i[0:-1]) for i in dic['store'][1:-1]]
net = [float(i[0:-1]) for i in dic['net'][1:-1]]
print('mem: ', mem)
print('cpu: ', cpu)
print('store: ', store)
print('net: ', net)


def average(var):
    return np.mean(var)


def _min(var):
    return np.min(var)


def _max(var):
    return np.max(var)


def _median(var):
    return np.median(var)


def _stdev(var):
    return np.std(var)


def regression(dg, x_ax):
    x_ax = np.array(x_ax)
    y_ax = list(range(0, len(x_ax)))
    y_ax = np.array(y_ax)
    y = x_ax[:, np.newaxis]
    x = y_ax[:, np.newaxis]

    polynomial_features = PolynomialFeatures(degree=dg)
    x_poly = polynomial_features.fit_transform(x)

    model = LinearRegression()
    model.fit(x_poly, y)
    y_poly_pred = model.predict(x_poly)
    nt = np.array(len(y_ax)+1)
    new = polynomial_features.fit_transform(nt)
    next_sample = model.predict(new)
    print('Next sample prediction: ', next_sample)

    rmse = np.sqrt(mean_squared_error(y, y_poly_pred))

    print('Root Mean Square Error: ', rmse)

    plt.scatter(x, y, s=10)
    plt.scatter(nt, next_sample, s=10, color='r')
    # sort the values of x before line plot
    sort_axis = operator.itemgetter(0)
    sorted_zip = sorted(zip(x, y_poly_pred), key=sort_axis)
    x, y_poly_pred = zip(*sorted_zip)
    plt.plot(x, y_poly_pred, color='m')
    plt.show()