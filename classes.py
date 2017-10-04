# -*- coding: utf-8 -*-
"""
    File Name: classes.py
    Author: Ari Madian
    Created: October 1, 2017 5:17 PM
    Python Version: 3.6
"""
import sys
import os

class Player:
    """The player class"""

    def __init__(self):
        self.player_name = None
        self.obj_type = 'player'
        self.health = 100
        self.attack = 30
        self.pos_x = 100
        self.pos_y = 100

class Projectile:

    def __init__(self, origin, mousepos):
        self.origin = origin
        self.mousepos = mousepos
        self.roation = None
        self.imagename = None

class Enemy_Grunt:
    """The basic Enemy Type"""

    def __init__(self, enemy_name):
        self.boss_name = enemy_name
        self.obj_type = 'enemy'
        self.sprite_type = 'enemy_grunt'
        self.health = 75
        self.attack = 15


class Enemy_Boss:
    """The enemy boss type"""

    def __init__(self, enemy_name):
        self.boss_name = enemy_name
        self.obj_type = 'enemy'
        self.sprite_type = 'enemy_boss'
        self.health = 500
        self.attack = 20

