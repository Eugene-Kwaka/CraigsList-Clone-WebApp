import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models

BASE_CRAIGSLIST_URL = 'https://kenya.craigslist.org/search/bbb?query={}'
# Create your views here.


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    # Getting the webpage, creating a Response object
    response = requests.get(final_url)
    # Extracting the source code of the page
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    #post_title = post_listings[0].find(class_='result-title').text
    #post_url = post_listings[0].find('a').get('href')
    #post_price = post_listings[0].find(class_='result-price')

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price')
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-imgid'):
            post_image_id = post.find(
                class_='result-image').get('data-imgid').split('_')[0].split('_')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append(
            (post_title, post_url, post_price, post_image_url))

    # print(post_title)
    # print(post_url)
    # print(post_price)

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
