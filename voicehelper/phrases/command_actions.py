from random import choice

from phrases import command_api
from phrases.utils import command_matcher, pymorpy_normalizer

from .models import CommandPhrases


commands = {
    'best_films_for_year': command_api.get_best_films_for_year,
    'full_film_data': command_api.get_film_information,
    'new_films': command_api.get_many_new_films,
    'new_film': command_api.get_one_new_film,
    'good_films': command_api.get_many_good_films,
    'good_film': command_api.get_one_good_film,
    'description': command_api.get_description,
    'writer_films': command_api.get_writer_films,
    'film_actor': command_api.get_film_actor,
    'film_writer': command_api.get_film_writer,
    'film_director': command_api.get_film_director,
    'actor_films': command_api.get_actor_films,
    'director_films': command_api.get_director_films,
    'film_duration': command_api.get_film_duration,
}

not_understand_phrases = ['Не знаю']


def execute_command_with_name(verbal_tokens: str) -> dict:
    """
    В этой функции проверяем есть ли в ответе пользователя ключевые фразы,
    если да - отдаём информацию которую запрашивали
    :param verbal_tokens: слова фразы которую произнёс пользователь
    :return: словарик с ключом text куда кладём текст, который отдадим голосовому ассистенту
    """
    for pattern_object in CommandPhrases.objects.values_list('values', flat=True):
        pattern_phrases = tuple(pattern_object['values'])
        is_match, additional_words = command_matcher(verbal_tokens, pattern_phrases)
        if is_match:
            return {'text': commands[pattern_object['name']](additional_words)}
    return {'text': choice(not_understand_phrases)}
