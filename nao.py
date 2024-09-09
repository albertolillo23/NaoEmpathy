import sys
import os
import urllib2
import json
from naoqi import ALProxy
import ssl
import time

last_id = 0


def json_request(url):
    try:
        # Create an SSL context that does not verify certificates
        context = ssl._create_unverified_context()

        # Open the URL without certificate verification
        response = urllib2.urlopen(url, context=context)
        content = response.read()

        # Parse the JSON content
        data_cloud = json.loads(content)

        id = data_cloud["id"]
        best_emotion = data_cloud["best_emotion"].encode("utf-8")

        return id, last_id, best_emotion

    except urllib2.URLError as e:
        print("Network error: ", e.reason)
    except ValueError as e:
        print("Parsing error: ", e)


def retrieve_json_data(path):
    with open(path, "r") as file:
        data = json.load(file)
        return data


def retrieve_color_data(path):
    with open(path, "r") as file:
        data = json.load(file)
        return data


def main(tts, leds):
    global last_id

    url = "https://whisper.wollybrain.di.unito.it/control"
    path_json = os.getcwd() + "/json_ex.json"
    path_color = os.getcwd() + "/colors.json"

    counter = 1

    data_local = retrieve_json_data(path_json)
    data_color = retrieve_color_data(path_color)

    while True:
        id, last_id, best_emotion = json_request(url)
        print(id, last_id)
        leds.reset("FaceLeds")
        if id != last_id:
            last_id = id
            if counter == 1:
                tts.say(str(data_local[str(counter)][0]["neutral"]))
                counter += 1
            if counter < 7 & counter > 1:
                R = data_color[str(best_emotion)][0]
                G = data_color[str(best_emotion)][1]
                B = data_color[str(best_emotion)][2]

                leds.fadeRGB("FaceLeds", 256*256*R + 256*G + B, 1)
                tts.say(str(data_local[str(counter)][0][best_emotion]))
                counter += 1

        time.sleep(1)


if __name__ == "__main__":
    ip = "nao01.local"
    port = 9559
    tts = ALProxy("ALTextToSpeech", ip, port)
    leds = ALProxy("ALLeds", ip, port)
    tts.setLanguage("Italian")
    tts.setVolume(0.5)
    tts.setParameter("speed", 100)
    main(tts, leds)
