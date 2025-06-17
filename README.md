Projet: Analyse marché BooktoScrape
Auteur: Samuel Guillot

---

1. Résumé Projet: 
Ce programme est la version bêta d'une analyse de marché qui 'scrape' les informations du site BookstoScrape.com
Ce programme est conçu pour être utiliser à la demande pour collecter les informations des livres en temps réel. 

2. Nécessités au préalable
Pour exécuter le scripte il est requis d'avoir installer python3 sur votre système ainsi que d'une connection internet. 

3. Installation et Set up
Cloner le repository:
git clone https://github.com/SamuelGuillot/projet1_analyse_marche.git

Installer les dépendences: 
pip install -r requirements.txt

4. Executer le scripte dans votre environnement virtuel
Executer main.py

5. Exports
Le scripte générera des fichiers CSV pour chaque catégorie. 
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

Un nouveau dossier 'Images' sera créé. Ce dossier contiendra toutes les images téléchargées des livres. 

ATTENTION: Ce scripte fonctionne seulement pour le site Booktoscrape.com

