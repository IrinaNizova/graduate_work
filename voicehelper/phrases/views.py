import logging.config
from marshmallow import ValidationError
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from config.logger import LOGGER
from phrases.command_actions import execute_command_with_name
from phrases.consant_phrases import WRONG_REQUEST
from phrases.talks import continue_dialogue, first_phrase
from phrases.utils import get_talk_params_from_request, create_request_json, validate_request_obj

logging.config.dictConfig(LOGGER)
logger = logging.getLogger(__name__)


@csrf_exempt
def main(request):
    """
    Главная функция через которую идёт обработка
    :param request: объект запроса
    :return: ответ - сериализованный json
    """
    request_body = json.loads(request.body)
    logging.info(request_body)
    try:
        validate_request_obj(request_body)
    except ValidationError as err:
        logging.error(err.messages)
        response_json = create_request_json(request_body, WRONG_REQUEST, 0, 0)
        return HttpResponse(json.dumps(response_json))
    req_tokens, req_dialogue_number, req_speech_number = get_talk_params_from_request(request_body)
    res_text, res_dialogue, res_speech = handle_dialog(req_tokens, req_dialogue_number, req_speech_number)
    response_json = create_request_json(request_body, res_text, res_dialogue, res_speech)
    logging.info(response_json)
    return HttpResponse(json.dumps(response_json))


def handle_dialog(tokens, req_dialogue_number, req_speech_number) -> tuple:
    """
    :param tokens: токены - слова, приведённые в к нормальной форме из запроса
    :param req_dialogue_number: - номер диалога, который ведётся с пользователем
    :param req_speech_number: номер реплики диалога
    :return: текст, номер диалога и номер реплики которые отправятся в ответ
    """
    # управление диалогом
    # если нет в jsonе текста, то есть фраза первая - начинаем диалог
    if not tokens:
        params_dict = first_phrase()
    # если диалог идёт - продолжаем его
    elif req_dialogue_number:
        params_dict = continue_dialogue(tokens, req_dialogue_number, req_speech_number)
    # если диалога нет - ищем ключевые слова во фразе
    else:
        params_dict = execute_command_with_name(tokens)
    return params_dict.get('text'), params_dict.get('dialogue'), params_dict.get('speech')
