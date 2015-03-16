import threading, time, requests, json
from raspberric import get_history, getRaspberricId

POLLING = False

def polling(timeInterval, callback):
	i = 0
	while True:
		callback(i)
		time.sleep(timeInterval)
		i+=1

def fetchRaspberricData(measureId):
	print 'Fetching data from raspberric...'
	raspberricId = getRaspberricId();
	measure = json.loads(get_history("papp", 60*60, 'hour', 24))
	print 'Data fetched'
	data = json.dumps({'measure_id': measureId, 'raspberric_id': raspberricId, 'measure': measure})
	return data

def sendData(data, url="http://devgone.herokuapp.com/measures/"):
	headers = {'content-type': 'application/json'}
	req = requests.post(url, data=data, headers=headers)
	return req.text

def repeatTask(measureId):
	json = fetchRaspberricData(measureId)
	sendData(json)
	print 'Data sent'

def startPollingRaspberric(timeInterval):
	if "polling" not in startPollingRaspberric.__dict__:
		startPollingRaspberric.polling = True
		print 'Start polling'
		thread = threading.Thread(target=polling, name='Polling', kwargs={'timeInterval': timeInterval, 'callback': repeatTask})
		thread.daemon = True
		thread.start()

def ping(pingId, url="http://devgone.herokuapp.com/"):
	req = requests.get(url)
	print 'Pinged Heroku: ' + str(req.status_code)

def startHerokuIdlingPrevention():
	if "polling" not in startHerokuIdlingPrevention.__dict__:
		startHerokuIdlingPrevention.polling = True
		print 'Start idling prevention'
		thread = threading.Thread(target=polling, name='Idling', kwargs={'timeInterval': 60*10, 'callback': ping})
		thread.daemon = True
		thread.start()

