from flask import Flask,jsonify
import json
import datetime
from flask_wtf import CSRFProtect
import tempfile
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_APP')
csrf = CSRFProtect(app)

class Water():
    def __init__(self):
        self.quantity_drunk_l = 0

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
    return water
    
def save_water_by_user(water, user_id):
    with open(f'./water{user_id}.json', 'w') as f:
        f.write(json.dumps(water))
    return water

# Ajoute de l'eau
@app.route('/add_water', methods=['GET'])
def add_water():
    water = read_water()
    added_quantity = 10
    water["water"] += added_quantity
    added_water = {'added_at': str(datetime.datetime.now()), 'quantity': added_quantity}
    if  "adding" in water.keys():
      water["adding"].append(added_water)
    else:
       water["adding"] = [added_water]
    return save_water(water)

# Get water
@app.route('/water', methods=['GET'])
def water():
    logfile = tempfile.TemporaryFile()
    logfile.write(f'getting water at {datetime.datetime.now()}'.encode())
    logfile.close()
    return read_water()
  


@app.route('/add_water/<user_id>')
def add_water_user(user_id):
    water = read_water_by_user(user_id)
    water["water"] += 10
    save_water_by_user(water, user_id)
    return water

@app.route('/add_alert/<user_id>')
def check_alert(user_id):
    water = read_water_by_user(user_id)
    if water["water"] < 10:
        return jsonify("alert missing water")
    return jsonify("everything is ok")

if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG', False))

    

