from fastapi import FastAPI
from utilities import Address, execute_query, calculations
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

app = FastAPI()


@app.post('/create-address')
def create_address(address:Address):
    data = address.dict()
    query = config["DATABASE"]["CREATE_ADDRESS"]
    query = query.format(latitude=data['latitude'], longitude=data['longitude'])
    execute_query(query)
    result = data       # returning the same data
    return result


@app.put('/update-address/{id}')
def update_address(id, address:Address):
    id = id
    data = address.dict()
    query = config["DATABASE"]["UPDATE_ADDRESS"]
    query = query.format(latitude=data['latitude'], longitude=data['longitude'], id=id)
    execute_query(query)
    return {"message" : "Row updated sucessfully"}


@app.get('/get-address/{id}')
def get_address(id):
    id = id
    query = config["DATABASE"]["GET_ADDRESS"]
    query = query.format(id=id)
    response = execute_query(query)
    result = {}
    for each_value in response:
        result['id'] = each_value[0]
        result['latitude'] = each_value[1]
        result['longitude'] = each_value[2]
    if len(result)!= 0:
        return result
    else:
        return {"message": "Address id is not present"}


@app.get('/get-addresses-within-distance')
def get_addresses_within_distance(latitude, longitude, distance):
    db = []
    latitude = latitude
    longitude = longitude
    distance = distance
    base_query =  'SELECT * FROM address'
    all_addresses = execute_query(base_query)
    query = config["DATABASE"]["GET_ADDRESS_WITHIN_DISTANCE"]

    for each_record in all_addresses:
        calculated_result  = calculations(latitude=latitude, longitude=longitude,lat=each_record[1],lng=each_record[1])
        query = query.format(value=calculated_result, distance=distance)
        print("********")
        print(query)
        response = execute_query(query)
        db.append(response)
    return db


@app.delete('/delete-addresses')
def delete_address(id):
    id = id
    query = config["DATABASE"]["DELETE_ADDRESS"]
    query = query.format(id=id)
    execute_query(query)
    return {}




