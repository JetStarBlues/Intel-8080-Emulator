;
;	Fibonnaci Sequence
;	 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610
;
;	Code based on,
;	 https://www.youtube.com/watch?v=ERCxf3BSNMU
;	 http://8085programs.blogspot.ca/2010/12/program-to-genereate-fibonacci-sequence.html
;
;	Something akin to,
;	 https://www.youtube.com/watch?v=a73ZXDJtU48
;

      MVI B,11    ; Counter for number of items want to generate (2 + x)
      LXI H,1000  ; Memory base address where results will be stored
      MVI M,0	; Set Memory[HL] = 0
      INX H       ; HL += 1
      MVI M,1     ; Set Memory[HL] = 1
LOOP: DCX H       ; HL -= 1
      MOV A,M     ; A = Memory[HL],   A = previous fibNum
      INX H       ; HL += 1
      ADD M       ; A += Memory[HL],  A += current fibNum
      INX H       ; HL += 1
      MOV M,A     ; Memory[HL] = A,   next fibNum
      DCR B       ; decrement counter
      JNZ LOOP    ; loop if counter != zero
; DONE: HLT


; Display result ---------------------------

; Send result to IO device 0
DONE:  MOV A,M
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
