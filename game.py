import pygame
import random


pygame.init()
pygame.mixer.init()  

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ball Avoidance Game")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


player_width = 50
player_height = 50
player_speed = 5


falling_object_width = 50
falling_object_height = 50
falling_object_speed = 5
falling_objects = []


player_img = pygame.image.load('assets/player.png')
player_img = pygame.transform.scale(player_img, (player_width, player_height))

falling_object_img = pygame.image.load('assets/falling_object.png')
falling_object_img = pygame.transform.scale(falling_object_img, (falling_object_width, falling_object_height))

background_img = pygame.image.load('assets/background.png')
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))


pygame.mixer.music.load('assets/background_music.mp3')
pygame.mixer.music.play(-1, 0.0) 


font = pygame.font.SysFont(None, 36)


def display_text(text, color, x, y):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


def display_menu():
    screen.blit(background_img, (0, 0))
    display_text("Welcome to Ball Avoidance Game", BLACK, screen_width // 4, screen_height // 4)
    display_text("Press 'Space' to Start", GREEN, screen_width // 4 + 50, screen_height // 2)
    pygame.display.update()


def game_over_screen(final_score):
    while True:
        screen.blit(background_img, (0, 0))
        display_text("Game Over!", RED, screen_width // 2 - 100, screen_height // 3)
        display_text(f"Your Score: {final_score}", BLACK, screen_width // 2 - 100, screen_height // 3 + 50)
        display_text("Press R to Restart or ESC to Quit", BLACK, screen_width // 2 - 180, screen_height // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False


def game_loop():
    player_x = screen_width // 2 - player_width // 2
    player_y = screen_height - player_height - 10
    falling_objects.clear()
    score = 0
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed

        
        if random.random() < 0.02:
            falling_object_x = random.randint(0, screen_width - falling_object_width)
            falling_objects.append([falling_object_x, -falling_object_height])

        for obj in falling_objects[:]:
            obj[1] += falling_object_speed
            if obj[1] > screen_height:
                falling_objects.remove(obj)
                score += 1

 
        for obj in falling_objects:
            if (player_x < obj[0] + falling_object_width and
                player_x + player_width > obj[0] and
                player_y < obj[1] + falling_object_height and
                player_y + player_height > obj[1]):
                if game_over_screen(score):
                    return game_loop()
                else:
                    return

 
        screen.blit(background_img, (0, 0))
        screen.blit(player_img, (player_x, player_y))
        for obj in falling_objects:
            screen.blit(falling_object_img, (obj[0], obj[1]))
        display_text(f"Score: {score}", BLACK, 10, 10)

        pygame.display.update()
        clock.tick(60)

def main():
    while True:
        display_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()


main()
