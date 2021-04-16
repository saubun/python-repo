import pygame
import random as r

WIDTH = 600
HEIGHT = 480
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("gravity")
clock = pygame.time.Clock()


class Circle:
    '''A class to create a circle object'''

    def __init__(self, pos: pygame.Vector2, radius: int, mass: int):
        self.pos = pygame.Vector2(pos)
        self.radius = radius
        self.velocity = pygame.Vector2(0, 0)
        self.mass = mass

    def draw(self, color: set or list):
        '''Draw the Circle'''
        self.color = color
        pygame.draw.circle(screen, self.color, self.pos, self.radius, 1)

    def applyForce(self, force: pygame.Vector2):
        '''Apply the given force to the Circle'''
        self.pos += force

    def collisionCheckOtherCircle(self, circle, distance) -> bool:
        '''Does circle collision checking between given circle and self'''
        if distance < self.radius + circle.radius:
            return True
        else:
            return False

    def checkInsideScreen(self) -> bool:
        '''Checks if the Circle is inside the visual screen space'''
        if self.pos.x < 0:
            return True
        elif self.pos.x > WIDTH:
            return True
        elif self.pos.y < 0:
            return True
        elif self.pos.y > HEIGHT:
            return True
        else:
            return False


def main():
    '''Main function containing the game loop'''

    balls = []

    speed = 1

    running = True
    while running:
        clock.tick(FPS)

        # Main event listening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_1:
                    speed = 1
                if event.key == pygame.K_2:
                    speed = 10
                if event.key == pygame.K_3:
                    speed = 100
                if event.key == pygame.K_4:
                    speed = 1000
                if event.key == pygame.K_5:
                    speed = 10000
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ...

        if pygame.mouse.get_pressed()[0]:
            radius = r.randint(5, 10)
            mass = radius * 1000000
            balls.append(Circle((pygame.mouse.get_pos()), radius, mass))

        # Reset display
        screen.fill(BLACK)

        # For all balls
        for ball in balls:

            # Delete balls if they are offscreen for performance
            if ball.checkInsideScreen():
                balls.remove(ball)

            # Draw ball
            ball.draw(GREEN)

            # For every other ball
            for otherBall in balls:

                # Calculate forces
                oldVelocity = ball.velocity

                displacement = ball.pos - otherBall.pos

                try:
                    direction = displacement.normalize()
                except ValueError:
                    direction = displacement

                ball.velocity = direction * speed
                distance = displacement.magnitude()

                acceleration = (ball.velocity - oldVelocity) / FPS

                try:
                    forceMagnitude = 0.0000000000667 * (
                        (ball.mass * otherBall.mass) / distance**2)
                except ZeroDivisionError:
                    forceMagnitude = 0

                force = acceleration * forceMagnitude

                # Apply force and collision
                if ball.collisionCheckOtherCircle(otherBall, distance):
                    ball.pos = otherBall.pos + (
                        direction * (ball.radius + otherBall.radius))
                else:
                    ball.applyForce(-force)

        # Update display
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
