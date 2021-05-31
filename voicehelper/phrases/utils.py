import Levenshtein
import pymorphy2
from typing import List, Tuple

from config.config import LEVENSHTEIN_DIVERCE
from phrases.validators import Request


def get_talk_params_from_request(request: dict) -> tuple:
    """
    :param request: json запроса как он пришёл
    :return: нужные там параметры из запроса: токены, номер диалога, номер реплики
    """
    morph = pymorphy2.MorphAnalyzer()
    tokens = [morph.parse(name)[0].normal_form for name in request['request']['nlu']['tokens']]
    dialogue = request.get('state', {}).get('session', {}).get('dialogue', 0)
    speech = request.get('state', {}).get('session', {}).get('speech', 0)
    return tokens, dialogue, speech


def create_request_json(request: dict, text: str, dialogue: int, speech: int) -> dict:
    """
    :param request: json запроса как он пришёл
    :param text:  текст, который должен ответить ассистент
    :param dialogue: номер диалога
    :param speech: омер реплики
    :return: json ответа
    """
    return {
        'session': request['session'],
        'version': request['version'],
        'response': {
            'end_session': False,
            "text": text
        },
        "session_state": {
            "dialogue": dialogue,
            "speech": speech
        }
    }


def validate_request_obj(request: dict) -> None:
    """
    Валидируем полученный json в объект
    :param request: что мы получили по http
    :return: сериализованный объект
    """
    return Request().load(dict(user_id=request['session']['user_id'],
                               session_id=request['session']['session_id'],
                               skill_id=request['session']['skill_id'],
                               message_id=request['session']['message_id'],
                               application_id=request['session']['application']['application_id'],
                               version=request['version'],
                               text=request['request']['command'],
                               tokens=request['request']['nlu']['tokens'],
                               dialogue=request.get('state', {}).get('session', {}).get('dialogue', 0) or 0,
                               speech=request.get('state', {}).get('session', {}).get('speech', 0) or 0))


def command_matcher(verbal_tokens: List[str], pattern_phrases: List[str]) -> Tuple[bool, str]:
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
    return False, ""


def pymorpy_normalizer(phrase: str) -> List[str]:
    """
    :param phrase: фраза пользователя
    :return: фраза пользователя разбитая на токены
    """
    morph = pymorphy2.MorphAnalyzer()
    return [morph.parse(name)[0].normal_form for name in phrase.split(" ")]


def levenshtein_processing(pattern_tokens: List[str], verbal_tokens: List[str]) -> Tuple[int, List[str]]:
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
