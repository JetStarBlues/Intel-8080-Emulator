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

      MVI B,12    ; Counter for number of items want to generate (2 + x)
      LXI H,0     ; Memory base address where results will be stored
      MVI M,0	  ; Set Memory[HL] = 0
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
      HLT

;
;	Final Binary
;
; 00000110  // MVI B, 12
; 00001100
; 00100001  // LXI HL, 0
; 00000000
; 00000000
; 00110110  // MVI M, 0
; 00000000
; 00100011  // INX HL
; 00110110  // MVI M, 1
; 00000001
; 00101011  // DCX HL
; 01111110  // MOV A, M
; 00100011  // INX HL
; 10000110  // ADD M
; 00100011  // INX HL
; 01110111  // MOV M, A
; 00000101  // DCR B
; 11000010  // JNZ LOOP
; 00001010  // 10
; 00000000
; 01110110  // HLT
