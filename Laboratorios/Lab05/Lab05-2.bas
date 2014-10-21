low B.4     			; activa modo escritura
low B.6
for b0 = 0 to 9        
	readadc B.5, b1   	; lee el LDR - Luz
	readtemp B.7, b2  	; lee el DS18B20 - Temp
	i2cslave %10100110, i2cfast, i2cbyte	; set Banco 3
	writei2c b0, (b1)        ; escribe 
	pause 20    		; pausa para escribir
	i2cslave %10101010, i2cfast, i2cbyte	; set Banco 5
	writei2c b0, (b2)       ; escribe        	
	pause 500  
next b0

envia:
	high B.6    		; enciende LED Verde
	for b0 = 0 to 9
		i2cslave %10100110, i2cfast, i2cbyte	; set Banco 3
		readi2c b0, (b1)
		i2cslave %10101010, i2cfast, i2cbyte	; set Banco 5
		readi2c b0, (b2)  
		pause 100 
		sertxd("L", #b1, "*")       		; envia registro de LDR
		sertxd("D", #b2, "*")     		; envia registro de DS18B20
		pause 200
	next b0
	sertxd("FIN*" ,13, 10)      	; envia fin de los registros
low B.6
pause 10000
	
goto envia
end