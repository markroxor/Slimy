import pygame,time,random

pygame.init()
display_width = 800
display_height = 600

white = (255,255,255)
black = (0,0,0)
red  = (255,0,0)
green  = (34,177,76)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Slither")

icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)

img = pygame.image.load('head.png')
appleimg = pygame.image.load('apple.png')

clock = pygame.time.Clock()

AppleThickness = 30
block_size = 20
FPS = 20

direction = "right"

# smallfont = pygame.font.Font(None,25)
smallfont = pygame.font.SysFont("comicsansms",25)
medfont = pygame.font.SysFont("comicsansms",50)
largefont = pygame.font.SysFont("comicsansms",80)

def pause():
	paused = True

	message_to_screen("Paused",
		black,-100,"large")
	message_to_screen("Press C to continue or Q to quit:",
		black,25)

	pygame.display.update()

	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					paused = False
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()

		# gameDisplay.fill(white)

		clock.tick(5)

def score(score):
	text = smallfont.render("Score: " + str(score),True, black)
	gameDisplay.blit(text,[0,0])

def randAppleGen():
	randAppleX = round(random.randrange(0,display_width-block_size)/10.0)*10
	randAppleY = round(random.randrange(0,display_height-block_size)/10.0)*10

	return randAppleX,randAppleY

randAppleX,randAppleY = randAppleGen()

def game_intro():
	intro = True

	while intro:

		for event in pygame.event.get():
			if event.type ==pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					intro = False
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()

		gameDisplay.fill(white)
		message_to_screen("Welcome to Slither",
			green,-100,"large")
		message_to_screen("The objetive of the game is to eat red apples",
			black,-30)
		message_to_screen("The more apples you eat the longer you get",
			black,10)
		message_to_screen("If you run into yourself or the edges, you die!",
			red,50)
		message_to_screen("Press C to play, P to pause or Q to quit.",
			red,180)

		pygame.display.update()
		clock.tick(15)

def snake(block_size,snakeList,direction):
	# global direction
	if direction == "right":
		head = pygame.transform.rotate(img,270)

	elif direction == "left":
		head = pygame.transform.rotate(img,90)

	elif direction == "up":
		head = img

	elif direction == "down":
		head = pygame.transform.rotate(img,180)

	gameDisplay.blit(head,(snakeList[-1][0],snakeList[-1][1]))
	for XnY in snakeList[:-1]:
		pygame.draw.rect(gameDisplay,green,[XnY[0],XnY[1],block_size,block_size])

def text_objects(text,color,size):
	if size == 'small':
		textSurface = smallfont.render(text,True,color)
	elif size == 'medium':
		textSurface = medfont.render(text,True,color)
	elif size == 'large':
		textSurface = largefont.render(text,True,color)
	
	return textSurface,textSurface.get_rect()

def message_to_screen(msg,color,y_displace=0,size='small'):
	textSurf, textRect = text_objects(msg,color,size)
	textRect.center = (display_width/2),(display_height/2)+y_displace
	gameDisplay.blit(textSurf,textRect)

def gameLoop():
	global direction
	direction = "right"

	gameExit = False
	gameOver = False

	lead_x = display_width/2
	lead_y = display_height/2

	lead_x_change = 20
	lead_y_change = 0


	snakeList = []
	snakeLength = 2

	randAppleX,randAppleY = randAppleGen()
	
	while not gameExit:
		if gameOver:
			message_to_screen("Game over",red,-50,"large")
			message_to_screen( "press C to play again or Q to quit",black,50,"medium")
			pygame.display.update()
 

		while gameOver:
			# gameDisplay.fill(white)
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameOver = False
					gameExit = True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameExit = True
						gameOver = False
					elif event.key == pygame.K_c:
						gameLoop()


		for event in pygame.event.get():
			print event

			if event.type == pygame.QUIT:
				gameExit = True

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					direction = "left"
					lead_x_change = -block_size
					lead_y_change = 0
				elif event.key == pygame.K_RIGHT:
					direction = "right"
					lead_x_change = block_size
					lead_y_change = 0
				elif event.key == pygame.K_UP:
					direction = "up"
					lead_y_change = -block_size
					lead_x_change = 0
				elif event.key == pygame.K_DOWN:
					direction = "down"
					lead_y_change = block_size
					lead_x_change = 0

				elif event.key == pygame.K_p:
					pause()

		lead_x +=lead_x_change
		lead_y +=lead_y_change

		gameDisplay.fill(white)

		#so that the Apple stays within boundaries of frame.
		# pygame.draw.rect(gameDisplay,red,[(randAppleX)%(display_width-AppleThickness),(randAppleY)%(display_height-AppleThickness),AppleThickness,AppleThickness])
		
		gameDisplay.blit(appleimg,(randAppleX,randAppleY))

		snakeHead = []
		snakeHead.append(lead_x)
		snakeHead.append(lead_y)
		snakeList.append(snakeHead)

		if snakeHead[0]<0 or snakeHead[0]>=display_width or snakeHead[1]<0 or snakeHead[1]>=display_height:
			gameOver = True


		if len(snakeList)>snakeLength:
			del snakeList[0]

		for eachSegment in snakeList[:-1]:
			if eachSegment == snakeHead:
				gameOver = True

		score(snakeLength-1)
		
		snake(block_size,snakeList,direction)
		
		pygame.display.update()

		if lead_x>randAppleX and lead_x< randAppleX+AppleThickness or lead_x + block_size>randAppleX \
			and lead_x + block_size < randAppleX + AppleThickness:
			
			if lead_y>randAppleY and lead_y< randAppleY+AppleThickness:# or lead_y + block_size>randAppleX \
				snakeLength += 1
				randAppleX,randAppleY = randAppleGen()
		
			elif lead_y + block_size > randAppleY and lead_y + block_size< randAppleY + AppleThickness:
				snakeLength += 1
				randAppleX,randAppleY = randAppleGen()
		
		clock.tick(FPS)


	pygame.quit()
	quit() 

game_intro()
gameLoop()