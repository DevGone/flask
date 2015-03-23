import threading, time, requests, json
from raspberric import get_yesterday_consumption, getRaspberricId

POLLING = False

SERVER = "http://devgone.herokuapp.com"
#SERVER = "http://localhost:3000"

def polling(timeInterval, callback, raspberricData):
	i = 0
	while True:
		callback(i, raspberricData)
		time.sleep(timeInterval)
		i+=1

def idling(timeInterval):
	i = 0
	while True:
		ping(i)
		time.sleep(timeInterval)
		i+=1

def fetchRaspberricData(measureId, raspberricData):
	print 'Fetching data from raspberric...'
	measure = json.loads(get_yesterday_consumption())
	print 'Data fetched'
	data = json.loads(raspberricData)
	data['measure'] = measure
	return json.dumps(data)

def sendData(data, url=SERVER+"/measures/"):
	headers = {'content-type': 'application/json'}
	req = requests.post(url, data=data, headers=headers)
	return req.text

def repeatTask(measureId, raspberricData):
	json = fetchRaspberricData(measureId, raspberricData)
	sendData(json)
	print 'Data sent'

def startPollingRaspberric(timeInterval, raspberricData):
	if "polling" not in startPollingRaspberric.__dict__:
		startPollingRaspberric.polling = True
		print 'Start polling'
		thread = threading.Thread(target=polling, name='Polling', kwargs={'timeInterval': timeInterval, 'callback': repeatTask, 'raspberricData':raspberricData})
		thread.daemon = True
		thread.start()

def ping(pingId, url=SERVER):
	req = requests.get(url)
	print 'Pinged Heroku: ' + str(req.status_code)

def startHerokuIdlingPrevention():
	if "polling" not in startHerokuIdlingPrevention.__dict__:
		startHerokuIdlingPrevention.polling = True
		print 'Start idling prevention'
		thread = threading.Thread(target=idling, name='Idling', kwargs={'timeInterval': 60*10})
		thread.daemon = True
		thread.start()

