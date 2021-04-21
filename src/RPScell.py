import pygame
import random

WIDTH = 610
HEIGHT = 485
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MARGIN = 0
CELLSIZE = 5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors Cellular Automata")
clock = pygame.time.Clock()


class Cell:
    """An object for each individual cell"""

    def __init__(self, pos: pygame.Vector2, value: int, level: int):
        self.pos = pygame.Vector2(pos)
        self.value = value
        self.level = level

    def draw(self):
        """Draw a cell with the given parameters"""
        if self.value == 0:
            self.color = WHITE
        elif self.value == 1:
            self.color = RED
        elif self.value == 2:
            self.color = BLUE
        elif self.value == 3:
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
        self.gameStarted = False

        for x in range(self.cols):
            self.cells.append([])
            for y in range(self.rows):
                self.cells[x].append(Cell((x, y), 0, 0))

    def update(self):
        """Update grid state"""

        # Draw all cells
        for x in range(self.cols):
            for y in range(self.rows):
                self.cells[x][y].draw()

        # Main logic
        for x in range(self.cols):
            for y in range(self.rows):
                state = self.cells[x][y].value
                level = self.cells[x][y].level

                if self.gameStarted:

                    # For reds
                    if state == 1:
                        blues = self.getNeighborOfColor(x, y, 2)

                        for cell in blues:
                            cell.value = 1
                            if cell.level < 9:
                                cell.level += 1

                        if level > 0:
                            level -= 1

                    # For blues
                    elif state == 2:
                        greens = self.getNeighborOfColor(x, y, 3)

                        for cell in greens:
                            cell.value = 2
                            if cell.level < 9:
                                cell.level += 1

                        if level > 0:
                            level -= 1

                    # For greens
                    elif state == 3:
                        reds = self.getNeighborOfColor(x, y, 1)

                        for cell in reds:
                            cell.value = 3
                            if cell.level < 9:
                                cell.level += 1

                        if level > 0:
                            level -= 1

                # For dead cells
                if state == 0:
                    reds = self.getNeighborOfColor(x, y, 1)
                    blues = self.getNeighborOfColor(x, y, 2)
                    greens = self.getNeighborOfColor(x, y, 3)

                    for cell in reds:
                        if cell.level < 9:
                            state = cell.value
                            cell.level += 1

                    for cell in blues:
                        if cell.level < 9:
                            state = cell.value
                            cell.level += 1

                    for cell in greens:
                        if cell.level < 9:
                            state = cell.value
                            cell.level += 1

    def getNeighborOfColor(self, x: int, y: int, value: int) -> list:
        """Get the amount neighboring alive cells from the cell
        of the passed in x and y values"""
        sum: list = []

        # Add all the neighbors
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if self.cells[x + i][y + j].value == value:
                        sum.append(self.cells[x + i][y + j])
                except IndexError:
                    pass

        # Don't count self as a neighbor
        try:
            sum.pop(sum.index(self.cells[x][y]))
        except ValueError:
            pass

        return sum


def main():
    """Main function containing the game loop"""
    running = True
    grid = Grid()
    color = 1
    global FPS

    while running:
        clock.tick(FPS)

        if grid.gameStarted:
            FPS = 10
        else:
            FPS = 60

        # Main event listening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if not grid.gameStarted:
                    if event.key == pygame.K_0:
                        color = 0
                    elif event.key == pygame.K_1:
                        color = 1
                    elif event.key == pygame.K_2:
                        color = 2
                    elif event.key == pygame.K_3:
                        color = 3

                    if event.key == pygame.K_r:
                        for x in range(grid.cols):
                            for y in range(grid.rows):
                                grid.cells[x][y].value = random.randint(0, 4)

                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_SPACE:
                    grid.gameStarted = not grid.gameStarted

        # Reset display
        screen.fill((150, 150, 150))

        # Draw selected cell type
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            # Change the screen coordinates to grid coordinates
            row = pos[0] // (CELLSIZE + MARGIN)
            col = pos[1] // (CELLSIZE + MARGIN)

            # Color the square if its empty
            if color == 0:
                grid.cells[row][col].value = 0
            elif color == 1:
                grid.cells[row][col].value = 1
            elif color == 2:
                grid.cells[row][col].value = 2
            elif color == 3:
                grid.cells[row][col].value = 3

        # Render and update grid
        grid.update()

        # Update display
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
