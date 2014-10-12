import pygame
import math
import random as RA
import time
import serial

(width, height) = (1000, 750)
background = (255,255,255)
screen = pygame.display.set_mode((width, height))
screen.fill(background)
pygame.init()

pygame.display.set_caption('MicroControladores - Pong')
mesa = pygame.Surface((900,650))

mesa.fill((0,0,0))
pygame.draw.rect(mesa, (20,255,30), (0,0, mesa.get_width(), mesa.get_height() ), 10)

class Player():
	def __init__(self, (x,y), color, (width, height), puntaje, name ):
		self.x = x
		self.y = y
		self.color = color
		self.width = width
		self.height = height
		self.puntaje = puntaje
		self.name = name
		
	def display(self):
		pygame.draw.rect(mesa, self.color, (self.x, self.y, self.width, self.height))
		fuente = pygame.font.Font(None, 30)
		# -------------- etiquetas ------------------
		etiqueta = fuente.render(self.name +": " +str(self.puntaje),1, self.color)	
		
		screen.blit(etiqueta, (self.x, 20))		
	def move(self, dir):
		if self.y + dir > 15 and self.y + dir < mesa.get_height() - self.height -15:
			self.y += 2*dir
			
class ball():
	def __init__(self, (x,y),color, size, vel, angle):
		self.x = x
		self.y = y
		self.color = color
		self.size = size
		self.vel = vel
		self.angle = angle
	def display(self):
		pygame.draw.circle(mesa, self.color, (int(self.x), int(self.y)), self.size)
		
	def move(self):
		self.x += math.sin(self.angle)*self.vel
		self.y += math.cos(self.angle)*self.vel
	def bounce(self, P):
		if self.x > mesa.get_width() - self.size :	
			self.x = 2*(mesa.get_width() - self.size) - self.x      
			self.angle = -self.angle
		elif self.x < self.size:
			self.x = 2*self.size - self.x
			self.angle = -self.angle
		if self.y > mesa.get_height() - self.size:
			self.y = 2*(mesa.get_height() - self.size) - self.y
			self.angle = math.pi - self.angle
		elif self.y < self.size:
			self.y = 2*self.size - self.y
			self.angle = math.pi - self.angle			
		if P.x < mesa.get_width()/2: # si es la paleta izquierda
			if self.x < self.size + P.x + P.width and self.y > P.y and self.y < P.y+P.height:
				self.x = P.x + P.width+ self.size
				self.angle = -self.angle
		else: # si es la paleta derecha
			if self.x > P.x - self.size and self.y > P.y and self.y < P.y+P.height:
				self.x = P.x - self.size
				self.angle = -self.angle
	def anota(self, P):
		if P.x < mesa.get_width()/2: # si es la paleta izquierda
			if self.x > mesa.get_width() - self.size :	# si anota a la derecha
				P.puntaje += 10
				self.angle = RA.uniform(0,math.pi*2)
				self.x = mesa.get_width()/2
				self.y = mesa.get_height()/2
				self.vel += .2		# aumenta la velocidad de la pelota
				time.sleep(.5)
		else: # si es la paleta derecha
			if self.x < self.size:	# si anota a la derecha
				P.puntaje += 10
				self.angle = RA.uniform(0,math.pi*2)
				self.x = mesa.get_width()/2
				self.y = mesa.get_height()/2
				self.vel += .2		# aumenta la velocidad de la pelota
				time.sleep(.5)
		return P
# ----------- Inicia jugadores -----------------
player = []
player.append( Player((30, 100), (0,0,255), (20,100), 0, "Player 1"))
player.append( Player((mesa.get_width()-50, 100), (255,0,0), (20,100), 0, "Player 2"))
player[0].display()
player[1].display()

# -----------------------------------------
pelota = ball((mesa.get_width()/2, mesa.get_height()/2), (20,255,30), 15, 2, RA.uniform(0,math.pi))
pelota.display()
screen.blit(mesa, (50,90))

s = serial.Serial(4)
s.baurate = 9600
s.timeout = 0
run = True
while run:
	button = s.readline()
	even = pygame.event.get()
	cKey = pygame.key.get_pressed()
	screen.fill((0,0,0))
	mesa.fill((0,0,0))
	pygame.draw.rect(mesa, (20,255,30), (0,0, mesa.get_width(), mesa.get_height() ), 10)
	pelota.move()
	player[0] = pelota.anota(player[0])
	player[1] = pelota.anota(player[1])
	pelota.bounce(player[0])
	pelota.bounce(player[1])
	pelota.display()
	
	player[0].display()
	player[1].display()	
	
	screen.blit(mesa, (50,90))	
	
	if button == "16": 		# button CK+
		player[0].move(-1)
	elif button == "17":   # button CH-
		player[0].move(1)
	elif button == "18":		# button Vol+
		player[1].move(1)
	elif button == "19": 	#button Vol-
		player[1].move(-1)
	
	for e in even:
		if e.type == pygame.QUIT:
			run = False
	if cKey[pygame.K_UP]:
		player[0].move(-1)
	if cKey[pygame.K_DOWN]:
		player[0].move(1)
	if cKey[pygame.K_LEFT]:
		player[1].move(-1)
	if cKey[pygame.K_RIGHT]:
		player[1].move(1)
	pygame.display.flip()
