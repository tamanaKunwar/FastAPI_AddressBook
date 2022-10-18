import sqlite3
from pydantic import BaseModel
from cmath import acos, sin, cos
from math import radians
import logging

logger = logging.getLogger()


class Address(BaseModel):
    """
    Address inherited from BaseModel which defines what to expect in request body.
    """
    latitude: float
    longitude: float


def execute_query(query):
    """
    Executes the database query
    :param query: query string
    :return: The sqlite cursor object.
    """
    response = None
    conn = sqlite3.connect('addressbook.db', check_same_thread=False)
    try:
        response = conn.execute(query)
        conn.commit()
    except Exception as e:
        logger.warning("Some Exception occurred while executing query " + str(e))
    finally:
        # conn.close()
        return response


def check_distance(latitude, longitude, lat, lng, distance):
    """
    checks using Haversine formula; if the distance between user provided lat, long and each_row's lat, long lies between user provided distance.
    :param latitude: User provided latitude
    :param longitude: User provided longitude
    :param lat: each_row's latitude
    :param lng: each_row's longitude
    :param distance: User provided distance
    :return: True if the calculated distance is <= provided distance; else False.
    """
    latitude = float(latitude)
    longitude = float(longitude)
    result = 3959 * acos(
        cos(radians(latitude))
        * cos(radians(lat))
        * cos(radians(lng) - radians(longitude))
        + sin(radians(latitude))
        * sin(radians(lat))
    )
    if result.real <= float(distance):
        return True
    return False
