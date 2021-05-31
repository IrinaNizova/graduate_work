import random
from typing import Union, Optional

import requests
from config.config import BASE_URL


def create_request(url: str) -> Optional[dict]:
    """
    запрос к movie api
    :param url: адрес запроса
    :return: json ответа
    """
    response = requests.get(url)
    if response.status_code == 200 and len(response.json()):
        return response.json()


def get_random_items(url: str, field: str) -> str:
    """
    запрашиваем первую страницу ответов и с неё выбираем 3 случайных ответа
    :param url: адрес запроса
    :param field: поле которое возьмём для ответа
    :return: строка ответов или надпись Ничего не найдено
    """
    response = create_request(url)
    if not response:
        return "Ничего не найдено"
    items_list = [item[field] for item in response]
    random.shuffle(items_list)
    return ", ".join(items_list[:3])


def get_random_item(url: str, field: str) -> str:
    """
    запрашиваем первую страницу ответов и с неё выбираем случайный ответ
    :param url: адрес запроса
    :param field: поле которое возьмём для ответа
    :return: случайный ответ по заданному полю из первого листа выдачи
    """
    response = create_request(url)
    if not response:
        return "Ничего не найдено"
    items_list = [item[field] for item in response]
    return random.choice(items_list)


def get_random_film_data(url: str) -> Union[str, dict]:
    """
    Информация про случайный фильм
    :param url: адрес запроса
    :return: json с данными про фильм
    """
    films = create_request(url)
    if not films:
        return "Ничего не найдено"
    random.shuffle(films)
    return create_request(BASE_URL + 'film/' + films[0]['id'])


def get_film_param(url: str, param: Union[str, None] = None) -> Union[str, dict]:
    """
    Информация про конкретный фильм
    :param url: адрес запроса
    :param param: поле объекта которое вернём
    :return: поле объекта или json
    """
    response = create_request(url)
    if not response:
        return "Ничего не найдено"
    film_id = response[0]['id']
    response = create_request(BASE_URL + 'film/' + film_id)
    if not response:
        return "Ничего не найдено"
    if not param:
        return response
    else:
        return str(response[param])


def get_person_param(url: str, param: str) -> str:
    """
    Информация по персоне
    :param url: адрес запроса
    :param param: поле объекта которое вернём
    :return: поле объекта или json
    """
    response = create_request(url + param)
    if not response:
        return "Ничего не найдено"
    return response[0][param]
