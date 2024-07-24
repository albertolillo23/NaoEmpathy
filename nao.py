import sys

import qi
import urllib2
import json
from naoqi import ALProxy


# Specify the URL

# Chiamata al servizio
def json_request(url):
    try:
        # Open the URL and read the response
        response = urllib2.urlopen(url)
        content = response.read()

        # Parse the JSON content
        data = json.loads(content)
        #print(data)
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
def load_json_file(file):
    try:
        with open(file, 'r') as file:
            data = json.load(file)
            return data
    except IOError:
        print "Errore impossibile aprire il file"
    except ValueError:
        print "Errore non valido"
    except Exception as e:
        print "Errore", e
    return None


def main():
    #tts_service = session.service("ALTextToSpeech")
    url = "https://whisper.wollybrain.di.unito.it/control"
    counter = 1
    vecchio_id = None

    while True:
        risposta = json_request(url)
        id = risposta.get('id')

        if id != vecchio_id:
            emozione = risposta.get('best_emotion')
            file_path = 'json_ex.json'
            data = load_json_file(file_path)

            if data:
                if str(counter) in data:
                    print "Dati per il contatore:", counter
                    if emozione in data[str(counter)][0]:
                        frase = data[str(counter)][0][emozione]
                        print(frase)
                        counter += 1
                    else:
                        print("Emozione non trovata nel dizionario per il contatore:", str(counter))
                else:
                    print("Contatore non valido o chiave non trovata nel JSON:", str(counter))
            else:
                print("Errore nel caricamento del JSON.")

            vecchio_id = id

            #tts_service.say(value)



if __name__ == '__main__':
    main()

#if __name__ == "__main__":
#    ip = "nao01.local"
#    port = 9559
#    session = qi.Session()
#    try:
#       session.connect("tcp://" + ip + ":" + str(port))
#    except RuntimeError:
#        print ("Can't connect to Naoqi at ip \"" + ip + "\" on port " + str(port) + ".\n"
#                                                                                    "Please check your script arguments. Run with -h option for help.")
#        sys.exit(1)

#    main(session)
