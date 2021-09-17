import sys,pygame 
import os 
pygame.init()
pygame.font.init()
pygame.mixer.init()
# pygame - 2D graphics library 

WIDTH, HEIGHT = 1000, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('GAME')

WHITE = (255,255,255)

COLOR = (100 , 100, 100)

RED = (255, 0, 0)

YELLOW = (255, 255, 0)

BULLET_SOUND = pygame.mixer.Sound(os.path.join('img_and_sound', 'hitsound.wav'))

BULLET_FIRE = pygame.mixer.Sound(os.path.join('img_and_sound', 'gunshot.mp3'))

VICTORY_SOUND = pygame.mixer.Sound(os.path.join('img_and_sound', 'gamewin.wav'))

BORDER = pygame.Rect(WIDTH//2 - 5 , 0 , 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)

WINNER_FONT = pygame.font.SysFont('arial', 120)

FPS = 60 #Frames per second 

MAX_BULLETS = 5

VELOCITY = 3

BULLET_VELOCITY = 6

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

SPACEASHIP_WIDTH, SPACESHIP_HEIGHT = 60, 50

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('img_and_sound', 'spaceship_yellow.png'))

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACEASHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.image.load(os.path.join('img_and_sound', 'spaceship_red.png')), 270)

RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACEASHIP_WIDTH, SPACESHIP_HEIGHT))

SPACE_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('img_and_sound', 'space.png')), (WIDTH, HEIGHT) )


def draw_window(red, yellow, red_bullet, yellow_bullet, red_health, yellow_health):
	WIN.blit(SPACE_BACKGROUND, (0, 0))#changing background color to white
	pygame.draw.rect(WIN, COLOR, BORDER)

	red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
	yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
	WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
	WIN.blit(yellow_health_text, (10, 10))
	WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) 
	WIN.blit(RED_SPACESHIP, (red.x, red.y))

	for bullet in red_bullet:
		pygame.draw.rect(WIN, RED, bullet)

	for bullet in yellow_bullet:
		pygame.draw.rect(WIN, YELLOW, bullet)

	pygame.display.update() # here we give pygame.display.update() so that the our code abve shows up on the window 

def yellow_spaceship_movement(keys_pressed, yellow):
		if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0: #LEFT
			yellow.x -= VELOCITY 

		if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x: #RIGHT
			yellow.x += VELOCITY

		if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0: #UP
			yellow.y -= VELOCITY

		if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT: #D
			yellow.y += VELOCITY

def red_spaceship_movement(keys_pressed, red):
		if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width: #LEFT
			red.x -= VELOCITY 

		if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < 1000: #RIGHT
			red.x += VELOCITY

		if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0: #UP
			red.y -= VELOCITY

		if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT: #D
			red.y += VELOCITY

def handle_bullets_position(yellow_bullet, red_bullet, yellow, red):
	for bullet in yellow_bullet:
		bullet.x += BULLET_VELOCITY
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(RED_HIT))
			yellow_bullet.remove(bullet)
		elif bullet.x > WIDTH:
			yellow_bullet.remove(bullet)

	for bullet in red_bullet:
		bullet.x -= BULLET_VELOCITY
		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(YELLOW_HIT))
			red_bullet.remove(bullet)
		elif bullet.x < 0:
			red_bullet.remove(bullet)

def winner(text):
	winner_text = WINNER_FONT.render(text, 1, WHITE)
	WIN.blit(winner_text, (WIDTH//2 - winner_text.get_width()/2, HEIGHT//2 - winner_text.get_height()/2))
	pygame.display.update()
	pygame.time.delay(5000)
	

def main():
	red = pygame.Rect(800, 250, SPACEASHIP_WIDTH, SPACESHIP_HEIGHT)
	yellow = pygame.Rect(200, 250, SPACEASHIP_WIDTH, SPACESHIP_HEIGHT)

	red_bullet = []
	yellow_bullet = []

	red_health = 10
	yellow_health = 10

	clock = pygame.time.Clock() #to set FPS 
	run = True;
	while run:
		clock.tick(FPS) #this will always work at 60 FPS. That is it the same for all the computers  
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False;
				pygame.quit()
				sys.exit()

		
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LCTRL and len(yellow_bullet) < MAX_BULLETS:
					bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 3 , 10, 6)
					yellow_bullet.append(bullet)
					BULLET_FIRE.play()

				if event.key == pygame.K_RCTRL and len(red_bullet) < MAX_BULLETS:
					bullet = pygame.Rect(red.x , red.y + red.height//2 - 3 , 10, 6)
					red_bullet.append(bullet)
					BULLET_FIRE.play()

			if event.type == RED_HIT:
				red_health -= 1
				BULLET_SOUND.play()

			if event.type == YELLOW_HIT:
				yellow_health -= 1
				BULLET_SOUND.play()
		
		winner_text = ""
		if red_health <= 0:
			winner_text = "YELLOW WINS!"

		if yellow_health <= 0:
			winner_text = "RED WINS!"

		if winner_text != "":
			winner(winner_text)
			break


		keys_pressed = pygame.key.get_pressed()
		yellow_spaceship_movement(keys_pressed, yellow)
		red_spaceship_movement(keys_pressed, red)
		
		handle_bullets_position(yellow_bullet, red_bullet, yellow, red)

		draw_window(red, yellow, red_bullet, yellow_bullet, red_health, yellow_health)	


	VICTORY_SOUND.play()
	main()


if __name__ == "__main__": #to run this only here and not run when it is imported
	main()