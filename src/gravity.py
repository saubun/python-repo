import pygame

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

    def __init__(self, pos: pygame.Vector2, radius: int):
        self.pos = pygame.Vector2(pos)
        self.radius = radius
        self.bounce = 0
        self.oldVelocity = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)

    def draw(self, color: set or list):
        '''Draw the Circle'''
        self.color = color
        pygame.draw.circle(screen, self.color, self.pos, self.radius, 1)

    def applyForce(self, force: pygame.Vector2):
        '''Apply the given force to the Circle'''
        self.pos += force

    def collisionCheckOtherCircle(self, circle) -> bool:
        '''Does circle collision checking between given circle and self'''
        ...


def main():
    '''Main function containing the game loop'''

    balls = []

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

        # Mouse
        if pygame.mouse.get_pressed()[0]:
            balls.append(Circle((pygame.mouse.get_pos()), 5))

        # Reset display
        screen.fill(BLACK)

        # Draw balls
        for ball in balls:
            ball.draw(GREEN)

            # For every other ball
            for otherBall in balls:
                # Calculate gravity
                oldVelocity = ball.velocity

                try:
                    displacement = ball.pos - otherBall.pos
                    direction = displacement.normalize()
                    ball.velocity = direction * 1.0
                    # distance = displacement.magnitude()

                    acceleration = (ball.velocity - oldVelocity) / FPS
                    force = ball.radius * acceleration

                    # Check distance
                    if ball.collisionCheckOtherCircle(otherBall, ):
                        ...

                    # Apply gravity
                    else:
                        otherBall.applyForce(force)
                        ball.applyForce(force)

                except ValueError:
                    pass

        # ball.applyForce(pygame.Vector2(1, 0))

        # Update display
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
