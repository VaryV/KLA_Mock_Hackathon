"""Capacited Vehicles Routing Problem (CVRP)."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import json


def create_data_model(n):
    data1 = json.load(open("D:\\KLA_Mock_Hackathon\\Level1\\Level1b\\level1b.json"))
    vehicles = data1["vehicles"]
    neighbourhoods = data1["neighbourhoods"]
    restaurants = data1["restaurants"]

    ref = restaurants["r0"]["neighbourhood_distance"]
    d2 = [[0] + ref]
    for i in neighbourhoods:
        d2.append([ref[int(i.strip("n"))]] + neighbourhoods[i]["distances"])

    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = d2
    data["demands"] = [0] + [neighbourhoods[i]["order_quantity"] for i in neighbourhoods]
    data["vehicle_capacities"] = [vehicles["v0"]["capacity"]]*n
    data["num_vehicles"] = n
    data["depot"] = 0
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    total_distance = 0
    total_load = 0
    paths = []
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        route_load = 0
        path = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["demands"][node_index]
            path.append(node_index)
            plan_output += f" {node_index} Load({route_load}) -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        path.append(0)
        paths.append(path)
        plan_output += f" {manager.IndexToNode(index)} Load({route_load})\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        plan_output += f"Load of the route: {route_load}\n"
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print(f"Total distance of all routes: {total_distance}m")
    print(f"Total load of all routes: {total_load}")
    return paths


def main():
    for i in range(1, 10):
        """Solve the CVRP problem."""
        # Instantiate the data problem.
        data = create_data_model(i)

        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(
            len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
        )

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

        # Create and register a transit callback.
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data["distance_matrix"][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Add Capacity constraint.
        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            return data["demands"][from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            data["vehicle_capacities"],  # vehicle maximum capacities
            True,  # start cumul to zero
            "Capacity",
        )

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_parameters.time_limit.FromSeconds(1)

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if solution:
            paths = print_solution(data, manager, routing, solution)
            new_paths = []
            for path in paths:
                np = []
                for j in path:
                    if j == 0:
                        np.append("r0")
                    else:
                        np.append(f"n{j-1}")
                new_paths.append(np)
            print(f"{i} trips")
            c = 1
            dictionary = {"v0": {}}
            for i in new_paths:
                dictionary["v0"][f"path{c}"] = i
                c += 1
            print(dictionary)
            with open("D:\\KLA_Mock_Hackathon\\Level1\\Level1b\\level1b_output.json", "w") as newfile:
                json.dump(dictionary, newfile)
            break


if __name__ == "__main__":
    main()