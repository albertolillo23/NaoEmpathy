import sys
import os
import qi
import urllib2
import json
from naoqi import ALProxy
import ssl
import time

last_id = None


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


def main(session):
    global last_id
    tts_service = session.service("ALTextToSpeech")
    led_service = session.service("ALLeds")
    url = "https://whisper.wollybrain.di.unito.it/control"
    path_json = os.getcwd() + "/json_ex.json"
    path_color = os.getcwd() + "/colors.json"

    counter = 1

    data_local = retrieve_json_data(path_json)
    data_color = retrieve_color_data(path_color)

    while True:
        id, last_id, best_emotion = json_request(url)
        print(id, last_id)
        if id != last_id:
            last_id = id
            if counter < 7:
                # tts_service.say(data_local[str(counter)][0][best_emotion])
                #color_settings(data_color[best_emotion], led_service)
                # print (data_color["neutral"], type(data_color["neutral"]))
                R = data_color["disgust"][0]
                G = data_color["disgust"][1]
                B = data_color["disgust"][2]

                led_service.fadeRGB("FaceLeds", 0 + 255 + 0, 0.5)
                led_service.reset("FaceLeds")

                counter += 1
            else:
                break
        time.sleep(1)


def color_settings(led_color, led_service):
    led_service.fadeRGB("FaceLeds", led_color, 1.0)


if __name__ == "__main__":
    ip = "nao01.local"
    port = 9559
    session = qi.Session()
    try:
        session.connect("tcp://" + ip + ":" + str(port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + ip + "\" on port " + str(port) + ".\n"
                                                                                    "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    main(session)
