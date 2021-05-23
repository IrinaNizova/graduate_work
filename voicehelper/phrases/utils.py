import Levenshtein
import pymorphy2
import typing

from config.config import LEVENSHTEIN_DIVERCE
from phrases.validators import Request, Response


def create_request_objs(request):
    """
    Преобразуем полученный json в объект
    :param request: что мы получили по http
    :return: объект класса Request
    """
    morph = pymorphy2.MorphAnalyzer()
    return Request(user_id=request['session']['user_id'],
                   session_id=request['session']['session_id'],
                   message_id=request['session']['message_id'],
                   version=request['version'],
                   text=request['request']['command'],
                   tokens=[morph.parse(name)[0].normal_form for name in request['request']['nlu']['tokens']],
                   dialogue=request.get('state', {}).get('session', {}).get('dialogue', 0),
                   speech=request.get('state', {}).get('session', {}).get('speech', 0))


def create_response_objs(body):
    """
    Создаёт объект ответа
    :param body: что мы получили по http
    :return: объект класса Response
    """
    return Response(user_id=body['session']['user_id'],
                    session_id=body['session']['session_id'],
                    message_id=body['session']['message_id'],
                    version=body['version'])


def command_matcher(verbal_tokens: typing.List[str], pattern_phrases: typing.List[str]):
    """
    Тут проверяем есть ли совпадение фразы пользователя с ключевыми фразами
    :param verbal_tokens: фраза пользователя разбитая на токены
    :param pattern_phrases: ключевая фраза разбитая на токены
    :return: есть ли совпадение, не слова фразы пользователя, не вошедшие в ключевую фразу
    """
    for pattern_phrase in pattern_phrases:
        # приводим токены ключевой фразы к нормальной форме
        pattern_tokens = pymorpy_normalizer(pattern_phrase)
        distance, union_phrases = levenshtein_processing(pattern_tokens, verbal_tokens)
        # если ошибок меньше чем 1 на 10 - вызываем команду
        if distance < len(pattern_phrase) / LEVENSHTEIN_DIVERCE:
            # передаём команде слова фразы пользователя, которые не совпали
            return True, " ".join((p for p in verbal_tokens if p not in union_phrases))
        else:
            return False, ""


def pymorpy_normalizer(phrase):
    """
    :param phrase: фраза пользователя
    :return: фраза пользователя разбитая на токены
    """
    morph = pymorphy2.MorphAnalyzer()
    return [morph.parse(name)[0].normal_form for name in phrase.split(" ")]


def levenshtein_processing(pattern_tokens, verbal_tokens):
    """
    ищем ближайший к токену ключевой фразы токен фразу пользователя
    :param pattern_tokens: ключевая фраза из базы
    :param verbal_tokens: фраза пользователя разбитая на токены
    :return: дистанция между фразами по Левенштейну, общие токены между фразами
    """
    union_phrases = []
    distance = 0
    for pattern_token in pattern_tokens:
        sorted_tokens = sorted(verbal_tokens, key=lambda x: Levenshtein.distance(x, pattern_token))
        distance += Levenshtein.distance(sorted_tokens[0], pattern_token)
        union_phrases.append(sorted_tokens[0])
    return distance, union_phrases
