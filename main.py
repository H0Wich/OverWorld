import random
from typing import Optional

import pygame as pg

from bat import Bat
from platfofm import Platform
from player import Player
from settings import *
from spriteimage import SpriteImage

from pypresence import Presence
import time

client_id = ""

try:
    RPC = Presence(client_id)
    RPC.connect()
    RPC.update(
        state="For OverWorld | By HoWich",
        large_image="icon"
    )
except:
    pass    

class Game:
    def __init__(self) -> None:

        self.running = True

        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        pg.display.set_icon(pg.image.load("icon.png"))
        self.clock = pg.time.Clock()

        self.load_data()


    def load_data(self) -> None:

        self.game_dir = os.path.dirname(__file__)

        self.sprites_dir = os.path.join(self.game_dir, 'sprites')
        self.sounr_dir = os.path.join(self.game_dir, 'sounds')
        self.font_dir = os.path.join(self.game_dir, 'fonts')
        self.highscore = 0

        self.start_game_sound = pg.mixer.Sound(os.path.join('./sounds/game-start.wav'))
        self.jump_sound = pg.mixer.Sound(os.path.join('./sounds/jump.wav'))
        self.collect_coin_sound = pg.mixer.Sound(os.path.join('./sounds/collectcoin.wav'))

        self.background = SpriteImage(
            os.path.join('./sprites/background/background.png')
        ).get_image(320, 0, WIDTH, HEIGHT)
        self.background_rect = self.background.get_rect()

        self.dim = pg.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.dim.fill((0, 0, 0, 180))


    def new(self) -> None:

        self.collected_coins = 0
        self.mob_timer = 0

        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.bats = pg.sprite.Group()
        self.warning_signs = pg.sprite.Group()

        self.player = Player(self)

        for plat in PLATFORM_START_LIST:
            Platform(self, *plat)

        pg.mixer.music.load(os.path.join('./sounds/main.wav'))

        self.run()


    def run(self) -> None:

        pg.mixer.music.play(loops=-1)

        self.playing = True
        self.paused = False

        self.hardness = HARDNESS
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            if not self.paused:
                self.update()
            self.draw()

        pg.mixer.music.fadeout(500)


    def update(self) -> None:

        self.all_sprites.update()

        now = pg.time.get_ticks()
        if now - self.mob_timer > MOB_SPAWN_FREQUENCY - (500 * self.hardness) + random.choice([
            -1000 + 200 * self.hardness,
            1000 - 200 * self.hardness,
            500 - 200 * self.hardness,
            -500 + 200 * self.hardness,
            0]):
            self.mob_timer = now

            Bat(self)


        mob_hits = pg.sprite.spritecollide(self.player, self.bats, False, pg.sprite.collide_mask)
        if mob_hits:
            self.playing = False

        if self.player.velocity.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, dokill=False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit

                if self.player.position.x > lowest.rect.left + 2 and \
                   self.player.position.x < lowest.rect.right - 2:
                    if self.player.position.y < lowest.rect.bottom:
                        self.player.position.y = lowest.rect.top
                        self.player.velocity.y = 0

                        self.player.jumping = False

        if self.player.rect.top <= HEIGHT / 4:
            self.player.position.y += abs(self.player.velocity.y)

            for mob in self.bats:
                mob.rect.y += abs(self.player.velocity.y)

            for coin in self.coins:
                coin.rect.y += abs(self.player.velocity.y)

            for warning_sign in self.warning_signs:
                warning_sign.rect.y += abs(self.player.velocity.y)

            for platform in self.platforms:
                platform.rect.y += abs(self.player.velocity.y)

                if platform.rect.top >= HEIGHT:

                    platform_offset = platform.rect.top - HEIGHT

                    new_platform_size = random.randrange(3, PLATFORM_MAX_SECTIONS + 1 - (self.hardness // 2))
                    new_platform_x = random.randrange(
                        0,
                        GRID * GRID_STEP - (new_platform_size * GRID_STEP),
                        GRID_STEP)
                    new_platform_y = random.randrange(
                        platform_offset - 2*GRID_STEP,
                        platform_offset - GRID_STEP,
                        GRID_STEP)

                    Platform(
                        _game = self,
                        _x = new_platform_x,
                        _y = new_platform_y,
                        _size = new_platform_size
                    )

                    platform.kill()

        coins = pg.sprite.spritecollide(self.player, self.coins, dokill=True)
        if coins:
            self.collected_coins += SCORE_PER_COIN
            self.collect_coin_sound.play()

        if self.collected_coins // 100 > self.hardness \
        and not self.collected_coins // 100 > MAX_HARDNESS:
            self.hardness += 1

        if self.player.rect.bottom > HEIGHT:

            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.velocity.y, 10)

                if sprite.rect.bottom < 0:
                    sprite.kill()

            if len(self.platforms) == 0:
                self.playing = False


    def events(self) -> None:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if not self.paused:
                        self.player.jump()

                if event.key == pg.K_ESCAPE:
                    self.paused = not self.paused

                    if self.paused:
                        pg.mixer.music.pause()
                    else:
                        pg.mixer.music.unpause()

            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_short()


    def draw(self) -> None:

        self.screen.blit(self.background, self.background_rect)

        self.all_sprites.draw(self.screen)

        self.draw_text(f'Coins: { str(self.collected_coins) }', 24, WHITE, WIDTH // 2, 15)

        if self.paused:
            self.screen.blit(self.dim, (0, 0))
            overworldlogo = pg.image.load('sprites/overlogo.png')
            overworldlogose = pg.transform.scale(overworldlogo, (50, 50))
            self.screen.blit(overworldlogose, (214, 20))
            self.draw_text('Paused', 48, WHITE, WIDTH // 2, 100)
            self.draw_text(f'Highscore: {self.highscore}', 30, WHITE, WIDTH // 2, 70)
            self.draw_text('Press ESC to continue...', 20, WHITE, WIDTH // 2, HEIGHT -75)

        pg.display.flip()


    def show_splash_screen(self) -> None:
        overworldlogo = pg.image.load('sprites/overlogo.png')
        overworldlogose = pg.transform.scale(overworldlogo, (100, 100))
        pg.mixer.music.load(os.path.join('./sounds/menu.wav'))
        pg.mixer.music.play(loops=-1)

        self.screen.fill(BLACK)
        self.screen.blit(overworldlogose, (190, 30))
        self.draw_text('OVERWORLD', 48, WHITE, WIDTH // 2, 140)
        self.draw_text("Move:    WASD / Arrows", 24, WHITE, WIDTH // 2, HEIGHT // 2 - 10)
        self.draw_text("Jump:           Space         ", 24, WHITE, WIDTH // 2, HEIGHT // 2 + 10)
        self.draw_text(f"Highscore: { self.highscore }", 20, WHITE, WIDTH // 2, HEIGHT - 150)
        self.draw_text("Press any key to continue...", 20, WHITE, WIDTH // 2, HEIGHT - 75)

        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

        self.start_game_sound.play()


    def show_game_over_screen(self) -> None:

        if not self.running:
            return

        pg.mixer.music.load(os.path.join('./sounds/game_over.wav'))
        pg.mixer.music.play(loops=-1)

        overworldlogo = pg.image.load('sprites/overlogo.png')
        overworldlogose = pg.transform.scale(overworldlogo, (100, 100))

        self.screen.fill(BLACK)
        self.screen.blit(overworldlogose, (190, 30))
        self.draw_text("Game over", 48, WHITE, WIDTH // 2, 140)
        self.draw_text(f"You have collected { self.collected_coins } coins!", 24, WHITE, WIDTH // 2, HEIGHT // 2)
        self.draw_text("Press R to respawn...", 20, WHITE, WIDTH // 2, HEIGHT - 100)

        if self.collected_coins > self.highscore:
            self.highscore = self.collected_coins
            self.draw_text("New highscore!", 24, WHITE, WIDTH // 2, HEIGHT // 2 + 40)

            with open(os.path.join(self.game_dir, 'hightscore.txt'), 'w') as f:
                f.write(str(self.highscore))

        pg.display.flip()
        self.wait_for_key(pg.K_r)
        self.start_game_sound.play()

        pg.mixer.music.fadeout(500)


    def wait_for_key(self, _key: Optional[int] = None) -> None:

        waiting = True
        while waiting:
            self.clock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False

                if event.type == pg.KEYDOWN:
                    if _key:
                        keystate = pg.key.get_pressed()
                        if keystate[_key]:
                            waiting = False
                    else:
                        waiting = False


    def draw_text(self, _text: str, _size: int, _color: tuple[int, int, int], _x: int, _y: int) -> None:

        font = pg.font.Font(os.path.join("./fonts/fonts.ttf"), _size)

        text_surface = font.render(_text, True, _color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (_x, _y)

        self.screen.blit(text_surface, text_rect)


game = Game()
game.show_splash_screen()
while game.running:
    game.new()
    game.show_game_over_screen()

pg.quit()
