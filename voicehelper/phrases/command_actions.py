from random import choice

import Levenshtein
import pymorphy2

from phrases.command_api import (get_actor_films, get_best_films_for_year,
                                 get_description, get_film_actor,
                                 get_film_director, get_film_duration,
                                 get_film_information, get_film_writer,
                                 get_good_film, get_good_films,
                                 get_many_new_films, get_one_new_film)

from .models import CommandPhrases


def get_vaulue_for_obj(name):
    return tuple(CommandPhrases.objects.filter(name=name).first().values)


commands = {
    get_vaulue_for_obj('best_films_for_year'): get_best_films_for_year,
    get_vaulue_for_obj('full_film_data'): get_film_information,
    get_vaulue_for_obj('new_films'): get_many_new_films,
    get_vaulue_for_obj('new_film'): get_one_new_film,
    get_vaulue_for_obj('good_film'): get_good_film,
    get_vaulue_for_obj('good_films'): get_good_films,
    get_vaulue_for_obj('description'): get_description,
    get_vaulue_for_obj('film_actor'): get_film_actor,
    get_vaulue_for_obj('film_writer'): get_film_writer,
    get_vaulue_for_obj('film_director'): get_film_director,
    get_vaulue_for_obj('actor_films'): get_actor_films,
    get_vaulue_for_obj('film_duration'): get_film_duration,
}

not_understand_phrases = ['Не знаю']


def execute_command_with_name(verbal_command, res):
    morph = pymorphy2.MorphAnalyzer()
    # приводим токены фразы пользователя к нормальной форме
    verbal_tokens = [morph.parse(name)[0].normal_form for name in verbal_command.tokens]
    for pattern_phrases in commands.keys():
        for pattern_phrase in pattern_phrases:
            # приводим токены ключевой фразы к нормальной форме
            pattern_tokens = [morph.parse(name)[0].normal_form for name in pattern_phrase.split(" ")]
            distance = 0
            union_phrases = []
            for pattern_token in pattern_tokens:
                # ищем ближайший к токену ключевой фразы токен фразу пользователя
                sorted_tokens = sorted(verbal_tokens, key=lambda x: Levenshtein.distance(x, pattern_token))
                distance += Levenshtein.distance(sorted_tokens[0], pattern_token)
                union_phrases.append(sorted_tokens[0])
            # если ошибок меньше чем 1 на 10 - вызываем команду
            if distance < len(pattern_phrase) / 10:
                # передаём команде слова фразы пользователя, которые не совпали
                res.text = commands[pattern_phrases](" ".join((p for p in verbal_tokens if p not in union_phrases)))
                break
    if not res.text:
        res.text = choice(not_understand_phrases)
