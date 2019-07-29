from elasticsearch import Elasticsearch
import names
import random
es = Elasticsearch()

# Create contact index with data mapping
def set_index():
    body = {
        "mappings" : {
            "properties" : {
                "name" : { "type" : "text" },
                "cellphone" : { "type" : "long" },
                "home_phone" : { "type" : "long" },
                "email" : { "type" : "text" },
                "address" : { "type" : "text" },
                "company" : { "type" : "text" }
            } 
        }
    }

    es.indices.create(index="contact", body=body)

# Populate index with 200 random contacts
def seed_data():
    companies = ["Microsoft", "Google", "Amazon", "Apple", "IBM", "Qualcomm"]
    for i in range(200):
        # Set up fields randomly
        name = names.get_full_name()
        cellphone = random.randint(1000000000, 9999999999)
        road_num = random.randint(100, 999)
        zip_code = random.randint(10000, 99999)
        address = f"{road_num} Placeholder Rd, SomeCity, SomeState, {zip_code}, SomeCountry"

        # Apply fields to body
        body = {
            "name" : name,
            "cellphone" : cellphone,
            "address" : address,
            "home_phone" : None,
            "email" : None,
            "company" : None
        }

        # Decide whether to populate optional fields
        if random.randint(0,1) == 1:
            body["home_phone"] = random.randint(1000000000, 9999999999)
        if random.randint(0,1) == 1:
            body["email"] = f"{name.lower().replace(' ', '-')}@example.com"
        if random.randint(0,1) == 1:
            body["company"] = companies[random.randint(0, len(companies)-1)]

        es.index(index="contact", body=body, id=name.lower().replace(" ", "-"))
