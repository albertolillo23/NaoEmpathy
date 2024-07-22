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



#def main(session):
#   tts_service = session.service("ALTextToSpeech")
    #   url = "https://whisper.wollybrain.di.unito.it/control"
    #  counter = 0


#  while True:
#  json_request(url)


def main(session):
    tts_service = session.service("ALTextToSpeech")
    url = "https://whisper.wollybrain.di.unito.it/control"
    counter = 0
    vecchio_id = None

    while True:
        data = json_request(url)

        if data is None:
            continue

        new_id = data.get('id')

        if new_id != vecchio_id:
            vecchio_id = new_id

            best_emotion = data.get('best_emotion')

            if best_emotion:
                key = best_emotion

                try:
                    with open('json_ex.json', 'r') as file:
                        json_ex_data = json.load(file)

                    # Assicurati che la chiave sia presente nel file JSON
                    if key in json_ex_data:
                        values = json_ex_data[key]

                        # Assicurati che l'indice sia valido
                        if 0 <= counter < len(values):
                            value = values[counter]
                            print("Emozione: {key}, Valore: {value}")

                            # per far parlare il robot con tts_service
                           # tts_service.say(value)

                        counter += 1


                except IOError:
                    print("File 'json_ex.json' non trovato o errore di I/O.")
                except ValueError:
                    print("Errore nel decodificare il file JSON.")
                except Exception as e:
                    print("Errore: ", e)




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

