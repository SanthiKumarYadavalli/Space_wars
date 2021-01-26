import pygame
import game_functions as funcs
import settings

name = input("Enter your name: ").title()
print(f'\nHello {name}!\nWelcome to Space Wars!\n')
print("CONTROLS:\n\tRight and Left keys -> Ship movement\n\tSpace -> Fire Bullet\n")
print(f'Good Luck {name}!\n')
print("Press 'Enter' to start!")
input()

pygame.init()

screen = pygame.display.set_mode((1280, 700), 0, 32)  # Setting Screen
screen_rect = screen.get_rect()
icon = pygame.image.load('Images/icon.png')  # Icon
space = pygame.image.load('Images/space.jpg')  # Background
ship = pygame.image.load('Images/ship.png')  # Ship
pygame.display.set_caption("Space Wars")  # Title
pygame.display.set_icon(icon)  # Setting Icon

start_game = False

# SHIP
ship_rect = ship.get_rect()
ship_rect.midbottom = screen_rect.midbottom

# Bullet
bullet_rect = pygame.Rect(ship_rect.x + 52, 610, settings.bullet_width, settings.bullet_height)
bullet_sounds = ["Sounds/laser_1.wav",
                 "Sounds/laser_2.wav",
                 "Sounds/laser_3.wav"]

# Aliens
alien_list, alien_rect_list, alien_speed_list, alien_drop_speed_list = funcs.create_aliens()

# HIGH SCORES
try:
    with open('high_score.txt', 'r') as file:
        the_high_score = file.readlines()[-1]
        high_scorer, high_score = the_high_score.strip().split(', ')
except FileNotFoundError:
    high_scorer, high_score = 'Computer', 0

while True:
    screen.blit(space, (0, 0))
    start_game = funcs.play_button(screen, screen_rect)
    if start_game:
        funcs.check_events(ship_rect, bullet_rect, bullet_sounds)
        funcs.bullet_movement(bullet_rect, settings.bullet_speed, ship_rect)
        funcs.collision(bullet_rect, alien_rect_list)
        funcs.alien_movement(alien_list, alien_rect_list, alien_speed_list, alien_drop_speed_list, screen)
        funcs.show_stats(screen, screen_rect, high_score, high_scorer)
        pygame.draw.rect(screen, (255, 0, 0), bullet_rect)
        screen.blit(ship, ship_rect)
        funcs.checking_game_over(alien_rect_list, ship_rect, bullet_rect, screen, screen_rect, high_score, name)
    pygame.display.flip()
