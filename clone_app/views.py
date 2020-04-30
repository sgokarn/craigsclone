from django.shortcuts import render
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup

BASE_URL = []
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    BASE_URL = []
    return render(request, template_name='clone_app/home.html')


def city(request):
    city_name = request.POST.get('destination')
    base_url = 'https://' + city_name + '.craigslist.org/search/?query={}'
    print(base_url)
    BASE_URL.append(base_url)
    return render(request, template_name='clone_app/city.html')


def search(request):
    query = request.POST.get('search')

    final_url = BASE_URL[len(BASE_URL)-1].format(quote_plus(query))

    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []
    for post in post_listings:
        # extract - title
        post_title = post.find(class_='result-title').text

        # extract - url
        post_url = post.find('a')['href']

        # extract - price if it has any
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        # extract - if it has an image associated with it
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find('a')['data-ids'].split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            # print(post_image_url)
        else:
            # post_image_url = 'https://craigslist.org/images/peace.jpg'
            post_image_url =  'https://fsb.zobj.net/crop.php?r=ghDw07TGCGLagKoPKJBeBgufFC877dhpIWhqTKAuwSn5YP8KGVA2Bk1GbSg3FHrUcZTX8n7dIIDa4Dx13qBG4afz8qz_Q4LsaVqaQyfafG6FCvHTSwQ2T8AAxO7530OpCeC1kLRGrXfJrazP'

        final_postings.append((post_title, post_url, post_price, post_image_url))

    low_to_high = final_postings.copy()
    na = []
    i = 0
    while i < len(low_to_high):
        if low_to_high[i][2] == 'N/A':
            na.append(low_to_high.pop(i))
        else:
            i += 1
    low_to_high.sort(key= lambda x: int(x[2].split('$')[1]))
    high_to_low = low_to_high.copy()
    high_to_low = high_to_low[::-1]

    return_stuff = {
        'search': query,
        'final_postings': final_postings,
        'low_to_high': low_to_high,
        'high_to_low': high_to_low,
        'N/A': na,
    }

    return render(request, template_name='clone_app/city.html', context=return_stuff)

