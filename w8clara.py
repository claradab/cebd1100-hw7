import argparse
import csv
import matplotlib.pyplot as plt
import os.path as op
import numpy as np
import pandas as pd
from sklearn import datasets
import seaborn as sns

#pip3 install scikit-learn --user

def outlier(y,outlier_sensitivity):
    q75, q25 = np.percentile(y, [75 ,25])
    iqr = q75 - q25
    max_suspected = outlier_sensitivity*iqr + q75
    min_suspected = q25 - outlier_sensitivity*iqr
    outliers = []
    for i in y:
        if (i < min_suspected) or (i > max_suspected):
            outliers.append(i)
    return np.array(outliers)
       
    
def scattergraph(x,y,xtitle,ytitle,graphtitle,outlier_treatment,outlier_sensitivity):
    o = outlier(y,outlier_sensitivity)
    for i,point in enumerate(x):
        if y[i] in o:
            if outlier_treatment == 'color':
                plt.scatter(point,y[i],color="#f7cac9")
            elif outlier_treatment == 'shape':
                plt.scatter(point,y[i],color="#92a8d1",marker="^")
            else: #default to size
                plt.scatter(point,y[i],s=50,color="#92a8d1")
        else:
            plt.scatter(point,y[i],color="#92a8d1",marker='.')
    plt.xlabel(xtitle,size='small', weight='bold',color='#034f84')
    plt.ylabel(ytitle,size='small',weight='bold',color='#034f84')
    plt.title(graphtitle, weight='bold',color='#034f84')
    plt.xticks(size="small",color='#034f84')
    plt.yticks(size="small",color='#034f84')
    coefs = np.polyfit(x, y, 2)
    stepsize = np.abs((np.max(x) - np.min(x)) / 100)
    new_xs = np.arange(np.min(x), np.max(x), stepsize)
    ffit = np.polyval(coefs, new_xs)
    plt.plot(new_xs,ffit,color="#f7786b")
    plt.show()   

   
# Load the data and learn about it

boston = datasets.load_boston()
# print(dir(boston))
# print(boston.feature_names)
# print(boston.data.shape)
boston['MEDV']=boston.target
#print(boston.target)


#Plot the distribution of Home Values

sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.set_color_codes()
sns.distplot(boston['MEDV'], bins=30, color='#9999ff')
plt.xticks(size="small",color='#00004d')
plt.yticks(size="small",color='#00004d')
plt.title("Distribution of Home Values", weight='bold', color='#00004d')
plt.show()

# Plot Number of Rooms vs Home Values

x = np.array(boston.data[:,5])
y = np.array(boston.target)
xtitle = "Number of Rooms"
ytitle = "Median Value of Owner-Occupied Homes ($1000's)"
graphtitle = "Effect of Number of Rooms on Home Values"
outlier_treatment = 'color'
outlier_sensitivity = 1.4
scattergraph(x,y,xtitle,ytitle,graphtitle,outlier_treatment,outlier_sensitivity)

#Plot pupil-to-teacher Ratio vs Home Values

x = np.array(boston.data[:,10])
y = np.array(boston.target)
xtitle = "Pupil/Teacher Ratio"
ytitle = "Median value of owner-occupied homes ($1000's)"
graphtitle = "Effect of Pupil/Teacher Ratio on Home Values"
outlier_treatment = 'shape'
outlier_sensitivity = 1.2
scattergraph(x,y,xtitle,ytitle,graphtitle,outlier_treatment,outlier_sensitivity)

#Plot Age and Proximity to Employment Centre

x = np.array(boston.data[:,7])
y = np.array(boston.data[:,6])
xtitle="Distances to Employment Centres"
ytitle="Proportion of Owner-Occupied Units Built Prior to 1940"
graphtitle="Effect of Distance to Employment Centres on Home Ages"
outlier_treatment = 'size'
outlier_sensitivity = 0.5
scattergraph(x,y,xtitle,ytitle,graphtitle,outlier_treatment,outlier_sensitivity)








