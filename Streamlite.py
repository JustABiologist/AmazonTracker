import streamlit as st
import pandas as pd
import numpy as np
import os
from plotting import readJSONS

import Selenium

##Variables
filepathXLSX = 'C:/Users/iamfl/Desktop/Skripte/PapaFBA/ExcelTest/'

def save_uploadedfile(uploadedfile, filepath):
    with open(os.path.join(filepath,uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success(f"Saved File:{uploadedfile.name} to {filepath}.")

def listFiles(dirpath):
    return os.listdir(dirpath)

def FileDropdown(dirpath):
    fileList = listFiles(dirpath)
    option = st.selectbox("Alle hochgeladenen Dateien", fileList)
    if option:
        df = pd.read_excel(dirpath+option)
        st.write(df)
        st.success(f"Angezeigte Datei:{option}!")
        download = st.download_button("Download this file?", data=dirpath+option)
        st.success(f"Heruntergeladene Datei:{option}!")
        delete = st.button("Diese Datei löschen?")
        if delete:
            os.remove(dirpath+option)
            st.success(f"Gelöschte Datei:{option}!")
    return None

def makePlots(jsondir):
    all_jsons = readJSONS(jsondir)
    for dic in all_jsons:
        prices = 
        


        
        


        



#{Dateiname: {unique_link1:[[timestamp, preis, Stock],[timestamp, preis, Stock]]}

    

        
    


    






    
    




st.title('Amazon FBA Scanner!')

Uploaded_files = st.file_uploader(".xlsx Dateien mit Amazon Links bitte hochladen!", type=".xlsx", accept_multiple_files=True)

for file in Uploaded_files:
    save_uploadedfile(file, filepathXLSX)

FileDropdown(filepathXLSX)




