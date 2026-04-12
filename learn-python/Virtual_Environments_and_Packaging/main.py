import yaml

# Read from file
with open("config.yaml", "r") as f:
    data = yaml.safe_load(f)

print(data["name"])          # Alice
print(data["languages"])     # ['Python', 'JavaScript', 'Go']
print(data["address"]["city"])  # Hyderabad
