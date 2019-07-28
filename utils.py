from elasticsearch import Elasticsearch
import names
import random
es = Elasticsearch()

def set_index():
    body = {
        "mappings" : {
            "properties" : {
                "name" : { "type" : "keyword" },
                "cellphone" : { "type" : "long" },
                "home_phone" : { "type" : "long" },
                "email" : { "type" : "text" },
                "address" : { "type" : "text" },
                "company" : { "type" : "text" }
            } 
        }
    }

    es.indices.create(index="contact", body=body)

def seed_data():
    companies = ["Microsoft", "Google", "Amazon", "Apple", "IBM", "Qualcomm"]
    for i in range(200):
        name = names.get_full_name().lower().replace(" ", "-")
        cellphone = random.randint(1000000000, 9999999999)
        road_num = random.randint(100, 999)
        zip_code = random.randint(10000, 99999)
        address = f"{road_num} Placeholder Rd, SomeCity, SomeState, {zip_code}, SomeCountry"

        body = {
            "name" : name,
            "cellphone" : cellphone,
            "address" : address,
            "home_phone" : None,
            "email" : None,
            "company" : None
        }

        if random.randint(0,1) == 1:
            body["home_phone"] = random.randint(1000000000, 9999999999)
        if random.randint(0,1) == 1:
            body["email"] = f"{name}@example.com"
        if random.randint(0,1) == 1:
            body["company"] = companies[random.randint(0, len(companies)-1)]

        es.index(index="contact", body=body)

es.indices.delete("contact")
set_index()
seed_data()