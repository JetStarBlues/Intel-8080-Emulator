;
;	Multibyte subtraction
;	Enabled by 'subtract with borrow'
;
;	As seen on pg.55 of 8080 Programming Manual
;
;	B1B2B3..BX + B1B2B3..BX
;	
;	The D register holds the number of bytes per number.
;	The numbers to be added are stored from low-order to
;	high-order byte at memory locations FIRST and SECOND
;	E.g. 84BA90 - 32AF8A = 520B06
;	     M[FIRST + 0] = 06
;	     M[FIRST + 1] = 0B
;	     M[FIRST + 2] = 52
;	E.g. 32AF8A - 84BA90 = ?? (twos complement)
;	     M[FIRST + 0] = ??
;	     M[FIRST + 1] = ??
;	     M[FIRST + 2] = ??
;	The result is stored at M[FIRST]
;

SETUP:         MVI  D,3             ; load with number of bytes
               CALL MULTIBYTE_ADD
               HLT

MULTIBYTE_ADD: LXI  B,FIRST         ; load address FIRST to BC
               LXI  H,SECOND        ; load address SECOND to HL
               XRA  A               ; clear carry bit

LOOP:          LDAX B               ; load byte of FIRST to A
               SBB  M               ; add with carry byte of SECOND
               STAX B               ; store result at FIRST
               DCR  D               ; done if D = 0
               JZ   DONE
               INX  B               ; point to next byte of FIRST
               INX  H               ; point to next byte of SECOND
               JMP  LOOP            ; add next two bytes
; DONE:	         RET


; Display result ---------------------------

; Send result to IO device 0
DONE:  LXI  H,FIRST+2  ; send z first byte
       MOV  A,M
       CALL BYTEO
       DCX  H          ; send z second byte
       MOV  A,M
       CALL BYTEO
       DCX  H          ; send z third byte
       MOV  A,M
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


; ----------------------------------------

SECOND: DB 8AH
        DB 0AFH
        DB 32H

FIRST:  DB 90H
        DB 0BAH
        DB 84H
