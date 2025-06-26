import os
import urllib.request
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

def document_generator(url):
    url_request = requests.get(url)
    url_request.encoding = "utf-8"
    return BeautifulSoup(url_request.text, 'html.parser')

def download_image(url_image, relative_folder, file_name):
    final_file_name = file_name + ".jpg"
    full_path = os.path.join(relative_folder, final_file_name)
    urllib.request.urlretrieve(url_image, full_path)

def url_join(base_url, relative_url):
    return urljoin(base_url, relative_url)
