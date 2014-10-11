	;#terminal 9600    			; Use the terminal for display

main: pulsin B.4,1, b0				; Read IR key press
	sertxd( "Key code = ", #b0, cr, lf )	; Report which key was pressed
	goto main   					; Repeat
