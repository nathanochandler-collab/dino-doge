
import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Arcade")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 28)

MENU = "menu"
DINO = "dino"
FLAPPY = "flappy"


class DinoGame:
    def __init__(self):
        self.player = pygame.Rect(100, 300, 40, 40)
        self.vel_y = 0
        self.gravity = 1
        self.jump_power = -15
        self.ground = 300
        self.obstacles = []
        self.timer = 0
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.player.bottom >= self.ground:
            self.vel_y = self.jump_power

        self.vel_y += self.gravity
        self.player.y += self.vel_y

        if self.player.bottom > self.ground:
            self.player.bottom = self.ground
            self.vel_y = 0

        self.timer += 1
        if self.timer > 90:
            self.timer = 0
            self.obstacles.append(pygame.Rect(WIDTH, 280, 30, 50))

        for o in self.obstacles:
            o.x -= 6

        self.obstacles = [o for o in self.obstacles if o.x > -50]

        for o in self.obstacles:
            if self.player.colliderect(o):
                return MENU

        self.score += 1
        return DINO

    def draw(self):
        screen.fill((240, 240, 240))
        pygame.draw.rect(screen, (0, 0, 0), self.player)
        for o in self.obstacles:
            pygame.draw.rect(screen, (200, 0, 0), o)
        screen.blit(FONT.render(f"Score: {self.score}", True, (0,0,0)), (10,10))


class FlappyGame:
    def __init__(self):
        self.bird = pygame.Rect(100, 200, 30, 30)
        self.vel = 0
        self.gravity = 0.6
        self.flap = -10
        self.pipes = []
        self.timer = 0
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.vel = self.flap

        self.vel += self.gravity
        self.bird.y += self.vel

        self.timer += 1
        if self.timer > 100:
            self.timer = 0
            gap = random.randint(100, 250)
            self.pipes.append({
                "x": WIDTH,
                "top": pygame.Rect(WIDTH, 0, 60, gap),
                "bottom": pygame.Rect(WIDTH, gap + 120, 60, HEIGHT)
            })

        for p in self.pipes:
            p["x"] -= 5
            p["top"].x = p["x"]
            p["bottom"].x = p["x"]

        self.pipes = [p for p in self.pipes if p["x"] > -60]

        for p in self.pipes:
            if self.bird.colliderect(p["top"]) or self.bird.colliderect(p["bottom"]):
                return MENU

        if self.bird.top < 0 or self.bird.bottom > HEIGHT:
            return MENU

        self.score += 1
        return FLAPPY

    def draw(self):
        screen.fill((135, 206, 235))
        pygame.draw.rect(screen, (255, 255, 0), self.bird)
        for p in self.pipes:
            pygame.draw.rect(screen, (0, 200, 0), p["top"])
            pygame.draw.rect(screen, (0, 200, 0), p["bottom"])
        screen.blit(FONT.render(f"Score: {self.score}", True, (0,0,0)), (10,10))


def draw_menu():
    screen.fill((30, 30, 30))
    title = FONT.render("Mini Arcade", True, (255,255,255))
    screen.blit(title, (320, 50))

    dino_btn = pygame.Rect(300, 150, 200, 50)
    flappy_btn = pygame.Rect(300, 250, 200, 50)

    pygame.draw.rect(screen, (70,130,180), dino_btn)
    pygame.draw.rect(screen, (34,139,34), flappy_btn)

    screen.blit(FONT.render("Dino", True, (255,255,255)), (370,160))
    screen.blit(FONT.render("Flappy", True, (255,255,255)), (360,260))

    return dino_btn, flappy_btn


def main():
    state = MENU
    dino = DinoGame()
    flappy = FlappyGame()

    while True:
        clock.tick(60)

        dino_btn, flappy_btn = draw_menu() if state == MENU else (None, None)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == MENU and event.type == pygame.MOUSEBUTTONDOWN:
                if dino_btn.collidepoint(event.pos):
                    dino = DinoGame()
                    state = DINO
                if flappy_btn.collidepoint(event.pos):
                    flappy = FlappyGame()
                    state = FLAPPY

        if state == DINO:
            state = dino.update()
            dino.draw()

        elif state == FLAPPY:
            state = flappy.update()
            flappy.draw()

        pygame.display.update()


if __name__ == "__main__":
    main()
