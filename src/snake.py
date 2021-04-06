import pygame
import random
import math

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
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

Vector2 = pygame.Vector2


def randomBase10Int(max, min=0):
    num = random.randint(min, max)
    num = math.ceil(num / 10) * 10
    return num


class Snake:
    def __init__(self):
        self.parts = [Vector2(300, 240)]
        self.dx = 10
        self.dy = 0
        self.length = len(self.parts)

    def draw(self):
        self.length = len(self.parts)
        for part in self.parts:
            partRect = pygame.Rect(part.x, part.y, 10, 10)
            pygame.draw.rect(screen, GREEN, partRect, 1)

    def move(self):
        head = Vector2(self.parts[0].x + self.dx, self.parts[0].y + self.dy)
        self.parts.insert(0, head)
        self.parts.pop()

    def checkWallCollision(self):
        ...

    def checkSelfCollision(self):
        ...


class Food:
    def __init__(self):
        self.pos = Vector2(randomBase10Int(WIDTH), randomBase10Int(HEIGHT))

    def draw(self):
        foodRect = pygame.Rect(self.pos.x, self.pos.y, 10, 10)
        pygame.draw.rect(screen, GREEN, foodRect)


def main():
    running = True
    snake = Snake()
    foodCount = 0
    while running:
        clock.tick(FPS)

        # Main event listening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_UP:
                    snake.dx = 0
                    snake.dy = -10
                if event.key == pygame.K_DOWN:
                    snake.dx = 0
                    snake.dy = 10
                if event.key == pygame.K_LEFT:
                    snake.dx = -10
                    snake.dy = 0
                if event.key == pygame.K_RIGHT:
                    snake.dx = 10
                    snake.dy = 0

        # Reset display
        screen.fill(BLACK)

        # Snake drawing
        snake.draw()
        snake.move()

        # Food drawing
        if foodCount == 0:
            food = Food()
            foodCount += 1

        try:
            food.draw()
        except Exception:
            pass

        # Food COllision checkSelfCollision
        if snake.parts[0] == food.pos:
            foodCount = 0
            snake.parts.append(snake.parts[len(snake.parts)-1])

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
