from math import inf, sqrt, pow
from heapq import heappop, heappush

def find_path(source_point, destination_point, mesh):
    path = []
    visited_boxes = {}
    source_box = None
    destination_box = None

    for box in mesh['boxes']:
        if within(source_point, box):
            source_box = box
        if within(destination_point, box):
            destination_box = box

    path = dijkstras_shortest_path(source_box, destination_box, mesh, mesh['adj'], source_point, destination_point)
    if path == None:
        print("Error path cannot be found!")
    return path[0], path[1]

    pass

def dijkstras_shortest_path(initial_position, destination, graph, adj, start_point, end_point):
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
    visited_boxes=[]
    path = None
    current_point = start_point
    destination_point = end_point
    if initial_position==None or destination==None:
        return None
    forward_dist = {initial_position: 0}           # Table of distances to cells
    back_dist = {destination: 0}
    forward_prev = {start_point: None}
    back_prev = {end_point: None}
    remaining_distance = get_dist(start_point, end_point)
    queue = [(remaining_distance, (initial_position, current_point, destination))]
    heappush(queue, (remaining_distance, (destination, end_point, initial_position)))
    forward_point = start_point
    back_point = end_point
    # The heap/priority queue used

    # Initial distance for starting position
    while queue:
        # Continue with next min unvisited node
        current_distance, current_box = heappop(queue)
        current_node = current_box[0]
        current_point = current_box[1]
        current_goal = current_box[2]
        if current_goal==destination:
            current_distance = forward_dist[current_node]
            forward_point = current_point
        else:
            current_distance = back_dist[current_node]
            back_point = current_point
        # Early termination check: if the destination is found, return the path
        if forward_point in back_prev:
            path = []
            back_point = back_prev[forward_point]
            path.append((back_point, forward_point))
            while back_point!=None and back_prev[back_point]!=None:
                path.append((back_prev[back_point], back_point))
                back_point = back_prev[back_point]
            #path = path[-2::-1]
            #path.append((, forward_point))
            while forward_point!=None and forward_prev[forward_point]!=None:
                path.append((forward_prev[forward_point], forward_point))
                forward_point = forward_prev[forward_point]
            path.append((start_point, forward_point))
            return (path[-2::-1], visited_boxes)

        if back_point in forward_prev:
            path = []
            forward_point = forward_prev[back_point]
            path.append((back_point, forward_point))
            while back_point!=None and back_prev[back_point]!=None:
                path.append((back_prev[back_point], back_point))
                back_point = back_prev[back_point]
            #path = path[-2::-1]
            #path.append((, forward_point))
            while forward_point!=None and forward_prev[forward_point]!=None:
                path.append((forward_prev[forward_point], forward_point))
                forward_point = forward_prev[forward_point]
            path.append((start_point, forward_point))
            return (path[-2::-1], visited_boxes)
        visited_boxes.append(current_node)
        # Calculate tentative distances to adjacent cells
        for adjacent_node in adj[current_node]:
            point, dist = touching_corners(current_node, adjacent_node, current_point)
            if point == None:
                print("Error no points")
            else:
                if current_point is not None:
                    new_distance = current_distance + dist

                if current_goal==destination:
                    if adjacent_node not in forward_dist or new_distance < forward_dist[adjacent_node]:
                        # Assign new distance and update link to previous cell
                        forward_dist[adjacent_node] = new_distance
                        if point not in forward_prev:
                            forward_prev[point] = current_point
                        remaining_distance = get_dist(point, end_point)
                        heappush(queue, (remaining_distance, (adjacent_node, point, destination)))
                else:
                    if adjacent_node not in back_dist or new_distance < back_dist[adjacent_node]:
                        # Assign new distance and update link to previous cell
                        back_dist[adjacent_node] = new_distance
                        if point not in back_prev:
                            back_prev[point] = current_point
                        remaining_distance = get_dist(point, start_point)
                        heappush(queue, (remaining_distance, (adjacent_node, point, initial_position)))

    print("Failed to find a path from", initial_position, "to", destination)
    return None


def within(point, box):
    if point[0] >= box[0] and point[0] <= box[1]:
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
        touching.append((adj[0], adj[2]))
        touching.append((adj[0], adj[3]))
    if (adj[1] == box[1]):
        touching.append((adj[1], adj[2]))
        touching.append((adj[1], adj[3]))
    if (adj[2] == box[2]):
        touching.append((adj[0], adj[2]))
        touching.append((adj[1], adj[2]))
    if (adj[3] == box[3]):
        touching.append((adj[0], adj[3]))
        touching.append((adj[1], adj[3]))
    if (adj[1] == box[0]):
        touching.append((adj[1], adj[2]))
        touching.append((adj[1], adj[3]))
    if (adj[0] == box[1]):
        touching.append((adj[0], adj[2]))
        touching.append((adj[0], adj[3]))
    if (adj[3] == box[2]):
        touching.append((adj[0], adj[3]))
        touching.append((adj[1], adj[3]))
    if (adj[2] == box[3]):
        touching.append((adj[0], adj[2]))
        touching.append((adj[1], adj[2]))
    dist = inf

    for points in touching:
        temp = get_dist(current_point, points)
        if temp < dist:
            point = points
            dist = temp
    return point, dist
pass


def get_dist(current_point, point):
    return sqrt(pow(point[0]-current_point[0], 2) + pow(point[1]-current_point[1], 2))
pass