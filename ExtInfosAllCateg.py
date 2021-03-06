import requests as req
from bs4 import BeautifulSoup
import csv
import os 
import re



def get_categories(url):
    print("get_categories:", url)
    response = req.get(url)

    if not response.ok:
        raise Exception("oups")

    soup = BeautifulSoup(response.text, 'lxml')
    
    categories_list = soup.find('ul', attrs={'class': 'nav nav-list'})
    categorie_items = categories_list.find_all('li')
    categorie_links = []
   
    for li in categorie_items:
        a = li.find('a')
        cat = a['href'].replace('../', '')
        categorie_links.append(url + cat)
    categorie_links.remove(url + 'catalogue/category/books_1/index.html')
    return categorie_links

def get_books(url):
    print("get_books:", url)
    response = req.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        pager = soup.find('ul', attrs={'class': 'pager'})
        if pager is None:
            return get_books_single_page(soup)
          
        else:
            books = get_books_single_page(soup)
            next_button = pager.find('li', attrs={'class': 'next'})
            if next_button is not None:
                rel_link = next_button.a["href"]
                base_url = url.rsplit('/', 1)[0]
                next_url = base_url + '/' + rel_link
                books += get_books(next_url)
            return books
    return []

def main():
    cats = get_categories("https://books.toscrape.com/")
    books = []
    
    for idx, cat in enumerate(cats):
        book = get_books(cat)

        with open ("categ" + ' ' + str(idx) + ".csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, book[0].keys())
            writer.writeheader()
            writer.writerows(book)
        books += get_books(cat)
    

def get_books_single_page(soup):
    print("get_books_single_page:")
    articles = soup.findAll('article', attrs={'class': 'product_pod'})
    books = []
   
    for article in articles:
        a = article.find('a')
        page = a['href'].replace('../../..',"")
        book = get_book_infos("https://books.toscrape.com/catalogue" + page)
        if book is not None:
            books.append(book)
    
    return books
            
def get_book_infos(url):
    print("get_book_infos:", url)
    response = req.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'lxml')
        infos_table = soup.table
        desc = soup.find('div',{"id": "product_description"})
        if desc is None:
            desc = ""
        else:
            desc = desc.find_next('p').get_text()
        catego = soup.find("ul",{"class": "breadcrumb"}).find_next("li").find_next("li").find_next("li").get_text().strip('\n')
        infos = {}
        for row in infos_table.find_all("tr"):
            infos[row.th.get_text()] = row.td.get_text()
    
    
    
    path = catego
    
    if not os.path.exists(path):
        os.makedirs(path)
    Titre = soup.find('h1').text
    title = re.sub('[^a-zA-Z0-9 \n]', '', Titre)
    Image = soup.img["src"].strip('../../')
    Image_book = 'http://books.toscrape.com/' + Image       
    with open(path + '/' + title + ".jpg", "wb") as file:
        res = req.get(Image_book)
        file.write(res.content)


        
        return {
            "Categorie": catego,
            "image": Image_book, 
            "Titre": soup.title.text,
            "Description": desc,
            **infos
        }
    
    print("failed")
    
    
    
main()

   
