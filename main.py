from bs4 import BeautifulSoup
import requests
import csv
import re
from urllib.parse import urljoin
import urllib.request  
import os


# Récupération de l'url de la page d'accueil

url_homepage = "http://books.toscrape.com/"
url_request_homepage = requests.get(url_homepage) # METTRE DANS LE GET ENCODING
url_request_homepage.encoding = "utf-8" # Je m'assure de l'encodage pour les éléments comme €

doc_homepage = BeautifulSoup(url_request_homepage.text, 'html.parser')

total_book_number = 0
processed_book_counter = 0
book_upc_found = 0
book_upc_not_found = 0
book_price_inc_found = 0
book_price_inc_not_found = 0
book_price_excl_found = 0
book_price_excl_not_found = 0
book_avaibility_found = 0
book_avaibility_not_found = 0
book_description_found = 0
book_description_not_found = 0
book_category_found = 0
book_category_not_found = 0
book_image_url_found = 0
book_image_url_not_found = 0
book_review_found = 0
book_review_not_found = 0



RATING_DICTIONARY = {
    "One" : 1,
    "Two" : 2,
    "Three" : 3, 
    "Four" :  4,
    "Five" :  5 
}

FILEDNAMES_PP = [
    'Product_page_url',
    'Universal_product_code',
    'Title',
    'price_including_tax',
    'price_excluding_tax',
    'number_available',
    'product_description',
    'category',
    'review_rating',
    'image_url'
] # Création des entêtes pour les fichiers csv


url_homepage = "http://books.toscrape.com/"


def document_generator(url): # Permet de créer à l'aide d'un url un document
    url_request = requests.get(url)
    url_request.encoding = "utf-8"
    document = BeautifulSoup(url_request.text, 'html.parser')
    return document


# Création de la fonction pour télécharger les images

def download_image(url_image, relative_folder, file_name):  
    final_file_name = file_name + ".jpg"
    full_path = os.path.join(relative_folder, final_file_name) # os.path permet de manipuler les chemins (ici joindre)
    urllib.request.urlretrieve(url_image, full_path) # Télécharge un document vers un fichier local

def find_category_title(document_category):
    category_title = document_category.find('h1').string
    category_title = category_title.lower()
    category_title = category_title.replace(' ',"-")
    return category_title

def find_book_title(doc_product_page):
    book_title = doc_product_page.find('h1').string
    if book_title:
        print(f"Le titre du livre: {book_title}" )
        return str(book_title)

def find_book_upc(doc_product_page):
    global book_upc_found
    global book_upc_not_found
    upc_tag = doc_product_page.find('th', string = "UPC")
    if upc_tag:
        upc_pp = upc_tag.find_next('td').string
        book_upc_found += 1
        return(upc_pp)
    else:
        book_upc_not_found += 1
        return 'No upc Found'
    

def find_price_inc(doc_product_page):
    global book_price_inc_found
    global book_price_inc_not_found
    price_inc_tag = doc_product_page.find('th', string = "Price (incl. tax)")
    if price_inc_tag:
        price_inc = price_inc_tag.find_next('td').string
        book_price_inc_found += 1
        return price_inc
    else:
        book_price_inc_not_found += 1

def find_price_excl(doc_product_page):
    global book_price_excl_found
    global book_price_excl_not_found
    price_excl = None
    price_excl_tag = doc_product_page.find('th', string = "Price (excl. tax)")
    if price_excl_tag:
        price_excl = price_excl_tag.find_next('td').string
        book_price_excl_found += 1
        print(f"Le prix du livre taxe excluse: {price_excl}" )
        return price_excl
    else:
        book_price_excl_not_found += 1
        print(f"Le prix du livre taxe excluse n'a pas été trouvé" )

def find_number_available(doc_product_page):
    global book_avaibility_found
    global book_avaibility_not_found
    number_available_tag = doc_product_page.find('th', string="Availability")
    if number_available_tag:
        number_available_string = number_available_tag.find_next('td').string
        number_available_match = re.search(r'\d+', number_available_string) # Regex qui récupère seuelement les digits
        number_available = number_available_match.group()
        print(f"Il reste {number_available} exemplaires" )
        book_avaibility_found +=1
        return number_available
    else:
        book_avaibility_not_found += 1
    
def find_description(doc_product_page):
    global book_description_found
    global book_description_not_found
    book_description_tag = doc_product_page.find("h2", string ="Product Description")
    if book_description_tag:
        book_description = book_description_tag.find_next('p').string
        print(f"La description du livre: {book_description}")
        book_description = str(book_description)
        book_description_found +=  1  
        return book_description      
    else:
        book_description = "La descritpion de ce produit n'a pas pu être trouvée"
        book_description_not_found += 1
        return "La description n'a pas été trouvée"

def find_category_book(doc_product_page): 
    global book_category_found
    global book_category_not_found
    book_category_tag = doc_product_page.find('a', string = 'Books')
    book_category = book_category_tag.find_next("a").string
    if book_category: 
        book_category_found += 1
        print(f"La catégorie du livre: {book_category}")
        return book_category
    else: 
        book_category_not_found += 1

def url_join(base_url, relative_url):
    return urljoin(base_url, relative_url)


def find_image_url(doc_product_page, base_url): 
    global book_image_url_found
    global book_image_url_not_found
    relative_url = None
    tag_img_product_page= doc_product_page.find('img')
    relative_url = tag_img_product_page['src']
    absolute_url = urljoin(base_url, relative_url)
    if absolute_url:
        book_image_url_found += 1
        return absolute_url
    else:
        book_image_url_not_found += 1

def find_book_review(doc_product_page):
    global book_review_found
    global book_review_not_found
    review = None
    review_tag = doc_product_page.find('p', class_= 'star-rating')
    if review_tag:
        review_classes = review_tag['class'] # On utilise 'class' comme clé
        review = review_classes[1] # Je récupère dans la liste la note
        for x in RATING_DICTIONARY:
                    if review == x: 
                        review = RATING_DICTIONARY[x]
        book_review_found += 1
        return review
    else:
        book_review_not_found += 1


def find_categories(url, base_url):
    relative_url = None
    category_list = []
    all_ul_class_nav = url.find('ul', class_='nav nav-list')
    all_li = all_ul_class_nav.find_all('li')
    for li in all_li[1:]:    
        all_li_a = li.find("a") # On recherche les liens
        if all_li_a and "href" in all_li_a.attrs: # Utilisation d'attribut comme clé
            relative_url = all_li_a['href']
            category_url = url_join(base_url, relative_url)
            category_list.append(category_url)
            
    return category_list



def find_books_url(doc_category, base_url):
    url_books_list = []
    all_h3_book_category_tag = doc_category.find_all('h3')
    for tag in all_h3_book_category_tag:
        all_h3_a = tag.find("a") # On recherche les liens
        if all_h3_a and "href" in all_h3_a.attrs: # Utilisation d'attribut comme clé
            relative_url = all_h3_a['href']
            book_url = url_join(base_url, relative_url)
            url_books_list.append(book_url)
    return url_books_list

def is_there_next_page(document): # Fonction qui établie s'il y a une page suivante
    li_next = document.find('li', class_= 'next')
    if li_next:
        return True
    else: 
        return False
    
def next_page_url(document , current_url): # Fonction qui retrouve l'url de la prochaine page
    li_next = document.find('li', class_= 'next')
    li_next_a = li_next.find("a")
    relative_url = li_next_a['href']
    next_page_url = url_join(current_url, relative_url)
    return next_page_url

def full_page_search(url_book): # Recherche intégrale d'un livre ainsi que le téléchargement
    book_document = document_generator(url_book)
    url = url_book
    upc_pp = find_book_upc(book_document)
    book_title = find_book_title(book_document)
    price_inc = find_price_inc(book_document)
    price_excl = find_price_excl(book_document)
    number_available = find_number_available(book_document)
    book_description = find_description(book_document)
    book_category = find_category_book(book_document)
    review = find_book_review(book_document)
    url_image_product_page = find_image_url(book_document,url_book)

    # Download image
    file_name = re.sub("[\W]","-", book_title) # On substitue tous les caractères spéciaux pour l'ecriture de chemin avec la Regex \W
    folder_name = 'Images'
    download_image(url_image_product_page, folder_name, file_name)

    Book_dictionnary = ({
                    'Product_page_url' : url,
                    'Universal_product_code': upc_pp,
                    'Title' : book_title,
                    'price_including_tax' : price_inc,
                    'price_excluding_tax' : price_excl,
                    'number_available' : number_available,
                    'product_description': book_description,
                    'category' : book_category,
                    'review_rating' : review, 
                    'image_url' : url_image_product_page
                    }) # Création du dictionnaire avec toutes les clés et valeurs
    
    return Book_dictionnary


def function_category_search(document_category, url_category): # Fonction Recherche par catégorie
    category_books_data = []
    while True:
        document_category = document_generator(url_category)
        list_url_books = find_books_url(document_category, url_category)

        for url in list_url_books:
            book_dictionary = full_page_search(url)
            category_books_data.append(book_dictionary)

        if is_there_next_page(document_category):
            url_category = next_page_url(document_category, url_category)
        else:
            break
    return category_books_data 


# Creation premier document

document_homepage = document_generator(url_homepage)
    
 # Récupération des catégories

list_categories = find_categories(document_homepage, url_homepage)

for category in list_categories:
    document_category = document_generator(category)
    category_title = find_category_title(document_category)
    with open(f'{category_title}.csv', "w", newline ='', encoding='utf-8') as csvfile: # Ouverte/ Création de fichier csv
        writer = csv.DictWriter(csvfile, delimiter= ',', fieldnames= FILEDNAMES_PP)
        writer.writeheader()
        category_books_data = function_category_search(category, category)
        for book in category_books_data:
            writer.writerow(book)




print("=== Résumé du traitement des livres ===")
print(f"Total books processed: {total_book_number}")
print(f"Processed book counter: {processed_book_counter}")
print(f"Book UPCs found: {book_upc_found}, not found: {book_upc_not_found}")
print(f"Prices (incl. tax) found: {book_price_inc_found}, not found: {book_price_inc_not_found}")
print(f"Prices (excl. tax) found: {book_price_excl_found}, not found: {book_price_excl_not_found}")
print(f"Availability found: {book_avaibility_found}, not found: {book_avaibility_not_found}")
print(f"Descriptions found: {book_description_found}, not found: {book_description_not_found}")
print(f"Categories found: {book_category_found}, not found: {book_category_not_found}")
print(f"Image URLs found: {book_image_url_found}, not found: {book_image_url_not_found}")
print(f"Review ratings found: {book_review_found}, not found: {book_review_not_found}")
