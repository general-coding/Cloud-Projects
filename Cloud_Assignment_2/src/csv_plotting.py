'''
Created on Feb 26, 2015

@author: puneeth
'''

import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt('all_month.csv', skip_header=1)
plt.plot(data)