import logging.config
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from config.logger import LOGGER
from phrases.command_actions import execute_command_with_name
from phrases.talks import continue_dialogue, first_phrase
from phrases.utils import create_request_objs, create_response_objs

logging.config.dictConfig(LOGGER)
logger = logging.getLogger(__name__)


@csrf_exempt
def main(request):
    body = json.loads(request.body)
    logger.info(body)
    response = create_response_objs(body)
    request = create_request_objs(body)
    handle_dialog(response, request)
    logger.info(response.to_json())
    return JsonResponse(response.to_json())


def handle_dialog(response, request):
    if not request.text:
        first_phrase(response)
    elif request.dialogue:
        continue_dialogue(response, request)
    else:
        execute_command_with_name(request, response)
