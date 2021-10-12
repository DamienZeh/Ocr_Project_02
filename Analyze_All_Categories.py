

import requests
from bs4 import BeautifulSoup
import csv



def main(url):
    names_categories = etl_list_names_categories(url)
    links_categories = etl_links_all_categories(url)
    for csv in etl_list_names_categories(url):   # on crée d'abord les csv avec l'en-tête.
        creation_csv(csv)

    for link, name_category in zip(links_categories, names_categories):
        all_data_books_in_category(link, name_category)


def all_data_books_in_category(link_first_page_category, name_category):
    for page in etl_pages_category(link_first_page_category):
        etl_books_in_page(page)
        for books in etl_books_in_page(page):
            writer_books_category_csv(etl_book(books), name_category)


def etl_links_all_categories(url_all_categories): #récupère les liens des catégories
    page = requests.get(url_all_categories)
    soup = BeautifulSoup(page.content, 'html.parser')
    links_categories = soup.find('ul', class_="nav nav-list").find_all('a')
    list_links_categories_raw = []
    for category in links_categories:
        list_links_categories_raw.append(category.get('href'))
    #on va récupérer les liens des catégories:
    del list_links_categories_raw[0] #on supprime le premier lien inutile
    list_links_categories= []
    for link in list_links_categories_raw:
        link_full= "https://books.toscrape.com/"+link
        list_links_categories.append(link_full)  #on obtient ici notre liste de liens de catégories.
    return list_links_categories

def etl_list_names_categories(url_names_categories):    #récupère les noms des catégories.
    list_links_categories_raw= etl_links_all_categories(url_names_categories)  # on récupère d'abord la liste des liens de categories.
    # on récupère le nom des catégories. pb, selon les noms, il y a soit les 2 caractères de la fin à enlever, soit 3.
    list_names_str = ','.join(list_links_categories_raw)
    str_names_without_star = list_names_str.replace("https://books.toscrape.com/catalogue/category/books/","")  # on enlève d'abord la partie du lien de début
    str_names_without_end = str_names_without_star.replace("/index.html", "")  # puis la partie de lien de fin.
    names_with_number = str_names_without_end.split(',')
    first_names_without_number = []
    last_names_without_number = []
    names_first_part = names_with_number[0:7]  # on sépare la liste entre ceux qui ont 2 caractère à enlever et ceux qui ont 3.
    names_end_part = names_with_number[8:50]
    for name in names_first_part:  # on enlève les 2 derniers caractères de cette partie de la liste
        first_name_without_number = name[:-2]
        first_names_without_number.append(first_name_without_number)
    for name in names_end_part:
        last_name_without_number = name[:-3]  # on enlève les 3 derniers caractères de cette partie de la liste
        last_names_without_number.append(last_name_without_number)
    list_names = first_names_without_number + last_names_without_number  # on a enfin notre liste avec les noms de catégories!
    return list_names


def etl_pages_category(url_pages_category): # récupère toutes les pages d'une catégorie, si on lui donne la première
    page = requests.get(url_pages_category)
    soup = BeautifulSoup(page.content, 'html.parser')

    #'pager' va servir de référence pour le nombre max de page. On vérifie qu'il existe avec try/except. Si oui, c'est qu'il y a plus d'une page.
    try:
        pager =  soup.find(class_='current').text   # affiche page actuel sur page suivante. ex: Page 2 of 4
        str_pager = pager.replace('Page 1 of ', '') # on récupère le dernier chiffre pour avoir le nombre max de page
        number_max_pages = int(str_pager)
        index_page=0
        pages_category=[]
        url_category = url_pages_category.replace("index.html","page-1.html")  # pour incrémenter, on remplace "index.html",par "page-1.html".
        while index_page < number_max_pages:
            index_page+=1
            url_category_index = url_category.replace("-1", f"-{index_page}")  # on remplace l'index str de la page par la variable 'indexPage'.
            pages_category.append(url_category_index)                #on stocke toutes les pages de la categorie dans la liste 'pageCategory'.
    except:             # et donc ici, c'est si il n'y a qu'une page.
        pages_category=[]
        url_category_index=url_pages_category
        pages_category.append(url_category_index)                #on stocke toutes les pages de la categorie dans la liste 'pageCategory'.
    return pages_category



def etl_books_in_page(url_page_livres):             # récupère tous les livres d'une page
    page = requests.get(url_page_livres)
    soup = BeautifulSoup(page.content, 'html.parser') #on obtient une variable qui a des doublons et des liens inutiles.
    links_books= soup.select('h3 > a')                #on récupère les liens html des livres.
    list_books_duplication = []
    for link in links_books:                          #on transforme les liens en liste, sans balises.
        list_books_duplication.append(link.get('href'))
    debut_de_lien ="https://books.toscrape.com/catalogue/"    #début à remplacer dans les liens
    str_list_books = ", ".join(list_books_duplication)     # on convertit la liste en str pour pouvoir remplacer la partie du lien manquant
    replace_link_books= str_list_books.replace("../../../", debut_de_lien) #on remplace le lien manquant
    books = replace_link_books.split(',')               # on a notre liste de liens pour les livres de la page
    return books


def etl_book(url_book): #on récupère les détails du livre
    page = requests.get(url_book)
    soup = BeautifulSoup(page.content, 'html.parser')
    details_prod_upc_tax_available = soup.find_all('td') #ici on trouve l'UPC, les taxes et la disponibilité

    # code UPC:
    universal_product_code = ''.join(details_prod_upc_tax_available[0])
    # titre:
    titles = ''.join(soup.find('li', class_="active"))
    # price_including_tax:
    price_including_tax = ''.join(details_prod_upc_tax_available[3])
    # price_excluding_tax:
    price_excluding_tax = ''.join(details_prod_upc_tax_available[2])
    # available:
    number_available = ''.join(details_prod_upc_tax_available[5])
    # description:
    try:     #il y a des livres qui n'ont pas de description, on gère cette possible erreur ici, avec un try except.
        product_descriptions = soup.find(class_='product_page').find_all('p')  # contenu de la classe product page
        product_description = ''.join(product_descriptions[3])  # 3 est la position de la description en 'p' dans la class product_page
    except:
        product_description = "pas de description pour ce livre."
    # category:
    categories_all = soup.find('ul', class_="breadcrumb").find_all('a')
    categories = ''.join(categories_all[2])
    # review_rating:
    review_rating_stars = soup.find('div', class_="col-sm-6 product_main").find_all('p')[2]
    rating_stars = (review_rating_stars['class'])
    review_rating = rating_stars[1]
    if review_rating == "One":       # on adapte le chiffre obtenu avec une note sur cing.
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
    reviews_rating = ''.join(review_rating)    #on le transforme en liste
    # image_url:
    pic_url = soup.img
    img_url = pic_url['src']
    str_img_url="".join(img_url)
    image_url= str_img_url.replace("../../", "https://books.toscrape.com/")#on a notre lien image url.

    data_book=url_book,universal_product_code, titles, price_including_tax, price_excluding_tax, number_available, product_description, categories, reviews_rating, image_url
    return data_book

# crée le csv avec l'entête.
def creation_csv(name_category):
    #en tête de la fiche
    heading = ["product_page_url", "universal_product_code (upc)", "title","price_including_tax", "price_excluding_tax", "number_available", "product_description", "category","review_rating", "image_url" ]
    with open('Analyze_Products_From_Category_'+name_category+'.csv', 'w', encoding='utf-8', errors='ignore') as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=',')
            writer.writerow(heading)

# crée les données d'un livre.
def writer_books_category_csv(data_category, name_category):
    with open('Analyze_Products_From_Category_'+name_category+'.csv', 'a', encoding='utf-8', errors='ignore') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(data_category)

#tapez dans les parenthèses, avec les guillemets, le lien de Book To Scrape.
main("https://books.toscrape.com/")
