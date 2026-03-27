import random
import json

file_path = "form.json"
def load():
    with open(file_path, "r") as f:
        data = json.load(f)
    return data

def save(data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

data = load()
size = len(data["data"])

data["data"][1:] = random.sample(data["data"][1:], len(data["data"]) - 1)

assert len(data["data"])==size, "Size should be consistent before and after update"

for i in range(1, size):
    data["data"][i]["createItem"]["location"]["index"] = i - 1

save(data)