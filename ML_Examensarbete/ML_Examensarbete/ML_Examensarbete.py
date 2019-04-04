
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import ExcelWriter
from pandas import ExcelFile
 
vaderdata = pd.read_csv(r"http://users.du.se/~h16wilwi/gik258/data/vaderdata.csv", sep=";", decimal=",")
#byt namn på kolumner till nåt lättare att jobba med
#Sätt tid till datetime
vaderdata['Tidpunkt'] = pd.to_datetime(vaderdata['Tidpunkt'])
 
#Ta endast datum
vaderdata['Tidpunkt'] = vaderdata['Tidpunkt'].dt.date
 
#Sätt tiden till index och till datetime
vaderdata = vaderdata.set_index("Tidpunkt")
vaderdata = vaderdata.set_index(pd.to_datetime(vaderdata.index))
 
vaderdata['Snow'] = np.where(vaderdata['Nedbtyp'] == 'Snö', '1', '0')
vaderdata['Sun'] = np.where(vaderdata['Nedbtyp'] == '-', '1', '0')
vaderdata['Rain'] = np.where(vaderdata['Nedbtyp'] == 'Regn', '1', '0')
vaderdata['Snowmix'] = np.where(vaderdata['Nedbtyp'] == 'SnöblandatRegn', '1', '0')

del vaderdata['Nedbtyp']



#Ta medelvärdet per dag
vaderdata_mean = vaderdata.groupby('Tidpunkt').apply(lambda x: x.resample('1d')['TLuft'].agg(['mean']))
print(vaderdata_mean)

#vaderdata_tluft_mean = vaderdata_tluft.groupby('Tidpunkt').apply(lambda x: x.resample('1d')['Tluft'].agg(['mean','count']))
vaderdata_mean = vaderdata_mean.reset_index(level=1, drop=True)
 
#Sätt index tillbaka till kolumn
vaderdata_mean.reset_index(level=0, inplace=True)
 
print(vaderdata_mean)
 
#Läs in inSAR mätningar
molndal = pd.read_csv(r"http://users.du.se/~h16wilwi/gik258/data/railway.csv", sep = ';')
 
#Transponera data frame
molndal_trans = molndal.transpose()
molndal_trans.reset_index(level=0, inplace=True)
molndal_trans = molndal_trans.iloc[7:]
 
#Endast datum from mölndal data settet
index_only = molndal_trans["index"]
index_only = pd.to_datetime(index_only)
index_only = index_only.to_frame()
index_only.columns = ["Tid"]
index_only = index_only.reset_index()
#index_only = pd.to_datetime(molndal_trans["Tid"])
 
print(index_only)
luft = list()
 
for j in range(len(vaderdata_mean)):
    for i in range(len(index_only["Tid"])):
        print(i)
        if vaderdata_mean["Tidpunkt"][j] == index_only["Tid"][i]:
            print(vaderdata_mean["Tidpunkt"][j])
            print(i)
            luft.append(vaderdata_mean["mean"][j])
 
 
#Justera för värden som inte kommer med (kontrollera längden t.ex.)
 
#Matcha de beräknade värden till mölndal data framen
index_only.loc[:,'TestMeanLuft'] = pd.Series(luft)
 
print(index_only)
 
#writer = ExcelWriter('.csv')
#index_only.to_excel(writer)
#writer.save()