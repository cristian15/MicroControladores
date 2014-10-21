# -----------------------------------------------
# ----- Nombre: Cristian Beltran Concha ---------
# ----- Prof: Luis Caro Saldivia ----------------
# ----- Asignatura: MicroControladores ----------
# -----------------------------------------------

import serial 
import time
import win32com.client as win32
import os


def toExcel():	
	excel = win32.DispatchEx("Excel.Application")		# inicia la Excel
	
	book = excel.Workbooks.Add()	# crea el libro
	sheet1 = book.Worksheets(1)		# selecciona la hoja de trabajo
	excel.Visible = True			# muestra el excel
	
	sheet1.Cells(1,1).Value = 'T(seg)'
	sheet1.Cells(1,2).Value = 'LDR'
	sheet1.Cells(1,3).Value = 'DS18B20'
	for i in range(0, len(LDR)):		# inserta datos a las celdas
		sheet1.Cells(i+2,1).Value = 0.5*i
		sheet1.Cells(i+2,2).Value = LDR[i]
	for i in range(0, len(DS)):		# inserta datos a las celdas
		sheet1.Cells(i+2,3).Value = DS[i]	
	sheet1.Shapes.AddChart() # agrega el grafico
	chart = sheet1.ChartObjects(1).Chart		# selecciona el grafico
	chart.ChartType = -4169		# grafico de dispercion	
	chart.SetSourceData(sheet1.Range("A:C"))		# selecciona datos	
	#chart.SeriesCollection(1).Trendlines().Add()	# agrega la regresion (linea de tendencia)
	return

	
	return
s = serial.Serial(2)		# COM3 Picaxe
s.baudrate = 4800
s.timeout = 0

LDR = []
DS = []
dato = ""
d = ""
# ---------------- Guarda los Datos -----------------------
run = True
while run:			
	dato = s.read()	
	if len(dato) > 0:
		while dato != "*":
			d += dato
			dato = s.read()
		d = d[:len(d)]
		print d
		if d == "FIN":
			run = False
		if d[:1] == "L":		# guarda si el datos es del sensor LDR
			LDR.append(d[1:] )
		elif d[:1] == "D":		# si es del sensor de temperatura
			DS.append(d[1:])		
		d = ""
	# ----------------------------------------------------------

toExcel()		# guarda en excel

# ---  escribe el archivo sensores.txt ----------
archivo = open("sensores.txt", 'w')	# crea el archivo
archivo.write("LRD: ")
for i in LDR:	
	archivo.write(i +",")
archivo.write("\nDS18B20: ")
for i in DS:
	archivo.write(i + ", ")
archivo.close()
# ---------------------------------------------------
