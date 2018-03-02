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

SETUP:			MVI  D,3             ; load with number of bytes
				CALL MULTIBYTE_ADD
				HLT

MULTIBYTE_ADD:	LXI  B,FIRST         ; load address FIRST to BC
				LXI  H,SECOND        ; load address SECOND to HL
				XRA  A               ; clear carry bit

LOOP:		    LDAX B               ; load byte of FIRST to A
				SBB  M               ; add with carry byte of SECOND
				STAX B               ; store result at FIRST
				DCR  D               ; done if D = 0
				JZ   DONE
				INX  B               ; point to next byte of FIRST
				INX  H               ; point to next byte of SECOND
				JMP  LOOP            ; add next two bytes
; DONE:			RET

; put z in A reg, then
; send contents of A reg to IO device 0
DONE:  LXI H,FIRST+2  ; send z first byte
       MOV A,M
       OUT 0
       LXI H,FIRST+1  ; send z second byte
       MOV A,M
       OUT 0
       LXI H,FIRST    ; send z third byte
       MOV A,M
       OUT 0
       RET


SECOND: DB 8AH
        DB 0AFH
        DB 32H

FIRST:  DB 90H
        DB 0BAH
        DB 84H


;
;	Final Binary
;
; 00010110  // MVI D, 3
; 00000011
; 11001101  // CALL MULTIBYTE_ADD
; 00000110  //  6
; 00000000
; 01110110  // HLT
; 00000001  // LXI BC, FIRST  // FIRST = 0
; 00000000
; 00000000
; 00100001  // LXI HL, SECOND  // SECOND = 10
; 00001010
; 00000000
; 10101111  // XRA A
; 00001010  // LDAX BC
; 10011110  // SBB M
; 00000010  // STAX BC
; 00010101  // DCR D
; 11001010  // JZ DONE
; 00011001  //  25
; 00000000
; 00000011  // INX BC
; 00100011  // INX HL
; 11000011  // JMP MADD_LOOP
; 00001101  //  13
; 00000000
; 11001001  // RET