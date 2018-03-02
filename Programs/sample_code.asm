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
       JZ DONE
       MOV A,B
       JNC MULT1
       ADD D
MULT1: RAR
       MOV B,A
       JMP MULT0
; DONE:  HLT

; put z in A reg, then
; send contents of A reg to IO device 0
DONE:  MOV A,B
       OUT 0    ; send z hi byte (9)
       MOV A,C
       OUT 0    ; send z lo byte (216)
       HLT


;
;	Final Binary
;
; 00010110  // MVI D, 42
; 00101010
; 00001110  // MVI C, 60
; 00111100
; 00000110  // MVI B, 0
; 00000000
; 00011110  // MVI E, 9
; 00001001
; 01111001  // MOV A, C
; 00011111  // RAR
; 01001111  // MOV C, A
; 00011101  // DCR E
; 11001010  // JZ DONE
; 00011001  //  25
; 00000000
; 01111000  // MOV A, B
; 11010010  // JNC MULT1
; 00010100  //  20
; 00000000
; 10000010  // ADD D
; 00011111  // RAR
; 01000111  // MOV B, A
; 11000011  // JMP MULT0
; 00001000  //  8
; 00000000
; 01110110  // HLT