import json
# from ortools.constraint_solver import routing_enums_pb2
# from ortools.constraint_solver import pywrapcp

# def create_data_model():
#     """Stores the data for the problem."""
#     data1 = json.load(open("D:\\KLA_Mock_Hackathon\\Level2\\Level2a\\level2a.json"))
#     vehicles = data1["vehicles"]
#     neighbourhoods = data1["neighbourhoods"]
#     restaurants = data1["restaurants"]

#     ref = restaurants["r0"]["neighbourhood_distance"]
#     d2 = [[0] + ref]
#     for i in neighbourhoods:
#         d2.append([ref[int(i.strip("n"))]] + neighbourhoods[i]["distances"])

#     data = {}
#     data['distance_matrix'] = d2
#     data['depot'] = 0
#     data['demands'] = [0] + [neighbourhoods[i]["order_quantity"] for i in neighbourhoods]
#     data["vehicle_capacities"] = [vehicles[i]["capacity"] for i in vehicles]
#     data["num_vehicles"] = len(data["vehicle_capacities"])

#     return data

# def print_solution(manager, routing, solution):
#     """Prints solution on console."""
#     print('Objective: {}'.format(solution.ObjectiveValue()))
#     index = routing.Start(0)
#     plan_output = 'Routes:\n'
#     route_distance = 0
#     while not routing.IsEnd(index):
#         plan_output += ' {} ->'.format(manager.IndexToNode(index))
#         previous_index = index
#         index = solution.Value(routing.NextVar(index))
#         route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
#     plan_output += ' {}\n'.format(manager.IndexToNode(index))
#     print(plan_output)
#     print('Route Distance: {}'.format(route_distance))

# def main():
#     """Entry point of the program."""
#     # Instantiate the data problem.
#     data = create_data_model()

#     # Create the routing index manager.
#     manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
#                                            data['num_vehicles'], data['depot'])

#     # Create Routing Model.
#     routing = pywrapcp.RoutingModel(manager)

#     # Create and register a transit callback.
#     def distance_callback(from_index, to_index):
#         """Returns the distance between the two nodes."""
#         return data['distance_matrix'][manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

#     transit_callback_index = routing.RegisterTransitCallback(distance_callback)

#     # Define cost of each arc.
#     routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

#     # Add capacity constraint.
#     def demand_callback(from_index):
#         """Returns the demand of the node."""
#         return data['demands'][manager.IndexToNode(from_index)]

#     demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
#     routing.AddDimensionWithVehicleCapacity(
#         demand_callback_index,
#         0,  # null capacity slack
#         data['vehicle_capacities'],  # vehicle maximum capacities
#         True,  # start cumul to zero
#         'Capacity'
#     )

#     # Setting first solution heuristic.
#     search_parameters = pywrapcp.DefaultRoutingSearchParameters()
#     search_parameters.time_limit.seconds = 1

#     # Solve the problem.
#     solution = routing.SolveWithParameters(search_parameters)

#     # Print solution on console.
#     if solution:
#         print_solution(manager, routing, solution)
#     else:
#         print("No solution found!")

# if __name__ == '__main__':
#     main()


from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model():
    data1 = json.load(open("D:\\KLA_Mock_Hackathon\\Level2\\Level2a\\level2a.json"))
    vehicles = data1["vehicles"]
    neighbourhoods = data1["neighbourhoods"]
    restaurants = data1["restaurants"]

    ref = restaurants["r0"]["neighbourhood_distance"]
    d2 = [[0] + ref]
    for i in neighbourhoods:
        d2.append([ref[int(i.strip("n"))]] + neighbourhoods[i]["distances"])

    data = {}
    data['distance_matrix'] = d2
    data['depot'] = 0
    data['demands'] = [0] + [neighbourhoods[i]["order_quantity"] for i in neighbourhoods]
    data["vehicle_capacities"] = [vehicles[i]["capacity"] for i in vehicles]
    data["num_vehicles"] = len(data["vehicle_capacities"])

    return data

    return data

def print_solution(manager, routing, solution):
    """Prints solution on console."""
    total_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = f'Route for Scooter {vehicle_id}:\n'
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += f' {manager.IndexToNode(index)} ->'
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        plan_output += f' {manager.IndexToNode(index)}\n'
        print(plan_output)
        print(f'Distance for Scooter {vehicle_id}: {route_distance}')
        total_distance += route_distance
    print(f'Total Distance for all Scooters: {total_distance}')

def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        return data['distance_matrix'][manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        return data['demands'][manager.IndexToNode(from_index)]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity'
    )

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.time_limit.seconds = 1

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution)
    else:
        print("No solution found!")

if __name__ == '__main__':
    main()
