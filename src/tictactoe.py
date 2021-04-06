import pygame
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MARGIN = 5
SIZE = 100

WIDTH = SIZE * 3 + MARGIN * 4
HEIGHT = SIZE * 3 + MARGIN * 4
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("tictactoe")
clock = pygame.time.Clock()


# Main function
def main():
    running = True
    turn = 1
    gameOver = False
    grid = [[0 for x in range(3)] for y in range(3)]
    while running:
        clock.tick(FPS)

        # Main event listening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Change the screen coordinates to grid coordinates
                col = pos[0] // (SIZE + MARGIN)
                row = pos[1] // (SIZE + MARGIN)

                # Color the square if its empty
                if grid[row][col] == 0:
                    if turn == 1:
                        grid[row][col] = 1
                        turn = 2
                    elif turn == 2:
                        grid[row][col] = 2
                        turn = 1

        # Reset display
        screen.fill(BLACK)

        # Render grid (x = green & o = red)
        for row in range(3):
            for col in range(3):
                if grid[row][col] == 1:
                    color = GREEN
                elif grid[row][col] == 2:
                    color = RED
                else:
                    color = WHITE
                p = pygame.Rect((MARGIN + SIZE) * col + MARGIN,
                                (MARGIN + SIZE) * row + MARGIN, SIZE, SIZE)
                pygame.draw.rect(screen, color, p)

        # Win checking (too lazy for an algorithm sorry)
        if grid[0][0] == 1 and grid[1][0] == 1 and grid[2][0] == 1:
            gameOver = True
        elif grid[0][1] == 1 and grid[1][1] == 1 and grid[2][1] == 1:
            gameOver = True
        elif grid[0][2] == 1 and grid[1][2] == 1 and grid[2][2] == 1:
            gameOver = True

        if grid[0][0] == 1 and grid[0][1] == 1 and grid[0][2] == 1:
            gameOver = True
        elif grid[1][0] == 1 and grid[1][1] == 1 and grid[1][2] == 1:
            gameOver = True
        elif grid[2][0] == 1 and grid[2][1] == 1 and grid[2][2] == 1:
            gameOver = True

        if grid[0][0] == 1 and grid[1][1] == 1 and grid[2][2] == 1:
            gameOver = True
        elif grid[0][2] == 1 and grid[1][1] == 1 and grid[2][0] == 1:
            gameOver = True

        if grid[0][0] == 2 and grid[1][0] == 2 and grid[2][0] == 2:
            gameOver = True
        elif grid[0][1] == 2 and grid[1][1] == 2 and grid[2][1] == 2:
            gameOver = True
        elif grid[0][2] == 2 and grid[1][2] == 2 and grid[2][2] == 2:
            gameOver = True

        if grid[0][0] == 2 and grid[0][1] == 2 and grid[0][2] == 2:
            gameOver = True
        elif grid[1][0] == 2 and grid[1][1] == 2 and grid[1][2] == 2:
            gameOver = True
        elif grid[2][0] == 2 and grid[2][1] == 2 and grid[2][2] == 2:
            gameOver = True

        if grid[0][0] == 2 and grid[1][1] == 2 and grid[2][2] == 2:
            gameOver = True
        elif grid[0][2] == 2 and grid[1][1] == 2 and grid[2][0] == 2:
            gameOver = True

        # Update display
        pygame.display.update()

        # Reset grid and restart game
        if gameOver:
            grid = [[0 for x in range(3)] for y in range(3)]
            time.sleep(0.5)
            gameOver = False

    pygame.quit()


if __name__ == '__main__':
    main()
