import json

data = {"name": "Srinivas"}
json_data = json.dumps(data)

print(json_data)


from collections import Counter

data = ["a", "b", "a"]
print(Counter(data))
