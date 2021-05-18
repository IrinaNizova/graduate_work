from src.command_actions import execute_command_with_name
from src.talks import first_phrase, continue_dialogue

from flask import Flask
from flask import request
import json

app = Flask(__name__)


@app.route('/post', methods=['POST'])
def main():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    return json.dumps(response)


def handle_dialog(res,req):
    phrase = req['request']['command']
    if not req['request']['command']:
        first_phrase(res)
    elif req.get('state', {}).get('session', {}).get('dialogue', 0) > 0:
        continue_dialogue(res, req)
    else:
        res['response']['text'] = execute_command_with_name(phrase)


if __name__ == '__main__':
    app.run()
