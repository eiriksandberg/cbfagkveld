from flask import Flask, jsonify, request
import requests
import logging
from werkzeug.contrib.fixers import ProxyFix
from enum import Enum


class Gender(Enum):
    MALE = 'gutt'
    FEMALE = 'jente'


# App setup
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# URLs
mannenUrl = 'https://www.vondess.com/mannen/api'
doUrl = 'https://labbentheoffice.azurewebsites.net/api/toilet/IsToiletAvailable'

# Enter your name and gender for a super personalized greeting
name = 'Eirik'
gender = Gender.MALE.value

@app.route('/login', methods=['POST'])
def login():
    return jsonify({'new_context': {'gender': gender, 'name': name}, 'exchange_slug': 'greeting_slug'})


@app.route('/mannen', methods=['POST'])
def mannen():
    response = requests.get(mannenUrl).json()
    status = response['falt_ned']
    slug = 'fallen' if status is True else 'not_fallen'
    return jsonify({"exchange_slug": slug})


@app.route('/tissetrengt', methods=['POST'])
def tissetrengt():
    # For extracting gender from kindly context. Does not work on Zeit for whatever reason
    #kindlyBody = request.get_json(force=True)
    #gender = kindlyBody['context']['gender']

    response = requests.get(doUrl).json()
    available_toilet = any([x for x in response.keys() if gender in x and response[x] is True])
    slug = 'available_toilet' if available_toilet is True else 'not_available_toilet'
    return jsonify({"exchange_slug": slug})


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
