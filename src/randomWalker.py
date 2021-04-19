from numpy.random import randint
import pygame

WIDTH = 610
HEIGHT = 485
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MARGIN = 1
CELLSIZE = 10

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random Walker")
clock = pygame.time.Clock()


class Cell:
    """An object for each individual cell"""

    def __init__(self, pos: pygame.Vector2, value: int):
        self.pos = pygame.Vector2(pos)
        self.value = value

    def draw(self):
        """Draw a cell with the given parameters"""
        # Empty
        if self.value == 0:
            self.color = WHITE
        
        # Path
        elif self.value == 1:
            self.color = BLACK
        
        # Head
        elif self.value == 2:
            self.color = GREEN

        rect = pygame.Rect(
            (MARGIN + CELLSIZE) * self.pos.x + MARGIN,
            (MARGIN + CELLSIZE) * self.pos.y + MARGIN,
            CELLSIZE,
            CELLSIZE,
        )
        pygame.draw.rect(screen, self.color, rect)


class Grid:
    """An object for the grid itself"""

    def __init__(self):
        self.rows = HEIGHT // (CELLSIZE + MARGIN)
        self.cols = WIDTH // (CELLSIZE + MARGIN)
        self.cells = []

        for x in range(self.cols):
            self.cells.append([])
            for y in range(self.rows):
                self.cells[x].append(Cell((x, y), 0))
        
        self.cells[self.cols//2][self.rows//2].value = 2
        
    def update(self):
        """Update grid state"""

        # Draw all cells
        for x in range(self.cols):
            for y in range(self.rows):
                self.cells[x][y].draw()

                if self.cells[x][y].value == 2:
                    direction = randint(1, 5)
                    self.cells[x][y].value = 1
                    
                    try:
                        # Up
                        if direction == 1:
                            self.cells[x][y-1].value = 2
                        
                        # Down
                        elif direction == 2:
                            self.cells[x][y+1].value = 2

                        # Left
                        elif direction == 3:
                            self.cells[x-1][y].value = 2

                        # Right
                        elif direction == 4:
                            self.cells[x+1][y].value = 2
                    except IndexError:
                        self.cells[randint(0, self.cols)][randint(0, self.rows)].value = 2
                    

def main():
    """Main function containing the game loop"""
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


if __name__ == "__main__":
    main()
