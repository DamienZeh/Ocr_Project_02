import requests
from bs4 import BeautifulSoup
import csv
import os


def main(url_book):
    data_book = etl_book(url_book) # on récupère les données du livre
    writer_data_book_csv(data_book) # on les écrit, avec l'en-tête.

    title_book = data_book[2] #on récupère le nom du livre et le lien de l'image_url pour enregistrer l'image.
    image_url = data_book[-1]
    writer_image_book(title_book, image_url) # on enregistre l'image.


def etl_book(url_book): #on récupère les détails du livre
    page = requests.get(url_book)
    soup = BeautifulSoup(page.content, 'html.parser')
    details_prod_upc_tax_available = soup.find_all('td')  # ici on trouve l'UPC, les taxes et la disponibilité
    universal_product_code = ''.join(details_prod_upc_tax_available[0])     # code UPC
    title_name = ''.join(soup.find('li', class_="active"))    # titre.
    title = title_name[:90].replace(',', '_').replace("'", '_').replace(':', '_').replace('/', '_').replace('"', '_').replace('*', '_')\
        .replace('?', '.').replace('#', '_').replace('%', '_').replace('-', '_').replace('é', 'e').replace('è', 'e')\
        .replace('à', 'a').replace('â', 'a').replace('â', 'a').replace(' ', '_')#sans caractères spéciaux, limite taille
    price_including_tax = ''.join(details_prod_upc_tax_available[3])    # price_including_tax
    price_excluding_tax = ''.join(details_prod_upc_tax_available[2])    # price_excluding_tax
    number_available = ''.join(details_prod_upc_tax_available[5])       # available

    # description
    try:                         #il y a des livres qui n'ont pas de description, on gère cette possible erreur ici, avec un try except.
        product_descriptions = soup.find(class_='product_page').find_all('p')    # contenu de la classe product page
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

    #data_book récupère toute les infos du livre
    data_book = url_book, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, categories, reviews_rating, image_url
    return data_book


# écrit l'image du livre avec le nom du titre.
def writer_image_book(title, image_url):
    path = 'Image_Book_Analyze_A_Product'
    try:                                    # On teste si le dossier existe déjà.
        os.mkdir('Image_Book_Analyze_A_Product')
    except:
        print('directory already exists')
    response = requests.get(image_url)
    with open(path+f'/{title}.jpg', 'wb') as image_file:
        image_file.write(response.content)


# écrit les données d'un livre + son en-tête.
def writer_data_book_csv(data_book):
    heading = ["product_page_url", "universal_product_code (upc)", "title","price_including_tax", "price_excluding_tax", "number_available", "product_description", "category","review_rating", "image_url" ]
    with open('Analyze_A_Product.csv', 'a', encoding='utf-8', errors='ignore') as fichier_csv:  # 'encoding='utf-8', errors='ignore', permet d'éviter les UnicodeError
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(heading)
        writer.writerow(data_book)


#tapez dans les parenthèses, avec les guillemets, le lien du livre désiré.
main("https://books.toscrape.com/catalogue/10-happier-how-i-tamed-the-voice-in-my-head-reduced-stress-without-losing-my-edge-and-found-self-help-that-actually-works_582/index.html")






