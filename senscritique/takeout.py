import json
import pathlib
import time

import requests
from bs4 import BeautifulSoup


def get_base_url(user_name=None):
    url = 'https://www.senscritique.com/'
    if user_name is not None:
        url += user_name + '/'
    return url


def get_collection_url(user_name, page_no=1):
    url = get_base_url(user_name=user_name) + 'collection/all/all/all/all/all/all/all/all/all/page-' + str(page_no)
    return url


def get_item_id(soup_name):
    return soup_name[0].attrs['id'].strip('product-title-')


def improve_readability(text):
    return text.replace('\n', '').replace('\t', '')


def read_soup_result(soup_result):
    text = [improve_readability(sample.text) for sample in soup_result]

    if len(text) == 1:
        text = text[0]

    if len(text) == 0 or text == ' ' or text == '-':
        text = None

    return text


def parse_collection_page(user_name='wok', page_no=1):
    url = get_collection_url(user_name=user_name, page_no=page_no)
    soup = BeautifulSoup(requests.get(url).content, 'lxml')

    collection_items = soup.find_all('li', 'elco-collection-item')

    data = dict()
    for item in collection_items:
        user_rating = item.find_all('div', {'class': 'elco-collection-rating user'})
        name = item.find_all('a', {'class': 'elco-anchor'})
        game_system = item.find_all('span', {'class': 'elco-gamesystem'})
        release_date = item.find_all('span', {'class': 'elco-date'})
        description = item.find_all('p', {'class': 'elco-baseline elco-options'})
        author = item.find_all('a', {'class': 'elco-baseline-a'})
        site_rating = item.find_all('a', {'class': 'erra-global'})

        item_id = get_item_id(name)

        data[item_id] = dict()
        data[item_id]['name'] = read_soup_result(name)
        data[item_id]['author'] = read_soup_result(author)
        data[item_id]['user_rating'] = read_soup_result(user_rating)
        data[item_id]['site_rating'] = read_soup_result(site_rating)
        data[item_id]['description'] = read_soup_result(description)
        data[item_id]['game_system'] = read_soup_result(game_system)
        data[item_id]['release_date'] = read_soup_result(release_date)

    return data


def get_collection_num_pages(user_name='wok'):
    url = get_collection_url(user_name=user_name, page_no=1)
    soup = BeautifulSoup(requests.get(url).content, 'lxml')

    collection_pages = soup.find_all('a', {'class': 'eipa-anchor'})

    try:
        num_pages = int(collection_pages[-1].attrs['data-sc-pager-page'])
    except IndexError:
        num_pages = 1

    return num_pages


def parse_collection(user_name='wok'):
    num_pages = get_collection_num_pages(user_name=user_name)

    print('Parsing {} pages of collection by {}.'.format(num_pages, user_name))

    data = dict()
    for page_no in range(num_pages):
        real_page_no = page_no + 1

        print('Parsing collection page n°{}'.format(real_page_no))

        page_data = parse_collection_page(user_name=user_name, page_no=real_page_no)

        print('[page n°{}] num_items = {}'.format(real_page_no, len(page_data)))
        data.update(page_data)

    return data


def get_data_folder():
    return 'data/'


def get_filename_separator():
    return '_'


def get_save_filename(user_name='wok', data_type='collection'):
    json_filename_suffix = '.json'

    sep = get_filename_separator()

    # Get current day as yyyymmdd format
    date_format = '%Y%m%d'
    current_date = time.strftime(date_format)

    # Database filename
    save_filename = current_date + sep + user_name + sep + data_type + json_filename_suffix

    return save_filename


def print_data(data, file_name=None):
    if file_name is None:
        print(data)
    else:
        # Reference of the following line: https://stackoverflow.com/a/14364249
        pathlib.Path(get_data_folder()).mkdir(parents=True, exist_ok=True)

        with open(file_name, 'w', encoding='utf8') as f:
            f.write(json.dumps(data))

    return


def parse(user_name='wok', data_type='collection'):
    if data_type == 'collection':
        data = parse_collection(user_name=user_name)
    else:
        data = dict()

    return data


def parse_and_cache(user_name='wok', data_type='collection'):
    save_file_name = get_data_folder() + get_save_filename(user_name=user_name, data_type=data_type)

    if pathlib.Path(save_file_name).is_file():
        print('File ' + save_file_name + ' already exists.')
        with open(save_file_name, 'r', encoding='utf8') as f:
            data = json.load(f)
    else:
        data = parse(user_name=user_name, data_type=data_type)
        if len(data) > 0:
            print_data(data, save_file_name)

    sentence = '[' + data_type + ' by ' + user_name + '] num_items = {}'
    print(sentence.format(len(data)))

    return data


def main():
    data = parse_and_cache(user_name='عمرالعرفاوي', data_type='collection')

    return True


if __name__ == '__main__':
    data = parse_and_cache(user_name='wok', data_type='collection')
