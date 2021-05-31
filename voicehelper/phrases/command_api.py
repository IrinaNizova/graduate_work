from datetime import datetime

from config.config import BASE_URL, URL_FILM_LIST_SORT, URL_FILM_SEARCH, URL_PERSON_SEARCH

from phrases import requests_to_api


def get_many_new_films(_: None) -> str:
    """
    выбирает 3 случайных фильма с первой страницы выдачи, отсоритованной по дате
    :param _:
    :return: строка с названиями 3 новых фильмов
    """
    return requests_to_api.get_random_items("".join(
        (BASE_URL, URL_FILM_LIST_SORT.format('-created_at'))), 'title')


def get_one_new_film(_: None) -> str:
    """
    выбирает случайный фильм с первой страницы выдачи, отсоритованной по дате
    :param _:
    :return: строка с названием нового фильма
    """
    return requests_to_api.get_random_item("".join(
        (BASE_URL, URL_FILM_LIST_SORT.format('-created_at'))), 'title')


def get_one_good_film(_: None) -> str:
    """
    выбирает случайный фильм с первой страницы выдачи, отсортированной по рейтингу
    :param _:
    :return строка с названием высокорейтингого фильма:
    """
    return requests_to_api.get_random_item("".join(
        (BASE_URL, URL_FILM_LIST_SORT.format('-imdb_rating'))), 'title')


def get_many_good_films(_: None) -> str:
    """
    выбирает 3 случайных фильма с первой страницы выдачи, отсортированной по рейтингу
    :param _:
    :return строка с названиями 3 высокорейтинговых фильмов:
    """
    return requests_to_api.get_random_items("".join(
        (BASE_URL, URL_FILM_LIST_SORT.format('-imdb_rating'))), 'title')


def get_film_duration(name: str) -> str:
    """
    продлжительность фильма
    :param name: название фильма
    :return: количество минут
    """
    duration = requests_to_api.get_film_param("".join(
        (BASE_URL, URL_FILM_SEARCH, name)), 'duration')
    return duration + " минуты" if duration.isnumeric() else duration


def get_film_actor(name: str) -> str:
    """
    актёры из фильма
    :param name: название фильма
    :return: строка с актёрами, которые снялись в фильме
    """
    return requests_to_api.get_film_param("".join(
        (BASE_URL, URL_FILM_SEARCH, name)), 'actors_names')


def get_film_writer(name: str) -> str:
    """
    сценаристы фильма
    :param name: название фильма
    :return: строка со сценаристами, которые написали фильм
    """
    return requests_to_api.get_film_param("".join(
        (BASE_URL, URL_FILM_SEARCH, name)), 'writers_names')


def get_film_director(name: str) -> str:
    """
    режиссёр фильма
    :param name: название фильма
    :return: строка с режиссёром который снял фильм
    """
    return requests_to_api.get_film_param("".join(
        (BASE_URL, URL_FILM_SEARCH, name)), 'director')


def get_random_film(_: None) -> dict:
    """
    случайный фильм
    :param _:
    :return: название фильма
    """
    return requests_to_api.get_random_film_data(BASE_URL + 'film?page[size]=50&sort=-imdb_rating')


def get_random_film_by_genre(genre: str) -> dict:
    """
    случайный фильм заданного жанра
    :param genre: название жанра
    :return: название фильма
    """
    search_params = 'film/search?page[size]=5&query={}&sort=-imdb_rating'
    return requests_to_api.get_random_film_data(BASE_URL + search_params.format(genre))


def get_description(name: str) -> str:
    """
    описание фильма
    :param name: название фильма
    :return: строка с описанием фильма
    """
    return requests_to_api.get_film_param("".join((BASE_URL, URL_FILM_SEARCH, name)), 'description')


def get_actor_films(name: str) -> str:
    """
    фильмы, в которых сняля актёр
    :param name: имя актёра
    :return: строка с фильмами где снялся актёр
    """
    return requests_to_api.get_person_param("".join(
        (BASE_URL, URL_PERSON_SEARCH, name)), 'films_as_actor')


def get_director_films(name: str) -> str:
    """
    фильмы, которые снял режиссёр
    :param name: имя режиссёра
    :return:  строка с фильмами которые снял режиссёр
    """
    return requests_to_api.get_person_param("".join(
        (BASE_URL, URL_PERSON_SEARCH, name)), 'films_as_director')


def get_writer_films(name: str) -> str:
    """
    фильмы, которые написал сценарист
    :param name: имя сценариста
    :return: строка с фильмами которые написал сценарист
    """
    return requests_to_api.get_person_param("".join(
        (BASE_URL, URL_PERSON_SEARCH, name)), 'films_as_writer')


def get_best_films_for_year(params: str) -> str:
    """
    лучшие фильмы одного года
    :param params: строка где содержится год
    :return: строка с названиями фильмов
    """
    if params.endswith("год"):
        year = params.strip("год").strip(" ")
        if year in ("прошлый", "прошедший", "предыдущий"):
            year = str(datetime.now().year - 1)
        elif year in ("этот", "текущий", "настоящий"):
            year = str(datetime.now().year)
        elif len(year) == 2:
            if int(year) > int(str(datetime.now().year)[2:]):
                year = "19" + year
            else:
                year = "20" + year
        search_params = 'film/search?page[size]=3&sort=-imdb_rating&year='
        return requests_to_api.get_random_items(BASE_URL + search_params + year, 'title')
    else:
        return get_many_good_films(None)


def get_film_information(name: str) -> str:
    """
    вся информация о фильме
    :param name: название фильма
    :return: строка с информацией о фильмек
    """
    data = requests_to_api.get_film_param(BASE_URL + URL_FILM_SEARCH + name)
    information = "{} это фильм в жанре {}. Он длится {} минуты. Пользователи оценили его в {} звезды. "\
        .format(data['title'], ", ".join(data['genre']), data['duration'], data['imdb_rating'])
    if data['director']:
        information += "Его снял {}. ".format(data['director'])
    if data['actors_names']:
        information += "Актёры фильма {}. ".format(data['actors_names'])
    if data['writers_names']:
        information += "Сценарий написали {}. ".format(data['writers_names'])
    return information
