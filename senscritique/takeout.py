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


def get_critiques_url(user_name, page_no=1):
    url = get_base_url(user_name=user_name) + 'critiques#page-' + str(page_no) \
          + '/filter-all/universe-all/order-publication/'

    return url


def get_listes_url(user_name, page_no=1):
    url = get_base_url(user_name=user_name) + 'listes/all/all/likes/page-' + str(page_no)
    return url


def get_item_id(soup_name):
    return soup_name[0].attrs['id'].strip('product-title-')


def get_review_id(soup_name):
    return soup_name[0].attrs['data-sc-review-id']


def improve_readability(text):
    return text.replace('\n', '').replace('\t', '')


def read_soup_result(soup_result, simplify_text=True):
    if simplify_text:
        text = [improve_readability(sample.text) for sample in soup_result]
    else:
        text = [sample.text for sample in soup_result]

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


def parse_critiques_page(user_name='wok', page_no=1):
    url = get_critiques_url(user_name=user_name, page_no=page_no)
    soup = BeautifulSoup(requests.get(url).content, 'lxml')

    collection_items = soup.find_all('div', {'class': 'ere-box-main'})

    data = dict()
    for item in collection_items:
        overview = item.find_all('button', {'class': 'ere-review-overview'})
        title = item.find_all('h3', {'class': 'd-heading2 ere-review-heading'})
        excerpt = item.find_all('p', {'class': 'ere-review-excerpt'})
        game_system = item.find_all('span', {'class': 'ere-review-gamesystem'})
        rating = item.find_all('div', {'class': 'elrua-useraction-action'})
        link = item.find_all('a', {'class': 'ere-review-anchor'})
        footer = item.find_all('footer', {'class': 'ere-review-details'})

        item_id = get_review_id(overview)

        data[item_id] = dict()
        data[item_id]['title'] = read_soup_result(title)
        data[item_id]['excerpt'] = read_soup_result(excerpt)
        data[item_id]['game_system'] = read_soup_result(game_system)
        data[item_id]['rating'] = read_soup_result(rating)
        data[item_id]['link'] = link[0].attrs['href']
        data[item_id]['date'] = footer[0].find_all('time')[0].text

        full_review_url = get_base_url() + data[item_id]['link']
        full_soup = BeautifulSoup(requests.get(full_review_url).content, 'lxml')

        review_items = full_soup.find_all('div', {'class': 'd-grid-main'})

        for review_item in review_items:
            content = review_item.find_all('div', {'class': 'rvi-review-content'})
            stats = review_item.find_all('div', {'data-rel': 'likebar'})

            data[item_id]['content'] = read_soup_result(content)
            data[item_id]['upvotes'] = stats[0].attrs['data-sc-positive-count']
            data[item_id]['downvotes'] = stats[0].attrs['data-sc-negative-count']

    return data


def parse_listes_page(user_name='wok', page_no=1):
    url = get_listes_url(user_name=user_name, page_no=page_no)
    soup = BeautifulSoup(requests.get(url).content, 'lxml')

    collection_items = soup.find_all('li', {'class': 'elth-thumbnail by3'})

    data = dict()
    for item in collection_items:
        category = item.find_all('span', {'class': 'elth-universe-label type-1'})
        overview = item.find_all('a', {'class': 'elth-thumbnail-title'})

        link = overview[0].attrs['href']

        item_id = int(link.rsplit('/')[-1])

        data[item_id] = dict()
        data[item_id]['category'] = read_soup_result(category)
        data[item_id]['name'] = read_soup_result(overview)
        data[item_id]['link'] = link

        full_review_url = get_base_url() + data[item_id]['link']

        num_pages = get_num_pages(full_review_url)

        data['elements'] = []

        for page_no in range(num_pages):

            current_url = full_review_url + '#page-' + str(page_no + 1)
            full_soup = BeautifulSoup(requests.get(current_url).content, 'lxml')

            description = full_soup.find_all('div', {'data-rel': 'linkify list-description'})
            data[item_id]['description'] = read_soup_result(description)

            review_items = full_soup.find_all('div', {'class': 'elli-content'})

            for review_item in review_items:
                soup_content = review_item.find_all('a', {'class': 'elco-anchor'})
                soup_comment = review_item.find_all('div', {'class': 'elli-annotation-content '})

                element = get_item_id(soup_content)
                comment = read_soup_result(soup_comment, simplify_text=False)

                data['elements'].append((element, comment))

    return data


def get_num_pages(url):
    soup = BeautifulSoup(requests.get(url).content, 'lxml')

    collection_pages = soup.find_all('a', {'class': 'eipa-anchor'})

    try:
        num_pages = int(collection_pages[-1].attrs['data-sc-pager-page'])
    except IndexError:
        num_pages = 1

    return num_pages


def get_keyword_home_url(user_name='wok', keyword='collection'):
    home_page_no = 1

    if keyword == 'collection':
        url = get_collection_url(user_name=user_name, page_no=home_page_no)
    elif keyword == 'critiques':
        url = get_critiques_url(user_name=user_name, page_no=home_page_no)
    else:
        url = get_listes_url(user_name=user_name, page_no=home_page_no)

    return url


def parse_keyword_page(user_name='wok', keyword='collection', page_no=1):
    if keyword == 'collection':
        page_data = parse_collection_page(user_name=user_name, page_no=page_no)
    elif keyword == 'critiques':
        page_data = parse_critiques_page(user_name=user_name, page_no=page_no)
    else:
        page_data = parse_listes_page(user_name=user_name, page_no=page_no)

    return page_data


def parse_collection(user_name='wok', keyword='collection'):
    url = get_keyword_home_url(user_name=user_name, keyword=keyword)

    num_pages = get_num_pages(url)

    print('Parsing {} pages of {} by {}.'.format(num_pages, keyword, user_name))

    data = dict()
    for page_no in range(num_pages):
        real_page_no = page_no + 1

        page_data = parse_keyword_page(user_name=user_name, keyword=keyword, page_no=real_page_no)

        print('[{} ; page n°{}] num_items = {}'.format(keyword, real_page_no, len(page_data)))

        data.update(page_data)

    return data


def parse_critiques(user_name='wok'):
    return parse_collection(user_name=user_name, keyword='critiques')


def parse_listes(user_name='wok'):
    return parse_collection(user_name=user_name, keyword='listes')


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
    elif data_type == 'critiques':
        data = parse_critiques(user_name=user_name)
    elif data_type == 'listes':
        data = parse_listes(user_name=user_name)
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


if __name__ == '__main__':
    for keyword in ['collection', 'critiques', 'listes']:
        taken_out_data = parse_and_cache(user_name='wok', data_type=keyword)
