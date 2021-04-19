import requests as req
from bs4 import BeautifulSoup

    

links = []

url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
response = req.get(url)
if response.ok:
   
   soup = BeautifulSoup(response.text, "lxml")
   tds = soup.findAll('article', attrs={'class': 'product_pod'})
   article = ("'article', attrs={'class': 'product_pod'}")
   
   for article in tds:
       a = article.find('a')
       link = a['href'].replace('../../..',"")
       links.append("https://books.toscrape.com/catalogue" + link)



for row in links:
    url = row.strip()
    response = req.get(url)
    if response.ok:
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
               
