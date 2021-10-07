import requests
from bs4 import BeautifulSoup
import csv


def etl_book(url_book): #on récupère les détails du livre
    page = requests.get(url_book)
    soup = BeautifulSoup(page.content, 'html.parser')
    details_prod_upc_tax_available = soup.find_all('td') #ici on trouve l'UPC, les taxes et la disponibilité

    # url link
    address_url = url_book.split()

    # code UPC
    universal_product_code = details_prod_upc_tax_available[0]

    # titre
    titles = soup.find('li', class_="active")

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
    heading = ["product_page_url", "universal_product_code (upc)", "title","price_including_tax", "price_excluding_tax", "number_available", "product_description", "category","review_rating", "image_url" ]
    # charger la donnée dans un fichier csv

    # review_rating
    review_rating_stars = soup.find('div', class_="col-sm-6 product_main").find_all('p')[2]
    rating_stars = (review_rating_stars['class'])
    review_rating = rating_stars[1]
    if review_rating == "One":
        review_rating = "1_/_5"
    elif review_rating == "Two":
        review_rating = "2_/_5"
    elif review_rating == "Three":
        review_rating = "3_/_5"
    elif review_rating == "Four":
        review_rating = "4_/_5"
    elif review_rating == "Five":
        review_rating = "5_/_5"
    else:
        review_rating = "0_/_5"
    reviews_rating = review_rating.split()    #on le transforme en liste

    # image_url
    pic_url = soup.img
    img_url = pic_url['src']
    str_img_url="".join(img_url)
    replace_img_url= str_img_url.replace("../../", "https://books.toscrape.com/")
    image_url =replace_img_url.split()        #on le transforme en liste



    writer_data_book('Analyze_A_Product.csv', heading, address_url,universal_product_code, titles, price_including_tax, price_excluding_tax, number_available, product_description, categories, reviews_rating, image_url)


#on écrit les doonnées du livre
def writer_data_book(name_file, heading, url, universal_product_code, titles, price_including_tax, price_excluding_tax, number_available, product_description, categories, reviews_rating, image_url):
    with open(name_file, 'w') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(heading)
        for address_url, upc, title, tax_inc, tax_excl, available, description, category, review_rating, img_url in zip(url, universal_product_code, titles, price_including_tax, price_excluding_tax, number_available, product_description, categories, reviews_rating, image_url):
            writer.writerow([address_url, upc, title, tax_inc, tax_excl, available, description, category, review_rating, img_url])


etl_book("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")

