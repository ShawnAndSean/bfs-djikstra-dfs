from constants import *


class VisualizePath():
    def __init__(self, surface, start_node_x, start_node_y, path, path_coords):
        self.surface = surface
        self.start_node_x = start_node_x
        self.start_node_y = start_node_y
        self.path = path
        self.path_coords = path_coords

    # For BFS and DFS mainly
    def get_path_coords(self):
        i = self.start_node_x
        j = self.start_node_y
        for move in self.path:
            if move == 'L':
                i -= 1
            elif move == 'R':
                i += 1
            elif move == 'U':
                j -= 1
            elif move == 'D':
                j += 1
            self.path_coords.append((i, j))

    def draw_path(self):
        self.path_coords.pop()
        car = pygame.image.load(f'road.png')
        liko = pygame.image.load(f'liko-road.png')
        intersection = [x[0] for x in self.path_coords]
        for index, (x_pos, y_pos) in enumerate(self.path_coords):
            if x_pos != intersection[0]:
                self.surface.blit(liko, (x_pos * 24 + 240, y_pos * 24, 24, 24))
                intersection[0] = x_pos
            else:
                self.surface.blit(car, (x_pos * 24 + 240, y_pos * 24, 24, 24))
