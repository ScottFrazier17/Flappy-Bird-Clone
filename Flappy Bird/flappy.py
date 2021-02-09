import pygame
import sys
import random

# Initializing the Game
pygame.init()

# FPS
clock = pygame.time.Clock()

# Window
screen = pygame.display.set_mode((403, 717))
running = True

# Score
score = 0
high_score = 0
game_font = pygame.font.Font('04B_19.ttf', 40)
def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
		score_rect = score_surface.get_rect(center= (200,100))
		screen.blit(score_surface,score_rect)
	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
		score_rect = score_surface.get_rect(center= (200,100))
		screen.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
		high_score_rect = high_score_surface.get_rect(center= (200,565))
		screen.blit(high_score_surface,high_score_rect)

# Update High Score
def update_high_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

# Game Over Surface
game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_surface = pygame.transform.scale(game_over_surface, (258, 374))

# Gravity
gravity = 0.5
bird_movement = 0

# Background
background = pygame.image.load('assets/background-day.png').convert()
background = pygame.transform.scale(background, (403, 717))

# Floor
floorX = 0
floorY = 600
floorX_change = 3
floor = pygame.image.load('assets/base.png').convert()
floor = pygame.transform.scale(floor, (470, 157))
def floor_movement():
	screen.blit(floor, (floorX, floorY))
	screen.blit(floor, (floorX + 470, floorY))

# Bird
bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_downflap = pygame.transform.scale(bird_downflap, (48, 34))
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_midflap = pygame.transform.scale(bird_midflap, (48, 34))
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_upflap = pygame.transform.scale(bird_upflap, (48, 34))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(80, 359))

# Rotation of Bird
def rotate_bird(bird_surface):
	new_bird = pygame.transform.rotozoom(bird_surface, -bird_movement * 3, 1)
	return new_bird
FLAPFRAME = pygame.USEREVENT + 1
pygame.time.set_timer(FLAPFRAME, 300)

# Bird Animation Function
def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (80, bird_rect.centery))
	return new_bird, new_bird_rect

# Pipes
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale(pipe_surface, (73, 448))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)
pipe_height = [300, 400, 450]
def create_pipe():
	random_pipe_height = random.choice(pipe_height)
	top_new_pipe = pipe_surface.get_rect(midbottom = (600, random_pipe_height - 175))
	bottom_new_pipe = pipe_surface.get_rect(midtop = (600, random_pipe_height))
	return top_new_pipe, bottom_new_pipe

def pipe_movement(pipes):
	global score
	for pipe in pipes:
		pipe.centerx -= 5

		# Better Sound
		if pipe.centerx == 120:
			score += .5
			score_sound.play()
	return pipes 

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 717:
			screen.blit(pipe_surface, pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface, False, True)
			screen.blit(flip_pipe, pipe)

# Collision
def check_collision(pipes):
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			death_sound.play()
			screen.blit(bird_surface, (60, 359))
			return False
	if bird_rect.bottom >= 600:
		death_sound.play()
		screen.blit(bird_surface, (60, 359))
		return False

	return True

# Import Sounds
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
swoosh_sound =pygame.mixer.Sound('sound/sfx_swooshing.wav')
score_sound_countdown = 100

# Restart Mechanic
game_active = True

# Open Window
while running:
	pygame.display.update()

	# Event Loop
	for event in pygame.event.get():

		# Quit Function
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				bird_movement = 0
				bird_movement -= 12
				flap_sound.play()

			# Restart if SPACE
			if event.key == pygame.K_SPACE and game_active is False:
				game_active = True
				score = 0
				pipe_list = []
				bird_movement = -12
				bird_rect.centery = 359
		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())
		if event.type == FLAPFRAME:
			bird_index += 1
			if bird_index > 2:
				bird_index = 0
		bird_surface,bird_rect = bird_animation()


	# Background
	screen.blit(background, (0,0))

	if game_active:

		# Bird
		bird_movement += gravity
		bird_rotated = rotate_bird(bird_surface)
		bird_rect.centery += bird_movement
		screen.blit(bird_rotated, bird_rect)

		# Pipes
		pipe_list = pipe_movement(pipe_list)
		draw_pipes(pipe_list)

		# Score
		score_display('main_game')
		game_active=check_collision(pipe_list)
#		if bird_movement >= 12:
#			swoosh_sound.play()
#		if bird_movement <= -12:
#			swoosh_sound.play()

	else:
		high_score = update_high_score(score, high_score)
		score_display('game_over')
		screen.blit(game_over_surface, (70,140))

	# Floor
	floorX -= floorX_change
	floor_movement()
	if floorX <= -470:
		floorX = 0

	pygame.display.update()
	clock.tick(60)
