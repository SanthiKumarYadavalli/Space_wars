import pygame
from pygame.locals import *
from random import choice, randint
from sys import exit
import settings


class Variables:
    def __init__(self):
        self.bullet_fired = False
        self.score = 0
        self.bullets_missed = 0
        self.start_game = False
        self.play_once = 0


var = Variables()


# Main Functions
def check_events(ship, bullet, bullet_sounds):
    """Checks Keyboard Events"""
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if bullet.y == 610:
                    bullet_sound = pygame.mixer.Sound(choice(bullet_sounds))
                    bullet_sound.play()
                var.bullet_fired = True
    keys = pygame.key.get_pressed()

    if keys[K_RIGHT]:
        if ship.right < 1280:
            ship.centerx += settings.ship_speed
            if not var.bullet_fired:
                bullet.x += settings.ship_speed

    elif keys[K_LEFT]:
        if ship.left > 0:
            ship.centerx -= settings.ship_speed
            if not var.bullet_fired:
                bullet.x -= settings.ship_speed


def create_aliens():
    alien_list = [pygame.image.load('Images/alien.png')] * settings.alien_number
    alien_rect_list = []
    for a in range(len(alien_list)):
        alien_rect = alien_list[a].get_rect()
        alien_rect.center = (randint(100, 1200), randint(150, 350))
        alien_rect_list.append(alien_rect)

    alien_speed_list = [settings.alien_speed] * settings.alien_number
    alien_drop_speed_list = [settings.alien_drop] * settings.alien_number

    return alien_list, alien_rect_list, alien_speed_list, alien_drop_speed_list


def alien_movement(aliens, rects, speeds, drop_speeds, screen):
    for i in range(settings.alien_number):
        screen.blit(aliens[i], rects[i])
        rects[i].x += speeds[i]
        if rects[i].x > 1210:
            speeds[i] = -speeds[i]
            rects[i].y += drop_speeds[i]
        elif rects[i].x < 0:
            speeds[i] *= -1
            rects[i].y += drop_speeds[i]


def bullet_movement(bullet, speed, ship):
    if var.bullet_fired:
        bullet.y -= speed
    if bullet.bottom < 0 or not var.bullet_fired:
        bullet.x = ship.x + 52
        bullet.y = 610
        var.bullet_fired = False
    if bullet.y < 0:
        var.bullets_missed += 1
        pygame.mixer.Sound("Sounds/error.wav").play()


def collision(bullet, alien):
    for i in range(settings.alien_number):
        if bullet.colliderect(alien[i]):
            var.bullet_fired = False
            pygame.mixer.Sound('Sounds/killed.wav').play()
            var.score += 1
            alien[i].center = (randint(100, 1200), randint(150, 350))


# Game Over
def game_over_text(screen, screen_rect, high_score, name):
    # Play Game Over Sound
    if var.play_once == 0 or var.play_once == 1:
        pygame.mixer.Sound("Sounds/gameover.wav").play()
        var.play_once = 2

    # Write High score in the file
    if var.play_once == 2:
        if var.score > int(high_score):
            with open('high_score.txt', 'w') as f:
                f.write(f"{name}, {var.score}")
            var.play_once = 3

    # Showing GameOver text
    font = pygame.font.SysFont("chalkduster", 100)
    text = font.render("GAME OVER", True, (255, 255, 0))
    rect = text.get_rect()
    rect.center = screen_rect.center
    screen.blit(text, rect)

    # showing 'new high score' if it is new high score
    high_score_font = pygame.font.SysFont("couriernew", 50)
    high_score_text = high_score_font.render("New High score!", True, (0, 255, 255))
    h_rect = high_score_text.get_rect()
    h_rect.centerx = rect.centerx
    h_rect.centery = rect.centery + 150
    if var.score > int(high_score):
        screen.blit(high_score_text, h_rect)


def show_how(the_text, screen, screen_rect):
    """Shows how the game ends on the screen"""
    font = pygame.font.SysFont("chalkboard", 32)
    text = font.render(the_text, True, (200, 20, 20))
    rect = text.get_rect()
    rect.midtop = screen_rect.midtop
    rect.y = screen_rect.y + 50
    screen.blit(text, rect)


def checking_game_over(aliens, ship, bullet, screen, screen_rect, high_score, name):
    """Checks if the game ends"""
    for i in range(settings.alien_number):  # if alien crashes ship
        if aliens[i].colliderect(ship) or aliens[i].bottom > 700:
            # Hiding ship, bullet and aliens
            ship.y = 2000
            bullet.y = 2000
            for x in range(settings.alien_number):
                aliens[x].y = 1000
            # Playing sound
            if var.play_once == 0:
                pygame.mixer.Sound('Sounds/explosion.wav').play()
                var.play_once = 1

            show_how('Your ship crashed!', screen, screen_rect)  # shows how
            game_over_text(screen, screen_rect, high_score, name)  # shows 'game over'

    if var.bullets_missed == settings.bullets_limit:  # if bullet limit reaches
        ship.y = 2000
        bullet.y = 2000
        for i in range(settings.alien_number):
            aliens[i].y = -100
        show_how("Missed Bullets limit reached!", screen, screen_rect)  # shows how
        game_over_text(screen, screen_rect, high_score, name)  # shows 'game over'


# show stats
def show_stats(screen, screen_rect, high_score, high_scorer):
    font1 = pygame.font.SysFont("comicsansms", 32)
    font2 = pygame.font.SysFont("comicsansms", 20)
    font3 = pygame.font.SysFont("comicsansms", 23)

    score_text = font1.render("Score: " + str(var.score), True, (255, 255, 255))
    high_score_text = font1.render("High score: " + str(high_score), True, (255, 255, 255))
    name_text = font2.render(f'By {high_scorer}', True, (255, 255, 255))
    bullets_text = font3.render(f"Bullets Missed: {var.bullets_missed} / {settings.bullets_limit}", True,
                                (255, 255, 255))

    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (1000, 10))
    screen.blit(name_text, (1000, 55))
    rect = bullets_text.get_rect()
    rect.midtop = screen_rect.midtop
    rect.y = screen_rect.y + 10
    screen.blit(bullets_text, rect)


def play_button(screen, screen_rect):
    font = pygame.font.SysFont("couriernew", 40)
    play_text = font.render("PLAY", True, (255, 255, 255), (0, 200, 0))
    rect = play_text.get_rect()
    rect.center = screen_rect.center
    if not var.start_game:
        screen.blit(play_text, rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    var.start_game = True
                    return True
    if var.start_game:
        return True
