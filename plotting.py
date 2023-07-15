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

def makeDataframe(json_dicts, filename):
    '''Takes in list of all JSONS in the folder in dict format and returns a list of all the datapoints pertaining to a certain excel file'''
    dicDF = [fileDic[filename] for fileDic in json_dicts]
    links = list(dicDF.keys)
    values = [dicDF[link] for link in links]
    listDF=[]

    for i,j in zip(links, values):
        row = [i, j[3], filename, j[2], j[1]]
        listDF.append(row)

    return pd.DataFrame(listDF, columns=["Links", "Timestamp", "Ursprungsexcel", "Preis", "Stückzahl"])


def main():
    jdicts, filenames =  readJSONS("./jsonDUMP")
    print(makeDataframe(jdicts, filenames[0]))
    return 

if __name__ == "__main__":
    main()