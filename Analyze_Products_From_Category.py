import requests
from bs4 import BeautifulSoup
import csv


def etl_pages_category(url_pages_category): # récupère toutes les pages d'une catégorie
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


    creation_csv()         #On crée le csv avec l'entête.


    for page in pages_category:    #on boucle sur la fonction etl_books_in_page()
        etl_books_in_page(page)


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

    for book in books:     #on boucle sur la fonction etl_book()
        etl_book(book)


def etl_book(url_book): #on récupère les détails du livre
    page = requests.get(url_book)
    soup = BeautifulSoup(page.content, 'html.parser')
    details_prod_upc_tax_available = soup.find_all('td')  # ici on trouve l'UPC, les taxes et la disponibilité

    # code UPC
    universal_product_code = ''.join(details_prod_upc_tax_available[0])

    # titre
    titles = ''.join(soup.find('li', class_="active"))

    # price_including_tax
    price_including_tax = ''.join(details_prod_upc_tax_available[3])

    # price_excluding_tax
    price_excluding_tax = ''.join(details_prod_upc_tax_available[2])

    # available
    number_available = ''.join(details_prod_upc_tax_available[5])

    # description
    try:                       #il y a des livres qui n'ont pas de description, on gère cette possible erreur ici, avec un try except.
        product_descriptions = soup.find(class_='product_page').find_all('p')  # contenu de la classe product page
        product_description = ''.join(product_descriptions[3])  # 3 est la position de la description en 'p' dans la class product_page
    except:
        product_description = "pas de description pour ce livre."

    # category
    categories_all = soup.find('ul', class_="breadcrumb").find_all('a')
    categories = ''.join(categories_all[2])

    # review_rating
    review_rating_stars = soup.find('div', class_="col-sm-6 product_main").find_all('p')[2]
    rating_stars = (review_rating_stars['class'])
    review_rating = rating_stars[1]
    if review_rating == "One":  # on adapte le chiffre obtenu avec une note sur cing.
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
    reviews_rating = ''.join(review_rating)  # on le transforme en liste

    # image_url
    pic_url = soup.img
    img_url = pic_url['src']
    str_img_url = "".join(img_url)
    image_url = str_img_url.replace("../../", "https://books.toscrape.com/")  # on a notre lien image url.

    data_book = url_book, universal_product_code, titles, price_including_tax, price_excluding_tax, number_available, product_description, categories, reviews_rating, image_url
    writer_data_book_csv(data_book)

# crée le csv avec l'entête.
def creation_csv():
    #en tête de la fiche
    heading = ["product_page_url", "universal_product_code (upc)", "title","price_including_tax", "price_excluding_tax", "number_available", "product_description", "category","review_rating", "image_url" ]
    with open('Analyze_Products_From_Category.csv', 'w', encoding='utf-8', errors='ignore') as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=',')
            writer.writerow(heading)

# écrit les données de tous les livres de toutes les pages d'une catégorie.
def writer_data_book_csv(data_book):
    with open('Analyze_Products_From_Category.csv', 'a', encoding='utf-8', errors='ignore') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(data_book)



#tapez dans les parenthèses, avec les guillemets, le lien de la première page de la catégorie désirée.
etl_pages_category("https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html")




#NOTE:
# dans 'with open', mettre 'encoding='utf-8', errors='ignore', permet d'éviter les UnicodeError