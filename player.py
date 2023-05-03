import pygame as pg

from settings import *
from spriteimage import SpriteImage


vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, _game) -> None:

        self._layer = PLAYER_LAYER
        self.groups = _game.all_sprites

        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = _game

        self.load_animation_frames()

        self.direction = 'Right'
        self.image = self.idleing_frames[self.direction][0]
        self.rect = self.image.get_rect()

        self.position = vec(WIDTH // 2, HEIGHT // 2)
        self.rect.center = self.position

        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

        self.idleing = True
        self.running = False
        self.jumping = False

        self.animation_start = pg.time.get_ticks()
        self.load_animation_frames()


    def jump_short(self):

        if self.jumping:
            if self.velocity.y < -7:
                self.velocity.y = -7


    def jump(self):

        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, dokill=False)
        self.rect.x -= 1

        if hits and not self.jumping:
            self.idleing = False
            self.running = False
            self.jumping = True

            self.animation_start = pg.time.get_ticks()

            self.velocity.y = -PLAYER_JUMP

            self.game.jump_sound.play()
            self.game.jump_sound.set_volume(0.1)


    def update(self) -> None:

        self.acceleration = vec(0, PLAYER_GRAVITY_CONSTANT)
        pressed_keys = pg.key.get_pressed()

        diff_x = 0
        if pressed_keys[pg.K_d] or pressed_keys[pg.K_RIGHT]:
            diff_x += PLAYER_ACCELERATION
        if pressed_keys[pg.K_a] or pressed_keys[pg.K_LEFT]:
            diff_x -= PLAYER_ACCELERATION

        self.acceleration.x = diff_x

        self.acceleration.x += self.velocity.x * PLAYER_FRICTION

        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        self.set_states()
        self.animate()

        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0

        self.rect.midbottom = self.position

        if self.rect.left > WIDTH:
            self.position.x = 0 - self.rect.width // 2
        if self.rect.right < 0:
            self.position.x = WIDTH + self.rect.width // 2


    def set_states(self) -> None:

        if self.jumping:
            self.idleing = False
            self.running = False
            self.jumping = True

            if self.velocity.x > 0:
                self.direction = 'Right'
            elif self.velocity.x < 0:
                self.direction = 'Left'

        elif self.velocity.x == 0:
            self.idleing = True
            self.running = False
            self.jumping = False

        elif self.velocity.x > 0:
            self.idleing = False
            self.running = True
            self.jumping = False

            self.direction = 'Right'

        elif self.velocity.x < 0:
            self.idleing = False
            self.running = True
            self.jumping = False

            self.direction = 'Left'

        else:
            raise Exception('No state activated.')


    def animate(self) -> None:

        def set_frame(_animation_frames: dict) -> None:
            now = pg.time.get_ticks()

            self.image = _animation_frames[self.direction][
                (
                    (now - self.animation_start) // _animation_frames['animation_tick']
                ) % len(
                    _animation_frames[self.direction]
                )
            ]

        if self.idleing:
            set_frame(self.idleing_frames)

        elif self.running:
            set_frame(self.running_frames)

        elif self.jumping:
            now = pg.time.get_ticks()
            animation_frames = self.jumping_frames

            ticks = (now - self.animation_start) // animation_frames['animation_tick']

            if (ticks) // len(animation_frames[self.direction]) >= 1:
                self.image = animation_frames[self.direction][-1]

            else:
                self.image = animation_frames[self.direction][(ticks) % len(
                        animation_frames[self.direction]
                    )
                ]

        else:
            raise Exception('No state activated.')

        self.mask = pg.mask.from_surface(self.image)


    def load_animation_frames(self) -> None:

        self.idleing_frames = {'Right': [], 'Left': [], 'animation_tick': 300}
        for i in range(2):
            image = SpriteImage(
                    os.path.join(f'.\\sprites\\player\\adventurer-idle-0{ i }.png')
                ).get_image(10, 0, 29, 37, _resize=1.5)
            image.set_colorkey(BLACK)

            self.idleing_frames['Right'].append(image)
            self.idleing_frames['Left'].append(pg.transform.flip(image, True, False))

        self.running_frames = {'Right': [], 'Left': [], 'animation_tick': 85}
        for i in range(6):
            image = SpriteImage(
                    os.path.join(f'.\\sprites\\player\\adventurer-run-0{ i }.png')
                ).get_image(10, 0, 29, 37, _resize=1.5)
            image.set_colorkey(BLACK)

            self.running_frames['Right'].append(image)
            self.running_frames['Left'].append(pg.transform.flip(image, True, False))

        self.jumping_frames = {'Right': [], 'Left': [], 'animation_tick': 60}
        for i in range(4):
            image = SpriteImage(
                    os.path.join(f'.\\sprites\\player\\adventurer-jump-0{ i }.png')
                ).get_image(10, 0, 29, 37, _resize=1.5)
            image.set_colorkey(BLACK)

            self.jumping_frames['Right'].append(image)
            self.jumping_frames['Left'].append(pg.transform.flip(image, True, False))
