import pygame
import random

#FOOD
class Food:
    def __init__(self, width, height, size):
        self.width = width
        self.height = height
        self.size = size

        self.images = [
            pygame.transform.scale(pygame.image.load("apple.jpeg"), (size, size)),
            pygame.transform.scale(pygame.image.load("durian.png"), (size, size)),
             pygame.transform.scale(pygame.image.load("banana.png"), (size, size))
        ]

        self.spawn()

    def spawn(self):
        self.x = random.randrange(0, self.width, self.size)
        self.y = random.randrange(0, self.height, self.size)

        # pilih gambar buah secara acak
        self.image = random.choice(self.images)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

#INIT GAME
pygame.init()
minion__img = pygame.image.load("minion.png")
minion__img = pygame.transform.scale(minion__img, (20, 20))
W = 400
screen = pygame.display.set_mode((W, W))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

#FONT & GAMBAR GAME OVER
font = pygame.font.SysFont(None, 36)
game_over_img = pygame.image.load("GameOverminion.png")
game_over_img = pygame.transform.scale(game_over_img, (250, 120))

# TOMBOL RESPWAN
button_Width = 160
button_height = 50
button_rect = pygame.Rect((W//2 - button_Width//2, W//2 + 60), (button_Width, button_height))

#VARIABEL GAME
snake = [(200, 200)]
direction = (20, 0)
food = Food(W, W, 20)
score = 0
game_over = False
running = True

#LOOP GAME
while running:
    clock.tick(5)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #KONTROL SNAKE
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 20):
                direction = (0, -20)
            if event.key == pygame.K_DOWN and direction != (0, -20):
                direction = (0, 20)
            if event.key == pygame.K_LEFT and direction != (20, 0):
                direction = (-20, 0)
            if event.key == pygame.K_RIGHT and direction != (-20, 0):
                direction = (20, 0)

        
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                snake = [(200, 200)]
                direction = (20, 0)
                score = 0
                food.spawn()
                game_over = False

    #UPDATE POSISI SNAKE
    if not game_over:
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, head)

        #CEK MAKAN ATAU GA
        if head == (food.x, food.y):
            score += 1
            food.spawn()
        else:
            snake.pop()

        #CEK MATI (NABRAK DINDING ATAU BADAN)
        if (
            head[0] < 0 or head[0] >= W or
            head[1] < 0 or head[1] >= W or
            head in snake[1:]
        ):
            game_over = True

    screen.fill((20, 20, 20))

    for s in snake:
        screen.blit(minion__img, s)

    food.draw(screen) #GAMBAR APEL

    #GAMBAR GAME OVER DAN TOMBOL RESPWAN
    if game_over:
        screen.blit(game_over_img, (75, 140))

        pygame.draw.rect(screen, (200, 200, 200), button_rect)
        text = font.render("Respawn", True, (0, 0, 0))
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
