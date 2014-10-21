	;#terminal 9600    			; Use the terminal for display

main: irin B.4, b0				; Read IR key press
	sertxd( #b0)	; Report which key was pressed
	pause 500
	goto main   					; Repeat