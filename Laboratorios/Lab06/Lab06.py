#!/usr/bin/python

# moculos 
from sqlite3 import connect as con
from serial import Serial as ser

# constantes de la comunicacion serial
port = 0
bd = 2400

# establecer conemunicacion serial
s = ser(port, bd)
s.timeout = 0
# conexion con la base de datos
conn = con('lab06DB')
c = conn.cursor()

# condiconal y aumentador
salir = False
n = 1

# loop
while not salir:
	recv = s.readline()
	c.execute("SELECT MAX(Id) FROM Tempe")
	for m in c:
		id = int(m[0])+1
	if len(recv) > 0:
		print "Tempe: "+ recv
		if recv == "salir":
			con.close()
			s.close()
			salir = True
		else:
			sql = "INSERT INTO Tempe(Id, Fecha, Tempe) VALUES("+str(id)+", date('now'),"+recv+" )"
			c.execute(sql)
			conn.commit()
	