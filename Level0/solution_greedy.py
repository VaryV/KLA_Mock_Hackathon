import json

# IMPLEMENTATION OF KRUSKAL'S ALGORITHM
def greedy_algorithm(neighbourhoods, restaurants):
    unvisited = [f"n{i}" for i in range(len(neighbourhoods))]
    dist = min(restaurants["r0"]["neighbourhood_distance"])
    path = ["r0"]
    path.append(unvisited.pop(restaurants["r0"]["neighbourhood_distance"].index(dist)))
    while unvisited:
        mini = 10000000
        n = None
        for i in range(len(neighbourhoods[path[-1]]["distances"])):
            if f"n{i}" not in path and neighbourhoods[path[-1]]["distances"][i] < mini:
                mini = neighbourhoods[path[-1]]["distances"][i]
                n = f"n{i}"
        dist += mini
        path.append(n)
        unvisited.remove(n)
    path.append("r0")
    dist += restaurants[f"r0"]["neighbourhood_distance"][int(path[-2].strip("n"))]
    print(dist)
    return path, dist

# OPENING AND STORING CONTENTS OF GIVEN JSON INPUT FILE
data = json.load(open("D:\\KLA_Mock_Hackathon\\Level0\\level0.json"))
vehicles = data["vehicles"]
neighbourhoods = data["neighbourhoods"]
restaurants = data["restaurants"]

# CALLING FUNCTION AND STORING RESULT IN OUTPUT FILE
path, distance = greedy_algorithm(neighbourhoods, restaurants)
print(path, distance)
out = {"v0": {"path": path}}
with open("D:\\KLA_Mock_Hackathon\\Level0\\level0_output.json", 'w') as newfile:
    json.dump(out, newfile)