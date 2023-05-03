import os

import pygame as pg

from settings import *


class Coin(pg.sprite.Sprite):
    def __init__(self, _game, _platform):

        self._layer = COIN_LAYER
        self.groups = _game.all_sprites, _game.coins

        pg.sprite.Sprite.__init__(self, self.groups)

        self.game = _game
        self.platform = _platform

        self.load_animation_frames()

        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.platform.rect.centerx
        self.rect.bottom = self.platform.rect.top - 5

        self.animation_start = pg.time.get_ticks()
        self.animation_tick = 75


    def update(self):

        self.animate()

        if not self.game.platforms.has(self.platform):
            self.kill()


    def animate(self) -> None:

        now = pg.time.get_ticks()

        self.image = self.animation_frames[
            (
                (now - self.animation_start) // self.animation_tick
            ) % len(
                self.animation_frames
            )
        ]


    def load_animation_frames(self) -> None:

        self.animation_frames = []
        for i in range(0, 15):
            self.animation_frames.append(
                pg.image.load(os.path.join(f'.\\sprites\\coin\\tile' + str(i).rjust(3, '0') +'.png')).convert()
            )
