import random

from config.phrase_sets import addition_phrases, new_phrases, regret_phrases, suggest_phrases
from src.command_actions import get_new_film, get_good_film, get_random_film, get_random_film_by_genre

dialogue_new_or_best_film = ["Хотите, посоветую вам фильм?", "Вам поновее или классику?"]
dialogue_genre = ["Вы больше любите фантастику, мультфильмы или комедии?", "В каком из них посоветовать вам фильм?"]
dialogue_random_film_all_info = ["Рассказать вам про какой-нибудь фильм?"]

dialogs = [dialogue_new_or_best_film, dialogue_random_film_all_info, dialogue_genre]


def first_phrase(res):
    number = random.randint(1, 3)
    res['session_state'] = {'dialogue': number, "speech": 1}
    res['response']['text'] = "Здравствуйте. Приветствую вас в нашем кинотеатре. " + dialogs[number-1][0]
    return res


def perform_dialogue_new_or_best_film(res, req):
    speech_number = req.get('state', {}).get('session', {}).get('speech', 0)
    if speech_number == 1:
        if set(req['request']['nlu']['tokens']) & set(suggest_phrases):
            res['session_state'] = {'dialogue': 1, "speech": 2}
            res['response']['text'] = dialogs[0][1]
        else:
            res['session_state'] = {'dialogue': 0}
            res['response']['text'] = ". ".join((random.choice(regret_phrases), random.choice(addition_phrases)))
    elif speech_number == 2:
        if set(req['request']['nlu']['tokens']) & set(new_phrases):
            res['response']['text'] = get_new_film("") + " - этот фильм вышел недавно. " + random.choice(addition_phrases)
        else:
            res['response']['text'] = get_good_film("") + " - у этого фильма высокий рейтинг. " + random.choice(addition_phrases)
        res['session_state'] = {'dialogue': 0}


def perform_dialogue_random_film_all_info(res, req):
    if set(req['request']['nlu']['tokens']) & set(suggest_phrases):
        f = get_random_film(None)
        res['session_state'] = {'dialogue': 0}
        res['response']['text'] = "Фильм {} в жанре {}. Пользователи оценили его в {} звёзд. Вот про что он {}. ". \
                                        format(f['title'], f['genre'][0], f['imdb_rating'],
                                            f['description']) + random.choice(addition_phrases)
    else:
        res['response']['text'] = ". ".join((random.choice(regret_phrases), random.choice(addition_phrases)))
    res['session_state'] = {'dialogue': 0}


def perform_dialogue_genre(res, req):
    if any([t.startswith('фантаст') for t in req['request']['nlu']['tokens']]):
        genre = 'Fantasy'
    elif any([t.startswith('мульт') for t in req['request']['nlu']['tokens']]):
        genre = 'Animation'
    elif any([t.startswith('комед') for t in req['request']['nlu']['tokens']]):
        genre = 'Comedy'
    else:
        res['response']['text'] = ". ".join((random.choice(regret_phrases), random.choice(addition_phrases)))
        return
    f = get_random_film_by_genre(genre)
    res['session_state'] = {'dialogue': 0}
    res['response']['text'] = "Тогда можем вам порекомендовать фильм {}. Пользователи оценили его в {} звёзд.".\
        format(f['title'], f['imdb_rating']) + random.choice(addition_phrases)


dialogs_functions = [perform_dialogue_new_or_best_film, perform_dialogue_random_film_all_info, perform_dialogue_genre]


def continue_dialogue(req, res):
    dialogue_number = res.get('state', {}).get('session', {}).get('dialogue', 0)
    dialogs_functions[dialogue_number-1](req, res)