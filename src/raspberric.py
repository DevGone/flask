LOCAL = 0

def correctUrl():
	if LOCAL == 1 :
		url = ""
	else 
		url = "http://raspberricdevgone.ddns.net/"
	return url

def getData():
    return "This the raspberric data"
