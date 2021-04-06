import pygame
import pygame.freetype
import random

WIDTH = 600
HEIGHT = 480
FPS = 8

SIZE = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

Vector2 = pygame.Vector2


def randomBaseSIZEInt(max, min=0):
    '''Gets a random integer that is divisible by SIZE'''
    num = random.randint(min, max)
    num = num // SIZE * SIZE
    return num


class Snake:
    def __init__(self):
        '''The snake object'''
        self.parts = [Vector2(WIDTH//2, HEIGHT//2)]
        self.dx = SIZE
        self.dy = 0
        self.length = len(self.parts)
        self.alive = True
        self.dir = RIGHT

    def draw(self):
        '''Draws the snake on the screen part by part'''
        self.length = len(self.parts)
        self.checkSelfCollision()
        self.checkWallCollision()
        for part in self.parts:
            partRect = pygame.Rect(part.x, part.y, SIZE, SIZE)
            pygame.draw.rect(screen, GREEN, partRect, 1)

    def move(self):
        '''Function to update position by moving the head and moving the
        previous parts to the position that the head used to be in'''
        head = Vector2(self.parts[0].x + self.dx, self.parts[0].y + self.dy)
        self.parts.insert(0, head)
        self.parts.pop()

    def checkWallCollision(self):
        '''Checks to see if the snake head is in contact with the wall'''
        if self.parts[0].x < 0:
            self.alive = False
        elif self.parts[0].x > WIDTH:
            self.alive = False
        elif self.parts[0].y < 0:
            self.alive = False
        elif self.parts[0].y > HEIGHT:
            self.alive = False

    def checkSelfCollision(self):
        '''Checks to see if the snake head is in contact with itself,
        this shouldn't be possible'''
        for part in self.parts[1:]:
            if self.parts[0] == part:
                self.alive = False


class Food:
    def __init__(self):
        '''Food object'''
        p = Vector2(randomBaseSIZEInt(WIDTH-10), randomBaseSIZEInt(HEIGHT-10))
        self.pos = p

    def draw(self):
        '''Draws the food onto the screen'''
        self.rect = pygame.Rect(self.pos.x, self.pos.y, SIZE, SIZE)
        pygame.draw.rect(screen, GREEN, self.rect)


def main():
    '''Main function with game loop'''
    running = True
    snake = Snake()
    foodCount = 0
    global FPS
    while running:
        # Limit frames
        clock.tick(FPS)

        # Display score
        pygame.display.set_caption(f"Snake - Score: {snake.length - 1}")

        # Main Game
        if snake.alive:

            # Reset display
            screen.fill(BLACK)

            # Main event listening
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake.dir != DOWN:
                        snake.dx = 0
                        snake.dy = -SIZE
                        snake.dir = UP
                    if event.key == pygame.K_DOWN and snake.dir != UP:
                        snake.dx = 0
                        snake.dy = SIZE
                        snake.dir = DOWN
                    if event.key == pygame.K_LEFT and snake.dir != RIGHT:
                        snake.dx = -SIZE
                        snake.dy = 0
                        snake.dir = LEFT
                    if event.key == pygame.K_RIGHT and snake.dir != LEFT:
                        snake.dx = SIZE
                        snake.dy = 0
                        snake.dir = RIGHT

            # Create a new food once one is eaten
            if foodCount == 0:
                food = Food()
                foodCount += 1

            # Snake drawing
            snake.draw()
            snake.move()

            # Draw the food
            try:
                food.draw()
            except Exception:
                pass

            # Food Collision
            if snake.parts[0] == food.pos:
                foodCount = 0
                snake.parts.append(Vector2(-SIZE, -SIZE))

        # Game over
        else:

            # Reset display
            screen.fill((50, 50, 50))

            # Reset food
            if foodCount != 0:
                foodCount = 0

            # Listen for restart & quiting
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        snake.alive = True
                        snake.parts = [snake.parts[0]]
                        snake.parts[0] = Vector2(WIDTH//2, HEIGHT//2)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
