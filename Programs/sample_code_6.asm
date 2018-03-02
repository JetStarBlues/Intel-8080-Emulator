;
;	Multibyte addition
;	Enabled by 'add with carry'
;
;	As seen on pg.55 of 8080 Programming Manual
;
;	B1B2B3..BX + B1B2B3..BX
;	
;	The D register holds the number of bytes per number.
;	The numbers to be added are stored from low-order to
;	high-order byte at memory locations FIRST and SECOND
;	E.g. 32AF8A + 84BA90 = B76A1A
;	     M[FIRST + 0] = 1A
;	     M[FIRST + 1] = 6A
;	     M[FIRST + 2] = B7
;	The result is stored at M[FIRST]
;

FIRST EQU 0
SECOND EQU 10

INIT:          MVI D,3         ; load with number of bytes

               LXI H,FIRST     ; first number
               MVI M,8AH
               LXI H,FIRST+1
               MVI M,0AFH
               LXI H,FIRST+2
               MVI M,32H

               LXI H,SECOND     ; second number
               MVI M,90H
               LXI H,SECOND+1
               MVI M,0BAH
               LXI H,SECOND+2
               MVI M,84H

MULTIBYTE_ADD: LXI B,FIRST     ; load address FIRST to BC
               LXI H,SECOND    ; load address SECOND to HL
               XRA A           ; clear carry bit

LOOP:          LDAX B          ; load byte of FIRST to A
               ADC M           ; add with carry byte of SECOND
               STAX B          ; store result at FIRST
               DCR D           ; done if D = 0
               JZ DONE
               INX B           ; point to next byte of FIRST
               INX H           ; point to next byte of SECOND
               JMP LOOP        ; add next two bytes
; DONE:          HLT


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
       HLT


;
;	Final Binary
;
; 00010110  // MVI D, 3
; 00000011
; 00000001  // LXI BC, FIRST  // FIRST = 0
; 00000000
; 00000000
; 00100001  // LXI HL, SECOND  // SECOND = 10
; 00001010
; 00000000
; 10101111  // XRA A
; 00001010  // LDAX BC
; 10001110  // ADC M
; 00000010  // STAX BC
; 00010101  // DCR D
; 11001010  // JZ DONE
; 00010101  //  21
; 00000000
; 00000011  // INX BC
; 00100011  // INX HL
; 11000011  // JMP LOOP
; 00001001  //  9
; 00000000
; 01110110  // HLT
