import re
import requests
from bs4 import BeautifulSoup

from senscritique.parse_utils import get_item_id
from senscritique.utils import get_base_url, read_soup_result


def get_collection_url(user_name, page_no=1):
    url = (
        get_base_url(user_name=user_name)
        + 'collection/all/all/all/all/all/all/all/all/all/page-'
        + str(page_no)
    )
    return url


def parse_collection_page(user_name='wok', page_no=1, verbose=False):
    url = get_collection_url(user_name=user_name, page_no=page_no)
    soup = BeautifulSoup(requests.get(url).content, 'lxml')

    collection_items = soup.find_all('li', 'elco-collection-item')

    data = {}
    for item in collection_items:
        user_rating = item.find_all('div', {'class': 'elco-collection-rating user'})
        item_type_p = item.find('div', {'class': re.compile("^d-media-[a-z]+$")})
        item_type = "unknown"
        if item_type_p:
            if 'data-sc-play-type' in item_type_p:
                item_type = item_type_p['data-sc-play-type']
        name = item.find_all('a', {'class': 'elco-anchor'})
        game_system = item.find_all('span', {'class': 'elco-gamesystem'})
        release_date = item.find_all('span', {'class': 'elco-date'})
        description = item.find_all('p', {'class': 'elco-baseline elco-options'})
        author = item.find_all('a', {'class': 'elco-baseline-a'})
        site_rating = item.find_all('a', {'class': 'erra-global'})

        item_id = get_item_id(name)

        data[item_id] = {}
        data[item_id]['name'] = read_soup_result(name)
        data[item_id]['author'] = read_soup_result(author)
        data[item_id]['user_rating'] = read_soup_result(user_rating)
        data[item_id]['site_rating'] = read_soup_result(site_rating)
        data[item_id]['description'] = read_soup_result(description)
        data[item_id]['game_system'] = read_soup_result(game_system)
        data[item_id]['release_date'] = read_soup_result(release_date)
        data[item_id]['item_type'] = item_type

        if verbose:
            print(
                '-   item n°{}: {}'.format(
                    item_id,
                    data[item_id]['name'],
                ),
            )

    return data
