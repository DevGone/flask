import threading
import urllib2
from datetime import datetime, timedelta

LOCAL = 0

def correct_url():
	if LOCAL == 1 :
		url = "http://rpic-remixmyenergy-edf.local/"
	else :
		url = "http://raspberricdevgone.ddns.net/"
	return url

def get_history(field, step, duration_type, duration):
	begin_datetime = get_begin_date(duration_type, duration)
	begin_date = convert_date(begin_datetime - timedelta(hours=1)) #need to remove 1 hour to get the same result as raspberric
	date = convert_date(datetime.now() - timedelta(hours=1)) #need to remove 1 hour to get the same result as raspberric
	print correct_url() + 'history?field=' + field + '&limit=none&step=' + step +'&begin=' + begin_date + 'Z&end=' + date + 'Z'
	req = urllib2.Request(correct_url() + 'history?field=' + field + '&limit=none&step=' + step +'&begin=' + begin_date + 'Z&end=' + date + 'Z')
	response = urllib2.urlopen(req)
	data = response.read()
	return data

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
	return str(datetime.date(value)) + 'T' + str(datetime.time(value))

def polling(timeInterval, callback):
  thread = threading.Timer(timeInterval, lambda: polling(timeInterval, callback))
  thread.daemon = True
  callback()
