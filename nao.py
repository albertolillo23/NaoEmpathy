import qi
import urllib2
import json

# Specify the URL
url = "https://whisper.wollybrain.di.unito.it/control"

try:
    # Open the URL and read the response
    response = urllib2.urlopen(url)
    content = response.read()

    # Parse the JSON content
    data = json.loads(content)
    print(data)
except urllib2.URLError as e:
    print("Network error: ", e.reason)
except ValueError as e:
    print("Parsing error: ", e)