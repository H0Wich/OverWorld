import random

import pygame as pg

from coin import Coin
from settings import *


class Platform(pg.sprite.Sprite):
    def __init__(self, _game, _x: int, _y: int, _size: int) -> None:

        self._layer = PLATFORM_LAYER
        self.groups = _game.all_sprites, _game.platforms

        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = _game

        self.image = self.get_platform_image(_size)

        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y

        if random.randrange(100) < COIN_SPAWN_CHANCE:
            Coin(self.game, self)


    def get_platform_image(self, _size: int) -> pg.Surface:

        if 3 <= _size <= PLATFORM_MAX_SECTIONS:
            platform = pg.image.load(os.path.join(f'sprites\\blocks\\{_size}_platform.png')).convert()
            platform.set_colorkey(WHITE)

            return platform

        raise Exception(f"Platform size must be between 3 and { PLATFORM_MAX_SECTIONS }")
