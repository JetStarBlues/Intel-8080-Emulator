; Test carry...

; MVI A,80
; SBI 40

; MVI A,40
; SBI 80

; MVI A,10
; MVI A,229
; MVI D,5
; CMP D

;MVI A,170
;RAL

; CMC
; MVI A,14H
; ACI 66

; CMC
; MVI C,3DH
; MVI A,42H
; ADC C

; MVI A,6CH
; MVI D,2EH
; ADD D

; MVI A,5
; CPI 4
; CPI 5
; CPI 6

; LXI SP,999
; LXI H,0
; DAD SP

; move chunk from one area to another
;       MVI  B,7        ; set counter
;       LXI  H,SOURCE+6 ; load HL with source addr
;       LXI  D,DEST+6   ; Load DE with dest addr
; LOOP: MOV  A,M        ; load byte to be moved
;       STAX D          ; store byte
;       DCX  D          ; decrement dest addr
;       DCX  H          ; decrement source addr
;       DCR  B          ; decrement counter
;       JNZ  LOOP

LXI SP,10ADH
MVI H,0BH
MVI L,3CH
XTHL

HLT



; ORG 200
; SOURCE: DB 'B'
;         DB 'O'
;         DB 'N'
;         DB 'J'
;         DB 'O'
;         DB 'U'
;         DB 'R'
; ORG 300
; DEST: NOP

ORG 10ADH
DB 0F0H
DB 0DH
