"""
Padde class for PyPong
"""


import pygame

from pypong.utils import logger

from pypong.constants import BLACK


class Paddle(pygame.sprite.Sprite):
    """
    This class represents a paddle. It derives from the "Sprite" class in Pygame.
    """

    _logger = logger

    def __init__(self, name: str, color: tuple, width: int, height: int) -> None:

        super().__init__()

        self._name = name

        # Pass in the color of the paddle, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

        self._logger.log(f'Paddle {self._name} created')

    def move_up(self, pixels: int) -> None:
        """
        Move the paddle up.

        :param pixels: The number of pixels to move the paddle up.
        :type pixels: int

        :rtype: None
        """

        self.rect.y -= pixels
        # Check that you are not going too far (off the screen)
        if self.rect.y < 0:
            self.rect.y = 0

    def move_down(self, pixels: int) -> None:
        """
        Move the paddle down.

        :param pixels: The number of pixels to move the paddle down.
        :type pixels: int

        :rtype: None
        """

        self.rect.y += pixels
        # Check that you are not going too far (off the screen)
        if self.rect.y > 400:
            self.rect.y = 400
