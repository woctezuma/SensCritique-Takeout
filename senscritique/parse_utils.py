import requests
from bs4 import BeautifulSoup


def get_item_id(soup_name):
    return soup_name[0].attrs['id'].replace('product-title-', '')


def get_review_id(soup_name):
    return soup_name[0].attrs['data-sc-review-id']


def get_num_pages(url):
    soup = BeautifulSoup(requests.get(url).content, 'lxml')

    collection_pages = soup.find_all('a', {'class': 'eipa-anchor'})

    try:
        num_pages = int(collection_pages[-1].attrs['data-sc-pager-page'])
    except IndexError:
        num_pages = 1

    return num_pages
