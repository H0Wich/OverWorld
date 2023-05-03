from typing import Optional, Union
import pygame as pg


class SpriteImage:
    def __init__(self, _filename: str):

        self.image_filename = pg.image.load(_filename).convert()


    def get_image(
        self, _x: int,
        _y: int,
        _width: int,
        _height: int,
        _resize: Optional[Union[int, float]] = None
        ) -> pg.Surface:

        image = pg.Surface((_width, _height))
        image.blit(self.image_filename, (0, 0), (_x, _y, _width, _height))

        if _resize:
            image_size = image.get_size()
            image = pg.transform.scale(image, (image_size[0] * _resize, image_size[1] * 1.5))

        return image
