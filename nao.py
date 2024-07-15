import qi
import urllib2

# Specify the URL
url = "https://whisper.wollybrain.di.unito.it/control"

try:
    # Open the URL and read the response
    response = urllib2.urlopen(url)
    content = response.read()
    print(content)
except urllib2.URLError as e:
    print("Error: ", e.reason)