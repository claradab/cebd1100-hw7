import argparse
import csv
import matplotlib.pyplot as plt
import os.path as op
import numpy as np
import statistics
from sklearn import datasets

#pip3 install scikit-learn --user

   

boston = datasets.load_boston()
print(dir(boston))
print(boston.feature_names)
print(boston.data.shape)
boston['MEDV']=boston.target
print(boston.target)
#Crime Rate and Home Values
#plt.hist(boston.data[:,0],label="Crime Rate", color="C0")
#Pupil-to-teacher Ratio and Home Values
x = np.array(boston.data[:,10])
y = np.array(boston.target)
print(len(y))
print(len(x))
plt.scatter(x,y,label="Pupil/Teacher Ratio", color="C5")
plt.xlabel("Pupil/Teacher Ratio")
plt.ylabel("Housing Prices")
coefs = np.polyfit(x, y, 2)

stepsize = np.abs((np.max(x) - np.min(x)) / 100)
new_xs = np.arange(np.min(x), np.max(x), stepsize)
ffit = np.polyval(coefs, new_xs)

# import pdb; pdb.set_trace()

plt.plot(new_xs,ffit)

# plt.plot(x)
# plt.show()

#Age and Proximity to Employment Centre

# plt.scatter(boston.data[:,6],boston.data[:,7])
plt.show()








