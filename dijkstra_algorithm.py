import heapq
import random
import json

from pyray import *

inf = float('inf')
nodes = list()
colors = [LIGHTGRAY, GRAY, DARKGRAY, YELLOW, GOLD, ORANGE, PINK, RED, MAROON, GREEN, LIME, DARKGREEN, SKYBLUE, BLUE, DARKBLUE, PURPLE, VIOLET, DARKPURPLE, BEIGE, BROWN, DARKBROWN,  WHITE,MAGENTA, RAYWHITE]
selected_nodes = [None for node in nodes]
class Node:
    def __init__(self, iterator, x, y, radius, color):
        self.id = iterator
        self.position = [x, y]
        self.radius = radius
        self.color = color
        self.nodes_adjacent = list()
        self.state = True
        self.labels = list()  # Lista de etiquetas [distance, node_ancestor, cycle]

    def detectCollision(self, nodes):
        for node in nodes:
            if node != self and ((node.position[0] - self.position[0]) ** 2 + (node.position[1] - self.position[1]) ** 2) ** 0.5 <= 2 * self.radius:
                return True
        return False
    
    def selected(self):
        if (get_mouse_x() - self.position[0]) ** 2 + (get_mouse_y() - self.position[1]) ** 2 <= self.radius ** 2:
            pass

def load_json_data(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    return data

def createNodesFromJSON(radius, color):
    json_data = load_json_data('nodes_position.json')
    for item in json_data:
        node = Node(item["id"], item["pos_x"], item["pos_y"], radius, color)
        nodes.append(node)

def createNodes(width, height, quantity, radius, color):
    for iterator in range(quantity):
        while True:
            try:
                x = random.randint(width / 3 + 2 * radius, (4 * width / 3) - 2 * radius)
                y = random.randint(height / 3 + radius, (4 * height / 3) - 2 * radius)
                node = Node(iterator + 1, x, y, radius, color)
                if not node.detectCollision(nodes):
                    break
            except:
                pass
        nodes.append(node)

def view_nodes():
    print("\n")
    for node in nodes:
        print(f"ID: {node.id} \n- position: {node.position[0]}, {node.position[1]} \n- nodes adjacent: ")
        adjacent_ids = [str(node_adjacent.id) for node_adjacent in node.nodes_adjacent]
        print(", ".join(adjacent_ids) + "\n")

        labels = [f"[{label[0]}, {label[1].id if label[1] else None}, {label[2]}]" for label in node.labels]
        print(", ".join(labels) + "\n")

def draw_nodes():
    for node in nodes:
        draw_circle(int(node.position[0]), int(node.position[1]), node.radius, node.color)
        font_size = node.radius
        
        text = f"{node.id}"
        text_width = measure_text(text, int(font_size))
        
        pos_x_text = node.position[0] - text_width * 0.5
        pos_y_text = node.position[1] - (1/3) * (font_size)
        #pos_y_text = node.position[1] + 1.2 * node.radius
        
        draw_text(text, int(pos_x_text), int(pos_y_text), int(font_size), BLACK)

def def_links():
    for node in nodes:
        print(f"\nNode {node.id}:")
        quantity_links = int(input("- Cantidad de nodos adyacentes => "))
        ids = []

        for iterator in range(quantity_links):
            id_valid = False
            while not id_valid:
                id = int(input(f"- id de nodo adyacente {iterator + 1} => "))
                if id >= 1 and id <= len(nodes) and id != node.id:
                    id_valid = True
                else:
                    print(
                        "ID de nodo no válido. Debe estar entre 1 y la cantidad total de nodos, y no debe ser igual al ID del nodo actual."
                    )
            ids.append(id)

        for id in ids:
            node_adjacent = nodes[id - 1]
            node.nodes_adjacent.append(node_adjacent)

def def_link_JSON():
    json_data = load_json_data('nodes_position.json')
    for item in json_data:
        node_id = item["id"]
        adjacent_ids = item.get("ids_adjacents", [])
        node = next((n for n in nodes if n.id == node_id), None)
        
        if node:
            node.nodes_adjacent = [n for n in nodes if n.id in adjacent_ids]

def draw_links():
    font_size = 25 
    color_index = 0
    for node in nodes:
        for node_adjacent in node.nodes_adjacent:
            color = colors[color_index % len(colors)]
            draw_line(node.position[0], node.position[1], node_adjacent.position[0], node_adjacent.position[1], color)
            
            mid_x = (node.position[0] + node_adjacent.position[0]) / 2
            mid_y = (node.position[1] + node_adjacent.position[1]) / 2
            
            distance = calculate_distance(node, node_adjacent)
            distance_text = f"{distance:.2f}"
            
            text_width = measure_text(distance_text, font_size)
            text_x = mid_x - text_width / 2
            text_y = mid_y - font_size / 2
            draw_text(distance_text, int(text_x), int(text_y), font_size, WHITE)
            
            color_index += 1


def dijkstra(id_node_initial):
    pq = [(0, id_node_initial)]
    heapq.heapify(pq)

    while pq:
        distance, current_id = heapq.heappop(pq)
        current_node = nodes[current_id - 1]

        if not current_node.labels:
            current_node.labels.append([distance, None, 1])

        if distance > current_node.labels[0][0]:
            continue

        for node_adjacent in current_node.nodes_adjacent:
            new_distance = distance + calculate_distance(current_node, node_adjacent)

            if not node_adjacent.labels:
                node_adjacent.labels.append([inf, None, None])

            if new_distance <= node_adjacent.labels[0][0]:
                if new_distance < node_adjacent.labels[0][0]:
                    node_adjacent.labels = []
                node_adjacent.labels.append([new_distance, current_node, 1])
                heapq.heappush(pq, (new_distance, node_adjacent.id))


def calculate_distance(node1, node2):
    return ((node1.position[0] - node2.position[0]) ** 2 + (node1.position[1] - node2.position[1]) ** 2) ** 0.5

def lesser_route(id_node_final, current_path=None, all_paths=None):
    if current_path is None:
        current_path = []
    if all_paths is None:
        all_paths = []

    node = nodes[id_node_final - 1]
    current_path.append(node)

    if node.labels[0][1] is None:
        all_paths.append(current_path.copy())
    else:
        for previous_node_label in node.labels:
            previous_node = previous_node_label[1]
            if previous_node:
                lesser_route(previous_node.id, current_path, all_paths)

    current_path.pop()

    return all_paths

def view_routes(id_node_final,width, height):
    font_size = 40
    routes = lesser_route(id_node_final)
    for route in routes:
        route.reverse()

    min_distance = float('inf')  # Inicializa la distancia mínima como infinito
    for route in routes:
        distance = sum(calculate_distance(route[i], route[i+1]) for i in range(len(route)-1))
        if distance < min_distance:
            min_distance = distance

    #print("Rutas con distancia mínima:")
    for iterator, route in enumerate(routes):
        distance = sum(calculate_distance(route[i], route[i+1]) for i in range(len(route)-1))
        prev_routes = [routes[j] for j in range(0, iterator - 1)] if iterator > 0 else []
        if distance == min_distance and not (route in prev_routes):
            #print(f"\nRuta {iterator + 1}:")
            ids_nodes = [str(node.id) for node in route]
            text_route = "Ruta mínima: "+" -> ".join(ids_nodes)
            draw_text(text_route, int(0.5 * (width - font_size * 0.5 * len(text_route))), int(height - (iterator + 1) * font_size), font_size, ORANGE)
            #print(text_route)
    #print(routes)


def main():
    width_window = 1000
    height_window = 800
    node_radius = 25

    #print("Ingrese datos:")
    #quantity = int(input("Cantidad de nodos => "))

    #createNodes(width_window * 0.6, height_window * 0.6, quantity, node_radius, WHITE)

    createNodesFromJSON(node_radius, WHITE)

    #def_links()
    def_link_JSON()

    id_node_initial = int(input("ID del nodo inicial => "))
    id_node_final = int(input("ID del nodo final => "))

    dijkstra(id_node_initial)

    view_nodes()
    
    init_window(width_window, height_window, "Algorithm Dijkstra") 

    while not window_should_close():
        begin_drawing()
        view_routes(id_node_final, width_window, height_window)
        draw_links()
        draw_nodes()
        clear_background(BLACK)
        end_drawing()
    
    close_window()

main()