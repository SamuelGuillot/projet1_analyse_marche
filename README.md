# Projet: Analyse marché BooktoScrape
Auteur: Samuel Guillot

---

##  Description du projet  
Ce programme est la version bêta d'une analyse de marché qui 'scrape' les informations du site **BookstoScrape.com**
Ce programme est conçu pour être utiliser à la demande pour collecter les informations des livres en temps réel et à pour but de établir une Pipeline **ETL**.  

**Extraction, transformation, chargement (ETL)** est un processus automatisé qui prend les données brutes, extrait l'information nécessaire à l'analyse, la transforme en un format qui peut répondre aux besoins opérationnels.  

 Ici nous extractons les données sur les pages html du site de vente de livres, les transormons pour pouvoir ensuite les écrire dans des documents csv.



## Installation et lancement du programme: 

Pour exécuter le scripte il est **requis** d'avoir installer **python3** sur votre système ainsi que d'une connection internet.  

Il faut ensuite créer un environement virtuel.  

**pip install -r requirements.txt** dans le terminal de votre environement virtuel.

**Executer le fichier main.py** afin de lancer le programme. 

Le scripte va alors se rendre sur le site bookstoscrape.com et collecter les caractéristiques de chacun des livres. 

Le scripte générera des fichiers CSV pour chacune des catégories de livres. 
Les éléments relevés sont: 
- Product Page URL
- Universal Product Code (UPC)
- Title
- Price Including Tax
- Price Excluding Tax
- Number Available
- Product Description
- Category
- Review Rating
- Image URL

Un nouveau dossier **'Images'**  sera créé à la racine du repository. Ce dossier contiendra toutes les images téléchargées des livres. 

**ATTENTION**: Ce scripte fonctionne seulement pour le site Booktoscrape.com

