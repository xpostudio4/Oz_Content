"""
This module crawl the webpage of the http://www.lpzoo.org and
gets it on the database.
"""
import requests
from bs4 import BeautifulSoup
from flask import Flask, current_app
from models import db, Animal

ROOT = 'http://www.lpzoo.org'
categories_list = [
    'http://www.lpzoo.org/animals/birds',
    'http://www.lpzoo.org/animals/mammals',
    'http://www.lpzoo.org/animals/reptiles',
    'http://www.lpzoo.org/animals/reptiles',
    'http://www.lpzoo.org/animals/amphibians',
    'http://www.lpzoo.org/animals/exhibits-animal-houses',
    'http://www.lpzoo.org/regenstein-african-journey',
    'http://www.lpzoo.org/mccormick-bear-habitat',
    'http://www.lpzoo.org/mccormick-bird-house',
    'http://www.lpzoo.org/regenstein-birds-prey-exhibit',
    'http://www.lpzoo.org/helen-brach-primate-house',
    'http://www.lpzoo.org/kovler-lion-house',
    'http://www.lpzoo.org/kovler-sea-lion-pool',
    'http://www.lpzoo.org/nature-boardwalk',
    'http://www.lpzoo.org/pritzker-family-childrens-zoo',
    'http://www.lpzoo.org/regenstein-small-mammal-reptile-house',
    'http://www.lpzoo.org/hope-b-mccormick-swan-pond',
    'http://www.lpzoo.org/waterfowl-lagoon',
    'http://www.lpzoo.org/regenstein-center-african-apes',
    'http://www.lpzoo.org/antelope-zebra-area',
    'http://www.lpzoo.org/farm-zoo',
    'http://www.lpzoo.org/node/16594',
]

def get_url_links(url):
    value = requests.get(url)
    c = value.content
    soup = BeautifulSoup(c)
    link_list = []
    for link in soup.find_all('a', href=True):
        if link['href'].startswith('http'):
            pass
            #link_list.append(link['href'])
        else:
            link_list.append(ROOT + link['href'])
    return filter_to_only_animals(link_list)


def filter_to_only_animals(url_list):
    start_text = '{0}{1}'.format(ROOT, '/animals/factsheet/')
    return [ link for link in url_list if link.startswith(start_text)]

def scrape_full_site(root):
    pending = [root]
    iterated = []
    while pending:
        actual_page = pending.pop()
        for link in get_url_links(actual_page):
            if not(link in pending or link in iterated or link == actual_page):
                pending.append(link)
        iterated.append(actual_page)
    return iterated


def get_animal_links(url_list):
    link_list = []
    for link in url_list:
        link_list.extend(get_url_links(link))
    return list(set(link_list))

def get_animal_name(page):
    return page.find("h1", {"class": "title"}).text

def get_page_data(link):
    """div afs_top_leftcol"""
    page_request = requests.get(link)
    page = BeautifulSoup(page_request.content)
    text = page.find("div", {"class": "afs_top_leftcol"}).text
    text += page.find("div", {"class": "afs_bottom"}).text
    image = page.find("img", {"class": "imagefield imagefield-field_picture"})['src']
    name = get_animal_name(page)
    return {'text':text, 'name': name, 'image': image, 'link': link}

def scrape_animal_page(link_list):
    animal_list = []
    for link in link_list:
        animal_list.append(get_page_data(link))
    return animal_list


if __name__ == '__main__':
    animal_links = get_animal_links(categories_list)
    print("Got animals webpage links")
    animals = scrape_animal_page(animal_links)
    print("Get scraping info from each animal")

    app = Flask(__name__)
    with app.app_context():
        for animal in animals:
            print("adding {} to the database".format(animal['name']))
            new_animal = Animal(name=animal['name'], text=animal['text'], url=animal['link'], picture_url=animal['image'])
            db.session.add(new_animal)
        db.session.commit()

