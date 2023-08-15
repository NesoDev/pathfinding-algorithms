from pyray import *
from raylib import *
SOFTBLACK = (68, 68, 68, 120)
    
class Mesh:
    def __init__(self, width, height, reason, horizontal_quantity, vertical_quantity, radius, color):
        self.quotient = width / height
        self.reason = reason
        self.quantity = [horizontal_quantity - 1, vertical_quantity - 1]
        self.width = width * reason
        self.height = self.width / self.quotient
        print(f"{self.width}, {self.height}")
        self.x0 = 0.5 * (width - self.width)
        self.y0 = 0.5 * (height - self.height)
        #self.points_position = list()
        self.radius = radius
        self.color = color
        self.points = list()
        self.sides = list()

    def determine_position_points(self):
        edge_horizontal = self.width / self.quantity[0]
        edge_height = self.height / self.quantity[1]

        x = [self.x0 + iterator * edge_horizontal for iterator in range(self.quantity[0] + 1)]
        y = [self.y0 + iterator * edge_height for iterator in range(self.quantity[1] + 1)]
        
        """for i in range(x):
            row = [[x[i], y[j]] for j in range(y)]
            self.points_position.append(row)"""
        
        for pos_x in x:
            for pos_y in y:
                point = Point(pos_x, pos_y, self.radius, self.color)
                self.points.append(point)
        
        """rows = [[point = Point(pos_x, pos_y, self.radius, self.color) for pos_y in y] for pos_x in x]
        for row in rows:
            self.points_position.extend(row)"""
    
    def draw_mesh(self):
        """for pos in self.points_position:
            draw_circle(int(pos[0]), int(pos[1]), int(self.radius), self.color)"""
        
        for point in self.points:
            point.draw_point()
    
    def view_state_point(self, state_points):
        indices = []
        for iterator, state in enumerate(state_points):
            if state == "True":
                indices.append(iterator)

        if len(indices) == 2:
            for point in self.points:
                point.selected = False
                point.color = SOFTBLACK
            
            print(", ".join([str(point.selected) for point in self.points]))

            side = Side(self.points[indices[0]], self.points[indices[1]], MAGENTA)
            self.sides.append(side)
        
    def detect_selected(self):
        for point in self.points:
            point.detect_selected()

    
    def draw_sides(self):
        for side in self.sides:
            side.draw_side()

class Side:
    def __init__(self, initial_point, final_point, color):
        self.points = [initial_point, final_point]
        self.color = color
    
    def draw_side(self):
        draw_line(int(self.points[0].position[0]), int(self.points[0].position[1]), int(self.points[1].position[0]), int(self.points[1].position[1]), self.color)

class Point:
    def __init__(self, x, y, radius, color):
        self.position = [x, y]
        self.radius = radius
        self.color = color
        self.selected = False
    
    def draw_point(self):
        draw_circle(int(self.position[0]), int(self.position[1]), int(self.radius), self.color)
    
    def detect_selected(self):
        if is_mouse_button_down(MOUSE_BUTTON_LEFT) and (get_mouse_x() - self.position[0]) ** 2 + (get_mouse_y() - self.position[1]) ** 2 <=  self.radius ** 2:
            self.selected = True
            self.color = RED

def main():
    window_width = 700
    window_height = 500

    mesh = Mesh(window_width, window_height, 0.8, 21, 15, 5, SOFTBLACK)
    mesh.determine_position_points()

    init_window(window_width, window_height, "Labyrinth")

    while not window_should_close():
        begin_drawing()
        mesh.draw_mesh()
        mesh.detect_selected()
        state_points = [str(point.selected) for point in mesh.points]
        mesh.draw_sides()
        mesh.view_state_point(state_points)  # Llamar a view_state_point después de draw_sides
        clear_background(BLACK)
        end_drawing()
    close_window()

main()
            


            





