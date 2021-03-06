import random
from flask import Flask, request, abort
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


@app.route("/api/catalog", methods=["post"])
def save_product():
    product = request.get_json()
    print(product)
    # data validations
    if not "title" in product or len(product["title"]) < 5:
        return abort(400, "Title is required and should be at least 5 characters long.")
    if not "price" in product:
        return abort(400, "Price is required")
    if not (isinstance(product["price"], float) and not isinstance(product["price"], int)):
        return abort(400, "Price should be a valid number.")
    if product["price"] <= 0:
        return abort(400, "The price must be greater than 0.")
    product["_id"] = random.randint(1000, 100000)
    catalog.append(product)
    return json.dumps(product)


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


@app.route("/api/catalog/<category>")
def get_by_category(category):
    category_list = []
    category = category.lower()
    for product in catalog:
        if product["category"].lower() == category:
            category_list.append(product)
    return json.dumps(category_list)


@app.route("/api/categories")
def get_categories():
    categories = []
    for product in catalog:
        if product["category"] not in categories:
            categories.append(product["category"])
    return json.dumps(categories)


# start the server


app.run(debug=True)