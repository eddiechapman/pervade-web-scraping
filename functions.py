from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import json


def get_page(url):
    try:
        response = get(url)
        if response.status_code == 200:
            print('Good response: ' + url)
            return BeautifulSoup(response.content, 'html.parser')
    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def to_json(degree):
    print(json.dumps(degree, indent=2))


def export_csv():
    pass