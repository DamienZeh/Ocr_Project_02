import requests
from bs4 import BeautifulSoup
import csv


def etl_pages_categorie(url_pages_category):
    page = requests.get(url_pages_category)
    soup = BeautifulSoup(page.content, 'html.parser')
    pager =  soup.find(class_='current').text             #signale qu'il n'y a plus de page 'next'.
    str_pager = pager.replace('Page 1 of ', '')
    numberMaxPages = int(str_pager)
    urlCategory= ""
    indexPage=0
    pagesCategory=[]
    urlCategory = url_pages_category.replace("index.html","page-1.html")  # pour incrémenter, on remplace "index.html",par "page-1.html".
    while indexPage < numberMaxPages:
        indexPage+=1
        urlCategoryIndex = urlCategory.replace("-1", f"-{indexPage}")  # on remplace l'index str de la page par la variable 'indexPage'.
        pagesCategory.append(urlCategoryIndex)                #on stocke toutes les pages de la categorie dans la liste 'pageCategory'.

    for page in pagesCategory:
        etl_livres_par_pages(page)


def etl_livres_par_pages(url_page_livres):
    page = requests.get(url_page_livres)
    soup = BeautifulSoup(page.content, 'html.parser')    #on obtient une variable qui a des doublons et des liens inutiles.
    list_books_duplication=[]
    links_books= soup.select('h3 > a')

    for link in links_books:                    #on transforme les liens en liste, sans balises.
        list_books_duplication.append(link.get('href'))

    debut_de_lien ="https://books.toscrape.com/catalogue/" #début à remplacer dans les liens
    str_list_books = ", ".join(list_books_duplication) # on convertit la liste en str pour pouvoir remplacer la partie du lien manquant
    replace_link_books= str_list_books.replace("../../../", debut_de_lien) #on remplace le lien manquant
    books = replace_link_books.split(',') # on a notre liste de liens pour les livres de la page

    print(books)



def etl_livre(url_livre):
    page = requests.get(url_livre)
    soup = BeautifulSoup(page.content, 'html.parser')
    details_prod_upc_tax_available = soup.find_all('td') #ici on trouve l'UPC, les taxes et la disponibilité
    print(soup)
    # url link
    adresse_url = [url_livre]

    # code UPC
    universal_product_code = details_prod_upc_tax_available[0]


    # titre
    titres = soup.find('li', class_="active")


    # price_including_tax
    price_including_tax = details_prod_upc_tax_available[3]


    # price_excluding_tax
    price_excluding_tax = details_prod_upc_tax_available[2]


    # available
    number_available = details_prod_upc_tax_available[5]


    # description
    product_descriptions = soup.find(class_='product_page').find_all('p')  # contenu de la classe product page
    product_description = product_descriptions[3]  # 3 est la position de la description en 'p' dans la class product_page

    # category
    categories_all = soup.find('ul', class_="breadcrumb").find_all('a')
    categories = categories_all[2]


    #en tête de la fiche
    en_tete = ["product_page_url", "universal_product_code (upc)", "title","price_including_tax", "price_excluding_tax", "number_available", "product_description", "category","review_rating", "image_url" ]
    # charger la donnée dans un fichier csv

    # review_rating
    review_rating_stars = soup.find('div', class_="col-sm-6 product_main").find_all('p')[2]
    rating_stars = (review_rating_stars['class'])
    review_rating = rating_stars[1]
    if review_rating == "One":
        review_rating = "1 / 5"
    elif review_rating == "Two":
        review_rating = "2 / 5"
    elif review_rating == "Three":
        review_rating = "3 / 5"
    elif review_rating == "Four":
        review_rating = "4 / 5"
    elif review_rating == "Five":
        review_rating = "5 / 5"
    else:
        review_rating = "0 / 5"
    reviews_rating = [review_rating]

    # image_url
    image_url = soup.img
    img_url = [image_url['src']]


    charger_donnees_livre('test_ donnee_ un livre_02.csv', en_tete, adresse_url,universal_product_code, titres, price_including_tax, price_excluding_tax, number_available, product_description, categories, reviews_rating, img_url)

def charger_donnees_livre(nom_fichier, en_tete, url, universal_product_code, titres, price_including_tax, price_excluding_tax, number_available, product_description, categories, reviews_rating, image_url):
    with open(nom_fichier, 'w') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(en_tete)
        for adresse_url, upc, titre, tax_inc, tax_excl, available, description, category, review_rating, img_url in zip(url, universal_product_code, titres, price_including_tax, price_excluding_tax, number_available, product_description, categories, reviews_rating, image_url):
            writer.writerow([adresse_url, upc, titre, tax_inc, tax_excl, available, description, category, review_rating, img_url])



etl_pages_categorie("https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html")
#etl_livres_par_pages('https://books.toscrape.com/catalogue/category/books/romance_8/index.html')
#etl_livre('https://books.toscrape.com/catalogue/worlds-elsewhere-journeys-around-shakespeares-globe_972/index.html')

