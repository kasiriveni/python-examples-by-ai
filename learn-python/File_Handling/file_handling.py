import csv
import json

# Working with CSV
with open('example.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Age', 'City'])
    writer.writerow(['Alice', 30, 'New York'])

with open('example.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

# Working with JSON
data = {'name': 'Alice', 'age': 30, 'city': 'New York'}

with open('example.json', 'w') as file:
    json.dump(data, file)

with open('example.json', 'r') as file:
    loaded_data = json.load(file)
    print(loaded_data)
