import json
import os
import datetime
import requests
import requests_cache

from flask import Flask, render_template, jsonify

app = Flask(__name__)

# This is a method using library requests_cache.
# This exactly suits the use case. Uses a temporary sqlite database for this purpose
requests_cache.install_cache('github_cache', backend='sqlite', expire_after=604800)


@app.route('/')
def hello_world():
    return render_template('index.html')


# Using library method
@app.route('/get_rate/<curr>/<year>/<month>/<day>')
def get_rate(curr, year, month, day):
    url = 'https://api.exchangeratesapi.io/' + year + '-' + month + '-' + day + '?base=' + curr
    response_dict = requests.get(url).json()
    return jsonify(response_dict)


# Raw method written using json file. Needs currency and date as input
@app.route('/get_rate_loc/<curr>/<year>/<month>/<day>')
def get_rate_loc(curr, year, month, day):
    # Unique key to store a request
    key = curr+year+month+day
    # Dictionary to be written in json file
    storage_dict = {}
    response_dict = {}
    # Check if file exists
    if os.path.isfile('data.txt'):
        # Loading json file
        with open('data.txt') as json_file:
            storage_dict = json.load(json_file)
    # If key in file, check age
    if key in storage_dict:
        response_dict = storage_dict[key]
        # Find age using datetime
        age = datetime.datetime.now() - datetime.datetime.strptime(response_dict['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        # Get number of days
        days = divmod(age.total_seconds(), 86400)[0]
        # If more than 7 days, remove the key pair. Will be populated with new value in next steps
        if days >= 7:
            del storage_dict[key]
    # If not in json, query API and get it
    if key not in storage_dict:
        # Build URL
        url = 'https://api.exchangeratesapi.io/' + year + '-' + month + '-' + day + '?base=' + curr
        response_dict = requests.get(url).json()
        # Store timestamp of the fetch record in same dict
        response_dict['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        # Add the record to json dump file with unique key
        storage_dict[key] = response_dict
        # Dump the dict to json file
        with open('data.txt', 'w') as outfile:
            json.dump(storage_dict, outfile)
    return jsonify(response_dict)


if __name__ == '__main__':
    app.run(debug=True)
