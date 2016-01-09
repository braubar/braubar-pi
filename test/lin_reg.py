print(__doc__)


# Code source: Jaques Grobler
# License: BSD 3 clause


import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model

# Load the diabetes dataset
diabetes = datasets.load_diabetes()

data = [(1452263810951, '2016-01-08T15:39:42.066381', 47.06),
                (1452263810951, '2016-01-08T15:39:39.938612', 47.06),
                (1452263810951, '2016-01-08T15:39:37.818718', 47.06),
                (1452263810951, '2016-01-08T15:39:35.689863', 47.06),
                (1452263810951, '2016-01-08T15:39:31.419443', 47.06),
                (1452263810951, '2016-01-08T15:39:33.564566', 47.06),
                (1452263810951, '2016-01-08T15:39:29.293816', 47.06),
                (1452263810951, '2016-01-08T15:39:27.172160', 47.06),
                (1452263810951, '2016-01-08T15:39:25.057442', 47.06),
                (1452263810951, '2016-01-08T15:39:22.938337', 47.06),
                (1452263810951, '2016-01-08T15:39:20.822455', 47.12),
                (1452263810951, '2016-01-08T15:39:18.702429', 47.12),
                (1452263810951, '2016-01-08T15:39:16.585970', 47.12),
                (1452263810951, '2016-01-08T15:39:14.461290', 47.12),
                (1452263810951, '2016-01-08T15:39:12.345385', 47.12),
                (1452263810951, '2016-01-08T15:39:10.224860', 47.12),
                (1452263810951, '2016-01-08T15:39:08.094073', 47.12),
                (1452263810951, '2016-01-08T15:39:05.957633', 47.12),
                (1452263810951, '2016-01-08T15:39:03.830800', 47.12),
                (1452263810951, '2016-01-08T15:39:01.709895', 47.12),
                (1452263810951, '2016-01-08T15:38:59.572879', 47.12),
                (1452263810951, '2016-01-08T15:38:57.395704', 47.18),
                (1452263810951, '2016-01-08T15:38:55.269936', 47.18),
                (1452263810951, '2016-01-08T15:38:53.154337', 47.18),
                (1452263810951, '2016-01-08T15:38:51.030096', 47.18),
                (1452263810951, '2016-01-08T15:38:48.893877', 47.18),
                (1452263810951, '2016-01-08T15:38:46.774857', 47.18),
                (1452263810951, '2016-01-08T15:38:44.633620', 47.25)]


temp_y = [row[2] for row in data]

# Use only one feature
diabetes_X = diabetes.data[:, np.newaxis, 2]

# Split the data into training/testing sets
diabetes_X_train = diabetes_X[:-20]
diabetes_X_test = diabetes_X[-20:]

# Split the targets into training/testing sets
diabetes_y_train = diabetes.target[:-20]
diabetes_y_test = diabetes.target[-20:]

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(diabetes_X_train, diabetes_y_train)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((regr.predict(diabetes_X_test) - diabetes_y_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(diabetes_X_test, diabetes_y_test))

# Plot outputs
plt.scatter(diabetes_X_test, diabetes_y_test,  color='black')
plt.plot(diabetes_X_test, regr.predict(diabetes_X_test), color='blue',
         linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()
