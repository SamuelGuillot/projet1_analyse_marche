from bs4 import BeautifulSoup
import requests
import csv

# Creation du document qui scrape un seul livre

url_product_page = "https://books.toscrape.com/catalogue/the-requiem-red_995/index.html"

url_request_product_page = requests.get(url_product_page)

doc_product_page = BeautifulSoup(url_request_product_page.text, 'html.parser')


# Creation du document qui scrape tous les livres

# url_all = "https://books.toscrape.com/"

# url_request_all = requests.get(url_all)

# doc_all = BeautifulSoup(url_request_all.text, 'html.parser')

print('----------------------------------------------------')

# Récupération des informations d'un seul livre

# Création d'une liste avec les informations contenu dans les td pour accès facile

liste_info_product_page = []
result = doc_product_page.find_all('td')
for info in result: 
    liste_info_product_page.append(info.string.strip())
print(liste_info_product_page)

# Url de la page du produit

print(f"L'url de la page du livre est: {url_product_page}")

print('------------------------------------')

# Titre

product_page_book_name = doc_product_page.find('h1').string
print(f"Le titre du livre: {product_page_book_name}" )
product_page_book_name = str(product_page_book_name) # conversion de la navigable str en str

print('------------------------------------')

# Universal_product_code (upc)

upc_product_page = liste_info_product_page[0]
print(f"L'upc du livre est: {upc_product_page}" )

print('------------------------------------')

# Prix taxe incluse
prix_taxe_incluse_product_page = liste_info_product_page[3]
print(f"Le prix du livre avec la taxe incluse est : {prix_taxe_incluse_product_page}")

print('------------------------------------')

# Prix taxe excluse
prix_taxe_excluse_product_page = liste_info_product_page[2]
print(f"Le prix du livre avec la taxe excluse est : {prix_taxe_excluse_product_page}")

print('------------------------------------')

# Nombre d'exmplaires restant
number_available_product_page = None
quantite_livres_parenthese = liste_info_product_page[5].split() # On retrouve l'info dans la liste grace à l'index que l'on sépare mot à mot
quantite_livres = quantite_livres_parenthese[2].replace("(",'') # On remplace la parenthèse par du vide pour isoler le nombre
number_available_product_page = quantite_livres

print(f"Il reste {number_available_product_page} exemplaires")

print('------------------------------------')

# Description du produit

product_page_description = doc_product_page.find_all("p")[3].string
print(f"La description du livre: {product_page_description}")
product_page_description = str(product_page_description) # conversion de la navigable str en str

print('------------------------------------')

# Catégorie du livre

category_product_page = doc_product_page.find_all('a')[3].string
print(f"La catégorie du livre: {category_product_page}")
category_product_page = str(category_product_page) # conversion de la navigable str en str

print('------------------------------------')

# Review

# review_product_page = liste_info_product_page[4]
# print(review_product_page)

all_p = doc_product_page.find_all("p")


for p_tag in all_p:
    classes_of_p_tag = p_tag.get('class') # On récupère les classes
    # print(classes_of_p_tag)

    if "star-rating" in classes_of_p_tag: 
        for words in classes_of_p_tag:
            if words != "star-rating": # si le mot n'est pas star-rating c'est le bon
                isolated_review_product_page_en = words
                break
        break
print(isolated_review_product_page_en)

print('------------------------------------')

# Traduction de la review en français et en int

# if isolated_review_product_page == "One":
#     isolated_review_product_page = "Une"
#     isolated_review_product_page_int = 1
# elif isolated_review_product_page == "Two":
#     isolated_review_product_page = "Deux"
#     isolated_review_product_page_int = 2
# elif isolated_review_product_page == "Three":
#     isolated_review_product_page = "Trois"
#     isolated_review_product_page_int = 3
# elif isolated_review_product_page == "Four":
#     isolated_review_product_page = "Quatre"
#     isolated_review_product_page_int = 4
# elif isolated_review_product_page == "Five":
#     isolated_review_product_page = "Cinq"
#     isolated_review_product_page_int = 5
    

rating_dictionary = {
    "One" : {"français": "Une", "int": 1 },
    "Two" : {"français": "Deux", "int": 2 },
    "Three" : {"français": "Trois", "int": 3 },
    "Four" : {"français": "Quatre", "int": 4 },
    "Five" : {"français": "Cinq", "int": 5 }
}

if isolated_review_product_page_en in rating_dictionary:
    inner_dictionnary = rating_dictionary.get(isolated_review_product_page_en)
    isolated_review_product_page_fr = inner_dictionnary.get("français")
    isolated_review_product_page_int = inner_dictionnary.get("int")

print(f"Le livre est a reçu la note de {isolated_review_product_page_fr} étoile sur Cinq ou {isolated_review_product_page_int}/5★")

print('------------------------------------')

# URL de l'image

image_url_product_page = None
tag_img_product_page= doc_product_page.find('img')
image_url_product_page = tag_img_product_page['src']
print(image_url_product_page) # A VOIR SI SUFFISANT


# Ecrire les données dans un fichier csv

en_tete = ['product_page_url','universal_product_code','title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url']

with open('data.csv','w') as csv_file:
    writer = csv.writer(csv_file,delimiter=',') 
    writer.writerow(en_tete)
    for product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url in zip(url_product_page, upc_product_page,product_page_book_name,prix_taxe_incluse_product_page,prix_taxe_excluse_product_page,number_available_product_page,product_page_description,category_product_page,isolated_review_product_page_fr,image_url_product_page):

        writer.writerow([product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url])

# print(type(url_product_page))
# print(type(upc_product_page))
# print(type(product_page_book_name))
# print(type(prix_taxe_incluse_product_page))
# print(type(prix_taxe_excluse_product_page))
# print(type(number_available_product_page))
# print(type(product_page_description))
# print(type(category_product_page))
# print(type(image_url_product_page))


