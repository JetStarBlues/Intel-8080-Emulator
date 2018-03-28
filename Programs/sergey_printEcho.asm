; ------------------------------------------------------------------------
; From http://www.malinov.com/Home/sergeys-projects/minimax8085
;
; USART (8251) test code
;  Prints "8085" to the serial port, and then echoes received characters.
; ------------------------------------------------------------------------

; USART registers
USART_DATA EQU 08h
USART_CMD  EQU 09h

START:

	LXI H, 0C000h   ; Load 0xC0000 to stack pointer?
	SPHL
	CALL USART_INIT

; Send '8085' to serial port
BANNER:

	MVI 	A, 38h  ; '8'
	MOV 	C, A
	CALL	USART_OUT
	MVI 	A, 30h  ; '0'
	MOV 	C, A
	CALL	USART_OUT
	MVI 	A, 38h  ; '8'
	MOV 	C, A
	CALL	USART_OUT
	MVI 	A, 35h  ; '5'
	MOV 	C, A
	CALL	USART_OUT
	MVI 	A, 0Dh  ; CR
	MOV 	C, A
	CALL	USART_OUT
	MVI 	A, 0Ah  ; LF
	MOV 	C, A
	CALL	USART_OUT

; Echo characters received from serial port
ECHO_LOOP:

	CALL 	USART_IN
	MOV 	C, A
	CALL	USART_OUT
	JMP 	ECHO_LOOP

; Initialize 8251 USART
USART_INIT:

	; Set USART to command mode - configure sync operation, write two dumy sync characters
	MVI 	A, 00h
	OUT 	USART_CMD
	OUT 	USART_CMD
	OUT 	USART_CMD

	; Issue reset command
	MVI 	A, 40h
	OUT 	USART_CMD

	; Write mode instruction - 1 stop bit, no parity, 8bits, divide clock by 16
	MVI 	A, 4Eh
	OUT 	USART_CMD

	; Write command instruction - activate RTS, reset error flags, enable RX, activate DTR, enable TX
	MVI 	A, 37h
	OUT 	USART_CMD

	; Clear the data register
	IN  	USART_DATA
	RET

; Read character from USART
USART_IN:

	IN  	USART_CMD   ; Read USART status
	ANI 	2           ; Test RX_ready bit
	JZ  	USART_IN    ; If zero, retry (wait till the data is ready)
	IN  	USART_DATA  ; Else, read the character/data
	RET

; Write character to USART
USART_OUT:

	IN  	USART_CMD  ; Read USART status
	ANI 	1          ; Test TX_ready bit
	JZ  	USART_OUT  ; If zero, wait till ready
	MOV 	A, C       ; Else, write the character
	OUT 	USART_DATA
	RET
