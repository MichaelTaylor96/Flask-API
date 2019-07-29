from elasticsearch import Elasticsearch
import json
host = input("Enter Elasticsearch host:")
port = input("Enter Elasticsearch port:")
es = Elasticsearch([f"{host}:{port}"])

# Delete data for refresh on startup
if es.indices.exists(index="contact"):
    es.indices.delete(index="contact")

def home(args):
    # Set arguments to default values in case they are not provided
    size = 10
    page = 1
    query = "_index:contact"

    # Set all arguments provided to the provided values
    if "pageSize" in args:
        size = int(args["pageSize"])
    if "page" in args:
        page = int(args["page"])
    if "query" in args:
        query = args["query"]
    
    # Search for list of contacts, then grab only the _source data from them
    contacts = es.search(index="contact", from_=(page-1)*size, size=size, q=query)["hits"]
    result = json.dumps([doc["_source"] for doc in contacts["hits"]])
    return result  


def post(body):
    # Clean the provided name, check that it is not already in use
    ID = body["name"].lower().replace(" ", "-")
    if es.exists(index="contact", id=ID):
        return "Name already in use"

    # Set all optional values to None if they were not provided
    if "home_phone" not in body.keys():
        body["home_phone"] = None
    if "email" not in body.keys():
        body["email"] = None
    if "company" not in body.keys():
        body["company"] = None

    # Make sure the phone numbers provided are exactly 10 digits long
    if (not 1000000000 < body["cellphone"] < 9999999999 or (body["home_phone"] and not 1000000000 < body["home_phone"] < 9999999999)):
        return "Invalid phone number" 

    es.create(index="contact", id=ID, body=body)
    return "Contact created"


def get(name):
    # Clean the provided name, check that it belongs to an existing contact
    ID = name.lower().replace(" ", "-")
    if not es.exists(index="contact", id=ID):
        return "Contact does not exist"

    return json.dumps(es.search(body={"query": {"match": {"_id":ID}}})["hits"]["hits"][0]["_source"])


def put(name, data):
    # Clean the provided name, check that it belongs to an existing contact
    ID = name.lower().replace(" ", "-")
    if not es.exists(index="contact", id=ID):
        return "Contact does not exist"

    body = {"doc":data}

    ## Make sure the phone numbers provided are exactly 10 digits long, if any are provided
    if ("cellphone" in body and (not 1000000000 < body["cellphone"] < 9999999999 or (body["home_phone"] and not 1000000000 < body["home_phone"] < 9999999999))):
        return "Invalid phone number"

    es.update(index="contact", id=ID, body=body)
    return "Contact updated"

def delete(name):
    # Clean the provided name, check that it belongs to an existing contact
    ID = name.lower().replace(" ", "-")
    if not es.exists(index="contact", id=ID):
        return "Contact does not exist"

    es.delete(index="contact", id=ID)
    return "Contact deleted"
