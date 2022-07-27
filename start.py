import sys
from buttons import *
from bfs import *
from dfs import *
from dijkstra import Dijkstra
from visualize_path_class import *
from maze_class import *
from constants import *

pygame.init()


class Start:
    def __init__(self):
        # Algorithm used - Dijkstra - Instantaneous ; Breadth - Good for Width-Dominant ; Depth - Good for Height-Dominants
        self.dijkstra = None
        self.dfs = None
        self.bfs = None
        self.algo_used = None

        # Draw the Paths for the Algorithm
        self.draw_path = None

        # Backgrounds for the menu and the maze
        self.bg_menu = None
        self.bg_maze = None

        # Pygame Settings
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption('Path Finder Services: Algorithm Demonstration Tool')

        # Driving is the start of the application
        self.driving = True
        self.pygame_state = 'menu'  # The state of the pygame at first; since we are at the menu

        # Draw the backgrounds for the Main Menu
        self.import_bg()

        # Going to be used as the starting and finishing lines of the nodes.
        self.node_input = 0

        # This is just for buttons
        self.mouse_drag = 0
        # Start and End Nodes Coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        # The limit of the searching system.
        self.wall_dead_end = boundary.copy()

        # Maze Class Instances
        self.maze = Maze(self, self.wall_dead_end)

        # Define Main-Menu buttons
        self.bfs_button = Buttons(self, WHITE, 40, MAIN_BUTTON_Y_POS, main_button_width, main_button_height,
                                  'Breadth-First Search')
        self.dfs_button = Buttons(self, WHITE, 270, MAIN_BUTTON_Y_POS, main_button_width, main_button_height,
                                  'Depth-First Search')
        self.djikstra_button = Buttons(self, WHITE, 160, 400, main_button_width, main_button_height,
                                       'Djikstra')

        # Define Grid-Menu buttons

        self.start_end_node_button = Buttons(self, lightblue, 20, START_END_BUTTON_HEIGHT, GRID_BUTTON_LENGTH,
                                             GRID_BUTTON_HEIGHT, 'Insert Destination')
        self.wall_node_button = Buttons(self, lightblue, 20,
                                        START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT + BUTTON_SPACER,
                                        GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Insert Traffic')
        self.start_button = Buttons(self, lightblue, 20,
                                    START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT * 2 + BUTTON_SPACER * 2,
                                    GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Find Path')
        self.main_menu_button = Buttons(self, lightblue, 20,
                                        START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT * 3 + BUTTON_SPACER * 3,
                                        GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Main Menu')
        self.maze_generate_button = Buttons(self, lightblue, 20,
                                            START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT * 4 + BUTTON_SPACER * 4,
                                            GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Generate Road')

    # import background
    def import_bg(self):
        self.bg_menu = pygame.image.load('main_background.png')

    # while the application is running
    def during_run(self):
        while self.driving:
            if self.pygame_state == 'menu':  # while the state is menu
                self.menu()
            if self.pygame_state == 'maze':  # while the state is maze
                self.call_maze()
            if self.pygame_state == 'destination' or self.pygame_state == 'traffic':
                self.add_nodes()
            if self.pygame_state == 'start visualizing':
                self.execute_search_algorithm()
            if self.pygame_state == 'aftermath':
                self.reset_or_main_menu()

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

        self.bg_menu = pygame.image.load('main_background.png')

        self.bfs_button = Buttons(self, WHITE, 40, MAIN_BUTTON_Y_POS, main_button_width, main_button_height,
                                  'Breadth-First Search')
        self.dfs_button = Buttons(self, WHITE, 270, MAIN_BUTTON_Y_POS, main_button_width, main_button_height,
                                  'Depth-First Search')
        self.dfs_button = Buttons(self, WHITE, 270, MAIN_BUTTON_Y_POS, main_button_width, main_button_height,
                                  'Djikstra')

    def sketch_main_menu(self):
        self.screen.blit(self.bg_menu, (0, 0))

        # Draw Buttons
        self.bfs_button.draw_button(lightblue)
        self.dfs_button.draw_button(lightblue)
        self.djikstra_button.draw_button(lightblue)

    def sketch_hotbar(self):
        self.screen.fill('white')
        pygame.draw.rect(self.screen, WHITE, (0, 0, 240, 768), 0)

    def sketch_grid(self):
        # Add borders for a cleaner look
        pygame.draw.rect(self.screen, 'black', (240, 0, width, height), 0)
        pygame.draw.rect(self.screen, 'black', (264, 24, maximum_grid_width, maximum_grid_height), 0)

        # Draw grid
        # There are 52 square pixels across on grid [ WITHOUT BORDERS! ]
        # There are 30 square pixels vertically on grid [ WITHOUT BORDERS! ]
        for x in range(52):
            pygame.draw.line(self.screen, ALICE, (grid_minimum_x + x * self.graph_node_length, grid_minimum_y),
                             (grid_minimum_x + x * self.graph_node_length, grid_maximum_y))
        for y in range(30):
            pygame.draw.line(self.screen, ALICE, (grid_minimum_x, grid_minimum_y + y * self.graph_node_length),
                             (grid_maximum_x, grid_minimum_y + y * self.graph_node_length))

    def sketch_grid_buttons(self):
        # Draw buttons
        self.start_end_node_button.draw_button(STEELBLUE)
        self.wall_node_button.draw_button(STEELBLUE)
        self.start_button.draw_button(STEELBLUE)
        self.main_menu_button.draw_button(STEELBLUE)
        self.maze_generate_button.draw_button(STEELBLUE)

    def grid_window_buttons(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_end_node_button.isOver(pos):
                self.pygame_state = 'destination'
            elif self.wall_node_button.isOver(pos):
                self.pygame_state = 'traffic'
            elif self.start_button.isOver(pos):
                self.pygame_state = 'start visualizing'
            elif self.main_menu_button.isOver(pos):
                pygame.display.update()
                self.screen = pygame.display.set_mode((500, 500))
                self.back_to_menu()
            elif self.maze_generate_button.isOver(pos):
                self.pygame_state = 'traffic'
                self.maze.generateSolid()
                self.pygame_state = 'destination'

        # Get mouse position and check if it is hovering over button
        if event.type == pygame.MOUSEMOTION:
            print(pos)
            if self.start_end_node_button.isOver(pos):
                self.start_end_node_button.colour = Yellow
            elif self.wall_node_button.isOver(pos):
                self.wall_node_button.colour = Yellow
            elif self.start_button.isOver(pos):
                self.start_button.colour = Yellow
            elif self.main_menu_button.isOver(pos):
                self.main_menu_button.colour = Yellow
            elif self.maze_generate_button.isOver(pos):
                self.maze_generate_button.colour = Yellow
            else:
                self.start_end_node_button.colour, self.wall_node_button.colour, \
                self.start_button.colour, self.main_menu_button.colour, self.maze_generate_button.colour = \
                    STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE

    def grid_button_keep_colour(self):
        if self.pygame_state == 'destination':
            self.start_end_node_button.colour = Yellow

        elif self.pygame_state == 'traffic':
            self.wall_node_button.colour = Yellow

    def execute_reset(self):
        self.node_input = 0

        # Start and End Nodes Coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        # Wall Nodes List (list already includes the coordinates of the borders)
        self.wall_dead_end = boundary.copy()

        # Switch States
        self.pygame_state = 'maze'

    def back_to_menu(self):
        self.node_input = 0

        # Start and End Nodes Coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        # Wall Nodes List (list already includes the coordinates of the borders)
        self.wall_dead_end = boundary.copy()

        # Switch States
        self.pygame_state = 'menu'
        pygame.display.update()
        self.screen = pygame.display.set_mode((500, 500))

    def menu(self):
        # Draw Background
        pygame.display.update()
        self.sketch_main_menu()
        # Check if game is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.driving = False
            pos = pygame.mouse.get_pos()
            # Get mouse position and check if it is clicking button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.bfs_button.isOver(pos):
                    pygame.display.update()
                    self.screen = pygame.display.set_mode((1536, 768))
                    self.algo_used = 'bfs'
                    self.pygame_state = 'maze'
                if self.dfs_button.isOver(pos):
                    pygame.display.update()
                    self.screen = pygame.display.set_mode((1536, 768))
                    self.algo_used = 'dfs'
                    self.pygame_state = 'maze'
                if self.djikstra_button.isOver(pos):
                    pygame.display.update()
                    self.screen = pygame.display.set_mode((1536, 768))
                    self.algo_used = 'dfs'
                    self.pygame_state = 'maze'

            # Get mouse position and check if it is hovering over button
            if event.type == pygame.MOUSEMOTION:
                if self.bfs_button.isOver(pos):
                    self.bfs_button.colour = lightblue
                elif self.dfs_button.isOver(pos):
                    self.dfs_button.colour = lightblue
                else:
                    self.bfs_button.colour, self.dfs_button.colour = WHITE, WHITE

    def call_maze(self):
        self.sketch_hotbar()
        self.sketch_grid_buttons()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.driving = False
            pos = pygame.mouse.get_pos()
            self.grid_window_buttons(pos, event)

    def add_nodes(self):
        self.grid_button_keep_colour()
        pygame.display.update()
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.driving = False

            # Grid button function from Helper Functions
            self.grid_window_buttons(pos, event)

            # Set boundaries for where mouse position is valid
            if 264 < pos[0] < 1512 and 24 < pos[1] < 744:
                x_grid_pos = (pos[0] - 264) // 24
                y_grid_pos = (pos[1] - 24) // 24
                # print('GRID-COORD:', x_grid_pos, y_grid_pos)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_drag = 1

                    if self.pygame_state == 'destination' and self.node_input < 2:
                        # Choose point colour for grid and record the coordinate of start pos
                        if self.node_input == 0 and (x_grid_pos + 1, y_grid_pos + 1) not in self.wall_dead_end:
                            car = pygame.image.load(f'liko.png')
                            self.start_node_x = x_grid_pos + 1
                            self.start_node_y = y_grid_pos + 1
                            # print(self.start_node_x, self.start_node_y)
                            self.node_input += 1

                        # Choose point colour for grid and record the coordinate of end pos
                        # Also, check that the end node is not the same point as start node
                        elif self.node_input == 1 and (x_grid_pos + 1, y_grid_pos + 1) != (
                                self.start_node_x, self.start_node_y) and (
                                x_grid_pos + 1, y_grid_pos + 1) not in self.wall_dead_end:
                            car = pygame.image.load(f'car2.png')
                            self.end_node_x = x_grid_pos + 1
                            self.end_node_y = y_grid_pos + 1
                            # print(self.end_node_x, self.end_node_y)
                            self.node_input += 1

                        else:
                            continue

                        # Draw point on Grid

                        self.screen.blit(car, (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24))
                # Checks if mouse button is no longer held down
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_drag = 0

                # Checks if mouse button is being held down; drag feature
                if self.mouse_drag == 1:
                    # Draw Wall Nodes and append Wall Node Coordinates to the Wall Nodes List
                    # Check if wall node being drawn/added is already in the list and check if it is overlapping start/end nodes
                    if self.pygame_state == 'traffic':
                        if (x_grid_pos + 1, y_grid_pos + 1) not in self.wall_dead_end \
                                and (x_grid_pos + 1, y_grid_pos + 1) != (self.start_node_x, self.start_node_y) \
                                and (x_grid_pos + 1, y_grid_pos + 1) != (self.end_node_x, self.end_node_y):
                            random_traffic = random.randint(1, 5)
                            traffic = pygame.image.load(f'traffic{random_traffic}.png')
                            self.screen.blit(traffic, (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24))
                            self.wall_dead_end.append((x_grid_pos + 1, y_grid_pos + 1))

    def execute_search_algorithm(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.driving = False
        if self.algo_used == 'bfs':
            self.bfs = BreadthFirst(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y,
                                    self.wall_dead_end)
            if self.start_node_x or self.end_node_x is not None:
                self.bfs.bfs_execute()
            # Make Object for new path
            if self.bfs.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, self.bfs.route, [])
                self.draw_path.get_path_coords()
                self.draw_path.draw_path()

            else:
                self.draw_text('Roads are Blocked by Traffic or Non-Existent!', self.screen, [768, 384], 50, ERROR, FONT, centered=True)


        elif self.algo_used == 'dfs':
            self.dfs = DepthFirst(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y,
                                  self.wall_dead_end)
            if self.start_node_x or self.end_node_x is not None:
                self.dfs.dfs_execute()
            # Make Object for new path
            if self.dfs.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, self.dfs.route, [])
                self.draw_path.get_path_coords()
                self.draw_path.draw_path()

            else:
                self.draw_text('Roads are Blocked by Traffic or Non-Existent!', self.screen, [768, 384], 50, ERROR, FONT, centered=True)

        elif self.algo_used == 'dijkstra':
            self.dijkstra = Dijkstra(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_dead_end)

            if self.start_node_x or self.end_node_x is not None:
                self.dijkstra.dijkstra_execute()

            if self.dijkstra.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, None, self.dijkstra.route)
                self.draw_path.draw_path()

            else:
                self.draw_text('Roads are Blocked by Traffic or Non-Existent!', self.screen, [768, 384], 50, 'red', FONT, centered=True)

        pygame.display.update()

        self.pygame_state = 'aftermath'

    def reset_or_main_menu(self):
        pygame.display.update()
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.driving = False
            if event.type == pygame.MOUSEMOTION:
                if self.start_end_node_button.isOver(pos):
                    self.start_end_node_button.colour = Yellow
                elif self.wall_node_button.isOver(pos):
                    self.wall_node_button.colour = Yellow
                elif self.start_button.isOver(pos):
                    self.start_button.colour = Yellow
                elif self.main_menu_button.isOver(pos):
                    self.main_menu_button.colour = Yellow
                else:
                    self.start_end_node_button.colour, self.wall_node_button.colour, self.start_button.colour, self.main_menu_button.colour = STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE,

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.main_menu_button.isOver(pos):
                    self.back_to_menu()
