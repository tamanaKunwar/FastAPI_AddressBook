from fastapi import FastAPI
from utilities import Address, execute_query, check_distance
import configparser
import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')

app = FastAPI()


@app.post('/create-address')
def create_address(address: Address):
    """
    Creates a new address and store the address details in database.
    :param address: Address instance which contains latitude, longitude.
    :return: Same Address data which is saved in database.
    """
    logger.info("Create Address API called")
    data = address.dict()
    query = config["DATABASE"]["CREATE_ADDRESS"]
    query = query.format(latitude=data['latitude'], longitude=data['longitude'])
    execute_query(query)
    result = data
    return result


@app.put('/update-address/{id}')
def update_address(id:int, address: Address):
    """
    Updates the address details in database.
    :param id: address id which needs to be updated.
    :param address: Address data containing latitude, longitude (sent in body of request)
    :return: Success message to client after successful updation.
    """
    logger.info("Update Address API called")
    data = address.dict()
    query = config["DATABASE"]["UPDATE_ADDRESS"]
    query = query.format(latitude=data['latitude'], longitude=data['longitude'], id=id)
    execute_query(query)
    return {"message": "Operation performed successfully"}


@app.get('/get-address/{id}')
def get_address(id):
    """
    Returns the address corresponding to the provided address id.
    :param id: address id which needs to be fetched.
    :return: Address details if found; else "Not found" message to the client.
    """
    logger.info("Get Address API called")
    query = config["DATABASE"]["GET_ADDRESS"]
    query = query.format(id=id)
    response = execute_query(query)
    result = {}
    for each_value in response:
        result['id'] = each_value[0]
        result['latitude'] = each_value[1]
        result['longitude'] = each_value[2]
    if len(result) != 0:
        return result
    else:
        logger.warning("Address not found for id: "+str(id))
        return {"message": "Address id is not present"}


@app.get('/get-addresses-within-distance')
def get_addresses_within_distance(latitude, longitude, distance):
    """
    Get all the addresses which falls within the provided distance from provided latitude and longitude using Haversine formula.
    :param latitude: User provided latitude
    :param longitude: User provided longitude
    :param distance: distance within which we need to fetch all falling addresses.
    :return: List of addresses if found.
    """
    query = config["DATABASE"]["GET_ALL_ADDRESSES"]
    all_addresses = execute_query(query)
    returned_list = []
    for each_record in all_addresses:
        logger.info("Calling check_distance")
        is_within_distance  = check_distance(latitude=latitude, longitude=longitude, distance=distance,
                                             lat=each_record[1], lng=each_record[2])
        logger.info("Distance calculated")
        if is_within_distance:
            returned_list.append({
                'latitude': each_record[1],
                'longitude': each_record[2]})
    return returned_list


@app.delete('/delete-addresses')
def delete_address(id):
    """
    Deletes the address from the database.
    :param id: Address id needs to be deleted.
    :return:
    """
    logger.info("Delete Address API called")
    query = config["DATABASE"]["DELETE_ADDRESS"]
    query = query.format(id=id)
    execute_query(query)
    return {}
