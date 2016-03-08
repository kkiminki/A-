from math import inf, sqrt, pow
from heapq import heappop, heappush

def find_path(source_point, destination_point, mesh):
    path = []
    visited_boxes = {}
    source_box = None
    destination_box = None

    #print("source_point = "+str(source_point))
    #print("destination_point = "+str(destination_point))

    #print("boxes = "+str(mesh['boxes']))

    for box in mesh['boxes']:
        #print("current box data = "+str(box))
        if within(source_point, box):
            source_box = box
        if within(destination_point, box):
            destination_box = box

    path = dijkstras_shortest_path(source_box, destination_box, mesh, mesh['adj'], source_point, destination_point)
    #print("retuned path = "+str(path))
    if path == None:
        print("Error path cannot be found!")
    return path[0], path[1]

    pass

def dijkstras_shortest_path(initial_position, destination, graph, adj, start_point, end_point):
    
    visited_boxes=[]
    path = None
    current_point = start_point
    destination_point = end_point
    if initial_position==None or destination==None:
        return None
    distances = {initial_position: 0}           # Table of distances to cells
    previous_cell = {current_point: None}    # Back links from cells to predecessors
    queue = [(0, (initial_position, current_point))]             # The heap/priority queue used

    # Initial distance for starting position
    distances[initial_position] = 0

    while queue:
        # Continue with next min unvisited node
        current_distance, current_box = heappop(queue)
        current_node = current_box[0]
        current_point = current_box[1]
        current_distance = distances[current_node]
        for box in queue:
            print(str(box))

        visited_boxes.append(current_node)
        # Early termination check: if the destination is found, return the path
        if current_node == destination:
            previous_cell[destination_point] = current_point
            current_point = destination_point
            path = []
            while current_point!=None:
                path.append((previous_cell[current_point], current_point))
                current_point = previous_cell[current_point]

            return (path[-2::-1], visited_boxes)
        # Calculate tentative distances to adjacent cells
        for adjacent_node in adj[current_node]:#for adjacent_node, edge_cost in adj[current_node]:
            point, dist = touching_corners(current_node, adjacent_node, current_point)
            if point == None:
                print("Error no points")
            else:
                if current_point is not None:
                    new_distance = current_distance + dist

                if adjacent_node not in distances or new_distance < distances[adjacent_node]:
                    distances[adjacent_node] = new_distance
                    if point not in previous_cell:
                        previous_cell[point] = current_point
                    remaining_distance = get_dist(point, end_point)
                    heappush(queue, (remaining_distance, (adjacent_node, point)))

    print("Failed to find a path from", initial_position, "to", destination)
    return None

'''

def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """

    distances = {initial_position: 0}           # Table of distances to cells
    previous_cell = {initial_position: None}    # Back links from cells to predecessors
    queue = [(0, initial_position)]             # The heap/priority queue used

    # Initial distance for starting position
    distances[initial_position] = 0

    while queue:
        # Continue with next min unvisited node
        current_distance, current_node = heappop(queue)

        # Early termination check: if the destination is found, return the path
        if current_node == destination:
            node = destination
            path = [node]
            while node is not None:
                path.append(previous_cell[node])
                node = previous_cell[node]
            return path[::-1]

        # Calculate tentative distances to adjacent cells
        for adjacent_node, edge_cost in touching_corners():
            new_distance = current_distance + edge_cost

            if adjacent_node not in distances or new_distance < distances[adjacent_node]:
                # Assign new distance and update link to previous cell
                distances[adjacent_node] = new_distance
                previous_cell[adjacent_node] = current_node
                heappush(queue, (new_distance, adjacent_node))

    # Failed to find a path
    print("Failed to find a path from", initial_position, "to", destination)
    return None
'''
def within(point, box):
    if point[0] >= box[0] and point[0] <= box[1]:
        #print("source in x range")
        if point[1] >= box[2] and point[1] <= box[3]:
            return True
    else:
        return False
pass


def corners(box):
    corner=[]
    corner.append((box[0],box[2]))
    corner.append((box[0], box[3]))
    corner.append((box[1],box[2]))
    corner.append((box[1], box[3]))
    return corner
pass


def touching_corners(box, adj, current_point):
    touching=[]
    point = None
    if (adj[0] == box[0]):
        #if adj[2] >= box[2]:
        touching.append((adj[0], adj[2]))
        #if adj[3] <= box[3]:
        touching.append((adj[0], adj[3]))
    if (adj[1] == box[1]):
        #if adj[2] >= box[2]:
        touching.append((adj[1], adj[2]))
        #if adj[3] <= box[3]:
        touching.append((adj[1], adj[3]))
    if (adj[2] == box[2]):
        #if adj[0] >= box[0]:
        touching.append((adj[0], adj[2]))
        #if adj[1] <= box[1]:
        touching.append((adj[1], adj[2]))
    if (adj[3] == box[3]):
        #if adj[0] >= box[0]:
        touching.append((adj[0], adj[3]))
        #if adj[1] <= box[1]:
        touching.append((adj[1], adj[3]))
    if (adj[1] == box[0]):
        #if adj[2] >= box[2]:
        touching.append((adj[1], adj[2]))
        #if adj[3] <= box[3]:
        touching.append((adj[1], adj[3]))
    if (adj[0] == box[1]):
        #if adj[2] >= box[2]:
        touching.append((adj[0], adj[2]))
        #if adj[3] <= box[3]:
        touching.append((adj[0], adj[3]))
    if (adj[3] == box[2]):
        #if adj[0] >= box[0]:
        touching.append((adj[0], adj[3]))
        #if adj[1] <= box[1]:
        touching.append((adj[1], adj[3]))
    if (adj[2] == box[3]):
        #if adj[0] >= box[0]:
        touching.append((adj[0], adj[2]))
        #if adj[1] <= box[1]:
        touching.append((adj[1], adj[2]))
    dist = inf

    for points in touching:
        #print("in for loop")
        temp = get_dist(current_point, points)
        #print("temp = "+str(temp))
        #print("point = "+str(points))
        if temp < dist:
            point = points
            dist = temp
            #print("points = "+str(points))
            #print("point = "+str(point))
        #else:
            #print("temp = "+str(temp))
            #print("dist = "+str(dist))

    #print("about to return point. point = "+str(point)+" and dist = "+str(dist))
    #print("BOX = "+str(box))
    #print("ADJ = "+str(adj))
    #print("TOUCHING = "+str(touching))
    #print("returning point = "+str(point))
    return point, dist
pass


def get_dist(current_point, point):
    return sqrt(pow(point[0]-current_point[0], 2) + pow(point[1]-current_point[1], 2))
pass
