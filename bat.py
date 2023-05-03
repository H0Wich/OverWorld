import os
import random

import pygame as pg

from settings import *


class Bat(pg.sprite.Sprite):
    def __init__(self, _game):

        self._layer = BAT_LAYER
        self.groups = _game.all_sprites, _game.bats

        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = _game

        self.load_animation_frames()

        self.direction = random.choice(['Right', 'Left'])
        self.image = self.animation_frames[self.direction][0]
        self.rect = self.image.get_rect()

        self.spawn_warning_image = pg.image.load(os.path.join('.\\sprites\\warning.png')).convert()
        self.warn_rect = self.spawn_warning_image.get_rect()

        self.velosity_x = random.randint(2 + self.game.hardness, 4 + self.game.hardness)

        if self.direction == 'Right':
            self.rect.centerx = -100
            self.warn_rect.centerx = 100
        else:
            self.rect.centerx = WIDTH + 100
            self.warn_rect.centerx = WIDTH - 20
            self.velosity_x *= -1

        self.rect.y = random.randrange(HEIGHT // 2)

        self.animation_tick = 100
        self.animation_start = pg.time.get_ticks()

        WarningSign(self.game, self)


    def update(self):

        self.animate()

        self.rect.x += self.velosity_x
        if self.rect.x > WIDTH + 200 or self.rect.x < -200:
            self.kill()


    def animate(self):

        now = pg.time.get_ticks()

        self.image = self.animation_frames[self.direction][
            (
                (now - self.animation_start) // self.animation_tick
            ) % len(
                self.animation_frames[self.direction]
            )
        ]

        self.mask = pg.mask.from_surface(self.image)


    def load_animation_frames(self):

        self.animation_frames = {'Right': [], 'Left': []}
        for i in range(3, 6):
            image = pg.image.load(os.path.join('.\\sprites\\bat\\tile' + str(i).rjust(3, '0') +'.png')).convert()

            self.animation_frames['Right'].append(image)
            self.animation_frames['Left'].append(pg.transform.flip(image, True, False))


class WarningSign(pg.sprite.Sprite):
    def __init__(self, _game, _bat):

        self._layer = WARNING_SIGN_LAYER
        self.groups = _game.all_sprites, _game.warning_signs

        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = _game
        self.bat = _bat

        self.image = pg.image.load(os.path.join('.\\sprites\\warning.png')).convert()
        self.rect = self.image.get_rect()

        if self.bat.direction == 'Right':
            self.rect.centerx = 20
        else:
            self.rect.centerx = WIDTH - 20

        self.rect.centery = self.bat.rect.centery

        self.timer = pg.time.get_ticks()


    def update(self):

        if pg.time.get_ticks() - self.timer > 500:
            self.kill()
