import unittest, json
from data import home, get, post, put, delete
from utils import set_index, seed_data
from elasticsearch import Elasticsearch

host = input("Enter Elasticsearch host:")
port = input("Enter Elasticsearch port:")
es = Elasticsearch([f"{host}:{port}"])

if es.indices.exists(index="contact"):
    es.indices.delete(index="contact")
set_index()
seed_data()

class TestHome(unittest.TestCase):

    def test_page_size(self):
        results = json.loads(home({"pageSize": 15}))
        self.assertEqual(len(results), 15)

    def test_page(self):
        page1 = json.loads(home({"page":1}))
        page2 = json.loads(home({"page":2}))
        self.assertNotEqual(page1[0], page2[0])

    def test_query(self):
        contact_to_search = json.loads(home({}))[0]
        search_term = contact_to_search["name"].split(" ")[0]
        results = json.loads(home({"query": f"name:{search_term}"}))
        self.assertIn(contact_to_search, results)


class TestGet(unittest.TestCase):

    def test_invalid_name(self):
        self.assertEqual(get("Invalid Name Here"), "Contact does not exist")

    def test_valid_name(self):
        contact = json.loads(home({}))[1]
        self.assertEqual(contact, json.loads(get(contact["name"])))


class TestPost(unittest.TestCase):

    def test_name_in_use(self):
        name = json.loads(home({}))[2]["name"]
        body = {
            "name" : name,
            "cellphone" : 1111111111,
            "address" : "Some random address",
            "home_phone" : 1111111111,
            "email" : None,
            "company" : None
        }
        self.assertEqual(post(body), "Name already in use")

    def test_invalid_cell(self):
        body = {
            "name" : "Random Name Here",
            "cellphone" : 1039403952030234910293,
            "address" : "Some random address",
            "home_phone" : None,
            "email" : None,
            "company" : None
        }
        self.assertEqual(post(body), "Invalid phone number")

    def test_invalid_home_phone(self):
        body = {
            "name" : "Random Name Here",
            "cellphone" : 1111111111,
            "address" : "Some random address",
            "home_phone" : 12039123012930192301923,
            "email" : None,
            "company" : None
        }
        self.assertEqual(post(body), "Invalid phone number")

    def test_valid_body(self):
        body = {
            "name" : "Random Name Here",
            "cellphone" : 1111111111,
            "address" : "Some random address",
            "home_phone" : 1111111111,
            "email" : "randomguy@example.com",
            "company" : "Google"
        }
        self.assertEqual(post(body), "Contact created")


class TestPut(unittest.TestCase):

    def test_invalid_name(self):
        body = {"cellphone": 1230492301}
        name = "Invalid Name Here"
        self.assertEqual(put(name, body), "Contact does not exist")

    def test_partial_body(self):
        name = json.loads(home({}))[3]["name"]
        body = {"company": "Momentum Learning"}
        self.assertEqual(put(name, body), "Contact updated")

    def test_complete_body(self):
        name = json.loads(home({}))[4]["name"]
        body = {
            "name" : name,
            "cellphone" : 1111111111,
            "address" : "Some random address",
            "home_phone" : 1111111111,
            "email" : "randomguy@example.com",
            "company" : "Google"
        }
        self.assertEqual(put(name, body), "Contact updated")


class TestDelete(unittest.TestCase):

    def test_invalid_name(self):
        name = "Invalid Name Here"
        self.assertEqual(delete(name), "Contact does not exist")

    def test_valid_name(self):
        name = json.loads(home({}))[5]["name"]
        delete(name)
        self.assertEqual(get(name), "Contact does not exist")


if __name__ == "__main__":
    unittest.main()
