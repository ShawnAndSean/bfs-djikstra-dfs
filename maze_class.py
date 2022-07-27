from constants import *
import random


class Maze:
    def __init__(self, app, wallPos):
        self.app = app
        self.visited = []
        self.walls = wallPos
        # x-range index on drawable surface is 1 to 52
        # y range index is 1 to 30
        self.xMax = 53
        self.yMax = 31

    def generateSolid(self):
        for y in range(1, self.yMax):
            for x in range(1, self.xMax):
                random_house = random.randint(1, 5)
                self.walls.append((x, y))
                house = pygame.image.load(f'house{random_house}.png')
                self.app.screen.blit(house, (x * 24 + 240, y * 24, 24, 24))
        self.draw_pathway_highlights()
        self.generateMaze()

    def generateMaze(self):
        x_pos = random.randint(1, self.xMax)
        y_pos = random.randint(1, self.yMax)
        start_pos = (x_pos, y_pos)
        self.recursiveDFS(start_pos)

    def checkValid(self, pos):
        if pos not in boundary and pos in self.walls:
            return True
        return False

    def recursiveDFS(self, pos):
        movesLeft = ['L', 'R', 'U', 'D']
        i, j = pos
        while movesLeft:
            chooseRandMove = random.randint(0, len(movesLeft) - 1)
            currMove = movesLeft.pop(chooseRandMove)
            # Temporary variabes to not update the original pos of the current node
            xTemp = i
            yTemp = j

            if currMove == 'L':
                xTemp -= 2
            elif currMove == 'R':
                xTemp += 2
            elif currMove == 'U':
                yTemp += 2
            else:
                yTemp -= 2

            newPos = (xTemp, yTemp)

            if self.checkValid(newPos):
                self.walls.remove(newPos)
                # calculate difference between curr pos and neighbouring pos
                xDiff = newPos[0] - i
                yDiff = newPos[1] - j

                # Determine the middle wall position to remove
                middleWallPos = (i + xDiff / 2, j + yDiff / 2)
                print(middleWallPos)

                # Remove the middle wall as well

                if middleWallPos in self.walls:
                    self.walls.remove((middleWallPos))
                    self.drawMaze(middleWallPos, 'lightblue')
                    self.drawMaze(newPos, 'lightblue')
                    self.recursiveDFS(newPos)

        return

    def create_pathway(self, pos, colour):
        i, j = pos
        pygame.draw.rect(self.app.screen, colour, (i * 24 + 240, j * 24, 24, 24), 0)
        pygame.display.update()

    def draw_pathway_highlights(self):
        for x in range(52):
            pygame.draw.line(self.app.screen, ALICE, (grid_minimum_x + x * 24, grid_minimum_y), (grid_minimum_x + x * 24, grid_maximum_y))
        for y in range(30):
            pygame.draw.line(self.app.screen, ALICE, (grid_minimum_x, grid_minimum_y + y * 24), (grid_maximum_x, grid_minimum_y + y * 24))
        pygame.display.update()

    def drawMaze(self, pos, colour):
        i, j = pos
        self.create_pathway(pos, colour)
        # Redraw grid (for aesthetic purposes lol)
        for x in range(52):
            pygame.draw.line(self.app.screen, ALICE, (grid_minimum_x + x * 24, grid_minimum_y), (grid_minimum_x + x * 24, grid_maximum_y), 1)
        for y in range(30):
            # self.app.screen.blit(house, (GS_X + x * 24, GS_Y))
            pygame.draw.line(self.app.screen, ALICE, (grid_minimum_x, grid_minimum_y + y * 24), (grid_maximum_x, grid_minimum_y + y * 24), 1)

        pygame.display.update()
