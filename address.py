from fastapi import FastAPI
from utilities import Address, execute_query, check_distance
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
    data = address.dict()
    query = config["DATABASE"]["UPDATE_ADDRESS"]
    query = query.format(latitude=data['latitude'], longitude=data['longitude'], id=id)
    execute_query(query)
    return {"message" : "Row updated sucessfully"}


@app.get('/get-address/{id}')
def get_address(id):
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
    query = config["DATABASE"]["GET_ALL_ADDRESSES"]
    all_addresses = execute_query(query)
    returned_list = []
    for each_record in all_addresses:
        is_within_distance  = check_distance(latitude=latitude, longitude=longitude, distance=distance,
                                             lat=each_record[1], lng=each_record[2])
        if is_within_distance:
            returned_list.append({
                'latitude': each_record[1],
                'longitude': each_record[2]})
    return returned_list


@app.delete('/delete-addresses')
def delete_address(id):
    id = id
    query = config["DATABASE"]["DELETE_ADDRESS"]
    query = query.format(id=id)
    execute_query(query)
    return {}




