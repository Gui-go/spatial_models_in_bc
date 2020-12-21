import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('data/bc_imoveis_filtered_d20201115.csv')

# Treat the data
data = data.iloc[:, 1:]
data = data.drop(['url', 'address', 'title', 'date'], axis=1)
data = data.replace(['--'],0)
data = data.apply(pd.to_numeric)
y = data['price'].values
x = data.drop(['price'], axis=1)
xs = data.drop(['price'], axis=1).values
xs_names = list(x.columns)

# Devide between train and test
y_train_data, y_test_data, xs_train_data, xs_test_data = train_test_split(
    y, xs, test_size = 0.002, random_state = 42
)

# Model the data
regressor = RandomForestRegressor(n_estimators = 10, random_state = 42)
regressor.fit(xs_train_data, y_train_data)
predictions_all = regressor.predict(xs_test_data)

# Compute the performance metrics
errors = abs(predictions_all - y_test_data)
print('Average model error:', round(np.mean(errors), 2))
mape = 100 * (errors / y_test_data)
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')

# Get numerical feature importances
importances = list(regressor.feature_importances_)
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(xs_names, importances)]
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
[print('Variable: {} Importance: {}'.format(*pair)) for pair in feature_importances]

# Plot feature importance 
plt.style.use('fivethirtyeight')
x_values = list(range(len(importances)))
plt.bar(x_values, importances, orientation = 'vertical', color = 'r', edgecolor = 'k', linewidth = 1.2)
plt.xticks(x_values, xs_names, rotation='horizontal')
plt.ylabel('Importance'); plt.xlabel('Variable'); plt.title('Variable Importances')
# plt.show()

# Cumulative feature importance sorted from most to least important
sorted_importances = [importance[1] for importance in feature_importances]
sorted_features = [importance[0] for importance in feature_importances]
cumulative_importances = np.cumsum(sorted_importances)
plt.plot(x_values, cumulative_importances, 'g-')
plt.hlines(y = 0.95, xmin=0, xmax=len(sorted_importances), color = 'r', linestyles = 'dashed')
plt.xticks(x_values, sorted_features, rotation = 'vertical')
plt.xlabel('Variable'); plt.ylabel('Cumulative Importance'); plt.title('Cumulative Importances')
# plt.show()

# Extract the most important features
important_feature_names = [feature[0] for feature in feature_importances[0:2]]
important_indices = [xs_names.index(feature) for feature in important_feature_names]
important_train_features = xs_train_data[:, important_indices]
important_test_features = xs_test_data[:, important_indices]

# Train the model with the important features
regressor.fit(important_train_features, y_train_data)
predictions_sub = regressor.predict(important_test_features)

# Compute the performance metrics
errors = abs(predictions_sub - y_test_data)
print('Average absolute error:', round(np.mean(errors), 2))
mape = 100 * (errors / y_test_data)
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')

# Compute the difference between the models
all_accuracy =  100 * (1- np.mean(abs(predictions_all - y_test_data) / y_test_data))
reduced_accuracy = 100 * (1- np.mean(abs(predictions_sub - y_test_data) / y_test_data))
comparison = pd.DataFrame({'features': ['all (4)', 'reduced (2)'], 
                           'accuracy': [round(all_accuracy, 2), round(reduced_accuracy, 2)]})
comparison[['features', 'accuracy']]
relative_accuracy_increase = abs(100 * (all_accuracy - reduced_accuracy) / all_accuracy)
print('Relative increase in accuracy:', round(relative_accuracy_increase, 3), '%.')


# Help
# https://github.com/WillKoehrsen/Data-Analysis/blob/master/random_forest_explained/Improving%20Random%20Forest%20Part%201.ipynb