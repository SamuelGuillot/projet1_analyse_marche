import csv
from constants import FILEDNAMES_PP
from book_details import full_page_search
from helpers import document_generator, url_join

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

def find_category_title(document_category):
    category_title = document_category.find('h1').string
    category_title = category_title.lower().replace(' ', "-")
    return category_title

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

# MAIN DEF
def books_to_scrape(URL_HOMEPAGE):
    document_homepage = document_generator(URL_HOMEPAGE)
    list_categories = find_categories(document_homepage, URL_HOMEPAGE)

    for category in list_categories:
        document_category = document_generator(category)
        category_title = find_category_title(document_category)
        with open(f'{category_title}.csv', "w", newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=FILEDNAMES_PP)
            writer.writeheader()
            category_books_data = function_category_search(document_category, category)
            for book in category_books_data:
                writer.writerow(book)
