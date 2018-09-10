# for more information on how to install requests
# http://docs.python-requests.org/en/master/user/install/#install
import requests
import json
import random

import sys
sys.path.append('./src/inflect/')

import inflect

# TODO: replace with your own app_id and app_key
app_id = '7c76b685'
app_key = '0eeb762c4e112acbc73dd9d7c5142812'

language = 'en'

def get_adjective():
	url = 'https://od-api.oxforddictionaries.com:443/api/v1/wordlist/' + language + '/lexicalCategory=adjective?limit=1&offset=' + random.randint(0, 47654).__str__()

	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

	print("code {}\n".format(r.status_code))
	print("text \n" + r.text)
	print("json \n" + json.dumps(r.json()))

	word = r.json()["results"][0]["word"]

	return word

def get_noun():
	url = 'https://od-api.oxforddictionaries.com:443/api/v1/wordlist/' + language + '/lexicalCategory=noun?limit=1&offset=' + random.randint(0, 158519).__str__()

	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

	print("code {}\n".format(r.status_code))
	print("text \n" + r.text)
	print("json \n" + json.dumps(r.json()))

	word = r.json()["results"][0]["word"]

	return word

def get_text():
	inf = inflect.engine()

	adj = get_adjective()
	noun = get_noun()
	artist = 'The ' + adj.title() + ' ' + inf.plural(noun).title()

	adj = get_adjective()
	noun = get_noun()
	album = adj.title() + ' ' + inf.plural(noun).title()

	adj = get_adjective()

	text = 'Zane Lowe recommends "' + album + '" -- the ' + adj + ' debut album by ' + artist + '.'

	return text