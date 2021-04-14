import pygame

WIDTH = 600
HEIGHT = 480
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("<name>")
clock = pygame.time.Clock()


def main():
    '''Main function containing the game loop'''
    running = True
    while running:
        clock.tick(FPS)

        # Main event listening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Reset display
        screen.fill(BLACK)

        # Update display
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
