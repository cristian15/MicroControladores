#!/usr/bin/python

# moculos 
from sqlite3 import connect as con
from serial import Serial as ser

# constantes de la comunicacion serial
port = 0
bd = 2400

# establecer conemunicacion serial
s = ser(port,bd)

# conexion con la base de datos
conn = con('lab06BD.db')
c = conn.cursor()

# condiconal y aumentador
salir = False
n = 1

# loop
while not salir:
	recv = s.readline()
	if recv != null:
		if recv == "salir":
			con.close()
			s.close()
			salir = True
		else:
			sql = "INSERT INTO T_Datos VALUES(?, ?, date('now'))"
			c.execute(sql,(n,recv))
			conn.commit()
	
		n += 1