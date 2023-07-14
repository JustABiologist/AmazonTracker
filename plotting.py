import json 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
import os

def readJSONS(json_dir):
    '''Takes a directory of jsons and reads them all in, returns a list of dicts.'''
    jsons = os.listdir(json_dir)
    dics = []
    for file in jsons:
        with open(json_dir+file) as jfile:
            dics.append(json.load(jfile))
    return dics





def main():
    return 0

if __name__ == "__main__":
    main()