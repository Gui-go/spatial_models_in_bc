
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression




data = pd.read_csv('data/bc_imoveis_filtered_d20201115.csv')

data.columns
data['price']
data['area']
x = np.array(data['area']).reshape((-1, 1))
y = np.array(data['price'])
model = LinearRegression()
model.fit(x, y)
r_sq = model.score(x, y)

x = np.array([5, 15, 25, 35, 45, 55]).reshape((-1, 1))
y = np.array([5, 20, 14, 32, 22, 38])

model = LinearRegression()
model.fit(x, y)
r_sq = model.score(x, y)
print('coefficient of determination:', r_sq)
print('intercept:', model.intercept_)
print('slope:', model.coef_)
y_pred = model.predict(x)
print('predicted response:', y_pred, sep='\n')