instructionLookup = {

	None : None,

	# Move, load, store ---

	# MOV R1,R2 -> 01DDDSSS -> Move register to register
	0b01000000 : 'MOV B,B',
	0b01000001 : 'MOV B,C',
	0b01000010 : 'MOV B,D',
	0b01000011 : 'MOV B,E',
	0b01000100 : 'MOV B,H',
	0b01000101 : 'MOV B,L',
	0b01000111 : 'MOV B,A',

	0b01001000 : 'MOV C,B',
	0b01001001 : 'MOV C,C',
	0b01001010 : 'MOV C,D',
	0b01001011 : 'MOV C,E',
	0b01001100 : 'MOV C,H',
	0b01001101 : 'MOV C,L',
	0b01001111 : 'MOV C,A',

	0b01010000 : 'MOV D,B',
	0b01010001 : 'MOV D,C',
	0b01010010 : 'MOV D,D',
	0b01010011 : 'MOV D,E',
	0b01010100 : 'MOV D,H',
	0b01010101 : 'MOV D,L',
	0b01010111 : 'MOV D,A',

	0b01011000 : 'MOV E,B',
	0b01011001 : 'MOV E,C',
	0b01011010 : 'MOV E,D',
	0b01011011 : 'MOV E,E',
	0b01011100 : 'MOV E,H',
	0b01011101 : 'MOV E,L',
	0b01011111 : 'MOV E,A',

	0b01100000 : 'MOV H,B',
	0b01100001 : 'MOV H,C',
	0b01100010 : 'MOV H,D',
	0b01100011 : 'MOV H,E',
	0b01100100 : 'MOV H,H',
	0b01100101 : 'MOV H,L',
	0b01100111 : 'MOV H,A',

	0b01101000 : 'MOV L,B',
	0b01101001 : 'MOV L,C',
	0b01101010 : 'MOV L,D',
	0b01101011 : 'MOV L,E',
	0b01101100 : 'MOV L,H',
	0b01101101 : 'MOV L,L',
	0b01101111 : 'MOV L,A',

	0b01111000 : 'MOV A,B',
	0b01111001 : 'MOV A,C',
	0b01111010 : 'MOV A,D',
	0b01111011 : 'MOV A,E',
	0b01111100 : 'MOV A,H',
	0b01111101 : 'MOV A,L',
	0b01111111 : 'MOV A,A',

	# MOV M,R -> 01110SSS -> Move register to memory
	0b01110000 : 'MOV M,B',
	0b01110001 : 'MOV M,C',
	0b01110010 : 'MOV M,D',
	0b01110011 : 'MOV M,E',
	0b01110100 : 'MOV M,H',
	0b01110101 : 'MOV M,L',
	0b01110111 : 'MOV M,A',

	# MOV R,M -> 01DDD110 -> Move memory to register
	0b01000110 : 'MOV B,M',
	0b01001110 : 'MOV C,M',
	0b01010110 : 'MOV D,M',
	0b01011110 : 'MOV E,M',
	0b01100110 : 'MOV H,M',
	0b01101110 : 'MOV L,M',
	0b01111110 : 'MOV A,M',

	# MVI R,data -> 00DDD110 -> Move immediate to register
	0b00000110 : 'MVI B,data',
	0b00001110 : 'MVI C,data',
	0b00010110 : 'MVI D,data',
	0b00011110 : 'MVI E,data',
	0b00100110 : 'MVI H,data',
	0b00101110 : 'MVI L,data',
	0b00111110 : 'MVI A,data',

	# MVI M,data -> 00110110 -> Move immediate to memory
	0b00110110 : 'MVI M,data',

	# LXI BC,data16 -> 00000001 -> Load immediate to register pair B & C
	0b00000001 : 'LXI BC,data16',
	# LXI DE,data16 -> 00010001 -> Load immediate to register pair D & E
	0b00010001 : 'LXI DE,data16',
	# LXI HL,data16 -> 00100001 -> Load immediate to register pair H & L
	0b00100001 : 'LXI HL,data16',
	# LXI SP,data16 -> 00110001 -> Load immediate to stack pointer
	0b00110001 : 'LXI SP,data16',

	# LDA addr -> 00111010 -> Load A direct
	0b00111010 : 'LDA addr',

	# STA addr -> 00110010 -> Store A direct
	0b00110010 : 'STA addr',

	# LHLD addr -> 00101010 -> Load H & L direct
	0b00101010 : 'LHLD addr',

	# SHLD addr -> 00100010 -> Store H & L direct
	0b00100010 : 'SHLD addr',

	# LDAX BC -> 00001010 -> Load A indirect
	# LDAX DE -> 00011010 -> Load A indirect
	0b00001010 : 'LDAX BC',
	0b00011010 : 'LDAX DE',

	# STAX BC -> 00000010 -> Store A indirect
	# STAX DE -> 00010010 -> Store A indirect
	0b00000010 : 'STAX BC',
	0b00010010 : 'STAX DE',

	# XCHG -> 11101011 -> Exchange register pair D & E with H & L
	0b11101011 : 'XCHG',


	# Stack ops ---

	# PUSH BC -> 11000101 -> Push register pair B & C on stack
	0b11000101 : 'PUSH BC',
	# PUSH DE -> 11010101 -> Push register pair D & E on stack
	0b11010101 : 'PUSH DE',
	# PUSH HL -> 11100101 -> Push register pair H & L on stack
	0b11100101 : 'PUSH HL',

	# PUSH PSW -> 11110101 -> Push A and Flags on stack
	0b11110101 : 'PUSH PSW',

	# POP BC -> 11000001 -> Pop top of stack onto register pair B & C
	0b11000001 : 'POP BC',
	# POP DE -> 11010001 -> Pop top of stack onto register pair D & E
	0b11010001 : 'POP DE',
	# POP HL -> 11100001 -> Pop top of stack onto register pair H & L
	0b11100001 : 'POP HL',

	# POP PSW  -> 11110001 -> Pop top of stack onto A and Flags
	0b11110001 : 'POP PSW',

	# XTHL -> 11100011 -> Exchange H & L with contents of location specified by stack pointer
	0b11100011 : 'XTHL',

	# SPHL -> 11111001 -> H & L to stack pointer
	0b11111001 : 'SPHL',


	# Jump ---

	# JMP addr -> 11000011 -> Jump unconditional
	0b11000011 : 'JMP addr',
	# JNZ addr -> 11000010 -> Jump on not zero
	0b11000010 : 'JNZ addr',
	# JZ addr -> 11001010 -> Jump on zero
	0b11001010 : 'JZ addr',
	# JNC addr -> 11010010 -> Jump on no carry
	0b11010010 : 'JNC addr',
	# JC addr -> 11011010 -> Jump on carry
	0b11011010 : 'JC addr',
	# JPO addr -> 11100010 -> Jump on parity odd
	0b11100010 : 'JPO addr',
	# JPE addr -> 11101010 -> Jump on parity even
	0b11101010 : 'JPE addr',
	# JP addr -> 11110010 -> Jump on positive
	0b11110010 : 'JP addr',
	# JM addr -> 11111010 -> Jump on minus
	0b11111010 : 'JM addr',

	# PCHL -> 11101001 -> H & L to program counter
	0b11101001 : 'PCHL',


	# Call ---

	# CALL addr -> 11001101 -> Call unconditional
	0b11001101 : 'CALL addr',
	# CNZ addr -> 11000100 -> Call on not zero
	0b11000100 : 'CNZ addr',
	# CZ addr -> 11001100 -> Call on zero
	0b11001100 : 'CZ addr',
	# CNC addr -> 11010100 -> Call on no carry
	0b11010100 : 'CNC addr',
	# CC addr -> 11011100 -> Call on carry
	0b11011100 : 'CC addr',
	# CPO addr -> 11100100 -> Call on parity odd
	0b11100100 : 'CPO addr',
	# CPE addr -> 11101100 -> Call on parity even
	0b11101100 : 'CPE addr',
	# CP addr -> 11110100 -> Call on positive
	0b11110100 : 'CP addr',
	# CM addr -> 11111100 -> Call on minus
	0b11111100 : 'CM addr',


	# Return ---

	# RET -> 11001001 -> Return unconditional
	0b11001001 : 'RET',
	# RNZ -> 11000000 -> Return on not zero
	0b11000000 : 'RNZ',
	# RZ -> 11001000 -> Return on zero
	0b11001000 : 'RZ',
	# RNC -> 11010000 -> Return on no carry
	0b11010000 : 'RNC',
	# RC -> 11011000 -> Return on carry
	0b11011000 : 'RC',
	# RPO -> 11100000 -> Return on parity odd
	0b11100000 : 'RPO',
	# RPE -> 11101000 -> Return on parity even
	0b11101000 : 'RPE',
	# RP -> 11110000 -> Return on positive
	0b11110000 : 'RP',
	# RM -> 11111000 -> Return on minus
	0b11111000 : 'RM',


	# Restart ---

	# RST -> 11NNN111 -> Restart
	0b11000111 : 'RST 0',
	0b11001111 : 'RST 1',
	0b11010111 : 'RST 2',
	0b11011111 : 'RST 3',
	0b11100111 : 'RST 4',
	0b11101111 : 'RST 5',
	0b11110111 : 'RST 6',
	0b11111111 : 'RST 7',

	# Increment and decrement ---

	# INR R -> 00DDD100 -> Increment register
	0b00000100 : 'INR B',
	0b00001100 : 'INR C',
	0b00010100 : 'INR D',
	0b00011100 : 'INR E',
	0b00100100 : 'INR H',
	0b00101100 : 'INR L',
	0b00111100 : 'INR A',

	# INR M -> 00110100 -> Increment memory
	0b00110100 : 'INR M',

	# INX BC -> 00000011 -> Increment B & C registers
	0b00000011 : 'INX BC',
	# INX DE -> 00010011 -> Increment D & E registers
	0b00010011 : 'INX DE',
	# INX HL -> 00100011 -> Increment H & L registers
	0b00100011 : 'INX HL',
	# INX SP -> 00110011 -> Increment stack pointer
	0b00110011 : 'INX SP',

	# DCR R -> 00DDD101 -> Decrement register
	0b00000101 : 'DCR B',
	0b00001101 : 'DCR C',
	0b00010101 : 'DCR D',
	0b00011101 : 'DCR E',
	0b00100101 : 'DCR H',
	0b00101101 : 'DCR L',
	0b00111101 : 'DCR A',

	# DCR M -> 00110101 -> Decrement memory
	0b00110101 : 'DCR M',

	# DCX BC -> 00001011 -> Decrement B & C registers
	0b00001011 : 'DCX BC',
	# DCX DE -> 00011011 -> Decrement D & E registers
	0b00011011 : 'DCX DE',
	# DCX HL -> 00101011 -> Decrement H & L registers
	0b00101011 : 'DCX HL',
	# DCX SP -> 00111011 -> Decrement stack pointer
	0b00111011 : 'DCX SP',


	# Add ---

	# ADD R -> 10000SSS -> Add register to A
	0b10000000 : 'ADD B',
	0b10000001 : 'ADD C',
	0b10000010 : 'ADD D',
	0b10000011 : 'ADD E',
	0b10000100 : 'ADD H',
	0b10000101 : 'ADD L',
	0b10000111 : 'ADD A',

	# ADD M -> 10000110 -> Add memory to A
	0b10000110 : 'ADD M',

	# ADI data -> 11000110 -> Add immediate to A
	0b11000110 : 'ADI data',

	# ADC R -> 10001SSS -> Add register to A with carry
	0b10001000 : 'ADC B',
	0b10001001 : 'ADC C',
	0b10001010 : 'ADC D',
	0b10001011 : 'ADC E',
	0b10001100 : 'ADC H',
	0b10001101 : 'ADC L',
	0b10001111 : 'ADC A',

	# ADC M -> 10001110 -> Add memory to A with carry
	0b10001110 : 'ADC M',

	# ACI data -> 11001110 -> Add immediate to A with carry
	0b11001110 : 'ACI data',

	# DAD BC -> 00001001 -> Add B & C to H & L
	0b00001001 : 'DAD BC',
	# DAD DE -> 00011001 -> Add D & E to H & L
	0b00011001 : 'DAD DE',
	# DAD HL -> 00101001 -> Add H & L to H & L
	0b00101001 : 'DAD HL',
	# DAD SP -> 00111001 -> Add stack pointer to H & L
	0b00111001 : 'DAD SP',


	# Subtract ---

	# SUB R -> 10010SSS -> Subtract register from A
	0b10010000 : 'SUB B',
	0b10010001 : 'SUB C',
	0b10010010 : 'SUB D',
	0b10010011 : 'SUB E',
	0b10010100 : 'SUB H',
	0b10010101 : 'SUB L',
	0b10010111 : 'SUB A',

	# SUB M -> 10010110 -> Subtract memory from A
	0b10010110 : 'SUB M',

	# SUI data -> 11010110 -> Subtract immediate from A
	0b11010110 : 'SUI data',

	# SBB R -> 10011SSS -> Subtract register from A with borrow
	0b10011000 : 'SBB B',
	0b10011001 : 'SBB C',
	0b10011010 : 'SBB D',
	0b10011011 : 'SBB E',
	0b10011100 : 'SBB H',
	0b10011101 : 'SBB L',
	0b10011111 : 'SBB A',

	# SBB M -> 10011110 -> Subtract memory from A with borrow
	0b10011110 : 'SBB M',

	# SBI data -> 11011110 -> Subtract immediate from A with borrow
	0b11011110 : 'SBI data',


	# Logical ---
	
	# ANA R -> 10100SSS -> And register with A
	0b10100000 : 'ANA B',
	0b10100001 : 'ANA C',
	0b10100010 : 'ANA D',
	0b10100011 : 'ANA E',
	0b10100100 : 'ANA H',
	0b10100101 : 'ANA L',
	0b10100111 : 'ANA A',

	# ANA M -> 10100110 -> And memory with A
	0b10100110 : 'ANA M',

	# ANI data -> 11100110 -> And immediate with A
	0b11100110 : 'ANI data',

	# XRA R -> 10101SSS -> Exclusive or register with A
	0b10101000 : 'XRA B',
	0b10101001 : 'XRA C',
	0b10101010 : 'XRA D',
	0b10101011 : 'XRA E',
	0b10101100 : 'XRA H',
	0b10101101 : 'XRA L',
	0b10101111 : 'XRA A',

	# XRA M -> 10101110 -> Exclusive or memory with A
	0b10101110 : 'XRA M',

	# XRI data -> 11101110 -> Exclusive or immediate with A
	0b11101110 : 'XRI data',

	# ORA R -> 10110SSS -> Or register with A
	0b10110000 : 'ORA B',
	0b10110001 : 'ORA C',
	0b10110010 : 'ORA D',
	0b10110011 : 'ORA E',
	0b10110100 : 'ORA H',
	0b10110101 : 'ORA L',
	0b10110111 : 'ORA A',

	# ORA M -> 10110110 -> Or memory with A
	0b10110110 : 'ORA M',

	# ORI data -> 11110110 -> Or immediate with A
	0b11110110 : 'ORI data',

	# CMP R -> 10111SSS -> Compare register with A
	0b10111000 : 'CMP B',
	0b10111001 : 'CMP C',
	0b10111010 : 'CMP D',
	0b10111011 : 'CMP E',
	0b10111100 : 'CMP H',
	0b10111101 : 'CMP L',
	0b10111111 : 'CMP A',

	# CMP M -> 10111110 -> Compare memory with A
	0b10111110 : 'CMP M',

	# CPI data -> 11111110 -> Compare immediate with A
	0b11111110 : 'CPI data',


	# Rotate ---

	# RLC -> 00000111 -> Rotate A left
	0b00000111 : 'RLC',
	# RRC -> 00001111 -> Rotate A right
	0b00001111 : 'RRC',
	# RAL -> 00010111 -> Rotate A left through carry
	0b00010111 : 'RAL',
	# RAR -> 00011111 -> Rotate A right through carry
	0b00011111 : 'RAR',


	# Specials ---

	# CMA -> 00101111 -> Complement A
	0b00101111 : 'CMA',
	# CMC -> 00111111 -> Complement carry
	0b00111111 : 'CMC',
	# STC -> 00110111 -> Set carry
	0b00110111 : 'STC',
	# DAA -> 00100111 -> Decimal adjust A
	0b00100111 : 'DAA',

	# Input / Output ---

	# IN port -> 11011011 -> Input
	0b11011011 : 'IN',
	# OUT port -> 11010011 -> Output
	0b11010011 : 'OUT',


	# Control ---

	# EI -> 11111011 -> Enable interrupts
	0b11111011 : 'EI',
	# DI -> 11110011 -> Disable interrupt
	0b11110011 : 'DI',
	# HLT -> 01110110 -> Halt
	0b01110110 : 'HLT',
	# NOP -> 00000000 -> No operation
	0b00000000 : 'NOP',
}


instructionsWithData = {

	# MVI R,data -> 00DDD110 -> Move immediate to register
	'MVI B,data' : 1,
	'MVI C,data' : 1,
	'MVI D,data' : 1,
	'MVI E,data' : 1,
	'MVI H,data' : 1,
	'MVI L,data' : 1,
	'MVI A,data' : 1,

	'MVI M,data' : 1,

	'LXI BC,data16' : 2,
	'LXI DE,data16' : 2,
	'LXI HL,data16' : 2,
	'LXI SP,data16' : 2,

	'LDA addr'  : 2,
	'STA addr'  : 2,
	'LHLD addr' : 2,
	'SHLD addr' : 2,

	'JMP addr' : 2,
	'JNZ addr' : 2,
	'JZ addr'  : 2,
	'JNC addr' : 2,
	'JC addr'  : 2,
	'JPO addr' : 2,
	'JPE addr' : 2,
	'JP addr'  : 2,
	'JM addr'  : 2,

	'CALL addr' : 2,
	'CNZ addr'  : 2,
	'CZ addr'   : 2,
	'CNC addr'  : 2,
	'CC addr'   : 2,
	'CPO addr'  : 2,
	'CPE addr'  : 2,
	'CP addr'   : 2,
	'CM addr'   : 2,

	'ADI data' : 1,
	'ACI data' : 1,
	'SUI data' : 1,
	'SBI data' : 1,
	'ANI data' : 1,
	'XRI data' : 1,
	'ORI data' : 1,

	'CPI data' : 1,
}
