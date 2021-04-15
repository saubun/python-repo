import pygame

WIDTH = 600
HEIGHT = 480
FPS = 120

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


class Block():
    '''A class to define a rectangle object'''

    def __init__(self, posX, posY, width, height):
        self.pos = pygame.Vector2(posX, posY)
        self.width = width
        self.height = height

    def draw(self, color):
        '''Draw the rect'''
        self.color = color
        self.rect = pygame.Rect(self.pos.x, self.pos.y,
                                self.width, self.height)
        pygame.draw.rect(screen, self.color, self.rect)


class Circle:
    '''A class to create a circle object'''

    def __init__(self, posX: int, posY: int, radius: int):
        self.pos = pygame.Vector2(posX, posY)
        self.radius = radius
        self.bounce = 0

    def draw(self, color: set or list):
        '''Draw the Circle'''
        self.color = color
        pygame.draw.circle(screen, self.color, self.pos, self.radius)

    def applyForce(self, force: pygame.Vector2):
        '''Apply the given force to the Circle'''
        self.pos += force

    def gravity(self):
        '''Applies gravity as a force'''
        self.applyForce(pygame.Vector2(0, 9.81))

    def collisionCheckOtherCircle(self, circle) -> bool:
        '''Does circle collision checking between given circle and self'''
        ...

    def collisionCheckRect(self, rect: Block) -> bool:
        '''Does circle collision checking between given rect and self'''
        if self.pos.y >= rect.pos.y - self.radius:
            return True


def main():
    '''Main function containing the game loop'''

    floor = Block(0, HEIGHT-20, WIDTH, 20)
    ball = Circle(WIDTH//2, HEIGHT//2, 20)

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

        # Key listening
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            ball.applyForce((-1, 0))
        if keys[pygame.K_d]:
            ball.applyForce((1, 0))
        if keys[pygame.K_SPACE]:
            ball.applyForce((0, -10))

        # Reset display
        screen.fill(BLACK)

        # Draw floor
        floor.draw(GREY)

        # Draw ball
        ball.draw(GREEN)

        # Apply gravity only if no collision with floor
        if ball.collisionCheckRect(floor):
            ball.pos.y = floor.pos.y - ball.radius
        else:
            ball.gravity()

        # ball.applyForce(pygame.Vector2(1, 0))

        # Update display
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
