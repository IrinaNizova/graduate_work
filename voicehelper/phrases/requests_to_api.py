import random
from typing import Union

import requests
from config.config import BASE_URL


def create_request(url: str) -> Union[str, dict]:
    """
    заспрос к movie api
    :param url: адрес запроса
    :return: json ответа или тект ошибки
    """
    response = requests.get(url)
    if response.status_code != 200:
        return "Сервер не отвечает"
    elif not len(response.json()):
        return "Ничего не нашлось"
    else:
        return response.json()


def get_random_items(url: str, field: str) -> str:
    """
    запрашиваем первую страницу ответов и с неё выбираем 3 случайных ответа
    :param url: адрес запроса
    :param field: поле которое возьмём для ответа
    :return: строка ответов или надпись Ничего не найдено
    """
    r = create_request(url)
    if isinstance(r, str):
        return r
    items_list = [item[field] for item in create_request(url)]
    random.shuffle(items_list)
    items = ", ".join(items_list[:3])
    return items if items else "Ничего не найдено"


def get_random_item(url: str, field: str) -> str:
    """
    запрашиваем первую страницу ответов и с неё выбираем случайный ответ
    :param url: адрес запроса
    :param field: поле которое возьмём для ответа
    :return: случайный ответ по заданному полю из первого листа выдачи
    """
    r = create_request(url)
    if isinstance(r, str):
        return r
    items_list = [item[field] for item in create_request(url)]
    return random.choice(items_list) if items_list else "Ничего не найдено"


def get_random_film_data(url: str) -> dict:
    """
    Информация про случайный фильм
    :param url: адрес запроса
    :return: json с данными про фильм
    """
    films = create_request(url)
    random.shuffle(films)
    r = requests.get(BASE_URL + 'film/' + films[0]['id'])
    return r.json()


def get_film_param(url: str, param: Union[str, None] = None) -> Union[str, dict]:
    """
    Информация про конкретный фильм
    :param url: адрес запроса
    :param param: поле объекта которое вернём
    :return: поле объекта или json
    """
    r = create_request(url)
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


def get_person_param(url: str, param: str) -> str:
    """
    Информация по персоне
    :param url: адрес запроса
    :param param: поле объекта которое вернём
    :return: поле объекта или json
    """
    r = requests.get(url + param)
    if not len(r.json()):
        return "Ничего не найдено"
    return r.json()[0][param]
