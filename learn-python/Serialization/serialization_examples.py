# Serialization: pickle and json
import pickle
import json

data = {'a': 1, 'b': 2}
# JSON
with open('data.json', 'w') as f:
    json.dump(data, f)
with open('data.json') as f:
    print('json', json.load(f))

# pickle
with open('data.pickle', 'wb') as f:
    pickle.dump(data, f)
with open('data.pickle', 'rb') as f:
    print('pickle', pickle.load(f))
