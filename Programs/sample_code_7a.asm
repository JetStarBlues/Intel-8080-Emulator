/*
	Multibyte subtraction
	Enabled by 'subtract with carry'

	As seen on pg.55 of 8080 Programming Manual

	B1B2B3..BX + B1B2B3..BX
	
	The D register holds the number of bytes per number.
	The numbers to be added are stored from low-order to
	high-order byte at memory locations FIRST and SECOND
	E.g. 32AF8A + 84BA90
	     M[FIRST + 0] = 8A
	     M[FIRST + 1] = AF
	     M[FIRST + 2] = 32
	The result is stored at M[FIRST]
*/

SETUP:			MVI  D, 3            ; load with number of bytes
				CALL MULTIBYTE_ADD
				HLT
MULTIBYTE_ADD:	LXI  B,  0           ; load address FIRST to BC
				LXI  H, 10           ; load address SECOND to HL
				XRA  A               ; clear carry bit
MADD_LOOP:		LDAX B               ; load byte of FIRST to A
				SBB  M               ; add with carry byte of SECOND
				STAX B               ; store result at FIRST
				DCR  D               ; done if D = 0
				JZ   DONE
				INX  B               ; point to next byte of FIRST
				INX  H               ; point to next byte of SECOND
				JMP  MADD_LOOP       ; add next two bytes
DONE:			RET
