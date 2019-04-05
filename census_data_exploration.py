# Licence: CC-BY
# Description: This script applies different data analysis methods for descriptive
# statistics. It uses the data calculated for the census data blocks of NY city
# It uses the pandas library and sets up the data set for further analysis using
# Tensor Flow
#
# Authors:  Diego Pajarito

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load data file
blocks = pd.read_csv('data/data_census.csv')

# get a correlation matrix, also a nice view of the correlation matrix
correlation = blocks.corr()
#sns.pairplot(blocks)

# Here some test for particular scatter plots that show some interesting relationships
# plt.scatter(blocks['area_m2'], blocks['area_res'], marker='^')
# plt.scatter(blocks['area_m2'], blocks['area_com'], marker='o')
# plt.scatter(blocks['area_m2'], blocks['area_plaza'], marker='*')
# plt.scatter(blocks['area_m2'], blocks['area_park'], marker='+')
#
# plt.scatter(blocks['area_res'], blocks['area_com'], marker='o')
# plt.scatter(blocks['area_res'], blocks['area_park'], marker='+')
# plt.scatter(blocks['area_res'], blocks['area_plaza'], marker='*')

# plt.scatter(blocks['area_res'], blocks['dist_metro'], marker='.', alpha=0.3)
# plt.scatter(blocks['area_com'], blocks['dist_metro'], marker='.', alpha=0.3)

# Setting up the training and testing sets using sklearn
X = blocks[['area_m2', 'coord_x', 'coord_y', 'area_com', 'area_park', 'area_plaza', 'area_open', 'area_prkng',
            'closest_me', 'dist_metro', 'area_roadb']]
y = blocks['area_res']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101)

# Training or fitting the linear model
lm = LinearRegression()
lm.fit(X_train, y_train)

# Estimating the predictions
predictions = lm.predict(X_test)

# Now lets see the errors in predictions
plt.scatter(y_test, predictions, marker='.', alpha=0.3)

plt.show()
