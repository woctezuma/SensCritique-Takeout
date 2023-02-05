from senscritique.parse_utils import get_num_pages
from senscritique.process_collection import get_collection_url, parse_collection_page
from senscritique.process_critiques import get_critiques_url, parse_critiques_page
from senscritique.process_listes import get_listes_url, parse_listes_page


def get_keyword_home_url(user_name='wok', keyword='collection'):
    home_page_no = 1

    if keyword == 'collection':
        url = get_collection_url(user_name=user_name, page_no=home_page_no)
    elif keyword == 'critiques':
        url = get_critiques_url(user_name=user_name, page_no=home_page_no)
    else:
        url = get_listes_url(user_name=user_name, page_no=home_page_no)

    return url


def parse_keyword_page(user_name='wok', keyword='collection', page_no=1, verbose=False):
    if keyword == 'collection':
        page_data = parse_collection_page(
            user_name=user_name,
            page_no=page_no,
            verbose=verbose,
        )
    elif keyword == 'critiques':
        page_data = parse_critiques_page(
            user_name=user_name,
            page_no=page_no,
            verbose=verbose,
        )
    else:
        page_data = parse_listes_page(
            user_name=user_name,
            page_no=page_no,
            verbose=verbose,
        )

    return page_data


def parse_keyword(user_name='wok', keyword='collection', verbose=False):
    url = get_keyword_home_url(user_name=user_name, keyword=keyword)

    num_pages = get_num_pages(url)

    print(f'Parsing {num_pages} pages of {keyword} by {user_name}.')

    data = {}
    for page_no in range(num_pages):
        real_page_no = page_no + 1

        page_data = parse_keyword_page(
            user_name=user_name,
            keyword=keyword,
            page_no=real_page_no,
            verbose=verbose,
        )

        print(
            '[{} ; page n°{}] num_items = {}'.format(
                keyword,
                real_page_no,
                len(page_data),
            ),
        )

        data.update(page_data)

    return data
