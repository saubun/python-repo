import pygame
import numpy as np

WIDTH = 610
HEIGHT = 485
FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MARGIN = 0
CELLSIZE = 5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()


class Cell:
    '''An object for each individual cell'''

    def __init__(self, pos: pygame.Vector2, value: int):
        self.pos = pygame.Vector2(pos)
        self.value = value

    def draw(self):
        '''Draw a cell with the given parameters'''
        if self.value == 0:
            self.color = WHITE
        elif self.value == 1:
            self.color = GREEN

        rect = pygame.Rect(
            (MARGIN + CELLSIZE) * self.pos.x + MARGIN,
            (MARGIN + CELLSIZE) * self.pos.y + MARGIN,
            CELLSIZE, CELLSIZE
        )
        pygame.draw.rect(screen, self.color, rect)


class Grid:
    '''An object for the grid itself'''

    def __init__(self):
        self.rows = HEIGHT // (CELLSIZE + MARGIN)
        self.cols = WIDTH // (CELLSIZE + MARGIN)
        self.cells = []
        self.newCells = []
        self.generation = 0

        for x in range(self.cols):
            self.cells.append([])
            for y in range(self.rows):
                self.cells[x].append(Cell((x, y), 0))

        self.gameStarted = False

    def update(self):
        '''Update grid state'''
        self.generation += 1

        # Draw all cells
        for x in range(self.cols):
            for y in range(self.rows):
                self.cells[x][y].draw()

        self.newCells = self.cells

        # Main game
        for x in range(self.cols):
            for y in range(self.rows):
                if self.gameStarted:

                    # Get neighbors and current cell state
                    sum = self.getAliveNeighborCount(x, y)
                    state = self.cells[x][y].value

                    # Game rules
                    if state == 0 and sum == 3:
                        self.newCells[x][y].value = 1
                    elif state == 1 and (sum < 2 or sum > 3):
                        self.newCells[x][y].value = 0
                    else:
                        self.newCells[x][y].value = state

        self.cells = self.newCells

    def getAliveNeighborCount(self, x, y) -> int:
        '''Get the amount neighboring alive cells from the cell
           of the passed in x and y values'''
        sum = 0

        # Add all the neighbors
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    sum += self.cells[x+i][y+j].value
                except IndexError:
                    pass

        return sum


def main():
    '''Main function containing the game loop'''
    running = True
    grid = Grid()

    # Fill in 50 random cells
    for _ in range(1000):
        y = np.random.randint(0, grid.rows-1)
        x = np.random.randint(0, grid.cols-1)
        grid.cells[x][y].value = np.random.randint(0, 2)

    while running:
        clock.tick(FPS)

        # Main event listening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                # Reset
                if event.key == pygame.K_ESCAPE:
                    for x in range(grid.cols):
                        for y in range(grid.rows):
                            grid.cells[x][y].value = 0

                # Fill cells randomly
                if event.key == pygame.K_r:
                    for _ in range(1000):
                        y = np.random.randint(0, grid.rows-1)
                        x = np.random.randint(0, grid.cols-1)
                        grid.cells[x][y].value = np.random.randint(0, 2)

                # Allow toggling whether the simulation is active or not
                if event.key == pygame.K_SPACE:
                    grid.gameStarted = not grid.gameStarted

            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Allow drawing default positions
                if not grid.gameStarted:
                    pos = pygame.mouse.get_pos()

                    # Change the screen coordinates to grid coordinates
                    row = pos[0] // (CELLSIZE + MARGIN)
                    col = pos[1] // (CELLSIZE + MARGIN)

                    # Color the square if its empty
                    if grid.cells[row][col].value == 0:
                        grid.cells[row][col].value = 1
                    elif grid.cells[row][col].value == 1:
                        grid.cells[row][col].value = 0

        # Reset display
        screen.fill(WHITE)

        # Render and update grid
        grid.update()

        # Update display
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
