import pygame
import math
import random as RA

(width, height) = (1000, 750)
background = (255,255,255)
screen = pygame.display.set_mode((width, height))
screen.fill(background)
pygame.init()

pygame.display.set_caption('MicroControladores - Pong')

mesa = pygame.Surface((900,650))

mesa.fill((255,255,255))

pygame.draw.rect(mesa, (0,0,0), (0,0,mesa.get_width(), mesa.get_height() ), 10)



class Player():
	def __init__(self, (x,y), color, (width, height) ):
		self.x = x
		self.y = y
		self.color = color
		self.width = width
		self.height = height
	def display(self):
		pygame.draw.rect(mesa, self.color, (self.x, self.y, self.width, self.height))
	
class ball():
	def __init__(self, (x,y),color, size, vel, angle):
		self.x = x
		self.y = y
		self.color = color
		self.size = size
		self.vel = vel
		self.angle = angle
	def display(self):
		pygame.draw.circle(mesa, self.color, (self.x, self.y), self.size)
	def move(self):
		self.x += math.sin(self.angle)*self.vel
		self.y += math.cos(self.angle)*self.vel
		
		
# ----------- Inicia jugadores -----------------
player = []
player.append( Player((30, 100), (0,0,255), (20,100)))
player.append( Player((mesa.get_width()-50, 100), (255,0,0), (20,100)))
player[0].display()
player[1].display()
# -----------------------------------------

pelota = ball((100,50), (0,0,0), 15, RA.random(), RA.uniform(0, math.pi/4))
pelota.display()
screen.blit(mesa,(50,90))
run = True
while run:
	even = pygame.event.get()
	cKey = pygame.key.get_pressed()
	for e in even:
		if e.type == pygame.QUIT:
			run = False
		if cKey[pygame.K_UP]:
			mesa.blit()
	pygame.display.flip()
