import pygame

WIDTH = 610
HEIGHT = 485
FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MARGIN = 1
CELLSIZE = 10

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("<name>")
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

        for x in range(self.cols):
            self.cells.append([])
            for y in range(self.rows):
                self.cells[x].append(Cell((x, y), 0))

    def update(self):
        '''Update grid state'''

        # Draw all cells
        for x in range(self.cols):
            for y in range(self.rows):
                self.cells[x][y].draw()

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

        # Don't count self as a neighbor
        sum -= self.cells[x][y].value

        return sum


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

        # Reset display
        screen.fill((150, 150, 150))

        # Render and update grid
        grid.update()

        # Update display
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
