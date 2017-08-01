from computer import *

g = Computer()
c = g.CPU


'''
# print( c.negate( 1 ) )

for i in [ 127, 126, 2, 1, 0, 255, 254, 130, 129, 128 ]:

	print( '{:<6}{}'.format( i, c.negate( i ) ) )
'''

'''
print( c.negate( 130 )  )
print( c.negate( 130 ) & c.negativeOne )
print( ( - 130 ) & c.negativeOne )
'''

'''
g.dataMemory.write( 0, 'kame' )
g.dataMemory.write( 1, 'hameha' )

print( c.read_M(1) )

c.write_M( 3, 'wave' )

print( g.dataMemory.registers [ 0:5 ] )
'''

'''
c.write_A( 100 )
c.flagALU_carry = 1
c.register_BC.writeUpperByte( 155 )
c.register_HL.write(2)
c.write_M( c.register_HL.read(), 140 )

# c.ADD_R( c.register_BC, True )
# c.ADC_R( c.register_BC, True )
c.ADD_M()
print( c.read_A() )
'''

'''
print( '---' )
x = 2 - 128
y = 2 + c.negate( 128 )
print( x )
print( y )
print( x & 0xff )
print( c.negate( x ) )
print( '---' )
c.updateALUFlags( x )
print( '---' )
c.updateALUFlags( y )
'''

'''
# c.write_A( 2 )
c.write_A( 64 )
c.flagALU_carry = 1
print( bin( c.read_A() )[2:].zfill( c.nBits ), c.flagALU_carry )
# c.RRC()
# c.RAR()
# c.RLC()
c.RAL()
print( bin( c.read_A() )[2:].zfill( c.nBits ), c.flagALU_carry )
'''

program_0 = [
		
	# Multiply using shift
	# As seen on pg.54 of 8080 Programming Manual
	# x . y = z
	# x -> D
	# y -> C
	# z -> BC
	0b00010110,  # MVI D, 42
	0b00101010,
	0b00001110,  # MVI C, 60
	0b00111100,
	0b00000110,  # MVI B, 0
	0b00000000,
	0b00011110,  # MVI E, 9
	0b00001001,
	0b01111001,  # MOV A, C
	0b00011111,  # RAR
	0b01001111,  # MOV C, A
	0b00011101,  # DCR E
	0b11001010,  # JZ DONE
	0b00011001,  #  25
	0b00000000,
	0b01111000,  # MOV A, B
	0b11010010,  # JNC MULT1
	0b00010100,  #  20
	0b00000000,
	0b10000010,  # ADD D
	0b00011111,  # RAR
	0b01000111,  # MOV B, A
	0b11000011,  # JMP MULT0
	0b00001000,  #  8
	0b00000000,
	0b01110110,  # HLT
]
def printOutput_0():

	print( '>>', c.register_BC.read() )

program_1 = [

	# Fibonnaci Sequence
	#  0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610
	0b00000110,  # MVI B, 12
	0b00001100,
	0b00100001,  # LXI HL, 0
	0b00000000,
	0b00000000,
	0b00110110,  # MVI M, 0
	0b00000000,
	0b00100011,  # INX HL
	0b00110110,  # MVI M, 1
	0b00000001,
	0b00101011,  # DCX HL
	0b01111110,  # MOV A, M
	0b00100011,  # INX HL
	0b10000110,  # ADD M
	0b00100011,  # INX HL
	0b01110111,  # MOV M, A
	0b00000101,  # DCR B
	0b11000010,  # JNZ LOOP
	0b00001010,  # 10
	0b00000000,
	0b01110110,  # HLT
]
def printOutput_1():

	b = 0  # memory base location for results
	n = 12 # n items
	for i in range( 2 + n ):
		print( '>>', c.read_M( b + i ) )

program_2 = [

	# 16 bit subtraction
	# Enabled by 'subtract with borrow'
	0b00000001,  # LXI BC, 0x22DB
	0b11011011,
	0b00100010,
	0b00010001,  # LXI DE, 0x1AF9
	0b11111001,
	0b00011010,
	0b00110111,  # STC
	0b00111111,  # CMC
	0b01111001,  # MOV A, C
	0b10011011,  # SBB E
	0b01101111,  # MOV L, A
	0b01111000,  # MOV A, B
	0b10011010,  # SBB D
	0b01100111,  # MOV H, A
	0b01110110,  # HLT
]
def printOutput_2():

	print( '>>', c.register_HL.read() )

program_3 = [

	# Multibyte addition
	# Enabled by 'add with carry'
	# As seen on pg.55 of 8080 Programming Manual
	0b00010110,  # MVI D, 3
	0b00000011,
	0b00000001,  # LXI BC, FIRST  # FIRST = 0
	0b00000000,
	0b00000000,
	0b00100001,  # LXI HL, SECOND  # SECOND = 10
	0b00001010,
	0b00000000,
	0b10101111,  # XRA A
	0b00001010,  # LDAX BC
	0b10001110,  # ADC M
	0b00000010,  # STAX BC
	0b00010101,  # DCR D
	0b11001010,  # JZ DONE
	0b00010101,  #  21
	0b00000000,
	0b00000011,  # INX BC
	0b00100011,  # INX HL
	0b11000011,  # JMP LOOP
	0b00001001,  #  9
	0b00000000,
	0b01110110,  # HLT
]
def init_3():
	
	c.write_M( 0, 0x8a )
	c.write_M( 1, 0xaf )
	c.write_M( 2, 0x32 )

	c.write_M( 10, 0x90 )
	c.write_M( 11, 0xba )
	c.write_M( 12, 0x84 )

def printOutput_3():

	b = 0
	n = 3
	out = 0
	for i in range( n ):
		by = c.read_M( b + i )
		print( '>', by )
		out |= by << 8 * i
	print( '>>', out )

program_4 = [

	# Multibyte subtraction
	# Enabled by 'subtract with borrow'
	# As seen on pg.55 of 8080 Programming Manual
	0b00010110,  # MVI D, 3
	0b00000011,
	0b00000001,  # LXI BC, FIRST  # FIRST = 0
	0b00000000,
	0b00000000,
	0b00100001,  # LXI HL, SECOND  # SECOND = 10
	0b00001010,
	0b00000000,
	0b10101111,  # XRA A
	0b00001010,  # LDAX BC
	0b10011110,  # SBB M
	0b00000010,  # STAX BC
	0b00010101,  # DCR D
	0b11001010,  # JZ DONE
	0b00010101,  #  21
	0b00000000,
	0b00000011,  # INX BC
	0b00100011,  # INX HL
	0b11000011,  # JMP LOOP
	0b00001001,  #  9
	0b00000000,
	0b01110110,  # HLT
]
def init_4():
	
	c.write_M( 0, 0x01 )
	c.write_M( 1, 0x13 )
	c.write_M( 2, 0x20 )

	c.write_M( 10, 0x03 )
	c.write_M( 11, 0x05 )
	c.write_M( 12, 0x00 )

program_5 = [

	# Multibyte subtraction
	# Testing CALL and RET
	0b00010110,  # MVI D, 3
	0b00000011,
	0b11001101,  # CALL MULTIBYTE_ADD
	0b00000110,  #  6
	0b00000000,
	0b01110110,  # HLT
	0b00000001,  # LXI BC, FIRST  # FIRST = 0
	0b00000000,
	0b00000000,
	0b00100001,  # LXI HL, SECOND  # SECOND = 10
	0b00001010,
	0b00000000,
	0b10101111,  # XRA A
	0b00001010,  # LDAX BC
	0b10011110,  # SBB M
	0b00000010,  # STAX BC
	0b00010101,  # DCR D
	0b11001010,  # JZ DONE
	0b00011001,  #  25
	0b00000000,
	0b00000011,  # INX BC
	0b00100011,  # INX HL
	0b11000011,  # JMP MADD_LOOP
	0b00001101,  #  13
	0b00000000,
	0b11001001,  # RET
]
def init_5():

	c.register_SP.write( 100 )
	init_4()


programs = [

	{ 'instructions' : program_0, 'init' : None,   'printOutput' : printOutput_0 },
	{ 'instructions' : program_1, 'init' : None,   'printOutput' : printOutput_1 },
	{ 'instructions' : program_2, 'init' : None,   'printOutput' : printOutput_2 },
	{ 'instructions' : program_3, 'init' : init_3, 'printOutput' : printOutput_3 },
	{ 'instructions' : program_4, 'init' : init_4, 'printOutput' : printOutput_3 },
	{ 'instructions' : program_5, 'init' : init_5, 'printOutput' : printOutput_3 },
]

def runProgram( pIdx ):

	program = programs[ pIdx ][ 'instructions' ]
	init = programs[ pIdx ][ 'init' ]
	printOutput = programs[ pIdx ][ 'printOutput' ]

	c.programMemory.load( program )
	# print( c.programMemory.registers[ : len( program ) ] )
	# print( '' )

	if init: init()

	iteration = 0
	while not c.halt:
		
		iteration += 1
		print( 'iteration -', iteration )
		
		c.fetchInstruction()
		c.executeInstruction()

		print( 'A  ', c.read_A() )
		print( 'B  ', c.register_BC.readUpperByte() )
		print( 'C  ', c.register_BC.readLowerByte() )
		print( 'D  ', c.register_DE.readUpperByte() )
		print( 'E  ', c.register_DE.readLowerByte() )
		print( 'H  ', c.register_HL.readUpperByte() )
		print( 'L  ', c.register_HL.readLowerByte() )
		print( 'CY ', c.flagALU_carry )
		print( '' )

	printOutput()

runProgram( 5 )
