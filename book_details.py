import re
import os
from constants import RATING_DICTIONARY
from urllib.parse import urljoin
from helpers import document_generator, download_image

def find_book_title(doc_product_page):
    book_title = doc_product_page.find('h1').string
    if book_title:
        print(f"Le titre du livre: {book_title}")
        return str(book_title)
    

def find_book_upc(doc_product_page):
    upc_tag = doc_product_page.find('th', string="UPC")
    if upc_tag:
        return upc_tag.find_next('td').string
    else: 
        return ""

def find_price_inc(doc_product_page):
    price_inc_tag = doc_product_page.find('th', string = "Price (incl. tax)")
    if price_inc_tag:
        price_inc = price_inc_tag.find_next('td').string
        return price_inc
    else:
        print(f"Le prix du livre taxe excluse n'a pas été trouvé")
        return ''


def find_price_excl(doc_product_page):
    price_excl = None
    price_excl_tag = doc_product_page.find('th', string = "Price (excl. tax)")
    if price_excl_tag:
        price_excl = price_excl_tag.find_next('td').string
        return price_excl
    else:
        print(f"Le prix du livre taxe excluse n'a pas été trouvé" )
        return ""


def find_number_available(doc_product_page):
    number_available_tag = doc_product_page.find('th', string="Availability")
    if number_available_tag:
        number_available_string = number_available_tag.find_next('td').string
        number_available_match = re.search(r'\d+', number_available_string) # TRANSFORMATION Regex qui récupère seuelement les digits
        number_available = number_available_match.group() #renvoit le résultat de la recherche
        return number_available
    else:
        print(f"Le nombre d'exemplaires n'a pas été trouvé" )
        return ''
    
def find_description(doc_product_page):
    book_description_tag = doc_product_page.find("h2", string ="Product Description")
    if book_description_tag:
        book_description = book_description_tag.find_next('p').string
        book_description = str(book_description)
        return book_description      
    else:
        print(f"La description n'a pas été trouvée" )
        return ""

def find_category_book(doc_product_page): 
    book_category_tag = doc_product_page.find('a', string = 'Books')
    book_category = book_category_tag.find_next("a").string
    if book_category: 
        print(f"La catégorie du livre: {book_category}")
        return book_category
    else: 
        print(f"La catégorie n'a pas été trouvée" )
        return ""


def url_join(base_url, relative_url):
    return urljoin(base_url, relative_url)

def find_image_url(doc_product_page, base_url): 
    relative_url = None
    tag_img_product_page= doc_product_page.find('img')
    relative_url = tag_img_product_page['src']
    absolute_url = urljoin(base_url, relative_url)
    if absolute_url:
        return absolute_url
    else:
        print(f"L'url de l'image du livre n'a pas été trouvée" )
        return ""


def find_book_review(doc_product_page):
    review = None
    review_tag = doc_product_page.find('p', class_= 'star-rating')
    if review_tag:
        review_classes = review_tag['class'] # On utilise 'class' comme clé
        review = review_classes[1] # Je récupère dans la liste la note
        for x in RATING_DICTIONARY:
                    if review == x: 
                        review = RATING_DICTIONARY[x] # TRANSFORMATION
        return review
    else:
        print(f"La note du livre n'a pas été trouvée" )
        return ""




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
    folder_name = 'Images'                      # Tranformation
    if not os.path.exists(folder_name): # Création d'un dosssier 'Images' s'il n'existe pas
        os.makedirs(folder_name)

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