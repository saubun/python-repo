import pygame
from numpy import random

WIDTH = 600
HEIGHT = 480
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (150, 150, 150)

NORD1 = (46, 52, 64)
NORD2 = (59, 66, 82)
NORD3 = (67, 76, 94)
NORD4 = (76, 86, 106)

LIGHTBLUE = (136, 192, 208)
LIGHTGREY = (216, 222, 233)
RED2 = (191, 97, 106)
GREEN2 = (163, 190, 140)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tatakae")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()


class Projectile:
    def __init__(
        self, pos: pygame.Vector2, size: int, direction: pygame.Vector2, speed: float
    ):
        """A subscriptable class to represent a projectile"""
        self.pos = pygame.Vector2(pos)
        self.size = size
        self.direction = pygame.Vector2(direction)
        self.speed = speed

    def getPos(self) -> pygame.Vector2:
        return self.pos

    def getSize(self) -> int:
        return self.size

    def getDirection(self) -> pygame.Vector2:
        return self.direction

    def setDirection(self, direcition: pygame.Vector2):
        self.direction = direcition

    def setSize(self, size: int):
        self.size = size

    def setPos(self, pos: pygame.Vector2):
        self.pos = pos

    def addToPos(self, pos: pygame.Vector2):
        self.pos += pos

    def getSpeed(self) -> float:
        return self.speed

    def setSpeed(self, speed: float):
        self.speed = speed

    def borderCheck(self) -> bool:
        if self.pos.x < self.size:
            return True
        if self.pos.x > WIDTH - self.size:
            return True
        if self.pos.y < self.size:
            return True
        if self.pos.y > HEIGHT - self.size:
            return True

        return False


class PlayerEntity:
    """Any entity that can spawn projectiles and move"""

    def __init__(self, pos: pygame.Vector2, size: int):
        self.pos = pygame.Vector2(pos)
        self.projectiles: pygame.Vector2 = []
        self.size = size

    def update(self):
        # Draw projectile and update position
        for proj in self.projectiles:
            proj.addToPos(proj.getDirection() * proj.getSpeed())
            pygame.draw.circle(screen, LIGHTGREY, proj.getPos(), proj.getSize())
            if proj.borderCheck():
                self.projectiles.remove(proj)

        # Draw player
        pygame.draw.circle(screen, GREEN2, self.pos, self.size)

        # Draw cursor
        pygame.draw.circle(screen, RED2, pygame.mouse.get_pos(), 5)

    def spawnProjectile(
        self, pos: pygame.Vector2, size: int, direction: pygame.Vector2, speed: float
    ):
        self.projectiles.append(Projectile(pos, size, direction, speed))

    def move(self, moveAmount: pygame.Vector2):
        self.pos += moveAmount


class Enemy(Projectile):
    pass


def main():
    """Main function containing the game loop"""

    player = PlayerEntity((WIDTH // 4, HEIGHT // 4), 10)

    getTicksLastFrame = 0
    fullAuto = True

    enemies: Enemy = []

    running = True
    while running:
        clock.tick(FPS)

        # Calculate deltatime
        t = pygame.time.get_ticks()
        deltaTime = (t - getTicksLastFrame) / 1000.0
        getTicksLastFrame = t

        # Spawn enemies (after two frames for deltatime to sort itself out)
        if pygame.time.get_ticks() > 1000:
            if len(enemies) < 5:
                size = random.randint(5, 20)
                enemy = Enemy(
                    (
                        random.randint(size, WIDTH - size),
                        random.randint(size, HEIGHT - size),
                    ),
                    size,
                    (0, 1),
                    0,
                )
                enemy.setSpeed(80 * deltaTime)
                enemies.append(enemy)

        # Main event listening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Single fire
                if pygame.mouse.get_pressed()[0]:
                    mousePos = pygame.Vector2(pygame.mouse.get_pos())
                    player.spawnProjectile(
                        player.pos,
                        player.size // 5,
                        -pygame.Vector2(player.pos - mousePos).normalize(),
                        800 * deltaTime,
                    )
            if event.type == pygame.KEYDOWN:
                # Quit game
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()

        # Controls for player
        if keys[pygame.K_a]:
            player.move(pygame.Vector2(-160, 0) * deltaTime)
        if keys[pygame.K_d]:
            player.move(pygame.Vector2(160, 0) * deltaTime)
        if keys[pygame.K_w]:
            player.move(pygame.Vector2(0, -160) * deltaTime)
        if keys[pygame.K_s]:
            player.move(pygame.Vector2(0, 160) * deltaTime)

        # Full auto fire
        if fullAuto:
            if pygame.mouse.get_pressed()[0]:
                mousePos = pygame.Vector2(pygame.mouse.get_pos())
                player.spawnProjectile(
                    player.pos,
                    player.size // 5,
                    -pygame.Vector2(player.pos - mousePos).normalize(),
                    800 * deltaTime,
                )

        # Reset display
        screen.fill(NORD1)

        # Draw player
        player.update()

        # Draw enemy
        for enemy in enemies:

            # Move enemy
            enemy.addToPos(enemy.getDirection() * enemy.getSpeed())
            pygame.draw.circle(screen, LIGHTBLUE, enemy.getPos(), enemy.getSize())

            # Check borders
            if enemy.borderCheck():
                enemy.setDirection(enemy.getDirection() * -1)

        # Update display
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
