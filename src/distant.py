import threading, time, requests, json
from raspberric import get_last_hour_consumption, get_informations

POLLING = False

SERVER = "http://devgone.herokuapp.com"
#SERVER = "http://localhost:3000"

def polling(timeInterval, callback, raspberricIds):
	i = 0
	while True:
		callback(i, raspberricIds)
		time.sleep(timeInterval)
		i+=1

def idling(timeInterval):
	i = 0
	while True:
		ping(i)
		time.sleep(timeInterval)
		i+=1

def fetchRaspberricData(measureId, raspberricIds):
	data = []
	print 'Fetching data from raspberrics...'
	for raspberricId in raspberricIds :
		info = json.loads(get_informations(raspberricId))
		measure = json.loads(get_last_hour_consumption(raspberricId))
		jsonResult = parseResults(raspberricId, info, measure)
		data.append(jsonResult)
	print 'Data fetched'
	return json.dumps(data)

def sendData(data, url=SERVER+"/measures/"):
	headers = {'content-type': 'application/json'}
	req = requests.post(url, data=data, headers=headers)
	return req.text

def repeatTask(measureId, raspberricIds):
	json = fetchRaspberricData(measureId, raspberricIds)
	sendData(json)
	print 'Data sent'

def startPollingRaspberric(timeInterval, raspberricIds):
	if "polling" not in startPollingRaspberric.__dict__:
		startPollingRaspberric.polling = True
		print 'Start polling'
		thread = threading.Thread(target=polling, name='Polling', kwargs={'timeInterval': timeInterval, 'callback': repeatTask, 'raspberricIds':raspberricIds})
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

def parseResults(raspberricId, info, measure):
	begin_date = info['data'][0]['begin']
	price_option = info['data'][0]['price-option']['slug']

	# Get delta of the total consumption
	measure_lenght = len(measure['data'])
	consumption = measure['data'][0]['value'] - measure['data'][measure_lenght-1]['value']

	result = {}
	result['raspberricId'] = raspberricId
	result['begin_date'] = begin_date
	result['price_option'] = price_option
	result['delta_consumption'] = consumption
	result['measure'] = measure['data']

	return result # json.dumps(result)