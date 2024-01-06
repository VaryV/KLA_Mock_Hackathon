import numpy as np, json
from itertools import combinations

def held_karp(distances):
    n = len(distances)
    C = {}
    for k in range(1, n):
        C[(1 << k, k)] = (distances[0][k], 0)
    for subset_size in range(2, n):
        for subset in combinations(range(1, n), subset_size):
            bits = 0
            for bit in subset:
                bits |= 1 << bit
            for k in subset:
                prev = bits & ~(1 << k)
                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prev, m)][0] + distances[m][k], m))
                C[(bits, k)] = min(res)
    bits = (2**n - 1) - 1
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + distances[k][0], k))
    opt, parent = min(res)
    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits
    path.append(0)
    return opt, list(reversed(path))

# OPENING AND STORING CONTENTS OF GIVEN JSON INPUT FILE
data = json.load(open("D:\\KLA_Mock_Hackathon\\Level0\\level0.json"))
vehicles = data["vehicles"]
neighbourhoods = data["neighbourhoods"]
restaurants = data["restaurants"]

ref = restaurants["r0"]["neighbourhood_distance"]
d2 = [[0] + ref]
for i in neighbourhoods:
    d2.append([ref[int(i.strip("n"))]] + neighbourhoods[i]["distances"])

cost, path = held_karp(d2)
new_path = []
for i in range(len(path)):
    if i == 0:
        new_path.append("r0")
    else:
        new_path.append(f"n{path[i]-1}")
new_path.append("r0")
dictionary = {"v0": {"path": new_path}}
print(dictionary)
with open("level0_output.json", "w") as newfile:
    json.dump(dictionary, newfile)