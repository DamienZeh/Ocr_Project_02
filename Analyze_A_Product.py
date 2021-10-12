import requests
from bs4 import BeautifulSoup
import csv


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
    try:                         #il y a des livres qui n'ont pas de description, on gère cette possible erreur ici, avec un try except.
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


def writer_data_book_csv(data_book):
    heading = ["product_page_url", "universal_product_code (upc)", "title","price_including_tax", "price_excluding_tax", "number_available", "product_description", "category","review_rating", "image_url" ]
    with open('Analyze_Product_From_Category.csv', 'a', encoding='utf-8', errors='ignore') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(heading)
        writer.writerow(data_book)


#tapez dans les parenthèses, avec les guillemets, le lien du livre désiré.
etl_book("https://books.toscrape.com/catalogue/emma_17/index.html")





#NOTE:
# dans 'with open', mettre 'encoding='utf-8', errors='ignore', permet d'éviter les UnicodeError