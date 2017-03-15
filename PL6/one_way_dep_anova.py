"""
Repeated measures One-Way ANOVA
From Andy Field, "Discovering Statistics using SPSS (3rd ed.), chapter 13
March 2016
Ernesto Costa
"""

import pandas as pd
import numpy as np
from scipy import stats

def one_way_dep_anova(data_frame):
   """
   Repeated measures one way ANOVA
   @data_frame: a  pandas DataFrame with the data
   """
   grand_mean = data_frame.values.mean()
   #grand_variance = data_frame.values.var(ddof=1)
   
   row_means = data_frame.mean(axis=1)
   column_means = data_frame.mean(axis=0)
   
   # n = number of subjects; k = number of conditions/treatments
   n,k = len(data_frame.axes[0]), len(data_frame.axes[1])
   # total number of measurements
   N = data_frame.size # or n * k
   
   # degrees of freedom
   df_total = N - 1
   df_between = k - 1
   df_subject = n - 1
   df_within = df_total - df_between
   df_error = df_within - df_subject   
      
   # compute variances
   SS_between = sum(n*[(m - grand_mean)**2 for m in column_means])   
   SS_within = sum(sum([(data_frame[col] - column_means[i])**2 for i,col in enumerate(data_frame)]))  
   SS_subject = sum(k* [(m - grand_mean)**2 for m in row_means])  
   SS_error = SS_within - SS_subject  
   #SS_total = SS_between + SS_within
   
   # Compute Averages
   MS_between = SS_between/df_between
   MS_error = SS_error/df_error
   MS_subject = SS_subject/df_subject
   
   # F Statistics
   F = MS_between/MS_error
   # p-value
   p_value = stats.f.sf(F,df_between,df_error)   
   
   return (F, p_value)


# Auxiliary
def display(data_frame,f,p_val):
   print('Data: \n', data_frame,'\n')
   print('F-ratio: %6.4f\n'%f)
   print('p_value: %6.4f\n'%p_val)
   if p_val < 0.05:
      print('Reject the null hypothesis.[95%]')
   else:
      print('Cannot reject the null hypothesis. [95%]')


# Examples            
def main_1():
   # example data (Andy Field (3rd ed), pg. 464
   insect = [8,9,6,5,8,7,10,12]
   kangaroo = [7,5,2,3,4,5,2,6]
   fish = [1,2,3,1,5,6,7,8]
   grub = [6,5,8,9,8,7,2,1]
   
   data_frame = pd.DataFrame({ "Insect":insect, "Kangaroo":kangaroo, "Fish":fish, "Grub": grub}) 
   f,p = one_way_dep_anova(data_frame)
   display(data_frame,f,p)  
   
def main_2():
   # exemplo de https://statistics.laerd.com/statistical-guides/repeated-measures-anova-statistical-guide-2.php
   X1 = [45,42,36,39,51,44]
   X2 = [50,42,41,35,55,49]
   X3 = [55,45,43,40,59,56]
   
   data_frame = pd.DataFrame({"X1":X1, "X2":X2, "X3":X3}) 
   f,p = one_way_dep_anova(data_frame)
   display(data_frame,f,p) 
   
def main_3():
   # exemplo de http://pythonpsychologist.tumblr.com/post/139246503057/repeated-measures-anova-using-python
   X1 = [6,4,5,1,0,2]
   X2 = [8,5,5,2,1,3]
   X3 = [10,6,5,3,2,4]
   
   data_frame = pd.DataFrame({ "X1":X1, "X2":X2, "X3":X3})
   f,p = one_way_dep_anova(data_frame)
   display(data_frame,f,p) 
           
if __name__ == '__main__':
   main_1()
   main_2()
   main_3()
   



   