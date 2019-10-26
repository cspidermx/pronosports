import os
from sys import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChOptions
from bs4 import BeautifulSoup
import csv
import time
import zipfile
from my_email import send_mail


def open_browser():
    chrome_options = ChOptions()
    chrome_options.add_argument('--headless')
    if platform.find('win') >= 0:
        chrome_driver = os.path.join(os.getcwd(), "chromedriver.exe")
    else:
        chrome_driver = os.path.join(os.getcwd(), "chromedriver")
    drv = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
    return drv


def getdias(driver):
    dias = ['', 'Jueves', 'Viernes', 'Sabado', 'Domingo', 'Lunes', 'Martes', 'Miercoles']
    url = 'https://www.pronosports.net/lista-de-juegos/'

    driver.get(url)
    wait = WebDriverWait(driver, 10)

    wait.until(EC.visibility_of_element_located((By.ID, "content")))
    btnsrch = driver.find_element_by_xpath("//button[@class='button btn wdt-pf-search-filters-button waves-effect']")
    btnfecha = driver.find_elements_by_xpath("(//button[@class='btn dropdown-toggle bs-placeholder btn-default'])")[1]
    btnshow = driver.find_elements_by_xpath("(//button[@class='btn dropdown-toggle btn-default'])")[0]
    btnfecha.click()
    fechalist = driver.find_elements_by_xpath("(//ul[@class='dropdown-menu inner'])")[1].find_elements_by_tag_name("li")

    i = 0
    cuantas = len(fechalist)
    for fecha in range(0, cuantas):
        if i != 0:
            if i != 1:
                btnfecha.click()
                x_p = "(//ul[@class='dropdown-menu inner'])"
                fechalist = driver.find_elements_by_xpath(x_p)[1].find_elements_by_tag_name("li")
            tabla = []
            ff = fechalist[i].text
            print(dias[i], ff)
            fechalist[i].click()
            btnsrch.click()
            btnshow.click()
            x_p = "(//ul[@class='dropdown-menu inner'])"
            showlist = driver.find_elements_by_xpath(x_p)[8].find_elements_by_tag_name("li")[6]
            showlist.click()
            k = 0
            while k == 0:
                revisa = driver.find_element_by_id('table_1').find_elements_by_class_name("column-fecha")
                if revisa[1].text == ff:
                    break
                else:
                    time.sleep(1)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            juegos = soup.findAll("table", {"id": "table_1"})
            titles = juegos[0].find('thead').find_all('th')
            tabla.append([ele.text.strip().replace('\xa0', ' ') for ele in titles])
            table_body = juegos[0].find('tbody')
            rows = table_body.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                tabla.append([ele for ele in cols if ele])  # Get rid of empty values
            file = "output/{:02d} {}.csv".format(i, dias[i])
            with open(os.path.join(os.getcwd(), file), 'w', newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(tabla)
        i += 1
    return cuantas


def get_nfl(driver, cuantas):
    url = 'https://www.pronosports.net/lista-de-juegos/'
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "content")))
    btnshow = driver.find_elements_by_xpath("(//button[@class='btn dropdown-toggle btn-default'])")[0]
    btnsport = driver.find_elements_by_xpath("(//button[@class='btn dropdown-toggle bs-placeholder btn-default'])")[4]
    btnsport.click()
    sportlist = driver.find_elements_by_xpath("(//ul[@class='dropdown-menu inner'])")[4].find_elements_by_tag_name("li")
    for s in sportlist:
        if s.text == 'F. AMERICANO':
            s.click()
            break
    print('F. AMERICANO')
    btnsrch = driver.find_element_by_xpath("//button[@class='button btn wdt-pf-search-filters-button waves-effect']")
    btnshow.click()
    showlist = driver.find_elements_by_xpath("(//ul[@class='dropdown-menu inner'])")[
        8].find_elements_by_tag_name("li")[6]
    showlist.click()
    btnsrch.click()
    k = 0
    while k == 0:
        revisa = driver.find_element_by_id('table_1').find_elements_by_class_name("column-deporte")
        if revisa[1].text == 'F. AMERICANO':
            break
        else:
            time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    juegos = soup.findAll("table", {"id": "table_1"})
    titles = juegos[0].find('thead').find_all('th')
    tabla = list()
    tabla.append([ele.text.strip().replace('\xa0', ' ') for ele in titles])
    table_body = juegos[0].find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        tabla.append([ele for ele in cols if ele])  # Get rid of empty values
    file = "output/{:02d} NFL.csv".format(cuantas)
    with open(os.path.join(os.getcwd(), file), 'w', newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(tabla)


directory = os.path.join(os.getcwd(), "output")
if not os.path.exists(directory):
    os.makedirs(directory)
d = open_browser()
ctas = getdias(d)
get_nfl(d, ctas)
d.close()

with zipfile.ZipFile(os.path.join(os.getcwd(), "output/pronosports.zip"), 'w') as myzip:
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            myzip.write(os.path.join(directory, filename), filename)
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"):
        os.remove(os.path.join(directory, filename))

send_mail(os.path.join(os.getcwd(), "output/pronosports.zip"), 'pronosports.zip')
os.remove(os.path.join(os.getcwd(), "output/pronosports.zip"))
