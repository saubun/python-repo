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


class Ball:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.pos = pygame.Vector2(self.x, self.y)

    def draw(self):
        pygame.draw.circle(screen, WHITE, self.pos, self.r)


def main():
    running = True
    balls = []
    radius = 0
    tempball = Ball(0, 0, 0)
    while running:
        clock.tick(FPS)

        # Make a grow effect while mouse is pressed
        if pygame.mouse.get_pressed()[0]:
            radius += 1
            pos = pygame.mouse.get_pos()
            tempball = Ball(pos[0], pos[1], radius)

        # Main event listening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Delete the grow effect ball and draw real one
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                del tempball
                balls.append(Ball(pos[0], pos[1], radius))
                radius = 0

        # Reset display
        screen.fill(BLACK)

        # Render all balls
        for ball in balls:
            ball.draw()

            # Collision detection for each ball
            for nball in balls:
                if nball != ball:
                    displacement = ball.pos - nball.pos
                    direction = displacement.normalize()
                    velocity = direction * 5
                    distance = displacement.magnitude()

                    if distance < ball.r + nball.r:
                        ball.pos += velocity

        # Draw the temp ball if it exists
        try:
            tempball.draw()
        except Exception:
            pass

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
