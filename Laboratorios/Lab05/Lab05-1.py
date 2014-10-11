import pygame
import PIL
import os
from VideoCapture import Device

(width, height) = (1000, 700)
background = (255,255,255)
screen = pygame.display.set_mode((width, height))
screen.fill(background)
pygame.init()

pygame.display.set_caption('MicroControladores')
#cam = Device()		# inicia la camara

secA = pygame.Surface((600, 600))
secB = pygame.Surface((300,300))
secC = pygame.Surface((300,290))
secA.fill((255,0,0))
secB.fill((255,0,0))
secC.fill((255,0,0))
screen.blit(secA,(10,40))
screen.blit(secB,(620, 40))
screen.blit(secC, (620, 350))


run = True
while run:
	even = pygame.event.get()
	cKey = pygame.key.get_pressed()
	for e in even:
		if e.type == pygame.QUIT:
			run = False
	pygame.display.flip()