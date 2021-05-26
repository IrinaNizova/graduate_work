from random import choice
import typing

from phrases.command_api import (get_actor_films, get_best_films_for_year,
                                 get_description, get_film_actor,
                                 get_film_director, get_film_duration,
                                 get_film_information, get_film_writer,
                                 get_one_good_film, get_many_good_films,
                                 get_many_new_films, get_one_new_film,
                                 get_director_films, get_writer_films)
from phrases.utils import command_matcher, pymorpy_normalizer
from phrases.validators import Response

from .models import CommandPhrases


def get_value_for_obj(name):
    return tuple(CommandPhrases.objects.filter(name=name).first().values)


class Command:
    def __init__(self, executor: typing.Callable):
        self.executor = executor

    def __call__(self, *args, **kwargs):
        return self.executor.objects.all()

    def get_phrases(self) -> typing.Iterable:
        return tuple(self.executor.objects.filter(name=self.name).values_list('values', flat=True)[0])


commands = {
    'best_films_for_year': get_best_films_for_year,
    'full_film_data': get_film_information,
    'new_films': get_many_new_films,
    'new_film': get_one_new_film,
    'good_films': get_many_good_films,
    'good_film': get_one_good_film,
    'description': get_description,
    'writer_films': get_writer_films,
    'film_actor': get_film_actor,
    'film_writer': get_film_writer,
    'film_director': get_film_director,
    'actor_films': get_actor_films,
    'director_films': get_director_films,
    'film_duration': get_film_duration,
}

not_understand_phrases = ['Не знаю']


def execute_command_with_name(verbal_command: str, res: Response) -> None:
    """
    В этой функции проверяем есть ли в ответе пользователя ключевые фразы,
    если да - отдаём информацию которую запрашивали
    :param verbal_command: фраза, которую произнёс пользователь
    :param res: в объект ответа кладём текст, которым надо ответить
    :return:
    """
    # приводим токены фразы пользователя к нормальной форме
    verbal_tokens = pymorpy_normalizer(verbal_command.text)
    for pattern_object in Command(executor=CommandPhrases)():
        pattern_phrases = tuple(pattern_object.values)
        is_match, additional_words = command_matcher(verbal_tokens, pattern_phrases)
        if is_match:
            print(pattern_object.name)
            res.text = commands[pattern_object.name](additional_words)
            break
    if not res.text:
        res.text = choice(not_understand_phrases)
