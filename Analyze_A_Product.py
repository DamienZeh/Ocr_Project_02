from bs4 import BeautifulSoup
import csv

url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

details_prod_upc_tax_available = soup.find_all('td') #ici on trouve l'UPC, les taxes et la disponibilité

# url link
adresse_url = [url]

# code UPC
universal_product_code = details_prod_upc_tax_available[0]
upc_textes = []
for upc in universal_product_code:
    upc_textes.append(upc.string)

#titre
titres = soup.find('li', class_ ="active")
titre_textes = []
for titre in titres:
    titre_textes.append(titre)

#price_including_tax
price_including_tax = details_prod_upc_tax_available[3]
tax_inc_textes = []
for tax_inc in price_including_tax:
    tax_inc_textes.append(tax_inc.string)

#price_excluding_tax
price_excluding_tax = details_prod_upc_tax_available[2]
tax_excl_textes = []
for tax_excl in price_including_tax:
    tax_excl_textes.append(tax_excl.string)

#available
number_available = details_prod_upc_tax_available[5]
available_textes = []
for available in number_available:
    available_textes.append(available.string)

#description
product_descriptions = soup.find(class_ = 'product_page').find_all('p') #contenu de la classe product page
product_description = product_descriptions[3] #3 est la position de la description en 'p' dans la class product_page
description_textes = []
for description in product_description:
    description_textes.append(description.string)

#category
categories_all = soup.find('ul',class_="breadcrumb").find_all('a')
categories=categories_all[2]
category_textes = []
for category in categories:
    category_textes.append(category)

#review_rating
review_rating_stars= soup.find('div', class_="col-sm-6 product_main").find_all('p')[2]
rating_stars=(review_rating_stars['class'])
reviews_rating =rating_stars[1]
if reviews_rating == "One":
    reviews_rating="1 / 5"
elif reviews_rating == "Two":
    reviews_rating="2 / 5"
elif reviews_rating == "Three":
    reviews_rating="3 / 5"
elif reviews_rating == "Four":
    reviews_rating="4 / 5"
elif reviews_rating == "Five":
    reviews_rating="5 / 5"
else:
    reviews_rating="0 / 5"
review_rating= reviews_rating


#image_url
image_url= soup.img
img_url=image_url['src']


#en tête de la fiche
en_tete = ["product_page_url", "universal_product_code (upc)", "title","price_including_tax", "price_excluding_tax", "number_available", "product_description", "category","review_rating", "image_url" ]

with open('01_analyze_a_product.csv', 'w') as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=',')
    writer.writerow(en_tete)
    for url, upc, titre, tax_inc, tax_excl, available, description, category, reviews_rating, image_url in zip(adresse_url, upc_textes, titre_textes, tax_inc_textes, tax_excl_textes, available_textes, description_textes, category_textes, review_rating, img_url):
        writer.writerow([url, upc, titre, tax_inc, tax_excl, available, description, category, review_rating, img_url])