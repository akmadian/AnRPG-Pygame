# -*- coding: utf-8 -*-
"""
    File Name: main.py
    Author: Ari Madian
    Created: July 23, 2017 2:02 PM
    Python Version: 3.6
"""

import pygame
import sys
import os
import time

# Game Resources
import classes
import inputbox
from colors_file import Color


#TODO: Blit a portion of an image so all related sprites can be in one image
#TODO: Projectiles with asyncio
#TODO: Config file implementation?

x = pygame.init()
player = classes.Player
player.pos_x = 100
player.pos_y =100

base_path = os.path.os.path.dirname(os.path.realpath(sys.argv[0]))
textures_base_path = base_path + '/Textures/'
fonts_path = base_path + '/Fonts/'
projectile_path = textures_base_path + '/projectiles'
projectile_fire_path = textures_base_path + '/Projectiles/Fire'

fps_font = pygame.font.Font(fonts_path + 'roboto/Roboto-Light.ttf', 20)
home = textures_base_path + 'Built-Textures/home_area_fixed.png'
player_sprite = textures_base_path + '/player_sprite.png'
player_sprite_reversed = textures_base_path + '/player_sprite_reversed.png'

window_width = 1200
window_height = 800
window_title = 'RPG Game'
pygame.display.set_caption(window_title)
game_display = pygame.display.set_mode((window_width, window_height),
                                       pygame.HWSURFACE)
keys_down = {'w': None, 'a': None, 's': None, 'd': None}
active_projectiles = []
player_facing = None



def title_screen():
    player.player_name = inputbox.ask(game_display, "Player Name")
    print(player.player_name)
    background = textures_base_path + '/title_screen.jpg'
    font_size = 0
    frames = 0
    enter_game = False
    while not enter_game:
        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                quit()
            elif event_.type == pygame.KEYDOWN:
                if event_.key == pygame.K_KP_ENTER or pygame.K_SPACE:
                    enter_game = True
            # print(event_)

        game_display.blit(pygame.image.load(background), (0, 0))
        font = pygame.font.Font(fonts_path + 'roboto/Roboto-Light.ttf', font_size)
        game_display.blit(font.render(str('An RPG'), True, Color.Goldenrod), (500, 111))
        game_display.blit(font.render(str(frames), True, Color.Goldenrod), (0, 0))

        if font_size < 65: font_size += 1
        if font_size == 65:
            game_display.blit(font.render(str('Press Enter To Play'), True, Color.Goldenrod), (345, 400))

        pygame.display.update()
        frames += 1
        time.sleep(0.01666667)


def projectile_rotation(origin, mousepos):
    """Calculates the rotation of a projectile object
    I'll probably make this based on math stuff at some point

    :param origin: Expects dict with the character postion at
                    the time of projectile creation
    :param mousepos: Expects dict with the mouse position at
                     the time of projectile creation
    :return: Degree rotation
    """
    # Vertical/ Horizontal Angles
    if origin['y'] == mousepos['y']:
        if origin['x'] < mousepos['x']: return '0'
        if origin['x'] > mousepos['x']: return '180'
    if origin['x'] == mousepos['x']:
        if origin['y'] < mousepos['y']: return '270'
        if origin['y'] > mousepos['y']: return '90'

    # Diagonal Angles
    if origin['x'] < mousepos['x']: # If mouse is to the right of player
        if origin['y'] < mousepos['y']: return '315'
        if origin['y'] > mousepos['y']: return '45'
    if origin['x'] > mousepos['x']: # If mouse is to the left of player
        if origin['y'] < mousepos['y']: return '225'
        if origin['y'] > mousepos['y']: return '135'


title_screen()
gameExit = False
while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

        ## Character Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w: keys_down['w'] = True
            elif event.key == pygame.K_a: keys_down['a'] = True
            elif event.key == pygame.K_s: keys_down['s'] = True
            elif event.key == pygame.K_d: keys_down['d'] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w: keys_down['w'] = False
            elif event.key == pygame.K_a: keys_down['a'] = False
            elif event.key == pygame.K_s: keys_down['s'] = False
            elif event.key == pygame.K_d: keys_down['d'] = False

        ## Projectiles and Targeting
        # Making the projectile
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(dict(zip(('x', 'y'), (player.pos_x, player.pos_y))))
            print(dict(zip(('x', 'y'), event.pos)))
            projectile = classes.Projectile(dict(zip(('x', 'y'), (player.pos_x, player.pos_y))),
                                            dict(zip(('x', 'y'), event.pos)))
            projectile.roation = projectile_rotation(projectile.origin, projectile.mousepos)
            projectile.imagename = '/projectile_fire_' + projectile.roation + '.png'
            active_projectiles.append(projectile)

        # Player Facing
        if event.type == pygame.MOUSEMOTION:
            if event.pos[0] > player.pos_x: player_facing = 'right'
            else: player_facing = 'left'

    ## Executing Movement
    if keys_down['w']: player.pos_y -= 5
    if keys_down['s']: player.pos_y += 5
    if keys_down['a']: player.pos_x -= 5
    if keys_down['d']: player.pos_x += 5

    ## Rendering
    fps_overlay = fps_font.render((str(player.pos_x) + ', ' + str(player.pos_y)), True, Color.Goldenrod)
    game_display.blit(pygame.image.load(home), (0,0))
    game_display.blit(fps_overlay, (0,0))

    if player_facing == 'right':
        game_display.blit(pygame.image.load(player_sprite), (player.pos_x, player.pos_y))
    elif player_facing == 'left':
        game_display.blit(pygame.image.load(player_sprite_reversed), (player.pos_x, player.pos_y))

    if len(active_projectiles) != 0:
        for projectile in active_projectiles:
            game_display.blit(pygame.image.load(projectile_fire_path + projectile.imagename),
                              (projectile.mousepos['x'], projectile.mousepos['y']))

    pygame.display.update()
    time.sleep(0.01666667)


pygame.quit()
quit()