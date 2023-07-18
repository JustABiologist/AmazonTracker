import json 
import matplotlib.pyplot as plt
import matplotlib.dates as md
import pandas as pd
import numpy as np 
from datetime import datetime
import os

def readJSONS(json_dir):
    '''Takes a directory of jsons and reads them all in, returns a list of dicts.'''
    jsons = os.listdir(json_dir)
    dics = []
    filenames = []
    for file in jsons:
        with open(json_dir+file) as jfile:
            jdict = json.load(jfile)
            dics.append(jdict)
            for filename in jdict.keys():
                if filename not in filenames:
                    filenames.append(filename)
    return dics, filenames

def flatten_concatenation(matrix):
    flat_list = []
    for row in matrix:
        flat_list += row
    return flat_list

def makeDataframe(json_dicts, filename):
    '''Takes in list of all JSONS in the folder in dict format and returns a list of all the datapoints pertaining to a certain excel file'''
    dicDF = [fileDic[filename] for fileDic in json_dicts]
    links = [list(dic.keys()) for dic in dicDF]
    links = list(set(flatten_concatenation(links)))
    values = []
    for dic in dicDF:
        for link in links:
            values.append(dic[link])
    values=flatten_concatenation(values)
    listDF=[]
    for j in values:
        row = [j[0], j[3], filename, j[2], j[1]]
        listDF.append(row)
    df = pd.DataFrame(listDF, columns=["Links", "Timestamp", "Ursprungsexcel", "Preis", "Stückzahl"])
    df['Timestamp'] = pd.to_datetime(df["Timestamp"], format='%d_%m_%Y %H')
    df_unique = df["Links"].unique().squeeze().tolist()
    df_l = [df[df["Links"] == unique] for unique in df_unique]
    return df_l

def makePlot(dfs):
    fontdict_xaxis = {'fontsize': 4}
    
    xmfd = md.DateFormatter('%d-%m-%y %H Uhr')
    fig, axs = plt.subplots(2,2, sharex=False, sharey=False)
    
    axs[0][0].set_title("Absolute Stückzahl im Lager")
    axs[0][0].xaxis.set_major_formatter(xmfd)
    
    for df in dfs:
        df = df.sort_values("Timestamp") #Very hacky wont work in August
        #timestapm = [datetime.strptime(time, '%d_%m_%Y %H') for time in df["Timestamp"].values.tolist()]
        plt.setp(axs, xticks=df["Timestamp"], xticklabels=df["Timestamp"])
        axs[0][0].plot(df["Timestamp"], df["Stückzahl"], label = df.iloc[0][0])
        axs[0][0].scatter(df["Timestamp"], df["Stückzahl"])
        #axs[0][0].legend()

        #axs[0][0].set_xticklabels(timestapm, rotation = 25, fontdict = fontdict_xaxis)

    axs[0][1].set_title("Preis gegen Timestamps")
    axs[1][0].set_title("Verkäufe gegen Timestamps")
    axs[1][1].set_title("Prozentuales Wachstum Verkäufe")
    return fig



#TODO 
#Make this plottable, and bring in right order/make a df for each diffrent link from this dataframe


def main():
    jdicts, filenames =  readJSONS("./jsonDUMP/")
    df_l = makeDataframe(jdicts, filenames[0])
    plot = makePlot(df_l)
    plt.show()
    return 

if __name__ == "__main__":
    main()