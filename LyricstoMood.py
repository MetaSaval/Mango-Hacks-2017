""" Code that uses IBM Watson to convert lyrics to mood """

import requests
import time
import serial

# Supposed to return the lyrics to the song name passed in as a parameter
# Needs to return a concatnated string of lyrics, search is not too efficient,
# needs to be made efficient
def lyrics(search):
    url = "https://api.cognitive.microsoft.com/bing/v5.0/news/search?q=" \
    + search + "&count=10&offset=0&mkt=en-us&safeSearch=Moderate"

    header = {'Host': 'api.cognitive.microsoft.com', \
    'Ocp-Apim-Subscription-Key': 'a7c37c0e2b124cfe8e74f4824693d0f6'}

    resp = requests.get(url, headers=header)
    if resp.status_code != 200:
        print(resp.status_code)

    respJson = resp.json()
    print(respJson)
    respVal = respJson['value']
    for a in range(0,len(respVal)):
        print(respVal[a]['description'])

# Supposed to return the percentages of mood found in a text
def moods(text):
    url = 'https://watson-api-explorer.mybluemix.net/tone-ana \
    lyzer/api/v3/tone?version=2016-05-19'
    data = text
    username = '7144acc5-8b6b-4721-98c0-7696a547a450'
    password = 'W0LzbWyPDmsl'
    header = {"content-type": "text/plain"}
    resp = requests.post(url, data=data, auth=(username, password), headers=header)
    if resp.status_code != 200:
        print(resp.status_code)

    respJson = resp.json()
    respDocTone = respJson['document_tone']
    respToneCat = respDocTone['tone_categories']
    respTones = respToneCat[0]
    respInTones = respTones['tones']

    # opening a serial port to send data to the Arduino
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    time.sleep(2)

    # write to serial
    for a in range(0, len(respInTones)):
        ser.write(str(respInTones[a]['score']) + " ")

    ser.close()

    # Big thanks to Matt
