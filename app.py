from flask import Flask, jsonify
from flask.json import dumps, loads
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
    file_name = './water.json'
    def __init__(self):
        self.__quantity_drunk_l = None
        self.__drunk_history = []
        
        
    @property
    def quantity_drunk_l(self) -> int:
        if self.__quantity_drunk_l is None:
            if  os.path.isfile(self.file_name):
                with open(self.file_name, 'r') as f:
                    data = f.read()
                    data_json = loads(data)
                    self.__quantity_drunk_l = data_json['water']
            else:
                self.__quantity_drunk_l = 0
        return self.__quantity_drunk_l
    
    @quantity_drunk_l.setter
    def quantity_drunk_l(self, value: int):
        if value - self.__quantity_drunk_l == int(os.getenv('DEFAULT_QUANTITY')):
            self.__quantity_drunk_l = value
        else:
            raise ValueError(f"Invalid value regarding default quantity: {os.getenv('DEFAULT_QUANTITY')}")
    
    
    def drink(self) -> int:
        self.quantity_drunk_l += int(os.getenv('DEFAULT_QUANTITY'))
        
        added_water = {'added_at': str(
            datetime.datetime.now()), 'quantity': int(os.getenv('DEFAULT_QUANTITY'))}
        if  os.path.isfile(self.file_name):
                with open(self.file_name, 'r') as f:
                    data = f.read()
                    data_json = loads(data)
                    if 'adding' in data_json:
                        self.__drunk_history = data_json['adding']
        self.__drunk_history.append(added_water) 
        return self.__quantity_drunk_l
                   
                
    
    def save_water(self):
        water = dumps(self.serialize())
        with open(self.file_name, 'w') as f:
            f.write(water)
            
    def serialize(self) -> dict:
        return {'water': self.quantity_drunk_l, 
                           "adding": self.__drunk_history}
    


def read_water_by_user(user_id: int):
    water = None
    with open(f'./water{user_id}.json', 'r') as f:
        data = f.read()
        water = loads(data)
    return water

def save_water_by_user(water: dict, user_id: int):
    with open(f'./water{user_id}.json', 'w') as f:
        f.write(dumps(water))
    return water

@app.route('/drink', methods=['GET'])
def drink_get():
    water = Water()
    water.drink()
    water.save_water()
    return jsonify(water.serialize())


@app.route('/status', methods=['GET'])
def water_status():
    water = Water()
    logfile = tempfile.TemporaryFile()
    logfile.write(f'getting water at {datetime.datetime.now()}'.encode())
    logfile.close()
    return jsonify(water.serialize())


@app.route('/add_water/<user_id>')
def add_water_user(user_id: int):
    water = read_water_by_user(user_id)
    water["water"] += 10
    save_water_by_user(water, user_id)
    return water


@app.route('/add_alert/<user_id>')
def check_alert(user_id: int):
    water = read_water_by_user(user_id)
    if water["water"] < 10:
        return loads("alert missing water")
    return loads("everything is ok")


if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG', False))
