import pymorphy2

from phrases.validators import Request, Response


def create_request_objs(request):
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
    return Response(user_id=body['session']['user_id'],
                    session_id=body['session']['session_id'],
                    message_id=body['session']['message_id'],
                    version=body['version'])
