import time


def get_filename_separator():
    return '_'


def get_save_filename(user_name='wok', data_type='collection'):
    json_filename_suffix = '.json'

    sep = get_filename_separator()

    # Get current day as yyyymmdd format
    date_format = '%Y%m%d'
    current_date = time.strftime(date_format)

    # Database filename
    save_filename = (
        current_date + sep + user_name + sep + data_type + json_filename_suffix
    )

    return save_filename
