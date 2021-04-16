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

    def __init__(self, pos: pygame.Vector2, color: pygame.Vector3):
        self.pos = pos
        self.color = color

    def draw(self):
        '''Draw a cell with the given parameters'''
        rect = pygame.Rect(
            (MARGIN + CELLSIZE) * self.pos[0] + MARGIN,
            (MARGIN + CELLSIZE) * self.pos[1] + MARGIN,
            CELLSIZE, CELLSIZE
        )
        pygame.draw.rect(screen, self.color, rect)


class Grid:
    '''An object for the grid itself'''

    def __init__(self):
        self.rows = 23
        self.cols = 29
        self.grid = [[0 for x in range(self.rows)] for y in range(self.cols)]

        self.gameStarted = False

    def update(self):
        '''Update grid state'''
        for i in range(self.cols):
            for j in range(self.rows):
                # Set color based on sqaure value
                if self.grid[i][j] == 0:
                    color = WHITE
                if self.grid[i][j] == 1:
                    color = GREEN

                # Draw grid square
                cell = Cell((i, j), color)
                cell.draw()


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
                    if grid.grid[row][col] == 0:
                        grid.grid[row][col] = 1
                    elif grid.grid[row][col] == 1:
                        grid.grid[row][col] = 0

        # Reset display
        screen.fill(BLACK)

        # Render and update grid
        grid.update()

        # Update display
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
