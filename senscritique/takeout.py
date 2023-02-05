import json
import pathlib
from pathlib import Path

from senscritique.data_utils import get_save_filename
from senscritique.process_generic import parse_keyword
from senscritique.utils import get_data_folder


def print_data(data, file_name=None):
    if file_name is None:
        print(data)
    else:
        # Reference of the following line: https://stackoverflow.com/a/14364249
        pathlib.Path(get_data_folder()).mkdir(parents=True, exist_ok=True)

        with Path(file_name).open('w', encoding='utf8') as f:
            f.write(json.dumps(data))

    return


def parse(user_name='wok', data_type='collection', verbose=False):
    if data_type == 'collection':
        data = parse_keyword(user_name=user_name, keyword='collection', verbose=verbose)
    elif data_type == 'critiques':
        data = parse_keyword(user_name=user_name, keyword='critiques', verbose=verbose)
    elif data_type == 'listes':
        data = parse_keyword(user_name=user_name, keyword='listes', verbose=verbose)
    else:
        data = {}

    return data


def parse_and_cache(user_name='wok', data_type='collection', verbose=False):
    save_file_name = get_data_folder() + get_save_filename(
        user_name=user_name,
        data_type=data_type,
    )

    if pathlib.Path(save_file_name).is_file():
        print('File ' + save_file_name + ' already exists.')
        with Path(save_file_name).open(encoding='utf8') as f:
            data = json.load(f)
    else:
        data = parse(user_name=user_name, data_type=data_type, verbose=verbose)
        if len(data) > 0:
            print_data(data, save_file_name)

    sentence = '[' + data_type + ' by ' + user_name + '] num_items = {}'
    print(sentence.format(len(data)))

    return data


if __name__ == '__main__':
    for keyword in ['collection', 'critiques', 'listes']:
        taken_out_data = parse_and_cache(user_name='wok', data_type=keyword)
