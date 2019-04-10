import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import ExcelWriter
from pandas import ExcelFile
 
vaderdata = pd.read_csv(r"http://users.du.se/~h16wilwi/gik258/data/vaderdata.csv", sep=";", decimal=",")
# byt namn på kolumner till nåt lättare att jobba med
# Sätt tid till datetime
vaderdata['Tidpunkt'] = pd.to_datetime(vaderdata['Tidpunkt'])
 
# Ta endast datum
vaderdata['Tidpunkt'] = vaderdata['Tidpunkt'].dt.date
 
# Sätt tiden till index och till datetime
vaderdata = vaderdata.set_index("Tidpunkt")
vaderdata = vaderdata.set_index(pd.to_datetime(vaderdata.index))
 
vaderdata['Snow'] = np.where(vaderdata['Nedbtyp'] == 'Snö', 1, 0)
vaderdata['Sun'] = np.where(vaderdata['Nedbtyp'] == '-', 1, 0)
vaderdata['Rain'] = np.where(vaderdata['Nedbtyp'] == 'Regn', 1, 0)
vaderdata['Snowmix'] = np.where(vaderdata['Nedbtyp'] == 'SnöblandatRegn', 1, 0)

del vaderdata['Nedbtyp']
# Ta medelvärdet per dag
def groupMeans(columns):
    for i in range(len(columns)):
        vaderdata_mean = vaderdata.groupby('Tidpunkt').apply(lambda x: x.resample('1d')[''+columns[i]+''].agg(['mean']))
        vaderdata_mean = vaderdata_mean.reset_index(level=1, drop=True)
        print("Column: " + columns[i])
        #Sätt index tillbaka till kolumn
        vaderdata_mean.reset_index(level=0, inplace=True)
        print(vaderdata_mean)
        addMeanColumn(vaderdata_mean, columns[i]+"_mean")
 
#Läs in inSAR mätningar
molndal = pd.read_csv(r"http://users.du.se/~h16wilwi/gik258/data/railway.csv", sep = ';')

#Transponera data frame
molndal_trans = molndal.transpose()
molndal_trans.reset_index(level=0, inplace=True)
molndal_trans_pnt = molndal_trans.iloc[:7]

molndal_trans = molndal_trans.iloc[7:]
molndal_trans["index"] = pd.to_datetime(molndal_trans["index"])

#Endast datum from mölndal data settet
index_only = molndal_trans["index"]
index_only = pd.to_datetime(index_only)
index_only = index_only.to_frame()
index_only.columns = ["Tid"]
index_only = index_only.reset_index()
#index_only = pd.to_datetime(molndal_trans["Tid"])

def addMeanColumn(dataset, column_label):
    meanList = list()
    for j in range(len(dataset)):
        for i in range(len(index_only["Tid"])):
            if dataset["Tidpunkt"][j] == index_only["Tid"][i]:
                meanList.append(dataset["mean"][j])
               

    #Matcha de beräknade värden till mölndal data framen
    index_only.loc[:,''+column_label+''] = pd.Series(meanList)
    print(index_only)


def merge_datasets():
    molndal_trans.rename(columns={"index": "Tid"}, inplace=True) 
    dates =pd.merge(molndal_trans, index_only, on="Tid", how='outer')
    dates = dates.set_index("index")
    dates.rename(columns={"Tid": "index"}, inplace=True)
    result = pd.concat([molndal_trans_pnt,dates], keys=['PNT', 'Dates'], sort=False)
    result["TLuft_mean"].fillna("-", inplace = True)
    result["TYta_mean"].fillna("-", inplace = True)
    result["Daggp_mean"].fillna("-", inplace = True)
    result["Lufu_mean"].fillna("-", inplace = True)
    result["TYtaDaggp_mean"].fillna("-", inplace = True)
    print(result)

    # TODO: Remove NaN above mean values with fillna method 
    # Skriver till excel,
    newResultset = result.transpose()
    write_to_excel(newResultset)
    print(newResultset)
    
    #newResultset.to_csv('datasheet.csv', encoding='utf-8', sep=';', index=False)
    
def write_to_excel(result):
    writer = ExcelWriter('dataset-examensarbete.xlsx', engine='xlsxwriter')
    result.to_excel(writer, sheet_name="Blad1")
    writer.save()

if __name__ == '__main__':
    column_list = list()
    column_list.extend(["TLuft", "TYta", "Daggp", "Lufu", "Snow_mm","Rain_mm","Melted_mm", "TYtaDaggp", "Snow", "Sun", "Rain", "Snowmix"])
    
    print(vaderdata)
    groupMeans(column_list)
    print(index_only)
    merge_datasets()
    
   
 
