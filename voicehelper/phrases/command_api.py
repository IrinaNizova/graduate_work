from datetime import datetime

from config.config import BASE_URL, URL_FILM_LIST_SORT, URL_FILM_SEARCH

from phrases.requests_to_api import (get_film_param, get_person_param,
                                     get_random_film_data, get_random_item,
                                     get_random_items)


def get_many_new_films(_):
    return get_random_items("".join(
        (BASE_URL, URL_FILM_LIST_SORT.format('-created_at'))), 'title')


def get_one_new_film(_):
    return get_random_item("".join(
        (BASE_URL, URL_FILM_LIST_SORT.format('-created_at'))), 'title')


def get_good_film(_):
    return get_random_item("".join(
        (BASE_URL, URL_FILM_LIST_SORT.format('-imdb_rating'))), 'title')


def get_good_films(_):
    return get_random_items("".join(
        (BASE_URL, URL_FILM_LIST_SORT.format('-imdb_rating'))), 'title')


def get_film_duration(name):
    duration = get_film_param("".join(
        (BASE_URL, URL_FILM_SEARCH, name)), 'duration')
    return duration + " минуты" if duration.isnumeric() else duration


def get_film_actor(name):
    return get_film_param("".join(
        (BASE_URL, URL_FILM_SEARCH, name)), 'actors_names')


def get_film_writer(name):
    return get_film_param("".join(
        (BASE_URL, URL_FILM_SEARCH, name)), 'writers_names')


def get_film_director(name):
    return get_film_param("".join(
        (BASE_URL, URL_FILM_SEARCH, name)), 'director')


def get_random_film(_):
    return get_random_film_data(BASE_URL + 'film?page[size]=50&sort=-imdb_rating')


def get_random_film_by_genre(genre):
    search_params = 'film/search?page[size]=5&query={}&sort=-imdb_rating'
    return get_random_film_data(BASE_URL + search_params.format(genre))


def get_description(name):
    return get_film_param("".join((BASE_URL, URL_FILM_SEARCH, name)), 'description')


def get_actor_films(name):
    return get_person_param("".join(
        (BASE_URL, URL_FILM_SEARCH, name)), 'films_as_actor')


def get_director_films(name):
    return get_person_param("".join(
        (BASE_URL, URL_FILM_SEARCH, name)), 'films_as_director')


def get_writer_films(name):
    return get_person_param("".join(
        (BASE_URL, URL_FILM_SEARCH, name)), 'films_as_writer')


def get_best_films_for_year(params):
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
        return get_random_items(BASE_URL + search_params + year, 'title')
    else:
        return get_good_films(None)


def get_film_information(name):
    data = get_film_param(BASE_URL + URL_FILM_SEARCH + name)
    information = "{} это фильм в жанре {}. Он длится {} минуты. Пользователи оценили его в {} звезды. "\
        .format(data['title'], ", ".join(data['genre']), data['duration'], data['imdb_rating'])
    if data['director']:
        information += "Его снял {}".format(data['director'])
    return information
