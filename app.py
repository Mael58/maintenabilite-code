from flask import Flask
import json
import datetime
from flask_wtf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)

class Water():
    def __init__(self):
        self.water = 0

def read_water():
    water = None
    with open('./water.json', 'r') as f:
        data = f.read()
        water = json.loads(data)
    return water

def read_water_by_user(user_id):
    water = None
    with open(f'./water{user_id}.json', 'r') as f:
        data = f.read()
        water = json.loads(data)
    return water

def save_water(water):
    with open('./water.json', 'w') as f:
        f.write(json.dumps(water))


def save_water_by_user(water, user_id):
    with open(f'./water{user_id}.json', 'w') as f:
        f.write(json.dumps(water))

# Ajoute de l'eau
@app.route('/add_water', methods=['GET'])
def add_water():
    water = read_water()
    print(water)
    water["water"] += 10
    if not "adding" in water.keys():
        water["adding"] = [{'added_at': str(datetime.datetime.now()), 'quantity': 10}]
        return save_water(water)
    else:
        water["adding"].append({'added_at': datetime.datetime.now(), 'quantity': 10})
        return save_water(water)

import tempfile

# Get water
@app.route('/water', methods=['GET'])
def water():
    filename = tempfile.TemporaryFile()
    logfile = open(filename, 'a')
    logfile.write(f'getting water at {datetime.datetime.now()}')
    logfile.close()
    return read_water()
  


@app.route('/add_water/<user_id>')
def add_water_user(user_id):
    water = read_water_by_user(user_id)
    print(water)
    water["water"] += 10
    save_water_by_user(water, user_id)
    return water

@app.route('/add_alert/<user_id>')
def check_alert(user_id):
    water = read_water_by_user(user_id)
    if water < 10:
        return 'altert missing water'
    else:
        return 'everything is ok'

if  __name__ == '__main__':
    print('using as import')
else:
    app.run(debug=True)

