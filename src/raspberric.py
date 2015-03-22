import requests
from datetime import datetime, timedelta
import json

LOCAL = 1

def correct_url():
	if LOCAL == 1 :
		return "http://rpic-remixmyenergy-edf.local/"
	else :
		return "http://raspberricdevgone.ddns.net/"

def get_history_from_now(field, step, duration_type, duration):
	begin_datetime = get_begin_date(duration_type, duration)
	begin_date = convert_date(begin_datetime - timedelta(hours=1)) #need to remove 1 hour to get the same result as raspberric
	end_date = convert_date(datetime.now() - timedelta(hours=1)) #need to remove 1 hour to get the same result as raspberric
	limit = 'none'
	url = correct_url() + "history"
	params = {'field': field, 'limit': limit, 'step': step, 'begin': begin_date, 'end': end_date}
	req = requests.get(url, params=params)
	return req.text

# Get information about the installation : compteur id, price option and begin date
def get_informations():
	url = correct_url() + "source/1/price_option"
	params = {}
	req = requests.get(url, params=params)
	all_informations = json.loads(req.text)
	compteur_id = all_informations['data']['source']['parameters']['adco']
	begin_date = all_informations['data']['begin']
	price_option = all_informations['data']['price_option']['name']
	data = json.dumps({'compteur_id': compteur_id, 'begin_date': begin_date, 'price_option': price_option})
	return data

def get_compteur_id():
	all_informations = json.loads(get_informations())
	compteur_id = all_informations['data']['source']['parameters']['adco']
	return compteur_id

def get_begin_date():
	all_informations = json.loads(get_informations())
	begin_date = all_informations['data']['begin']
	return begin_date

def get_price_option():
	all_informations = json.loads(get_informations())
	price_option = all_informations['data']['price_option']['name']
	return price_option

def convert_price_option_to_field(price_option):
	if price_option == "HP/HC" :
		value = "hchp"
	return value

#TODO : réflechir à une optimisation (as besoin de remonter toutes les données au milieu des deux dates)
def get_consumption(begin_date, end_date, step):
	url = correct_url() + "history"
	params = {'field': convert_price_option_to_field(), 'limit': 'none', 'step': step, 'begin': begin_date, 'end': end_date}
	req = requests.get(url, params=params)

	all_consumption = json.loads(req.text)
	all_consumption_lenght = len(all_consumption['data'])
	consumption = all_consumption['data'][0]['value'] - all_consumption['data'][all_consumption_lenght-1]['value']
	return str(consumption)

# Get consumption from a date to now in Watt-heure
#TODO : verifier impact du pattern sur résultat
def get_consumption_from_now(step, duration_type, duration) :
	url = correct_url() + "history"
	begin_datetime = get_begin_date(duration_type, duration)
	begin_date = convert_date(begin_datetime - timedelta(hours=1))
	end_date = convert_date(datetime.now() - timedelta(hours=1))

	field = "hchp"
	limit = 'none'
	params = {'field': field, 'limit': limit, 'step': step, 'begin': begin_date, 'end': end_date}
	req = requests.get(url, params=params)

	all_consumption = json.loads(req.text)
	all_consumption_lenght = len(all_consumption['data'])
	consumption = all_consumption['data'][0]['value'] - all_consumption['data'][all_consumption_lenght-1]['value']
	return str(consumption)

# Get consumption of the last 24 hours
#TODO : verifier que y a pas un decallage qui fait manquer une valeur
def get_yesterday_consumption() :
	return get_consumption_from_now(3600, 'day', 1)

def get_begin_date(duration_type, duration):
	if duration_type == "week" :
		return datetime.now() - timedelta(weeks=int(duration))
	elif duration_type == "day" :
		return datetime.now() - timedelta(days=int(duration))
	elif duration_type == "hour" :
		return datetime.now() - timedelta(hours=int(duration))
	elif duration_type == "minute" :
		return datetime.now() - timedelta(minutes=int(duration))
	elif duration_type == "second" :
		return datetime.now() - timedelta(seconds=int(duration))

def convert_date(value):
	return str(datetime.date(value)) + 'T' + str(datetime.time(value)) + 'Z'

def getRaspberricId():
	return 'vf6sxo78'
