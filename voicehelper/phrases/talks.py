import random
from typing import List

import pymorphy2

from phrases import command_api
from phrases import constant_phrases
from .models import VariousPhases


morph = pymorphy2.MorphAnalyzer()


def get_phrases(ph_type: str) -> List[str]:
    """
    :param ph_type: тип фраз
    :return: все фразы данного типа
    """
    return VariousPhases.objects.filter(type__type=ph_type).values_list('value', flat=True)


def get_phrase_tokens(phrases_type: List[str]) -> List[str]:
    """
    :param phrases_type: тип фраз
    :return: все фразы данного типа
    """
    return [morph.parse(phrases)[0].normal_form for phrases in phrases_type]


suggest_phrases = get_phrases('suggest_phrases')
regret_phrases = get_phrases('regret_phrases')
addition_phrases = get_phrases('addition_phrases')
new_phrases = get_phrases('new_phrases')


def has_intersection(text_tokens, pattern_tokens):
    return set(text_tokens) & set(pattern_tokens)


def first_phrase() -> dict:
    """
    Случайно выбираем один из диалогов и говорим его приветственную фразу
    :return: словарь с текстом, номером диалога и номером реплики
    """
    dialogue_number = random.randint(1, len(DIALOGS) + 1)
    text = constant_phrases.GREETING_PHRASE + DIALOGS[dialogue_number]['phrases'][0]
    return {'dialogue': dialogue_number, 'speech': 1, 'text': text}


def perform_dialogue_new_or_best_film(text_tokens: list, speech_number: int) -> dict:
    """
    Диалог где пользователь выбирает хочет он новый или популярный фильм
    :param text_tokens: слова из запроса
    :param speech_number: номер реплики
    :return: словарь с текстом, номером диалога и номером реплики
    """
    if speech_number == 1:
        if has_intersection(text_tokens, get_phrase_tokens(suggest_phrases)):
            return {"text": DIALOGS[1]['phrases'][1], "dialogue": 1, "speech": 2}
        else:
            text = ". ".join((random.choice(regret_phrases), random.choice(addition_phrases)))
            return {"text": text, "dialogue": 0}
    elif speech_number == 2:
        if has_intersection(text_tokens, new_phrases):
            text = command_api.get_one_new_film("") + constant_phrases.THIS_FILM_NEW + random.choice(addition_phrases)
        else:
            text = command_api.get_one_good_film("") + constant_phrases.THIS_FILM_GOOD + random.choice(addition_phrases)
        return {"text": text, "dialogue": 0}


def perform_dialogue_random_film_all_info(text_tokens: list, _) -> dict:
    """
    Диалог где рассказывают информацию про случайный фильм
    :param text_tokens: слова из запроса
    :param _:
    :return: словарь с текстом и номером диалога
    """
    if has_intersection(text_tokens, get_phrase_tokens(suggest_phrases)):
        f = command_api.get_random_film(None)
        text = constant_phrases.FILM_INFORMATION.format(f['title'], f['genre'][0], f['imdb_rating'], f['description']) \
                   + random.choice(addition_phrases)
    else:
        text = ". ".join((random.choice(regret_phrases), random.choice(addition_phrases)))
    return {"text": text, "dialogue": 0}


def perform_dialogue_genre(text_tokens: list, _) -> dict:
    """
    Диалог где пользователь выбирает жанр для фильма
    :param text_tokens: слова из запроса
    :param _:
    :return: словарь с текстом и номером диалога
    """
    if any([t.startswith('фантаст') for t in text_tokens]):
        genre = 'Fantasy'
    elif any([t.startswith('мульт') for t in text_tokens]):
        genre = 'Animation'
    elif any([t.startswith('комед') for t in text_tokens]):
        genre = 'Comedy'
    else:
        text = ". ".join((random.choice(regret_phrases), random.choice(addition_phrases)))
        return {"text": text, "dialogue": 0}
    f = command_api.get_random_film_by_genre(genre)
    text = constant_phrases.RECOMMENDED_FILM.format(f['title'], f['imdb_rating']) \
           + random.choice(addition_phrases)
    return {"text": text, "dialogue": 0}


DIALOGS = {
    1: {'phrases': ("Хотите, посоветую вам фильм?", "Вам поновее или классику?"),
        'performer': perform_dialogue_new_or_best_film},
    2: {'phrases': ("Рассказать вам про какой-нибудь фильм?",), 'performer': perform_dialogue_random_film_all_info},
    3: {'phrases': ("Вы больше любите фантастику, мультфильмы или комедии?",), 'performer': perform_dialogue_genre},
}


def continue_dialogue(text_tokens, dialogue_number, speech_number) -> dict:
    """
    Последующие фразы в зависимости от диалога
    :param text_tokens: слова из запроса
    :param dialogue_number: номер диалога
    param speech_number: номер реплики
    :return:
    """
    return DIALOGS[dialogue_number]['performer'](text_tokens, speech_number)
