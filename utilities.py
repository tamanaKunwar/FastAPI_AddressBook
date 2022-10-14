import sqlite3
from pydantic import BaseModel
from cmath import acos, sin, cos
from math import radians


class Address(BaseModel):
    latitude : float
    longitude: float


def execute_query(query):
    conn = sqlite3.connect('addressbook.db', check_same_thread=False)
    try:
        response = conn.execute(query)
        conn.commit()
    except Exception as e:
        print("Some Exception occured",e)
    finally:
        # conn.close()
        return response


'''
    Calculating the dictance using haversine formula
    Checking if the each_row lat, long distance is <= target distance then returning True 
'''
def check_distance(latitude, longitude, lat, lng, distance):
    latitude = float(latitude)
    longitude = float(longitude)

    result = 3959 * acos(
        cos(radians(latitude))
        * cos(radians(lat))
        * cos(radians(lng) - radians(longitude))
        + sin(radians(latitude))
        * sin(radians(lat))
    )
    if result <= distance:
        return True
    return False
