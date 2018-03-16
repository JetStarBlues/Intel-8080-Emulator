; http://8085-programs.blogspot.ca/2012/07/smallest-number-in-array-of-data.html

       LXI H,ARR    ;Set pointer for array
       MOV B,M      ;Load the Count
       INX  H       ;Set 1st element as largest data
       MOV A,M
       DCR B        ;Decremented the count
LOOP:  INX H
       CMP M        ;If A- reg < M go to AHEAD
       JC AHEAD
       MOV A,M      ;Set the new value as smallest
AHEAD: DCR B
       JNZ LOOP     ;Repeat comparisons till count = 0
       STA OUT      ;Store the largest value at 4300
; DONE:  HLT


; Display result ---------------------------

; Send result to IO device 0
DONE:  LXI  H,4300
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


; -------------------------------------------

ORG 4200

ARR: DB 5     ; size
     DB 0AH
     DB 0F1H
     DB 1FH
     DB 26H
     DB 07H

ORG 4300

OUT: DS 1
