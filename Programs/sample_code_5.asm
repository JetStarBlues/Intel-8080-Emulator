;
;	16 bit subtraction
;	Enabled by 'subtract with borrow'
;
;	Based on,
;	 http://www.8052.com/subb16.phtml
;

LXI B,22DBH     ; Load the first value into BC
LXI D,1AF9H     ; Load the second value into DE
STC             ; Always clear carry before first subtraction
CMC
MOV A,C         ; Move the low-byte into the accumulator
SBB E           ; Subtract the second low-byte from the accumulator
MOV L,A         ; Move the answer to the low-byte of the result
MOV A,B         ; Move the high-byte into the accumulator
SBB D           ; Subtract the second high-byte from the accumulator
MOV H,A         ; Move the answer to the high-byte of the result
; HLT


; Display result ---------------------------

; Send result to IO device 0
DONE:  MOV  A,H  ; send z hi byte (7)
       CALL BYTEO
       MOV  A,L  ; send z lo byte (226)
       CALL BYTEO
       HLT


; Print number as ASCII snippet. From,
;  MICROCOSM ASSOCIATES  8080/8085 CPU DIAGNOSTIC VERSION 1.0  (C) 1980
PCHAR: OUT  0
       RET

BYTEO: PUSH PSW
       CALL BYTO1
       CALL PCHAR
       POP  PSW
       CALL BYTO2
       JMP  PCHAR
BYTO1: RRC
       RRC
       RRC
       RRC
BYTO2: ANI  0FH
       CPI  0AH
       JM   BYTO3
       ADI  7
BYTO3: ADI  30H
       RET
