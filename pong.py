# Import the pygame library
import pygame
from paddle import Paddle

# Initialize the pygame engine
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PyPong")

paddle_a = Paddle(WHITE, 10, 100)
paddle_a.rect.x = 20
paddle_a.rect.y = 200

paddle_b = Paddle(WHITE, 10, 100)
paddle_b.rect.x = 670
paddle_b.rect.y = 200

all_sprites_list = pygame.sprite.Group()

all_sprites_list.add(paddle_a)
all_sprites_list.add(paddle_b)

# The loop will carry on until the user exits the game
carry_on = True

# A clock to controll how fast the screen updates
clock = pygame.time.Clock()

# -----------
# Main loop
# -----------
while carry_on:
	# -------- Main event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			carry_on = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_x:
				carry_on = False

	# -------- Game logic
	all_sprites_list.update()

	# -------- Drawing stuff

	# first of all, clear the screen
	screen.fill(BLACK)

	# Draw the net
	pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)

	all_sprites_list.draw(screen)

	# -------- Go ahead and update the screen with what we've drawn
	pygame.display.flip()

	# --------
	clock.tick(60)

# Once we have left the main loop we can stop the game engine
pygame.quit()

