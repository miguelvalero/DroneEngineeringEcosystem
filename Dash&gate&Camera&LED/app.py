import json

from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

#from data import data

# Testing Route
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})

# Routes
# clients wanting all stored positions will GET this URL:
# localhost:4000/data
@app.route('/data')
def getData():
    return jsonify(data)

# clients wanting all store a new position will POST the new position to this URL:
# localhost:4000/data
@app.route('/data', methods=['POST'])
def addData():
    # We add a time stamp to the position (lat, lon)
    now = datetime.now()
    # build the new json object containing the position (and time stamp)
    new_data = {
        'time': str(now),
        'lat': request.json['lat'],
        'lon': request.json['lon']
    }
    # add the new position to the list (in memory)
    data.append(new_data)
    json_string = json.dumps(data)
    # writes the new position in the file
    with open('data.json', 'w') as outfile:
        outfile.write(json_string)
    # returns the updated list as a result of the POST
    return jsonify(data)


if __name__ == '__main__':
    print ('Starting API')
    # Load stored positions
    # we want to have the stored positions in a list (in memory)
    with open('data.json') as json_file:
        data = json.load(json_file)
    # start listening
    app.run(debug=True, port=4000)