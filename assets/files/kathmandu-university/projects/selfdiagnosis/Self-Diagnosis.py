
# coding: utf-8

# In[448]:


import numpy as np
import pandas as pd
import csv
from sklearn import datasets
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB


# In[449]:


pd.options.mode.chained_assignment = None
data=pd.read_csv("C:/Users/pc/Desktop/hepatitis_csv.csv")
data2=pd.read_csv("C:/Users/pc/Desktop/diabetes.csv")


# In[450]:


data=data.replace(r'\s+', np.nan, regex=True)

# True or False Transformation
def transform(x):
    return 1 if x else 0

# Mean Value Fill
def  Mean_ValFill(col_name,value):
    data[col_name].fillna(value,inplace=True)
    
# Scaling Data for equal weightage
def Scaling_data(dataset,col_name):
   
    Max_Val=max(dataset[col_name])
    Min_Val=min(dataset[col_name])
    
    for i in range(len(dataset)):
        dataset[col_name][i]=(dataset[col_name][i]-Min_Val)/(Max_Val-Min_Val)
        dataset[col_name][i]="{0:.4f}".format(dataset[col_name][i])
        
    return dataset[col_name]

# Sex Transformation
def trans_sex(x):
    if x=='male':
        return 1
    if x=='female':
        return 0
    
# Class Transformation  
def trans_class(x):
    if x=='live':
        return 1
    if x=='die':
        return 0
    


  
data["steroid"]=data["steroid"].apply(transform)
data["antivirals"]=data["antivirals"].apply(transform)
data["fatigue"]=data["fatigue"].apply(transform)
data["malaise"]=data["malaise"].apply(transform)
data["anorexia"]=data["anorexia"].apply(transform)
data["liver_big"]=data["liver_big"].apply(transform)
data["liver_firm"]=data["liver_firm"].apply(transform)
data["spleen_palpable"]=data["spleen_palpable"].apply(transform)
data["spiders"]=data["spiders"].apply(transform)
data["ascites"]=data["ascites"].apply(transform)
data["varices"]=data["varices"].apply(transform)
data["histology"]=data["histology"].apply(transform)




# In[451]:


# Mean Value Fill
Mean_ValFill("albumin",4.25)
Mean_ValFill("alk_phosphate",80)
Mean_ValFill("sgot",22.5)
Mean_ValFill("protime",12)

# Class Transformation
data["class"]=data["class"].apply(trans_class)

# Sex Transformation 
data["sex"]=data["sex"].apply(trans_sex)


# In[452]:



# Hepatitis Dataset    
# Bilirubin_Scaled=Scaling_data(data,"bilirubin")
# Alkaline_Scaled=Scaling_data(data,"alk_phosphate")
# Sgot_Scaled=Scaling_data(data,"sgot")
# Protime_Scaled=Scaling_data(data,"protime")
# Albumin_Scaled=Scaling_data(data,"albumin")
# Age_Scaled=Scaling_data(data,"age")

# Diabetes Dataset
# pregnancies_scaled=Scaling_data(data2,"Pregnancies")
# glucose_scaled=Scaling_data(data2,"Glucose")
# bloodpressure_scaled=Scaling_data(data2,"BloodPressure")
# skinthickness_scaled=Scaling_data(data2,"SkinThickness")
# insulin_scaled=Scaling_data(data2,"Insulin")
# bmi_scaled=Scaling_data(data2,"BMI")
# DPF_scaled=Scaling_data(data2,"DiabetesPedigreeFunction")
# age_scaled=Scaling_data(data2,"Age")

# writer = pd.ExcelWriter('C:/Users/pc/Desktop/output.xlsx')
# data.to_excel(writer,'Sheet1')
# writer.save()


# In[453]:


data


# In[454]:


data2


# In[455]:


target_data=data["class"]
target_data2=data2["Outcome"]
del data["class"]
del data2["Outcome"]
data=data.values
data2=data2.values
target_data=target_data.values
target_data2=target_data2.values


# In[459]:


model=GaussianNB()
model.fit(data,target_data)
expected=target_data
predicted=model.predict(data)
confusion_matrix=metrics.confusion_matrix(expected,predicted)
accuracy=(confusion_matrix[0][0]+confusion_matrix[1][1])/(len(data))

print(accuracy*100)
print(confusion_matrix)

# result=model.predict([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
# result


# In[463]:


model2=GaussianNB()
model2.fit(data2,target_data2)
expected2=target_data2
predicted2=model2.predict(data2)
confusion_matrix=metrics.confusion_matrix(expected2,predicted2)
accuracy2=(confusion_matrix[0][0]+confusion_matrix[1][1])/(len(data2))

print(accuracy2*100)
print(confusion_matrix)


# In[469]:



# count=0;
# for i in range(len(target_data)):
#     if (target_data[i]==1):
#         count=count+1;
# print(count)    

