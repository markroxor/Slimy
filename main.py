import pygame,time,random

pygame.init()
display_width = 800
display_height = 600

white = (255,255,255)
black = (0,0,0)
red  = (255,0,0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Slither")


clock = pygame.time.Clock()

block_size = 10
FPS = 30

font = pygame.font.SysFont(None,25)
def snake(block_size,snakeList):
	for XnY in snakeList:
		pygame.draw.rect(gameDisplay,black,[XnY[0],XnY[1],block_size,block_size])

def message_to_screen(msg,color):
	screen_text = font.render(msg,True,color)
	gameDisplay.blit(screen_text,[display_width/2,display_height/2])

def gameLoop():
	gameExit = False
	gameOver = False

	lead_x = display_width/2
	lead_y = display_height/2

	lead_x_change = 0
	lead_y_change = 0

	snakeList = []
	snakeLength = 1

	randAppleX = round(random.randrange(0,display_width-block_size)/10.0)*10
	randAppleY = round(random.randrange(0,display_height-block_size)/10.0)*10

	while not gameExit:

		while gameOver:
			gameDisplay.fill(white)
			message_to_screen("Game over press C to play again or Q to quit",red)
			pygame.display.update()

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
					lead_x_change = -block_size
					lead_y_change = 0
				elif event.key == pygame.K_RIGHT:
					lead_x_change = block_size
					lead_y_change = 0
				elif event.key == pygame.K_UP:
					lead_y_change = -block_size
					lead_x_change = 0
				elif event.key == pygame.K_DOWN:
					lead_y_change = block_size
					lead_x_change = 0

			if lead_x<0 or lead_x>=display_width or lead_y<0 or lead_y>=display_height:
				gameOver = True

			# un-comment it to stop auto-pilot mode.
			# if event.type == pygame.KEYUP:
			# 	if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
			# 		lead_x_change = 0
			# 	elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
			# 		lead_y_change = 0
		
		lead_x +=lead_x_change
		lead_y +=lead_y_change

		gameDisplay.fill(white)

		AppleThickness = 30
		#so that the Apple stays within boundaries of frame.
		pygame.draw.rect(gameDisplay,red,[(randAppleX)%(display_width-AppleThickness),(randAppleY)%(display_height-AppleThickness),AppleThickness,AppleThickness])
		
		snakeHead = []
		snakeHead.append(lead_x)
		snakeHead.append(lead_y)
		snakeList.append(snakeHead)

		if len(snakeList)>snakeLength:
			del snakeList[0]

		for eachSegment in snakeList[:-1]:
			if eachSegment == snakeHead:
				gameOver = True

		snake(block_size,snakeList)
		pygame.display.update()

		# if lead_x == randAppleX and lead_y == randAppleY:
		# 	snakeLength += 1
		# 	randAppleX = round(random.randrange(0,display_width-block_size)/10.0)*10
		# 	randAppleY = round(random.randrange(0,display_height-block_size)/10.0)*10
		# 	print "nom nom nom"

		if lead_x <=randAppleX+AppleThickness and lead_x >= randAppleX:
			if lead_y <=randAppleY+AppleThickness and lead_y >= randAppleY :
				snakeLength += 1
				randAppleX = round(random.randrange(0,display_width-block_size)/10.0)*10
				randAppleY = round(random.randrange(0,display_height-block_size)/10.0)*10
				print "nom nom nom"

		clock.tick(FPS)


	pygame.quit()
	quit() 
gameLoop()