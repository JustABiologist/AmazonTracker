import json 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
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
    links = flatten_concatenation(links)
    values = []
    for dic in dicDF:
        for link in links:
            values.append(dic[link])
    values=flatten_concatenation(values)
    listDF=[]
    for i,j in zip(links, values):
        print(j)
        row = [i, j[3], filename, j[2], j[1]]
        listDF.append(row)
    df = pd.DataFrame(listDF, columns=["Links", "Timestamp", "Ursprungsexcel", "Preis", "Stückzahl"])
    df_unique = df["Links"].unique().squeeze().tolist()
    df_l = [df[df["Links"] == unique] for unique in df_unique]
    return df_l

#TODO 
#Make this plottable, and bring in right order/make a df for each diffrent link from this dataframe


def main():
    jdicts, filenames =  readJSONS("./jsonDUMP/")
    print(makeDataframe(jdicts, filenames[0])[0])
    return 

if __name__ == "__main__":
    main()