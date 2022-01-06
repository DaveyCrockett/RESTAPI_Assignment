

from flask import Flask
from mock_data import catalog
import json

app = Flask(__name__)
me = {
    "name": "David",
    "last": "Paredes",
    "age": 33,
    "occupation": "Package Handler",
    "hobbies": [],
    "address": {
        "street": "Walker",
        "number": 2345,
        "city": "Ranger"
        }
    }


@app.route("/")
def home():
    return "Hello from Python!"


@app.route("/test")
def any_name():
    return "I'm a test function"


@app.route("/about")
def about_me():
    return me["name"] + " " + me["last"]


# ********************************************
# **********API ENDPOINTS*********************
# ********************************************

@app.route("/api/catalog")
def get_catalog():
    # TODO read the catalog from a database
    return json.dumps(catalog)


@app.route("/api/cheapest")
def get_cheapest():
    # find the cheapest product on the catalog list
    cheapest = catalog[0]
    for product in catalog:
        if product["price"] < cheapest["price"]:
            cheapest = product
    # return json
    return json.dumps(cheapest)


@app.route("/api/product/<id>")
def get_product(id):
    #  find the product whose _id is equal to id
    for product in catalog:
        if product["_id"] == id:
            return json.dumps(product)

    return "NOT FOUND"

# start the server


app.run(debug=True)