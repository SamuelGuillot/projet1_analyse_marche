from bs4 import BeautifulSoup
import requests
import csv
import re
from urllib.parse import urljoin

# PHASE 1

# Creation du document qui scrape un seul livre

url_product_page = "https://books.toscrape.com/catalogue/the-requiem-red_995/index.html"

url_request_product_page = requests.get(url_product_page)
url_request_product_page.encoding = "utf-8" # Je m'assure de l'encodage pour les éléments comme €

doc_product_page = BeautifulSoup(url_request_product_page.text, 'html.parser')


# Creation du document qui scrape tous les livres

# url_all = "https://books.toscrape.com/"

# url_request_all = requests.get(url_all)

# doc_all = BeautifulSoup(url_request_all.text, 'html.parser')

print('----------------------------------------------------')

# Récupération des informations d'un seul livre

# Url de la page du produit

print(f"L'url de la page du livre est: {url_product_page}")

# Titre

product_page_book_name = doc_product_page.find('h1').string
print(f"Le titre du livre: {product_page_book_name}" )
product_page_book_name = str(product_page_book_name) # conversion de la navigable str en str

print('------------------------------------')

# Universal_product_code (upc)

upc_tag = doc_product_page.find('th', string = "UPC")
upc_pp = upc_tag.find_next('td').string
print(upc_pp)
print(f"L'upc du livre est': {upc_pp}" )

print('------------------------------------')

# Prix taxe incluse

prix_inc_tag = doc_product_page.find('th', string = "Price (incl. tax)")
prix_inc = prix_inc_tag.find_next('td').string
print(f"Le prix du livre taxe incluse: {prix_inc}" )

print('------------------------------------')

# Prix taxe excluse

prix_excl_tag = doc_product_page.find('th', string = "Price (excl. tax)")
prix_excl = prix_excl_tag.find_next('td').string
print(f"Le prix du livre taxe excluse: {prix_excl}" )

print('------------------------------------')

# Nombre d'exmplaires restant

livre_quantite_tag = doc_product_page.find('th', string="Availability")
livre_quantite_string = livre_quantite_tag.find_next('td').string
livre_quantite_list = re.findall(r'\d+', livre_quantite_string)
livre_quantite = livre_quantite_list[0]
print(f"Il reste {livre_quantite} exemplaires" )

print('------------------------------------')

# Description du produit

product_page_description_tag = doc_product_page.find("h2", string ="Product Description")
product_page_description = product_page_description_tag.find_next('p').string
print(f"La description du livre: {product_page_description}")
product_page_description = str(product_page_description) # 

print('------------------------------------')

# Catégorie du livre

category_product_page_tag = doc_product_page.find('a', string = 'Books')
category_product_page = category_product_page_tag.find_next("a").string
print(f"La catégorie du livre: {category_product_page}")

print('------------------------------------')

# Note du livre

review = None
review_tag = doc_product_page.find('p', class_= 'star-rating')
review_classes = review_tag['class'] # On utilise 'class' comme clé
review = review_classes[1] # Je récupère dans la liste la note

rating_dictionary = {
    "One" : {"français": "Une", "int": 1 },
    "Two" : {"français": "Deux", "int": 2 },
    "Three" : {"français": "Trois", "int": 3 },
    "Four" : {"français": "Quatre", "int": 4 },
    "Five" : {"français": "Cinq", "int": 5 }
}

for x in rating_dictionary:
    if review == x: 
        review = rating_dictionary[x] # je compare la note au dictionnaire afin de faire une traduction plus facilement

print(f"Le livre est a reçu la note de {review["français"]} étoile sur Cinq ou {review["int"]}/5★")

print('------------------------------------')

# URL de l'image

relative_image_url_product_page = None
tag_img_product_page= doc_product_page.find('img')
relative_image_url_product_page = tag_img_product_page['src']

url_de_base = "https://books.toscrape.com/index.html"
url_image_product_page = urljoin(url_de_base, relative_image_url_product_page) # Création de l'URL absolu

print(f"L\'URL de l'image du livre est: {url_image_product_page}")

print('------------------------------------')

Product_page_dictionnary = ({
    'Product_page_url' : url_product_page,
    'Universal_product_code': upc_pp,
    'Title' : product_page_book_name,
    'price_including_tax' : prix_inc,
    'price_excluding_tax' : prix_excl,
    'number_available' : livre_quantite,
    'product_description': product_page_description,
    'category' : category_product_page,
    'review_rating' : review['int'], 
    'image_url' : url_image_product_page
    }) # Création du dictionnaire avec toutes les clés et valeurs

# Ecrire les données dans un fichier csv

fieldnames_pp = Product_page_dictionnary.keys()

with open('data.csv', "w", newline ='', encoding='utf-8') as csvfile: 
    writer = csv.DictWriter(csvfile, delimiter= ',', fieldnames= fieldnames_pp)
    writer.writeheader()
    writer.writerow(Product_page_dictionnary)

# Creation du document qui scrape tous les livres

# url_all = "https://books.toscrape.com/"

# url_request_all = requests.get(url_all)

# doc_all = BeautifulSoup(url_request_all.text, 'html.parser')