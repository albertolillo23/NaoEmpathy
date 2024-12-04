# coding=utf-8
import json
import os
import time
import unicodedata
import socket
from naoqi import ALProxy
import sys


headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}


class NAO():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.checked = []
        # self.tts = self.create_proxy("ALTextToSpeech")
        self.tts = self.create_proxy("ALAnimatedSpeech")
        self.configuration = str({"bodyLanguageMode": "contextual"})
        self.leds = self.create_proxy("ALLeds")
        self.path_json = os.getcwd() + "/esperimento/phrase.json"
        self.path_color = os.getcwd() + "/esperimento/colors.json"
        self.final = {}
        self.id = 0
        self.last_id = 0
        self.best_emotion = ""
        self.counter = 1
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 12345)
        self.parla = False

    # init ALProxy for given module
    def create_proxy(self, name):

        try:
            proxy = ALProxy(name, self.ip, self.port)
            return proxy
        except Exception, e:
            print "Error when creating " + name + " proxy:"
            print str(e)

    @staticmethod
    def retrieve_json_data(path):
        with open(path, "r") as file:
            data = json.load(file)
            return data

    def run(self):

        # Connetti il socket all'indirizzo e alla porta del server
        self.client.connect(self.server_address)

        while True:
            data_local = self.retrieve_json_data(self.path_json)
            data_color = self.retrieve_json_data(self.path_color)

            while self.counter <= 14:

                self.final = self.retrieve_json_data(
                    "/Users/alberto/PycharmProjects/sentiment_local/data/temp_data/final.json")

                self.id = self.final["id"]
                self.best_emotion = self.final["best_emotion"]

                print(self.id, self.last_id)
                self.leds.reset("FaceLeds")
                if self.id != self.last_id:
                    self.last_id = self.id

                    if self.counter == 1:
                        starter = unicodedata.normalize('NFKD', data_local[str(self.counter)][0]["neutral"]).encode(
                            'ascii',
                            'ignore')
                        print data_local[str(self.counter)][0]["neutral"]
                        self.tts.say(starter, self.configuration)
                        self.counter += 1
                        print(self.counter)
                        self.client.sendall("False")

                    elif 1 < self.counter < 14:
                        R, G, B = data_color[str(self.best_emotion)][:3]

                        self.leds.fadeRGB("FaceLeds", 256 * 256 * R + 256 * G + B, 2)
                        phrase = unicodedata.normalize('NFKD',
                                                       data_local[str(self.counter)][0][self.best_emotion]).encode(
                            'ascii',
                            'ignore')
                        self.tts.say(phrase, self.configuration)
                        self.counter += 1
                        print(self.counter)
                        self.client.sendall("False")

                    else:
                        self.client.sendall("True")
                        time.sleep(5)
                        sys.exit()

                time.sleep(1)
            self.leds.reset("FaceLeds")
            self.client.close()


if __name__ == '__main__':
    nao = NAO('nao01.local', 9559)
    nao.run()
