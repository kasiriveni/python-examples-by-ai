# File handling: text, binary, CSV, JSON examples
import json

# Text
with open('fh_example.txt','w', encoding='utf-8') as f:
    f.write('Hello file')

with open('fh_example.txt','r', encoding='utf-8') as f:
    print(f.read())

# JSON
data = {'a':1}
with open('data.json','w') as f:
    json.dump(data, f)

with open('data.json') as f:
    print(json.load(f))
