def get_data_folder():
    return 'data/'


def get_base_url(user_name=None):
    url = 'https://old.senscritique.com/'
    if user_name is not None:
        url += user_name + '/'
    return url


def get_url_for_liste(item_id_for_liste, page_no_within_list=None):
    url = get_base_url() + 'sc2/liste/{}/'.format(item_id_for_liste)

    if page_no_within_list is not None:
        url += 'page-{}.ajax'.format(page_no_within_list)

    return url


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
