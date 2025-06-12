from bs4 import BeautifulSoup
import requests
import csv
import re
from urllib.parse import urljoin
# import urllib.request  # Puis-je seulement faire urllib import

# PHASE 1

# Creation du document qui scrape un seul livre
'''
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
livre_quantite_list = re.findall(r'd+', livre_quantite_string) #RAJOUTER ANTISLASH GAUCHE DE d
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

print(f"L'URL de l'image du livre est: {url_image_product_page}") #RAJOUTER ANTISLASH DROITE DE L

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
'''
# PHASE 2 

# Récupération de l'url de la page d'accueil

url_homepage = "http://books.toscrape.com/"
url_request_homepage = requests.get(url_homepage)
url_request_homepage.encoding = "utf-8" # Je m'assure de l'encodage pour les éléments comme €

doc_homepage = BeautifulSoup(url_request_homepage.text, 'html.parser')


rating_dictionary = {
    "One" : {"français": "Une", "int": 1 },
    "Two" : {"français": "Deux", "int": 2 },
    "Three" : {"français": "Trois", "int": 3 },
    "Four" : {"français": "Quatre", "int": 4 },
    "Five" : {"français": "Cinq", "int": 5 } # Création du dictionnaire avant la boucle
}

fieldnames_pp = [
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

# Récupération des liens des catégories de livres


category_list = []

# Les catégories se trouvent dans une balise <a> dans une balise <li> / dans une balise <ul> de classe "nav nav-list" 

all_ul_class_nav = doc_homepage.find('ul', class_='nav nav-list')
all_li = all_ul_class_nav.find_all('li')

# Pour chaque balise <li> sauf la première, on retrouve la balise <a> et nettoie son contenu pour en faire un url  par la suite

for li in all_li[1:]: # On saute le premier résultat qui est "Books"
    a_tag = li.find("a")
    category = a_tag.string.strip()
    category = category.replace(' ','-')
    category = category.lower()
    category_list.append(category)

url_category_base = "http://books.toscrape.com/catalogue/category/books/"
url_category_list = []

# Dans l'url des catégories les liens ont un numéro d'index +2 que l'on ajoute au lien

category_file_for_naming =[]


index = 2
for category in category_list:
    print(category)
    category_file_for_naming.append(category)
    url_category = f'{url_category_base}{category}_{str(index)}/index.html'
    url_category_list.append(url_category)
    index += 1


for url_category, name_for_file in zip (url_category_list, category_file_for_naming):

    with open(f'{name_for_file}.csv', "w", newline ='', encoding='utf-8') as csvfile: 
        writer = csv.DictWriter(csvfile, delimiter= ',', fieldnames= fieldnames_pp)
        writer.writeheader()
    # for x in range(len(category_file_for_naming)):
    #     name_for_file = category_file_for_naming[x-1]






        # Pour chaque lien de première page de catégorie on cherche le nombre de livres afin de savoir combien de pages chaque catégorie a
        url_request_categorie_page = requests.get(url_category)
        url_request_categorie_page.encoding = "utf-8" # Je m'assure de l'encodage
        doc_categorie_page = BeautifulSoup(url_request_categorie_page.text, 'html.parser') # Construction d'un document afin de trouver le nombre de livres par catégorie
        form_horizontal = doc_categorie_page.find('form', class_="form-horizontal")
        strong_tag = form_horizontal.find('strong') 
        number_books = int(strong_tag.text.strip()) # Transformation en int afin de faire des opérations avec
        print(f'Le nombre de livres {number_books}') # On retrouve le nombre total de livres pour cette catégorie
        nombre_pages = 1 + number_books // 20 # Floor division qui arrondit au plus bas pour déterminer le nombre total de pages
        print(f'Le nombre de pages est {nombre_pages}')


        

        if number_books > 20:
            print('changement de url car il y a plus de 20 livres')
            url_category = url_category.replace('index','page-1') # Seulement les pages qui ont plus de 20 livres ont besoin de leur url changé
            
        print(url_category)
    
    
    # url_base = "https://books.toscrape.com/catalogue/category/books/nonfiction_13/"
        url_base = url_category.replace("index.html","") 
        url_base = url_base.replace("page-1.html", '')
        
        
        list_url_to_search = [] # Liste dans laquelle nous allons chercher les livres
        page_counter = 1


        list_url_to_search.append(url_category) # On ajoute la première page de chaque catégorie dans une liste

        # Création des liens des pages suivantes

        books_counter = 0
        for book in range(number_books):
            books_counter += 1
            print(books_counter)
            if books_counter % 20 == 0: # Changement de page tous les 20 livres
                page_counter += 1
                print(f'Changement de page / url. Page n°{page_counter}')
                url_category = url_base + "page-" + str(page_counter) + ".html" # On change la page de l'url
                print(f'Nouvel url après page changée:{url_category}')
                if url_category not in list_url_to_search: # Si le lien n'est pas déjà dans la liste (éviter le premier lien qui est présent)
                    list_url_to_search.append(url_category) # On ajoute les liens des pages suivantes à la liste
        

        print(list_url_to_search)


        # product_counter = 0
        

        url_base_livre = "https://books.toscrape.com/catalogue/"
        # url_category_list = []
        url_individual_books_list = []
        titre_categorie_list = []



        for url in list_url_to_search: # Pour chaque url de page
            # Création d'un document
            url_request_category_page = requests.get(url)
            url_request_category_page.encoding = "utf-8" # Je m'assure de l'encodage pour les éléments comme €
            doc_category_page = BeautifulSoup(url_request_category_page.text, 'html.parser')



            all_h3_livre_categorie_tag = doc_category_page.find_all('h3')
            for tag in all_h3_livre_categorie_tag:
                all_h3_a = tag.find("a") # On recherche les liens
                if all_h3_a and "href" in all_h3_a.attrs: # Utilisation d'attribut comme clé
                    relative_url = all_h3_a['href']
                    extracted_url = relative_url.replace("../../../", "")
                    full_book_url = url_base_livre + extracted_url
                    url_individual_books_list.append(full_book_url) # Création d'une liste avec les liens de chaque livre
                if 'title' in all_h3_a.attrs:
                    titre_categorie_list.append(all_h3_a['title'])   

        # print(url_individual_books_list)
        # print(len(url_individual_books_list))
        # print(titre_categorie_list)

        # Récupération des informations d'un seul livre



            for url in url_individual_books_list:         
                print('================NOUVELLE_RECHERCHE_LIVRE=======')
                url_request_product_page = requests.get(url)
                url_request_product_page.encoding = "utf-8" # Je m'assure de l'encodage pour les éléments comme €

                doc_product_page = BeautifulSoup(url_request_product_page.text, 'html.parser')



                product_page_book_name = doc_product_page.find('h1').string
                print(f"Le titre du livre: {product_page_book_name}" )
                product_page_book_name = str(product_page_book_name) # conversion de la navigable str en str
                # book_name_und = product_page_book_name.replace(' ','-')
                # print(book_name_und)
                
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
                if product_page_description_tag is not None:
                    product_page_description = product_page_description_tag.find_next('p').string
                    print(f"La description du livre: {product_page_description}")
                    product_page_description = str(product_page_description) # 
                else:
                    product_page_description = "La descritpion de ce produit n'a pas pu être trouvée"
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


                # Téléchargement de l'image 

                

                Book_dictionnary = ({
                    'Product_page_url' : url,
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
                
                print(Book_dictionnary)

                # # On extrait la catégorie du livre pour la comparer à la liste

                # current_category = category_product_page
                # current_category = current_category.replace(' ','-')
                # current_category = current_category.lower()

                # if current_category 


                writer.writerow(Book_dictionnary)

                