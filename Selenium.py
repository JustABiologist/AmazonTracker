from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display


from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import time 
from datetime import datetime
import re
import pandas as pd 
import os
import json
import argparse
import openpyxl

#driver_path = 'C:/Users/iamfl/chromedriver'
#filepathXLSX = 'C:/Users/iamfl/Desktop/Skripte/PapaFBA/FileTest/'

def readExcel(Excelpath):
    df = pd.read_excel(Excelpath)
    print(df)
    return df['Testlinks'].values.tolist()


def makeCallStockAmazon(driver_path, link, sleeptime=None):
    
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    #driver = webdriver.Chrome()
    driver.get(link)
    driver.maximize_window()
    # time.sleep(3)
    cookie_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "sp-cc-rejectall-link")))
    #cookie_button = driver.find_element(By.XPATH,"//span[contains(text(),'//label[contains(text(), 'Menge')]')]")
    cookie_button.click()
    time.sleep(3)
    cart_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "add-to-cart-button")))
    cart_button.click()
    driver.get("https://www.amazon.de/cart?ref_=sw_gtc")
    time.sleep(5)
    dropdown = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "a-autoid-1")))
    dropdown.click()
    dropdown_option = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "quantity_10")))
    dropdown_option.click()
    actions = ActionChains(driver)
    actions.send_keys('999')
    actions.perform()
    aktualisieren = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "a-autoid-2-announce")))
    aktualisieren.click()
    time.sleep(5)
    stock = driver.find_element(By.XPATH, '//*[@id="sc-subtotal-label-buybox"]').text
    price = driver.find_element(By.XPATH, '//*[@id="sc-subtotal-amount-activecart"]').text

    stock_int = int(re.findall(r'\b\d+\b', stock)[0])
    price_float = float(re.findall(r"\d+\.\d+", price)[0])

    if sleeptime:
        time.sleep(sleeptime)
    driver.quit()
    now = datetime.now()
    return (link,stock_int, price_float, now.strftime("%d_%m_%Y %H"),)

def makeCallsFromExcel(Excelpath, driver_path):
    excel_list = readExcel(Excelpath)
    results = [makeCallStockAmazon(driver_path, address) for address in excel_list]
    return results

def FileReader(dirpath):
    print(os.listdir(dirpath))
    return {f"{file}":pd.read_excel(dirpath+file, engine='openpyxl') for file in os.listdir(dirpath)}

def FileWebScraper(dirpath, driverpath):
    filesDict = FileReader(dirpath)
    JSON = {}
    for fname in filesDict.keys():
        link_list = filesDict[fname]['Testlinks'].values.tolist()
        JSON[fname] = {link:[] for link in link_list}
        for address in link_list:
            current = makeCallStockAmazon(driverpath, address)
            JSON[fname][address].append(current)
    return JSON



def main():
    parser = argparse.ArgumentParser(description="Selenium Programm!")
    parser.add_argument("-c", "--chromiumpath", type= str, nargs=1, help="The chromium location for selenium")
    parser.add_argument("-x", "--exceldir", type= str, nargs=1, help="The folder with the exceldata to be parsed")
    parser.add_argument("-o", "--output", type = str, nargs=1, help="The output folder for the .jsons")
    
    args = parser.parse_args()
    chromepath = args.chromiumpath[0]
    excelpath = args.exceldir[0]
    outputpath = args.output[0]
    #display = Display(visible=0, size=(800, 600))
    #display.start()

    DATA = FileWebScraper(excelpath, chromepath)
    now = datetime.now()
    save_file = open(outputpath + f"AllDATA_{now.strftime('%d_%m_%Y %H')}.json", "w")  
    json.dump(DATA, save_file)
    save_file.close()

if __name__ == "__main__":
    main()

#TODO
'''
Make a webserver and GUI
Test on Excelsheet providwed by dad
Schedule jobs
Run on Raspi


Erledigt:
Cookies
In Einkaufswagen
Zum Einkaufswagen
Dropdown!
Text einfügen
auslesen
Extract price per Item !
return tuple of price, link, link and exact date of extraction!
Output auslesen
'''

