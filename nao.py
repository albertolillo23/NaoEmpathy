import sys

import qi
import urllib2
import json
from naoqi import ALProxy


# Specify the URL


def json_request(url):
    try:

        # Open the URL and read the response
        response = urllib2.urlopen(url)
        content = response.read()

        # Parse the JSON content
        data = json.loads(content)
        print(data)
        return data
    except urllib2.URLError as e:
        print("Network error: ", e.reason)
    except ValueError as e:
        print("Parsing error: ", e)


def main(session):
    tts_service = session.service("ALTextToSpeech")
    url = "https://whisper.wollybrain.di.unito.it/control"
    counter = 0

    while True:
        json_request(url)


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
