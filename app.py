from flask import Flask, jsonify
from flask.json import dumps, loads
import datetime
from flask_wtf import CSRFProtect
import tempfile
from dotenv import load_dotenv
import os
import logging

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_APP')
csrf = CSRFProtect(app)


class Water():
    
    def __init__(self,  **kwargs):
        self.__quantity_drunk_l = None
        self.__drunk_history = []
        if 'user_id' in kwargs and kwargs['user_id'] is not None:
            self.__user_id = int(kwargs['user_id'])
            self.__file_name = f'./water{self.__user_id}.json'
        else:
            self.__file_name = './water.json'
        
        
    @property
    def quantity_drunk_l(self) -> int:
        if self.__quantity_drunk_l is None:
            if  os.path.isfile(self.__file_name):
                with open(self.__file_name, 'r') as f:
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
        if  os.path.isfile(self.__file_name):
                with open(self.__file_name, 'r') as f:
                    data = f.read()
                    data_json = loads(data)
                    if 'adding' in data_json:
                        self.__drunk_history = data_json['adding']
        self.__drunk_history.append(added_water) 
        return self.__quantity_drunk_l                 
                
    
    def save_water(self):
        water = dumps(self.serialize())
        with open(self.__file_name, 'w') as f:
            f.write(water)
    
    def save_water_by_user(self, water: dict, user_id: int):
        with open(f'./water{user_id}.json', 'w') as f:
            f.write(dumps(water))
        return water
            
    def serialize(self) -> dict:
        return {'water': self.quantity_drunk_l, 
                           "adding": self.__drunk_history}  
           
@app.route('/drink', methods=['GET'])
@app.route('/drink/<int:user_id>', methods=['GET'])
def drink_get(user_id: int = None):
    water = Water(user_id=user_id)
    water.drink()
    water.save_water()
    return jsonify(water.serialize())


@app.route('/status', methods=['GET'])
@app.route('/status/<int:user_id>', methods=['GET'])
def water_status(user_id: int = None):
    water = Water(user_id=user_id)
    logfile = tempfile.TemporaryFile()
    logfile.write(f'getting water at {datetime.datetime.now()}'.encode())
    logfile.close()
    return jsonify(water.serialize())



@app.route('/add_alert/<int:user_id>')
def check_alert(user_id: int):
    water1 = Water(user_id=user_id)
    if water["water"] < 10:
        return loads("alert missing water")
    return loads("everything is ok")


if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG', False))
