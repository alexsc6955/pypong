# Import the pygame library
import pygame

# Initialize the pygame engine
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PyPong")

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

	# -------- Game logic

	# -------- Drawing stuff

	# first of all, clear the screen
	screen.fill(BLACK)

	# Draw the net
	pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)

	# -------- Go ahead and update the screen with what we've drawn
	pygame.display.flip()

	# --------
	clock.tick(60)

# Once we have left the main loop we can stop the game engine
pygame.quit()

