import urllib2
import json
import time
import os
import signal
import sys
import subprocess

verbose=False
apiKey=""
pws=""
temp=""
delay=5*60
#delay=30
doClock=False
pipe=None


def fetchData():
    global verbose, apiKey, pws, temp, doClock
    f=None
    if (doClock > 0):
        temp = time.strftime("%I:%M")
        if (verbose):
            print("VERBOSE: mockData=" + temp)
        return
    try:
        url = "http://api.wunderground.com/api/{0}/conditions/q/pws:{1}.json".format( apiKey, pws )
        if (verbose):
            print("VERBOSE: url=" + url)
        f = urllib2.urlopen( url )
        json_string = f.read()
        if (verbose):
            print("VERBOSE: result=" + json_string)
        parsed_json = json.loads(json_string)
        if ("error" in parsed_json):
            print("error in response: " + parsed_json["error"]["description"])
            temp = "error"
        else:
            temp_f = parsed_json['current_observation']['temp_f']
            temp= "{:.0f}".format(temp_f)
    except:
        temp = "error"
        print "Unexpected error:", sys.exc_info()[0]

    if (f != None):
        f.close()

def displayData():
    global verbose, temp, pipe
    if (verbose):
        print("VERBOSE: writing to pipe")
    pipe.stdin.write(  " " + temp + "\n" )

def main():
    global verbose, apiKey, pipe, pws
    apiKey=os.getenv('WUNDERGROUND_API_KEY',"")
    if (apiKey == ""):
        print "WUNDERGROUND_API_KEY doesn't exist"
        exit(1)
    pws=os.getenv('WUNDERGROUND_PWS',"")
    if (pws == ""):
        print "WUNDERGROUND_PWS doesn't exist"
        exit(1)
    dcled=os.getenv('DCLED',"")
    if (dcled == ""):
        print "DCLED doesn't exist"
        exit(1)

    try:
        pipe = subprocess.Popen(["sudo", dcled, "-rf"], stdin=subprocess.PIPE)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        exit(1)

    while (1):
        fetchData()
        displayData()
        time.sleep(delay)

if __name__ == "__main__":
    main()


