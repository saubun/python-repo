import pygame

WIDTH = 605
HEIGHT = 605
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MARGIN = 5
SIZE = 20

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding")
clock = pygame.time.Clock()


# Main function
def main():
    # Set up grid
    grid = [[0 for x in range(24)] for y in range(24)]

    running = True
    while running:
        clock.tick(FPS)

        # Main event listening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Reset display
        screen.fill(BLACK)

        # Render grid
        for row in range(24):
            for col in range(24):
                # Decide Color
                if grid[row][col] == 1:
                    color = RED
                else:
                    color = WHITE

                # Render squares
                p = pygame.Rect((MARGIN + SIZE) * col + MARGIN,
                                (MARGIN + SIZE) * row + MARGIN, SIZE, SIZE)
                pygame.draw.rect(screen, color, p)

        # Update screen
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
