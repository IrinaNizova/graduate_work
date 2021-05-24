import logging.config
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from config.logger import LOGGER
from phrases.command_actions import execute_command_with_name
from phrases.talks import continue_dialogue, first_phrase
from phrases.utils import create_request_objs, create_response_objs
from phrases.validators import Request, Response

logging.config.dictConfig(LOGGER)
logger = logging.getLogger(__name__)


@csrf_exempt
def main(request):
    """
    Главная функция через которую идёт обработка
    :param request: объект запроса
    :return: ответ в формате json
    """
    body = json.loads(request.body)
    logger.info(body)
    response = create_response_objs(body)
    request = create_request_objs(body)
    handle_dialog(response, request)
    logger.info(response.to_json())
    return JsonResponse(response.to_json())


def handle_dialog(response: Response, request: Request) -> None:
    # управление диалогом
    # если нет в объекте текста, то есть фраза первая - начинаем диалог
    if not request.text:
        first_phrase(response)
    # если диалог идёт - продолжаем его
    elif request.dialogue:
        continue_dialogue(response, request)
    # если диалога нет - ищем ключевые слова во фразе
    else:
        execute_command_with_name(request, response)
