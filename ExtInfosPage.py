import requests as req
from bs4 import BeautifulSoup
import csv
import os
import re


def Infos_Page(url):

    response = req.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    desc = soup.find('div',{"id": "product_description"})
    if desc is None:
        desc = ""
    else:
        desc = desc.find_next('p').get_text()
        catego = soup.find("ul",{"class": "breadcrumb"}).find_next("li").find_next("li").find_next("li").get_text().strip('\n')
        infos_table = soup.table
        infos = {}
        for row in infos_table.find_all("tr"):
            infos[row.th.get_text()] = row.td.get_text()
        Titre = soup.find('h1').text
        Image = soup.img["src"].strip('../../')
        Image_book = 'http://books.toscrape.com/' + Image
        
    
    infos_book = { 
        "Titre": Titre,
        "image": Image_book,
        "Description": desc,
        "Categorie": catego,
        **infos
        }
    
    path = "Image pour une page"
    
    if not os.path.exists(path):
        os.makedirs(path)
        
        title = re.sub('[^a-zA-Z0-9 \n]', '', Titre)
        
        with open(path + '/' + title + ".jpg", "wb") as file:
            res = req.get(Image_book)
            file.write(res.content)
    
    print(infos_book)
    
    
    
    
Infos_Page("http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html")