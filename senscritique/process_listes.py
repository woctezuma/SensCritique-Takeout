import requests
from bs4 import BeautifulSoup

from senscritique.parse_utils import get_item_id, get_num_pages
from senscritique.utils import get_base_url, get_url_for_liste, read_soup_result


def get_listes_url(user_name, page_no=1):
    url = (
        get_base_url(user_name=user_name) + 'listes/all/all/likes/page-' + str(page_no)
    )
    return url


def parse_listes_page(user_name='wok', page_no=1, verbose=False):
    url = get_listes_url(user_name=user_name, page_no=page_no)
    print(url)
    soup = BeautifulSoup(requests.get(url).content, 'lxml')

    collection_items = soup.find_all('li', {'class': 'elth-thumbnail by3'})

    listes_data = {}
    for item in collection_items:
        category = item.find_all('span', {'class': 'elth-universe-label'})
        overview = item.find_all('a', {'class': 'elth-thumbnail-title'})

        link = overview[0].attrs['href']

        item_id = int(link.rsplit('/')[-1])

        listes_data[item_id] = {}
        listes_data[item_id]['category'] = read_soup_result(category)
        listes_data[item_id]['name'] = read_soup_result(overview)
        listes_data[item_id]['link'] = link

        print(
            'List n°{}: {}'.format(
                item_id,
                listes_data[item_id]['name'],
            ),
        )

        full_review_url = get_url_for_liste(
            item_id_for_liste=item_id,
            page_no_within_list=None,
        )
        num_pages = get_num_pages(full_review_url)

        listes_data[item_id]['elements'] = {}

        for page_no_within_list in range(1, num_pages + 1):
            if verbose:
                print(
                    'Page n°{}/{}:'.format(
                        page_no_within_list,
                        num_pages,
                    ),
                )

            current_url = get_url_for_liste(
                item_id_for_liste=item_id,
                page_no_within_list=page_no_within_list,
            )
            full_soup = BeautifulSoup(requests.get(current_url).content, 'lxml')

            description = full_soup.find_all('div', {'data-rel': 'list-description'})
            listes_data[item_id]['description'] = read_soup_result(description)

            review_items = full_soup.find_all('div', {'class': 'elli-content'})

            for review_item in review_items:
                soup_content = review_item.find_all('a', {'class': 'elco-anchor'})
                soup_comment = review_item.find_all(
                    'div',
                    {'class': 'elli-annotation-content'},
                )

                element = get_item_id(soup_content)
                name = read_soup_result(soup_content)
                comment = read_soup_result(soup_comment, simplify_text=False)

                if verbose:
                    print(
                        '-   item n°{}: {}'.format(
                            element,
                            name,
                        ),
                    )

                listes_data[item_id]['elements'][element] = {}
                listes_data[item_id]['elements'][element]['name'] = name
                listes_data[item_id]['elements'][element]['comment'] = comment

    return listes_data
