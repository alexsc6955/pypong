# Import the pygame library
import pygame
from paddle import Paddle
from ball import Ball

# Initialize the pygame engine
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Open a new window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PyPong")

paddle_a = Paddle(WHITE, 10, 100)
paddle_a.rect.x = 20
paddle_a.rect.y = 200

paddle_b = Paddle(WHITE, 10, 100)
paddle_b.rect.x = 670
paddle_b.rect.y = 200

ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

# This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

# Add thepaddles to the list of sprites
all_sprites_list.add(paddle_a)
all_sprites_list.add(paddle_b)
all_sprites_list.add(ball)

# The loop will carry on until the user exits the game. (e.g. clicks the close button).
carry_on = True

# A clock to controll how fast the screen updates
clock = pygame.time.Clock()

# -----------
# Main loop
# -----------
while carry_on:
	# -------- Main event loop
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			carry_on = False # Flag that we are done so we exit this loop
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_x: # Pressing the x Key will quit the game
				carry_on = False

	# Moving the paddles when the user uses the arrow keys (player A) or "W/S" keys (player B)
	keys = pygame.key.get_pressed()
	if keys[pygame.K_w]:
		paddle_a.move_up(5)
	if keys[pygame.K_s]:
		paddle_a.move_down(5)
	if keys[pygame.K_UP]:
		paddle_b.move_up(5)
	if keys[pygame.K_DOWN]:
		paddle_b.move_down(5)

	# -------- Game logic
	all_sprites_list.update()

	# Check if the ball is bouncing against any of the 4 walls
	if ball.rect.x >= 690:
		ball.velocity[0] = -ball.velocity[0]
	if ball.rect.x <= 0:
		ball.velocity[0] = -ball.velocity[0]
	if ball.rect.y >= 490:
		ball.velocity[1] = -ball.velocity[1]
	if ball.velocity[1] <= 0:
		ball.velocity[1] = -ball.velocity[1]

	# Detect collitions between the ball and the paddles
	if pygame.sprite.collide_mask(ball, paddle_a) or pygame.sprite.collide_mask(ball, paddle_b):
		ball.bounce()

	# -------- Drawing stuff

	# first of all, clear the screen
	screen.fill(BLACK)

	# Draw the net
	pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)

	# Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
	all_sprites_list.draw(screen)

	# -------- Go ahead and update the screen with what we've drawn
	pygame.display.flip()

	# --------
	clock.tick(60)

# Once we have left the main loop we can stop the game engine
pygame.quit()

