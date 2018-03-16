;
;	Multiply using shift
;	As seen on pg.54 of 8080 Programming Manual
;	x . y = z
;	x -> D
;	y -> C
;	z -> BC
;

       MVI D,42  ; Load x
       MVI C,60  ; Load y
MULT:  MVI B,0
       MVI E,9
MULT0: MOV A,C
       RAR
       MOV C,A
       DCR E
       JZ  DONE
       MOV A,B
       JNC MULT1
       ADD D
MULT1: RAR
       MOV B,A
       JMP MULT0
; DONE:  HLT


; Display result ---------------------------

; Send result to IO device 0
DONE:  MOV  A,B
       ; OUT  0    ; send z hi byte (9)
       CALL BYTEO
       MOV  A,C
       ; OUT  0    ; send z lo byte (216)
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
