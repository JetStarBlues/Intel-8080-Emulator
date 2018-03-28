; -----------------------------------------------------
; From http://www.malinov.com/Home/sergeys-projects/minimax8085
;
; Blink a LED on SOD?
; -----------------------------------------------------

START:

	LXI H, 0C000h   ; Load 0xc0000 to stack pointer?
	SPHL

FLASH:

	MVI A, 0C0h  ; ??
	SIM          ; set interrupt mask??
	CALL DELAY
	MVI A, 040h  ; ??
	SIM          ; ??
	CALL DELAY
	JMP FLASH

DELAY:
	
	MVI A, 0FFh
	MOV B, A

PT1:

	DCR A

PT2:
	
	DCR B
	JNZ PT2
	CPI 00h
	JNZ PT1
	RET	     ; Return to HL when done ??
