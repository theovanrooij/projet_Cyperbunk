import json
 
# Opening JSON file
with open('links.json') as json_file:
    data = json.load(json_file)
    links = [link["linkbook"] for link in data]

with open('newlinks.json', 'w') as f:
    json.dump(links, f)