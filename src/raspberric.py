from datetime import datetime, timedelta
import requests
import json

LOCAL_ORIANE = 1
LOCAL_OTHER = 0

#TODO : Change to put the other raspberric adress
# Get the correct raspberric url depending if the programm is working in the local network or not by raspberric id
def correct_url(raspberricId):
	if raspberricId == 'vf6sxo78' :
		if LOCAL_ORIANE == 1 :
			return "http://rpic-remixmyenergy-edf.local/"
		else :
			return "http://raspberricdevgone.ddns.net/"
	else : 
		if LOCAL_OTHER == 1 :
			return "http://rpic-remixmyenergy-edf.local/"
		else :
			return "http://raspberricdevgone.ddns.net/"

# Get information about the installation by raspberric id
def get_informations(raspberricId):
	url = correct_url(raspberricId) + "source/1/price-option"
	params = {}
	req = requests.get(url, params=params)
	return req.text

# Get price option slug by raspberric id
def get_price_option(raspberricId):
	all_informations = json.loads(get_informations(raspberricId))
	price_option = all_informations['data'][0]['price-option']['slug']
	return price_option

#TODO : add more price options
# Get field from the price option
def convert_price_option_to_field(price_option):
	if price_option == "hp-hc" :
		return "hchp"
	return "base"

#Get consumption by raspberric id, begin date, end date, step in seconds
def get_consumption(raspberricId, begin_date, end_date, step):
	url = correct_url(raspberricId) + "history"
	price_option = get_price_option(raspberricId)
	field = convert_price_option_to_field(price_option)
	params = {'field': field, 'limit': 'none', 'step': step, 'begin': begin_date, 'end': end_date}
	req = requests.get(url, params=params)
	return req.text

#TODO : Verify number of hours to remove to make the raspberric work
# Get consumption from a date to now in Watt-heure
def get_consumption_from_now(raspberricId, step, duration_type, duration) :
	url = correct_url(raspberricId) + "history"
	begin_datetime = get_begin_date(duration_type, duration)
	begin_date = convert_date(begin_datetime - timedelta(hours=1))
	end_date = convert_date(datetime.now() - timedelta(hours=1))

	price_option = get_price_option(raspberricId)
	field = convert_price_option_to_field(price_option)
	params = {'field': field, 'limit': 'none', 'step': step, 'begin': begin_date, 'end': end_date, 'pattern': 'max'}
	req = requests.get(url, params=params)
	return req.text


#TODO : verifier que y a pas un decallage qui fait manquer une valeur
# Get consumption of the last 24 hours every hour
def get_yesterday_consumption(raspberricId) :
	return get_consumption_from_now(raspberricId, 60*10, 'day', 1)

# Get consumption of the last hour every 10 minutes
def get_last_hour_consumption(raspberricId) :
	return get_consumption_from_now(raspberricId, 60*10, 'hour', 1)

# Get a date before now in fonction of duration type and duration value
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

# Concert datetime in the system wanted by the raspberric
def convert_date(value):
	return str(datetime.date(value)) + 'T' + str(datetime.time(value)) + 'Z'

# Get datetime now in the correct format
def get_date_now():
	return convert_date(datetime.now())


##### WE DON'T USE IT #######

# Get compteur id by raspberric id
def get_compteur_id(raspberricId):
	all_informations = json.loads(get_informations(raspberricId))
	compteur_id = all_informations['data'][0]['source']['parameters']['adco']
	return compteur_id

# Get records' begin date by raspberric id
def get_raspberric_begin_date(raspberricId):
	all_informations = json.loads(get_informations(raspberricId))
	begin_date = all_informations['data'][0]['begin']
	return begin_date

# Get history from now
def get_history_from_now(raspberricId, field, step, duration_type, duration):
	begin_datetime = get_begin_date(duration_type, duration)
	begin_date = convert_date(begin_datetime - timedelta(hours=1)) #need to remove 1 hour to get the same result as raspberric
	end_date = convert_date(datetime.now() - timedelta(hours=1)) #need to remove 1 hour to get the same result as raspberric
	url = correct_url(raspberricId) + "history"
	params = {'field': field, 'limit': 'none', 'step': step, 'begin': begin_date, 'end': end_date}
	req = requests.get(url, params=params)
	return req.text