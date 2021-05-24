import random
from typing import List

import pymorphy2

from phrases.command_api import (get_one_good_film, get_one_new_film,
                                     get_random_film, get_random_film_by_genre)
from phrases.validators import Request, Response
from .models import VariousPhases

dialogue_new_or_best_film = ["Хотите, посоветую вам фильм?", "Вам поновее или классику?"]
dialogue_genre = ["Вы больше любите фантастику, мультфильмы или комедии?", "В каком из них посоветовать вам фильм?"]
dialogue_random_film_all_info = ["Рассказать вам про какой-нибудь фильм?"]

dialogs = [dialogue_new_or_best_film, dialogue_random_film_all_info, dialogue_genre]

morph = pymorphy2.MorphAnalyzer()


def get_phrases(ph_type: str) -> List[str]:
    """
    :param ph_type: тип фраз
    :return: все фразы данного типа
    """
    return [morph.parse(phrases.value)[0].normal_form
            for phrases in VariousPhases.objects.filter(type__type=ph_type).all()]


suggest_phrases = get_phrases('suggest_phrases')
regret_phrases = get_phrases('regret_phrases')
addition_phrases = get_phrases('addition_phrases')
new_phrases = get_phrases('new_phrases')


def first_phrase(res: Response) -> Response:
    """
    Случайно выбираем один из диалогов и говорим его приветственную фразу
    :param res: объект ответа
    :return: возвращаем объект ответа с текстом
    """
    number = random.randint(1, 3)
    res.dialogue = number
    res.speech = 1
    res.text = "Здравствуйте. Приветствую вас в нашем кинотеатре. " + dialogs[number - 1][0]
    return res


def perform_dialogue_new_or_best_film(res: Response, req: Request) -> None:
    """
    Диалог где пользователь выбирает хочет он новый или популярный фильм
    :param res: объект ответа
    :param req: объект запроса
    :return:
    """
    speech_number = req.speech
    if speech_number == 1:
        if set(req.tokens) & set(suggest_phrases):
            res.dialogue = 1
            res.speech = 2
            res.text = dialogs[0][1]
        else:
            res.dialogue = 0
            res.text = ". ".join((random.choice(regret_phrases), random.choice(addition_phrases)))
    elif speech_number == 2:
        if set(req.tokens) & set(new_phrases):
            res.text = get_one_new_film("") + " - этот фильм вышел недавно. " + random.choice(addition_phrases)
        else:
            res.text = get_one_good_film("") + " - у этого фильма высокий рейтинг. " + random.choice(addition_phrases)
        res.dialogue = 0


def perform_dialogue_random_film_all_info(res: Response, req: Request) -> None:
    """
    Диалог где рассказывают информацию про случайный фильм
    :param res: объект ответа
    :param req: объект запроса
    :return:
    """
    if set(req.tokens) & set(suggest_phrases):
        f = get_random_film(None)
        res.dialogue = 0
        res.text = "Фильм {} в жанре {}. Пользователи оценили его в {} звёзд. " \
                   "Вот про что он {}. ".format(f['title'], f['genre'][0], f['imdb_rating'], f['description']) \
                   + random.choice(addition_phrases)
    else:
        res.text = ". ".join((random.choice(regret_phrases), random.choice(addition_phrases)))
    res.dialogue = 0


def perform_dialogue_genre(res: Response, req: Request) -> None:
    """
    Диалог где пользователь выбирает жанр для фильма
    :param res: объект ответа
    :param req: объект запроса
    :return:
    """
    if any([t.startswith('фантаст') for t in req.tokens]):
        genre = 'Fantasy'
    elif any([t.startswith('мульт') for t in req.tokens]):
        genre = 'Animation'
    elif any([t.startswith('комед') for t in req.tokens]):
        genre = 'Comedy'
    else:
        res.text = ". ".join((random.choice(regret_phrases), random.choice(addition_phrases)))
        return
    f = get_random_film_by_genre(genre)
    res.dialogue = 0
    res.text = "Тогда можем вам порекомендовать фильм {}. Пользователи оценили его в {} звёзд.".\
        format(f['title'], f['imdb_rating']) + random.choice(addition_phrases)


dialogs_functions = [perform_dialogue_new_or_best_film,
                     perform_dialogue_random_film_all_info,
                     perform_dialogue_genre]


def continue_dialogue(res: Response, req: Request) -> None:
    """
    Последующие фразы в зависимости от диалога
    :param res: объект ответа
    :param req: объект запроса
    :return:
    """
    dialogue_number = req.dialogue
    dialogs_functions[dialogue_number - 1](res, req)
