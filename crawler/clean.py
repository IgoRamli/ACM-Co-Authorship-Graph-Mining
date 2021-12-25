import json
import os

# Get entities
with open('authors.json', 'r') as f:
    graph = json.load(f)
    authors = graph.keys()

for author,val in graph.items():
    with open(os.path.join('graph', author.split('/')[-1] + '.json'), 'r') as f:
        neighbours = json.load(f)
        for n in neighbours:
            if n['profile']['href'] in authors:
                val['adj'].append(n)

with open('graph.json', 'w+') as f:
    json.dump(graph, f)