import requests as req
from bs4 import BeautifulSoup
import csv



def Infos_Page(url):

    response = req.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    desc = soup.find('div',{"id": "product_description"})
    if desc is None:
        desc = ""
    else:
        desc = desc.find_next('p').get_text()
        catego = soup.find("ul",{"class": "breadcrumb"}).find_next("li").find_next("li").find_next("li").get_text()
        infos_table = soup.table
        infos = {}
        for row in infos_table.find_all("tr"):
            infos[row.th.get_text()] = row.td.get_text()
        
    info_books = { 
        "Titre": soup.title.text,
        "image": soup.img["src"],
        "Description": desc,
        "Categorie": catego,
        **infos
        }
    
    print(info_books)
    
    
    


url = "http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
Infos_Page(url)