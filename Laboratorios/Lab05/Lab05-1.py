# -----------------------------------------------
# ----- Nombre: Cristian Beltran Concha ---------
# ----- Prof: Luis Caro Saldivia ----------------
# ----- Asignatura: MicroControladores ----------
# -----------------------------------------------


import pygame
from pygame.locals import *
from PIL import Image
import os
from VideoCapture import Device
import ImageFilter
import serial
import time

(width, height) = (1000, 750)
background = (255,255,255)
screen = pygame.display.set_mode((width, height))
screen.fill(background)
pygame.init()

pygame.display.set_caption('MicroControladores')

full = pygame.Surface((1000, 800))
full.fill((255,255,255))
secA = pygame.Surface((600, 600))
secB = pygame.Surface((300,300))
secC = pygame.Surface((300,290))
secD = pygame.Surface((400, 80))
secMenu = pygame.Surface((250,300))
secD.fill((255,255,255))

# ------------ Carga imagenes ----------------------------
rutaCarpeta = "C:\\Imagenes"
imgs = []		# imagenes PIL
for file in os.listdir(rutaCarpeta):							# revisa los archivos de la carpeta
	if file.endswith(".jpg"):									# filtra los archivos jpg de la carpeta
		ruta = rutaCarpeta+'/'+ str(file)
		imgs.append(Image.open(ruta))
# ---------------------------------------------------------

def cargaSecA(img, BN = False):
	foto = img.resize(secA.get_size())
	fotoSu = pygame.image.fromstring(foto.tostring(), foto.size, foto.mode)
	secA.blit(fotoSu,(0,0))
	
	return 
def cargaSecB(img):
	foto = img.resize(secB.get_size())
	foto = foto.convert('L')		# convierte a B/N
	try:
		foto.save("a.bmp")			# guarda la foto B/N
		fotoSu = pygame.image.load('a.bmp')		# Carga la foto B/N
		secB.blit(fotoSu,(0,0))	
		os.remove('a.bmp')			# elimina archivo
	except:
		print "Error al cargar Imagen"
	return
def cargaSecD():
	fuente = pygame.font.Font(None, 30)
	# -------------- etiquetas ------------------
	etiqueta = fuente.render('WebCam',1, (0,0,0))	
	secD.blit(etiqueta, (0, 10))
	if onCam > 0:
		color = (255,0,0)
	else:
		color = (128,128,128)
	pygame.draw.circle(secD, color, (115,15), 15)
	return
def setMenu():
	# --------------- Menu -----------------
	secMenu.fill((255,255,255))
	pygame.draw.rect(secMenu, (0,0,0), (0,0,secMenu.get_width(), secMenu.get_height()),3)
	pygame.draw.circle(secMenu, (0,148,255),(230, 30 + iMenu*40),12)	# puntero
	fuente = pygame.font.Font(None, 40)
	# -------------- etiquetas ------------------
	etiqueta = fuente.render('Gray',1, (0,0,0))	
	secMenu.blit(etiqueta, (10, 20))
	etiqueta = fuente.render('Blend',1, (0,0,0))	
	secMenu.blit(etiqueta, (10, 60))
	etiqueta = fuente.render('Flip Horizontal',1, (0,0,0))	
	secMenu.blit(etiqueta, (10, 100))
	etiqueta = fuente.render('Flip Vertical',1, (0,0,0))	
	secMenu.blit(etiqueta, (10, 140))
	etiqueta = fuente.render('Rotate 90',1, (0,0,0))	
	secMenu.blit(etiqueta, (10, 180))
	etiqueta = fuente.render('Rotate 180',1, (0,0,0))	
	secMenu.blit(etiqueta, (10, 220))
	etiqueta = fuente.render('Filter Blur',1, (0,0,0))	
	secMenu.blit(etiqueta, (10, 260))
	secMenu.set_alpha(200)	# transparencia	
	# --------------------------------------
	return
def actualiza():
	if onMenu > 0:		
		setMenu()
		secA.blit(secMenu, (20,30))		
	cargaSecD()
	full.blit(secA,(10,40))
	full.blit(secB,(620, 40))
	full.blit(secC, (620, 350))	
	full.blit(secD,(10, 650))
	screen.blit(full,(30,0))
	return
cam = Device()
def getCam():	# carga imagen de camara en C
	image = cam.getImage()		# captura la imagen
	image = image.resize(secC.get_size())
	camar = pygame.image.fromstring(image.tostring(), image.size, 'RGB')
	secC.blit(camar,(0,0))
	return
	
run = True
iImage= 0	#id de imagen actual
onCam = -1	# on/off camara
onMenu = -1	# on/off Menu
iMenu = 0	# id menu seleccionado	
ImagenCargadaA = imgs[0]
ImagenCargadaB = ImagenCargadaA 

s = serial.Serial(2)		#COM5
s.baurate = 9600
s.timeout = 0
while run:
	cargaSecA(ImagenCargadaA)
	cargaSecB(ImagenCargadaB)
	actualiza()
	# ----------- Camara --------------
	if onCam >0:
		getCam()
	else:
		secC.fill((0,0,0))
	# ----------------------------------
	# ----------- Menu -----------------
	opcion = s.readline()
	print opcion
	if opcion == "21":	# button Power - enciende/apaga Camara
		onCam = -onCam
	if opcion == "9":	# button 0 - camptura camara
		if onCam > 0:
				ImagenCargadaA = cam.getImage()
	if opcion == "96":		# button Menu - Menu
		print "menu"
		time.sleep(.5)
		onMenu = -onMenu
		iMenu = 0
	# ------------ Recorre Menu ---------
	if onMenu > 0:		# si activa el menu
		if opcion == "16":	# CH+
			if iMenu > 0:
				iMenu -= 1
		elif opcion == "17":	# CH-
			if iMenu < 6:		#  Tope del menu
				iMenu += 1
		elif opcion == "18":	# Vol+
			if iMenu == 0:		# Grey
				try:
					foto = ImagenCargadaA.convert('L')		# convierte a B/N					
					foto.save("c.bmp")			# guarda la foto B/N
					fotoSu = pygame.image.load('c.bmp')		# Carga la foto B/N
					ImagenCargadaA = Image.fromstring('RGB',foto.size,pygame.image.tostring(fotoSu,'RGB',False))
					os.remove('c.bmp')			# elimina archivo
				except:
					print "Error Cargar Imagen" 
			elif iMenu == 1:		# Blend
				ImagenCargadaA = Image.blend(ImagenCargadaA.resize(secA.get_size()), imgs[iImage+1].resize(secA.get_size()), 0.5)
			elif iMenu == 2:		# Flip Horizontal
				ImagenCargadaA = ImagenCargadaA.transpose(Image.FLIP_LEFT_RIGHT)
			elif iMenu == 3:		# Flip Vertical
				ImagenCargadaA = ImagenCargadaA.transpose(Image.FLIP_TOP_BOTTOM)
			elif iMenu == 4:		# Rotate 90
				ImagenCargadaA = ImagenCargadaA.transpose(Image.ROTATE_90)
			elif iMenu == 5:		# Rotate 180
				ImagenCargadaA = ImagenCargadaA.transpose(Image.ROTATE_180)
			elif iMenu == 6:		# Rotate 180
				ImagenCargadaA = ImagenCargadaA.filter(ImageFilter.BLUR)
	else:	# menu desactivado
		if opcion == "16":	# CH+
			if iImage < len(imgs)-1:
				iImage += 1
				ImagenCargadaA = imgs[iImage]
				ImagenCargadaB = ImagenCargadaA
		elif opcion == "17":	# CH+-
			if iImage > 0:
				iImage -= 1 
				ImagenCargadaA = imgs[iImage]
				ImagenCargadaB = ImagenCargadaA
	# ----------------------------------
	
	# ----------------------------------
	even = pygame.event.get()
	cKey = pygame.key.get_pressed()
	for e in even:
		if e.type == pygame.QUIT:
			run = False
		if cKey[pygame.K_RIGHT]:
			if iImage < len(imgs)-1:
				iImage += 1
				ImagenCargadaA = imgs[iImage]
				ImagenCargadaB = ImagenCargadaA
		if cKey[pygame.K_LEFT]:
			if iImage > 0:
				iImage -= 1 
				ImagenCargadaA = imgs[iImage]
				ImagenCargadaB = ImagenCargadaA
		if cKey[pygame.K_c]:
			onCam = -onCam
		if cKey[pygame.K_m]:
			onMenu = -onMenu
			iMenu = 0
		if cKey[pygame.K_DOWN]:
			if iMenu < 6:
				iMenu += 1
		if cKey[pygame.K_UP]:
			if iMenu > 0:
				iMenu -= 1
		if cKey[pygame.K_0]:		# captura imagen Camara
			if onCam > 0:
				ImagenCargadaA = cam.getImage()
		
		if cKey[pygame.K_RETURN]:
			if onMenu > 0:
				if iMenu == 0:		# Grey
					try:
						foto = ImagenCargadaA.convert('L')		# convierte a B/N					
						foto.save("c.bmp")			# guarda la foto B/N
						fotoSu = pygame.image.load('c.bmp')		# Carga la foto B/N
						ImagenCargadaA = Image.fromstring('RGB',foto.size,pygame.image.tostring(fotoSu,'RGB',False))
						os.remove('c.bmp')			# elimina archivo
					except:
						print "Error Cargar Imagen"
				elif iMenu == 1:		# Blend
					ImagenCargadaA = Image.blend(ImagenCargadaA.resize(secA.get_size()), imgs[iImage+1].resize(secA.get_size()), 0.5)
				elif iMenu == 2:		# Flip Horizontal
					ImagenCargadaA = ImagenCargadaA.transpose(Image.FLIP_LEFT_RIGHT)
				elif iMenu == 3:		# Flip Vertical
					ImagenCargadaA = ImagenCargadaA.transpose(Image.FLIP_TOP_BOTTOM)
				elif iMenu == 4:		# Rotate 90
					ImagenCargadaA = ImagenCargadaA.transpose(Image.ROTATE_90)
				elif iMenu == 5:		# Rotate 180
					ImagenCargadaA = ImagenCargadaA.transpose(Image.ROTATE_180)
				elif iMenu == 6:		# Rotate 180
					ImagenCargadaA = ImagenCargadaA.filter(ImageFilter.BLUR)
		
	pygame.display.flip()
	
	