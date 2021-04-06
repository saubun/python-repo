import pygame
import numpy as np

WIDTH = 600
HEIGHT = 480
FPS = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting")
clock = pygame.time.Clock()

# Setup an array of length 135 with numbers from 10 - 400
arr = [np.random.randint(10, 400) for _ in range(135)]
newArr = []


def main():
    '''The main function containing the game loop'''
    running = True
    while running:

        # Limit FPS
        clock.tick(FPS)

        # Main event listening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Reset display
        screen.fill(BLACK)

        # Reset dummy value for spacing
        dummy = 30

        # Sorting
        if len(arr) > 0:
            min = 999  # Very large default min value not in the arr
            for item in arr:
                if item < min:
                    min = item
            newArr.append(min)
            try:
                arr.remove(min)
            except ValueError:
                pass

            # Draw the array
            for item in arr:
                dummy += 4
                p = pygame.Rect(WIDTH - dummy, HEIGHT - 20, 2, 0)
                p.inflate_ip(0, item)
                p.bottom = HEIGHT - 20
                pygame.draw.rect(screen, WHITE, p)

        # Reset dummy value for spacing
        dummy = 30

        # Draw new array
        for item in newArr:
            dummy += 4
            p = pygame.Rect(dummy, HEIGHT - 20, 2, 0)
            p.inflate_ip(0, item)
            p.bottom = HEIGHT - 20
            pygame.draw.rect(screen, WHITE, p)

        # Update display
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
