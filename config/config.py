import os

from dotenv import load_dotenv

load_dotenv()

API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = os.getenv('API_PORT', '8000')

BASE_URL = f'http://{API_HOST}:{API_PORT}/api/v1/'

URL_FILM_LIST_SORT = 'film/?sort={}'
URL_FILM_ITEM = 'film/'
URL_FILM_SEARCH = 'film/search?sort=-imdb_rating&query='
URL_PERSON_SEARCH = 'person/search?query='
