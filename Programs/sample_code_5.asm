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

; put z in A reg, then
; send contents of A reg to IO device 0
DONE:  MOV A,H
       OUT 0    ; send z hi byte (7)
       MOV A,L
       OUT 0    ; send z lo byte (226)
       HLT


;
;	Final Binary
;
; 00000001  // LXI BC, 0x22DB
; 11011011
; 00100010
; 00010001  // LXI DE, 0x1AF9
; 11111001
; 00011010
; 00110111  // STC
; 00111111  // CMC
; 01111001  // MOV A, C
; 10011011  // SBB E
; 01101111  // MOV L, A
; 01111000  // MOV A, B
; 10011010  // SBB D
; 01100111  // MOV H, A
; 01110110  // HLT
