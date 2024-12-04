import urllib2
import json
import ssl
import random

# Define the URL of the API endpoint
url = "https://whisper.wollybrain.di.unito.it/update"

# Create a dictionary with the data you want to update
data_to_update = {
    "id": random.randint(1, 1000),
    "best_emotion": "happy",
    "complex_dyads": "None"
}

# Convert the dictionary to a JSON string
json_data = json.dumps(data_to_update)

# Create an SSL context that does not verify certificates
context = ssl._create_unverified_context()

# Create a request object with the URL and data
request = urllib2.Request(url, data=json_data)

# Add a 'Content-Type' header to indicate JSON content
request.add_header('Content-Type', 'application/json')

try:
    # Open the request and read the response
    response = urllib2.urlopen(request, context=context)
    content = response.read()
    print("Update successful.")
    # Optionally, process the response data
    print(content)
except urllib2.URLError as e:
    print("Update failed. Error:", e.reason)



