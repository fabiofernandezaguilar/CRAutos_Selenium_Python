from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re
import matplotlib
import matplotlib.pyplot as plt
#%matplotlib inline
from scipy import stats
import glob

import os;
os.environ["PATH"] += os.pathsep + r''
driver = webdriver.Chrome()
url = 'http://crautos.com/rautosusados/'
driver.get(url)
driver.find_element_by_xpath('/html/body/section[2]/div/div[5]/table/tbody/tr/td/div/form/div[2]/table/tbody/tr[8]/td/input').click()

# empty = pd.DataFrame(None)

a = []
begin = 0
end = 5
for n in range(begin,end):
    try:
        print(n)
        #driver.find_element_by_xpath('/html/body/section[2]/div/div/div[1]/div[1]/div[1]/div[3]/ul/li['+str(n+1)+']/a').click()
        for i in range(1,20):
            try:
                m = driver.find_element_by_xpath('/html/body/section[2]/div/div/div[1]/div[1]/div[1]/form/div['+str(i)+']/a/div[1]').text
                for n in range(1):
                    try:
                        p = driver.find_element_by_xpath('/html/body/section[2]/div/div/div[1]/div[1]/div[1]/form/div['+str(i)+']/a/div[2]/div[1]').text
                    except:
                        p = driver.find_element_by_xpath('/html/body/section[2]/div/div/div[1]/div[1]/div[1]/form/div['+str(i)+']/a/div[4]/div[1]').text
                print(m, p)
                a.append({'model': m, 'price': p})
            except:
                print(i)
                continue
        if driver.find_element_by_xpath('/html/body/section[2]/div/div/div[1]/div[1]/div[1]/div[3]/ul/li[1]/a').text == '1':
            driver.find_element_by_xpath('/html/body/section[2]/div/div/div[1]/div[1]/div[1]/div[3]/ul/li[18]/a').click()
        else:
            driver.find_element_by_xpath('/html/body/section[2]/div/div/div[1]/div[1]/div[1]/div[3]/ul/li[19]/a').click()
    except:
        continue
empty = pd.concat([empty, pd.DataFrame(a)])

# # empty = pd.concat([empty, pd.DataFrame(a)])
# empty.to_csv('guardar.csv')

empty = pd.read_csv('empty_all.csv')

empty

len(empty)


def year(x):
    z = x.split()
    year = []
    maker = []
    model = []
    for ze in z:
        
        try:
            ye = ze[1]
            y = 0
            if (ye.isdigit() & (len(year) == 0)):
                year.append(ze)
            elif ((len(maker) == 0) & (len(year) == 1)):
                maker.append(ze)
            elif (ye.islower()):
                maker.append(ze)
            else:
                model.append(ze)
        except:
            continue
    return int(year[0])

def maker(x):
    z = x.split()
    year = []
    maker = []
    model = []
    for ze in z:
        
        try:
            ye = ze[1]
            y = 0
            if (ye.isdigit() & (len(year) == 0)):
                year.append(ze)
            elif ((len(maker) == 0) & (len(year) == 1)):
                maker.append(ze)
            elif (ye.islower()):
                maker.append(ze)
            else:
                model.append(ze)
        except:
            continue
    return str(maker)

def model(x):
    z = x.split()
    year = []
    maker = []
    model = []
    for ze in z:
        
        try:
            ye = ze[1]
            if (ye.isdigit() & (len(year) == 0)):
                year.append(ze)
            elif ((len(maker) == 0) & (len(year) == 1)):
                maker.append(ze)
            elif (ye.islower()):
                maker.append(ze)
            else:
                model.append(ze)
        except:
            model.append(ze)
            continue
    return str(model)

def value(x):
    y = str(x).replace('¢','').replace(',','')
    return int(y)
def top(x):
    if x in top_m:
        return 'top'
    else:
        return 'tail'


df = empty.copy()

df.head().dtypes

df['year'] = df.model.apply(year)
df['maker'] = df.model.apply(maker)
df['model2'] = df.model.apply(model)
df['value'] = df.price.apply(value).astype(int)
df['top'] = df.model2.apply(top)
df = df[(df.value< 70000000) & (df.year < 2018)]

top_m = df.groupby([ 'model2']).size().sort_values(ascending=False)[0:400].index

import matplotlib.pyplot as plt
tt = df[df.top == 'top'].pivot_table(index=['maker', 'model2'], columns='year', aggfunc='median', values= 'value')
tt.T.plot(legend=False, figsize=(18,6))

from pylab import * 

funcs = []
for i in range(50):
    try:
        data = tt.T.iloc[:,i]
        data = pd.DataFrame(data)
        data = data[data.iloc[:,0].isnull()==False]
        x = data.index
        y = data.iloc[:,0].values
        mm = data.columns[0]
        maker = mm[0]
        model = mm[1]
        r = stats.pearsonr(x, y)[0]
        m,b = polyfit(x, y, 1) 
        plot(x, y, 'yo', x, m*x+b, '--k') 
        show() 
        print(m,b)
        if (m > 0) &  (len(data) > 2):
            funcs.append({'maker':maker, 'model':model, 'm':m, 'b':b, 'r': r})
    except:
        continue


modelos = pd.DataFrame(funcs)
modelos.to_csv('modelos.csv', index= False)
modelos
