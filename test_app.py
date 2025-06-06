import pytest
import json
import os


from app import app, Water

@pytest.fixture()
def defapp():
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(defapp):
    return defapp.test_client()

@pytest.fixture()
def setup(request):
    water = { "water": 70 }
    with open('./water.json', 'w') as f:
        f.write(json.dumps(water))
    def teardown():
        os.remove('./water.json')
    request.addfinalizer(teardown)
    return water 

@pytest.fixture
def setup_user(request):
    water = {"water": 0}
    user_id = 32
    with open(f'./water{user_id}.json', 'w') as f:
        f.write(json.dumps(water))
    def teardown():
        os.remove(f'./water{user_id}.json')
        if os.path.exists('./water23.json'):
            os.remove('./water23.json')
    request.addfinalizer(teardown)
    return user_id

        
def test_request_example(client, setup):
    assert 70 == setup['water']
    response = client.get("/status")
    result = json.loads(response.data)
    assert 'water' in result
    assert 70 == result['water']
    
def test_request_save_exemple(client, setup):
    assert 70 == setup['water']
    response = client.get("/drink")
    result = json.loads(response.data)
    assert 'water' in result
    assert 80 == result['water']

def test_read_water(setup):
    water =Water()
    result = water.quantity_drunk_l
    assert 70 == result
    
def test_save_water(setup):
    assert 70 == setup['water']
    water = Water()     
    water.save_water()
    assert 70 == water.quantity_drunk_l
    
def test_request_save_exemple_several_time(client, setup):
    assert 70 == setup['water']
    for i in range(1,10):
        response = client.get("/drink")
        result = json.loads(response.data)
        assert 'water' in result, f'adding water level {i}'
        assert 70 + i*10 == result['water'], f'adding water level {i}'
 
def test_read_water_user(setup_user):
    water = Water(user_id = setup_user)
    assert 0 == water.quantity_drunk_l
        
def test_save_water_user(setup_user):
    water = Water(user_id =23)
    result = water.save_water()
    assert 0 == water.quantity_drunk_l


    
