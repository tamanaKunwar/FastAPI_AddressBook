# FastAPI_AddressBook

### This Repo provides a set of APIs to CREATE, GET, UPDATE, DELETE a set of Addresses.
### Along with this, there is an API which is used to get the addresses within a given range of lat longs and distance.

## How to run:
1. pip install -r requirements.txt
2. Run the below command: hypercorn address:app --reload
3. In the browser, open http://127.0.0.1:8000/docs
4. All the APIs are available and can be tried using Try it Out

## To fetch the records within provided distance from provided latitude, longitude.
    Please use below sample request to validate.
http://127.0.0.1:8000/get-addresses-within-distance?latitude=10.002&longitude=10.003&distance=2044

This will give the address within 2044 KM distance from provided latitude, longitude.
