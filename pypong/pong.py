"""
This is a simple Pong game using Python and Pygame.
"""


import pygame

from pypong.constants import BLACK
from pypong.constants import WHITE
from pypong.constants import WINDOW_SIZE

from pypong.utils import logger

from pypong.paddle import Paddle
from pypong.ball import Ball


class Pypong:
    """
    This is a simple Pong game using Python and Pygame.
    """

    _logger = logger

    _padde_a = None
    _paddle_b = None
    _ball = None
    _all_sprites_list = None

    _carry_on = True
    _clock = pygame.time.Clock()

    def __init__(self) -> None:

        self._logger.log('Initializing PyPong')

        pygame.init()
        self._logger.log('Pygame initialized')

        self._screen = self._open_window()
        pygame.display.set_caption("PyPong")
        self._logger.log('Window opened')

        self._paddle_a = self._add_paddle('paddle_a', WHITE, 10, 100, 20, 200)
        self._paddle_b = self._add_paddle('paddle_b', WHITE, 10, 100, 670, 200)
        self._ball = self._add_ball(WHITE, 10, 10, 345, 195)
        self._all_sprites_list = self._add_sprites(self._paddle_a, self._paddle_b, self._ball)

    def _open_window(self) -> pygame.Surface:
        """
        Open a window for the game.
        """

        self._logger.log('Opening window')
        return pygame.display.set_mode(WINDOW_SIZE)

    def _add_paddle(self, name: str, color: tuple, width: int, height: int, x: int, y: int) -> Paddle:
        """
        Add a paddle to the game.
        """

        paddle = Paddle(name, color, width, height)
        paddle.rect.x = x
        paddle.rect.y = y

        return paddle

    def _add_ball(self, color: tuple, width: int, height: int, x: int, y: int) -> Ball:
        """
        Add a ball to the game.
        """

        ball = Ball(color, width, height)
        ball.rect.x = x
        ball.rect.y = y

        return ball

    def _add_sprites(self, *sprites) -> pygame.sprite.Group:
        """
        Add sprites to the game.
        """

        all_sprites_list = pygame.sprite.Group()

        for sprite in sprites:
            all_sprites_list.add(sprite)

        self._logger.log('Sprites added')

        return all_sprites_list

    def _handle_events(self) -> None:
        """
        Handle events for the game.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._logger.log('Quitting PyPong')
                self._carry_on = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    self._carry_on = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self._paddle_a.move_up(5)
        if keys[pygame.K_s]:
            self._paddle_a.move_down(5)
        if keys[pygame.K_UP]:
            self._paddle_b.move_up(5)
        if keys[pygame.K_DOWN]:
            self._paddle_b.move_down(5)

    def _handle_game_logic(self) -> None:
        """
        Handle game logic for the game.
        """

        self._all_sprites_list.update()

        if self._ball.rect.x >= 690:
            self._ball.velocity[0] = -self._ball.velocity[0]
        if self._ball.rect.x <= 0:
            self._ball.velocity[0] = -self._ball.velocity[0]
        if self._ball.rect.y > 490:
            self._ball.velocity[1] = -self._ball.velocity[1]
        if self._ball.rect.y < 0:
            self._ball.velocity[1] = -self._ball.velocity[1]

        if pygame.sprite.collide_mask(self._ball, self._paddle_a) or pygame.sprite.collide_mask(self._ball, self._paddle_b):
            self._ball.bounce()

    def _draw_stuff(self) -> None:
        """
        Draw stuff for the game.
        """

        self._screen.fill(BLACK)

        pygame.draw.line(self._screen, WHITE, [349, 0], [349, 500], 5)

        self._all_sprites_list.draw(self._screen)

        pygame.display.flip()

    def run(self) -> None:
        """
        Run the game.
        """

        self._logger.log('Running PyPong')

        while self._carry_on:
            self._handle_events()
            self._handle_game_logic()
            self._draw_stuff()

            self._clock.tick(60)

        pygame.quit()
