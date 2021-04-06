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
pygame.display.set_caption("Sorting")
clock = pygame.time.Clock()

arr = [5, 7, 4, 7, 5, 4, 3, 2, 6, 5, 4, 1]


def main():
    running = True
    i = 20
    while running:
        clock.tick(FPS)

        # Main event listening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Reset display
        screen.fill(BLACK)

        for item in arr:
            i += 40
            p = pygame.Rect(i, HEIGHT - 20, 20, 0)
            p.inflate_ip(0, item * 20)
            p.bottom = HEIGHT - 20
            pygame.draw.rect(screen, WHITE, p)

        i = 20

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
