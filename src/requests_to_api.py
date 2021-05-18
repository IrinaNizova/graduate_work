import random
import requests

from config.config import BASE_URL


def create_request(u):
    r = requests.get(u)
    if r.status_code != 200:
        return "Сервер не отвечает"
    elif not len(r.json()):
        return "Ничего не нашлось"
    else:
        return r.json()


def get_random_items(u, field):
    r = create_request(u)
    if isinstance(r, str):
        return r
    items_list = [item[field] for item in create_request(u)]
    random.shuffle(items_list)
    items = ", ".join(items_list[:3])
    return items if items else "Ничего не найдено"


def get_random_item(u, field):
    r = create_request(u)
    if isinstance(r, str):
        return r
    items_list = [item[field] for item in create_request(u)]
    return random.choice(items_list) if items_list else "Ничего не найдено"


def get_random_film_data(u):
    films = create_request(u)
    random.shuffle(films)
    r = requests.get(BASE_URL + 'film/' + films[0]['id'])
    return r.json()


def get_film_param(u, param=None):
    r = create_request(u)
    if isinstance(r, str):
        return r
    film_id = r[0]['id']
    r = requests.get(BASE_URL + 'film/' + film_id)
    if r.status_code != 200 or not r.json():
        return "Ничего не найдено"
    if not param:
        return r.json()
    else:
        return str(r.json()[param])


def get_person_param(u, param):
    r = requests.get(u + param)
    if not len(r.json()):
        return "Ничего не найдено"
    return r.json()[0][param]
