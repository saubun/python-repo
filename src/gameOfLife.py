import pygame

WIDTH = 600
HEIGHT = 480
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MARGIN = 1
CELLSIZE = 20

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()


class Cell:
    '''An object for each individual cell'''

    def __init__(self, pos: pygame.Vector2, value: int):
        self.pos = pygame.Vector2(pos)
        self.value = value
        self.neighbors = []

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

    def checkNeighbors(self, cells, i: int, j: int):
        '''Checks neighboring cells in a very ugly way'''

        # Starts at top left
        try:
            self.neighbors.append(cells[i-1][j-1])
        except IndexError:
            pass
        try:
            self.neighbors.append(cells[i-1][j])
        except IndexError:
            pass
        try:
            self.neighbors.append(cells[i-1][j+1])
        except IndexError:
            pass
        try:
            self.neighbors.append(cells[i][j-1])
        except IndexError:
            pass
        try:
            self.neighbors.append(cells[i][j+1])
        except IndexError:
            pass
        try:
            self.neighbors.append(cells[i+1][j-1])
        except IndexError:
            pass
        try:
            self.neighbors.append(cells[i+1][j])
        except IndexError:
            pass
        try:
            self.neighbors.append(cells[i+1][j+1])
        except IndexError:
            pass


class Grid:
    '''An object for the grid itself'''

    def __init__(self):
        self.rows = 23
        self.cols = 29
        self.cells = []

        for x in range(self.cols):
            self.cells.append([])
            for y in range(self.rows):
                self.cells[x].append(Cell((x, y), 0))

        self.gameStarted = False

    def update(self):
        '''Update grid state'''
        for x in range(self.cols):
            for y in range(self.rows):

                # Draw all cells
                self.cells[x][y].draw()

                # Main game
                if self.gameStarted:
                    self.cells[x][y].checkNeighbors(self.cells, x, y)
                    if self.cells[x][y].value == 1:
                        self.cells[x][y].neighbors[0].value = 1


def main():
    '''Main function containing the game loop'''
    running = True
    grid = Grid()
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
        screen.fill(BLACK)

        # Render and update grid
        grid.update()

        # Update display
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
