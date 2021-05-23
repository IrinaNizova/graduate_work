from random import choice
import typing

from phrases.command_api import (get_actor_films, get_best_films_for_year,
                                 get_description, get_film_actor,
                                 get_film_director, get_film_duration,
                                 get_film_information, get_film_writer,
                                 get_one_good_film, get_many_good_films,
                                 get_many_new_films, get_one_new_film)
from phrases.utils import command_matcher, pymorpy_normalizer

from .models import CommandPhrases


def get_value_for_obj(name):
    return tuple(CommandPhrases.objects.filter(name=name).first().values)


class Command:
    def __init__(self, name: str, executor: typing.Callable):
        self.name = name
        self.executor = executor

    def __call__(self, *args, **kwargs):
        return self.executor(*args, **kwargs)

    def get_phrases(self) -> typing.Iterable:
        return tuple(self.executor.objects.filter(name=self.name).values_list('values', flat=True)[0])


commands = {
    Command(name='best_films_for_year', executor=CommandPhrases).get_phrases(): get_best_films_for_year,
    Command(name='full_film_data', executor=CommandPhrases).get_phrases(): get_film_information,
    Command(name='new_films', executor=CommandPhrases).get_phrases(): get_many_new_films,
    Command(name='new_film', executor=CommandPhrases).get_phrases(): get_one_new_film,
    Command(name='good_film', executor=CommandPhrases).get_phrases(): get_one_good_film,
    Command(name='good_films', executor=CommandPhrases).get_phrases(): get_many_good_films,
    Command(name='description', executor=CommandPhrases).get_phrases(): get_description,
    Command(name='film_actor', executor=CommandPhrases).get_phrases(): get_film_actor,
    Command(name='film_writer', executor=CommandPhrases).get_phrases(): get_film_writer,
    Command(name='film_director', executor=CommandPhrases).get_phrases(): get_film_director,
    Command(name='actor_films', executor=CommandPhrases).get_phrases(): get_actor_films,
    Command(name='film_duration', executor=CommandPhrases).get_phrases(): get_film_duration,
}

not_understand_phrases = ['Не знаю']
import pymorphy2


def execute_command_with_name(verbal_command, res):
    """
    В этой функции проверяем есть ли в ответе пользователя ключевые фразы,
    если да - отдаём информацию которую запрашивали
    :param verbal_command: фраза, которую произнёс пользователь
    :param res: в объект ответа кладём текст, которым надо ответить
    :return:
    """
    # приводим токены фразы пользователя к нормальной форме
    verbal_tokens = pymorpy_normalizer(verbal_command.text)
    for pattern_phrases in commands.keys():
        is_match, additional_words = command_matcher(verbal_tokens, pattern_phrases)
        if is_match:
            res.text = commands[pattern_phrases](additional_words)
            break
    if not res.text:
        res.text = choice(not_understand_phrases)
