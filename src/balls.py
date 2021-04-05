import pygame
import math

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
pygame.display.set_caption("Balls")
clock = pygame.time.Clock()


class Ball(object):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def draw(self):
        self.pos = pygame.Vector2(self.x, self.y)
        pygame.draw.circle(screen, WHITE, self.pos, self.r)


def main():
    running = True
    balls = []
    radius = 0
    tempball = Ball(0, 0, 0)
    while running:
        clock.tick(FPS)
        if pygame.mouse.get_pressed()[0]:
            radius += 1

            pos = pygame.mouse.get_pos()
            tempball = Ball(pos[0], pos[1], radius)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                del tempball
                pos = pygame.mouse.get_pos()
                balls.append(Ball(pos[0], pos[1], radius))
                radius = 0

        screen.fill(BLACK)

        for ball in balls:
            ball.draw()

            # Collision detection for each ball
            for nball in balls:
                if nball != ball:
                    dx = ball.x - nball.x
                    dy = ball.y - nball.y
                    distance = math.sqrt(dx * dx + dy * dy)

                    if distance < ball.r + nball.r:
                        print('collision')

        try:
            tempball.draw()
        except Exception:
            pass

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
