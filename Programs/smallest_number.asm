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
       HLT


ORG 4200

ARR: DB 5     ; size
     DB 0AH
     DB 0F1H
     DB 1FH
     DB 26H
     DB 07H

ORG 4300

OUT: DS 1
