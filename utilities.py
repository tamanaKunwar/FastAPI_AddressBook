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


def calculations(latitude, longitude, lat, lng):
    print("^^^^^^^^^^^^^^^")
    print(latitude)
    d = radians(latitude)

    print(d)
    print(type(radians(latitude)))

    result = 3959 * acos(
        cos(radians({float(latitude)}))
        * cos(radians(lat))
        * cos(radians(lng) - radians({longitude}))
        + sin(radians({latitude}))
        * sin(radians(lat))
    )
    print("5555555555555555555555555555555")
    print(result)
    return result
