from elasticsearch import Elasticsearch
es = Elasticsearch()

# def post():

def get(name):
    return es.search(body={"query": {"match": {"name":name}}})["hits"]
      