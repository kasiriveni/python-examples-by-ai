# Elasticsearch: Search and Analytics Engine

from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(["http://localhost:9200"])

# Index a document
es.index(index="users", id=1, document={"name": "Alice", "age": 30})

# Search documents
response = es.search(index="users", query={"match": {"name": "Alice"}})
for hit in response["hits"]["hits"]:
    print(hit["_source"])
