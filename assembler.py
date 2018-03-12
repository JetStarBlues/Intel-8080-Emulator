# ========================================================================================
# 
#  Description:
# 
#     Barebones assembler for the Intel 8080 Emulator
#
#     Do not use it if you don't have to!
# 
#  Attribution:
# 
#     Code by www.jk-quantized.com
# 
#  Redistribution and use of this code in source and binary forms must retain
#  the above attribution notice and this condition.
# 
# ========================================================================================


import re
from operator import itemgetter

debugMode = False

RAM = None

labels = {}
variables = {}
pc = 0

scheduleSecondPass = False
ranSecondPass = False
completedPasses = False
nPasses = 0

ops = [ '+', '-', '/', '>>', '&' ]
opsRe = '(\+|\-|/|>>|&)'

registers = {

	'B'   : '000',
	'C'   : '001',
	'D'   : '010',
	'E'   : '011',
	'H'   : '100',
	'L'   : '101',
	'M'   : '110',
	'A'   : '111',
	'SP'  : None,
	'PSW' : None
}

opcodes = {

	'LXI': {

		'B'  : '00000001',
		'D'  : '00010001',
		'H'  : '00100001',
		'SP' : '00110001'
	},
	'LDA' : '00111010',
	'STA' : '00110010',
	'LHLD': '00101010',
	'SHLD': '00100010',
	'LDAX': {

		'B' : '00001010',
		'D' : '00011010',
	},
	'STAX': {

		'B' : '00000010',
		'D' : '00010010',
	},
	'XCHG' : '11101011',

	'PUSH': {
		'B'   : '11000101',
		'D'   : '11010101',
		'H'   : '11100101',
		'PSW' : '11110101',
	},
	'POP': {
		'B'   : '11000001',
		'D'   : '11010001',
		'H'   : '11100001',
		'PSW' : '11110001',
	},
	'XTHL' : '11100011',
	'SPHL' : '11111001',

	'JMP'  : '11000011',
	'JNZ'  : '11000010',
	'JZ'   : '11001010',
	'JNC'  : '11010010',
	'JC'   : '11011010',
	'JPO'  : '11100010',
	'JPE'  : '11101010',
	'JP'   : '11110010',
	'JM'   : '11111010',
	'PCHL' : '11101001',

	'CALL' : '11001101',
	'CNZ'  : '11000100',
	'CZ'   : '11001100',
	'CNC'  : '11010100',
	'CC'   : '11011100',
	'CPO'  : '11100100',
	'CPE'  : '11101100',
	'CP'   : '11110100',
	'CM'   : '11111100',

	'RET' : '11001001',
	'RNZ' : '11000000',
	'RZ'  : '11001000',
	'RNC' : '11010000',
	'RC'  : '11011000',
	'RPO' : '11100000',
	'RPE' : '11101000',
	'RP'  : '11110000',
	'RM'  : '11111000',

	'INR' : { 'sfmt' : '00{}100' },
	'INX' : {

		'B'  : '00000011',
		'D'  : '00010011',
		'H'  : '00100011',
		'SP' : '00110011',
	},
	'DCR' : { 'sfmt' : '00{}101' },
	'DCX' : {

		'B'  : '00001011',
		'D'  : '00011011',
		'H'  : '00101011',
		'SP' : '00111011',
	},

	'ADD' : { 'sfmt' : '10000{}' },
	'ADI' : '11000110',
	'ADC' : { 'sfmt' : '10001{}' },
	'ACI' : '11001110',
	'DAD' : {

		'B'  : '00001001',
		'D'  : '00011001',
		'H'  : '00101001',
		'SP' : '00111001',
	},

	'SUB' : { 'sfmt' : '10010{}' },
	'SUI' : '11010110',
	'SBB' : { 'sfmt' : '10011{}' },
	'SBI' : '11011110',

	'ANA' : { 'sfmt' : '10100{}' },
	'ANI' : '11100110',
	'XRA' : { 'sfmt' : '10101{}' },
	'XRI' : '11101110',
	'ORA' : { 'sfmt' : '10110{}' },
	'ORI' : '11110110',
	'CMP' : { 'sfmt' : '10111{}' },
	'CPI' : '11111110',

	'RLC' : '00000111',
	'RRC' : '00001111',
	'RAL' : '00010111',
	'RAR' : '00011111',

	'CMA' : '00101111',
	'CMC' : '00111111',
	'STC' : '00110111',
	'DAA' : '00100111',

	'IN'  : '11011011',
	'OUT' : '11010011',

	'EI'  : '11111011',
	'DI'  : '11110011',
	'HLT' : '01110110',
	'NOP' : '00000000',
}

oneImmediate = [

	# cmd R,data
	'MVI',
	# cmd data
	'ADI', 'ACI',
	'SUI', 'SBI',
	'ANI', 'XRI', 'ORI', 'CPI',
	'IN', 'OUT'
]
twoImmediate = [

	# cmd R16,data16
	'LXI',
	# cmd data16
	'LDA', 'STA', 'LHLD', 'SHLD',
	'JMP', 'JNZ', 'JZ', 'JNC', 'JC', 'JPO', 'JPE', 'JP', 'JM',
	'CALL', 'CNZ', 'CZ', 'CNC', 'CC', 'CPO', 'CPE', 'CP', 'CM'
]

def pPrintDict( d, sortByValue=False ):

	if sortByValue:

		for k,v in sorted( d.items(), key=itemgetter( 1 ) ):

			print( k, v )

	else:

		for k,v in sorted( d.items() ):

			print( k, v )

def getBytes( x ):

	lo = x & 0xff
	hi = ( x >> 8 ) & 0xff

	return ( lo, hi )

def extractCommands( inputFile ):

	commands = []

	pendingLabels = []

	with open( inputFile, 'r' ) as file:

		for line in file:

			# print( line[:-1] )

			inString = False
			strTok = ''

			tokens = []
			token = ''

			# extract label, command, and arguments --------
			for c in line:

				# print( c )

				# comment
				if c == ';':

					break

				# start/end of string
				elif c == '"' or c == "'":

					if not inString:

						inString = True

						strTok = c

					elif c == strTok:

						inString = False

						strTok = ''

					token += c

				# delimiter
				elif ( c == ' ' or c == '\t' or c == '\n' ) and not inString:

					if token:

						tokens.append( token )

						token = ''

				# char in token
				else:

					token += c

			# make our lives easier --------
			nTokens = len( tokens )

			if nTokens == 2:

				if tokens[ 0 ][ - 1 ] == ':':

					# no argument
					tokens.append( None )  # argument

				else:

					# no label
					tokens.insert( 0, None )  # label

			elif nTokens == 1:

				if tokens[ 0 ][ - 1 ] == ':':

					# no command or argument
					tokens.append( None )  # command
					tokens.append( None )  # argument

				else:

					# no label or argument
					tokens.insert( 0, None )  # label
					tokens.append( None )     # argument


			# split arguments --------
			if tokens and tokens[ 2 ]:

				tokens[ 2 ] = tokens[ 2 ].split( ',' )


			# done --------
			if tokens:  # line with a command

				if debugMode: print( tokens )

				commands.append( tokens )

	# print( 'Done extracting commands' )

	return commands

def getLabels( commands ):

	global labels
	global variables
	global pc
	global RAM

	global scheduleSecondPass
	global ranSecondPass
	global nPasses
	global completedPasses

	commands_indexed = []

	# labels = {}
	# variables = {}
	pc = 0

	nPasses += 1

	for command in commands:

		if debugMode: print( pc, command )

		label = command[ 0 ]
		cmd   = command[ 1 ]
		args  = command[ 2 ]

		if cmd == 'END':

			break

		if cmd == 'EQU' or cmd == 'SET':

			variables[ label ] = parseExpression( args[ 0 ] )

			continue


		if label:

			label = label[ : - 1 ]  # remove ':'

			labels[ label ] = pc

		if cmd == None:

			continue  # standalone label


		if cmd == 'DB' or cmd =='DW' or cmd == 'DS':

			x, nArgs = parseArguments( args[ 0 ] )

			# if x[ 0 ] == None:

			# 	raise Exception( 'derp - {}, {}'.format( command, x ) )

			if cmd == 'DB':

				for e in x:

					if e == None:

						pc += 1  # take up space

					elif isinstance( e, list ):  # ex character array

						for c in e:

							RAM[ pc ] = c

							pc += 1

					else:

						RAM[ pc ] = e

						pc += 1

			elif cmd == 'DW':

				for e in x:

					if e == None:

						pass  # take up space

					elif isinstance( e, list ):  # ex character array

						# reversed??? 'A' stored as 4100, 'AB' as 4241
						# re 8085 programmers manual p.4-5

						if len( e ) == 2:

							RAM[ pc ]     = e[ 1 ]
							RAM[ pc + 1 ] = e[ 0 ]

						else:
						
							raise Exception( 'derp' )

					else:						

						lo, hi = getBytes( e )

						RAM[ pc ]     = lo
						RAM[ pc + 1 ] = hi

					pc += 2

			elif cmd == 'DS':

				nBlocks = x[ 0 ]

				pc += nBlocks

		elif cmd == 'ORG':

			pc = parseInt( args[ 0 ] )  # strict

		else:

			# do in second pass when labels and variables defined...
			commands_indexed.append( [ pc, command ] )
			pc += 1

			# allocate space for immediates
			if cmd in oneImmediate:

				pc += 1

			elif cmd in twoImmediate:

				pc += 2

	# pPrintDict( labels )
	# pPrintDict( labels, True )

	if scheduleSecondPass:

		print( 'Running second pass' )

		ranSecondPass = True
		scheduleSecondPass = False

		return getLabels( commands )

	else:

		completedPasses = True
		print( 'Completed passes ({})'.format( nPasses ) )

		return commands_indexed

def compileCommands( commands_indexed ):

	global pc

	for command in commands_indexed:

		pc = command[ 0 ]

		label = command[ 1 ][ 0 ]
		cmd   = command[ 1 ][ 1 ]
		args  = command[ 1 ][ 2 ]

		compileCommand( cmd, args )

def compileCommand( command, args ):

	global RAM

	if debugMode: print( pc, command, args )
	
	# cmd R,R
	if command == 'MOV':

		R1 = args[ 0 ]
		R2 = args[ 1 ]

		instruction = '01{}{}'.format( registers[ R1 ], registers[ R2 ] )

		RAM[ pc ] = int( instruction, 2 )
	
	# cmd R,data
	elif command == 'MVI':

		R = args[ 0 ]
		data = parseExpression( args[ 1 ] )

		if isinstance( data, list ):  # is a character
			data = data[ 0 ]

		instruction = '00{}110'.format( registers[ R ] )

		RAM[ pc ] = int( instruction, 2 )

		RAM[ pc + 1 ] = data
	
	# cmd R16,data16
	elif command == 'LXI':

		R = args[ 0 ]
		data = parseExpression( args[ 1 ] )

		instruction = opcodes[ command ][ R ]

		data_lo, data_hi = getBytes( data )

		RAM[ pc ] = int( instruction, 2 )

		RAM[ pc + 1 ] = data_lo
		RAM[ pc + 2 ] = data_hi
	
	# cmd data16
	elif command in [

		'LDA', 'STA', 'LHLD', 'SHLD',
		'JMP', 'JNZ', 'JZ', 'JNC', 'JC', 'JPO', 'JPE', 'JP', 'JM',
		'CALL', 'CNZ', 'CZ', 'CNC', 'CC', 'CPO', 'CPE', 'CP', 'CM',
	]:

		data = parseExpression( args[ 0 ] )

		instruction = opcodes[ command ]

		data_lo, data_hi = getBytes( data )

		RAM[ pc ] = int( instruction, 2 )

		RAM[ pc + 1 ] = data_lo
		RAM[ pc + 2 ] = data_hi

	# cmd data
	elif command in [

		'ADI', 'ACI',
		'SUI', 'SBI',
		'ANI', 'XRI', 'ORI', 'CPI',
		'IN', 'OUT'
	]:

		data = parseExpression( args[ 0 ] )

		instruction = opcodes[ command ]

		RAM[ pc ] = int( instruction, 2 )

		RAM[ pc + 1 ] = data

	# cmd R16
	elif command in [

		'LDAX', 'STAX',
		'PUSH', 'POP',
		'INX', 'DCX',
		'DAD',
	]:

		R = args[ 0 ]

		instruction = opcodes[ command ][ R ]

		RAM[ pc ] = int( instruction, 2 )

	# cmd R
	elif command in [

		'INR', 'DCR',
		'ADD', 'ADC',
		'SUB', 'SBB',
		'ANA', 'XRA', 'ORA', 'CMP'
	]:

		R = args[ 0 ]

		instruction = opcodes[ command ][ 'sfmt' ].format( registers[ R ] )

		RAM[ pc ] = int( instruction, 2 )
	
	# cmd
	elif command in [

		'XCHG',
		'XTHL', 'SPHL',
		'PCHL',
		'RET', 'RNZ', 'RZ', 'RNC', 'RC', 'RPO', 'RPE', 'RP', 'RM',
		'RLC', 'RRC', 'RAL', 'RAR',
		'CMA', 'CMC', 'STC', 'DAA',
		'EI', 'DI', 'HLT', 'NOP'
	]:

		instruction = opcodes[ command ]

		RAM[ pc ] = int( instruction, 2 )

	#
	elif command == 'RST':

		loc = int( args[ 0 ] )

		loc = bin( loc )[ 2 : ].zfill( 3 )

		instruction = '11{}111'.format( loc )

		RAM[ pc ] = int( instruction, 2 )

	#
	else:

		raise Exception( "Don't know how to compileCommand - {} {}".format( command, args ) )

def parseInt( s ):

	lastChar = s[ - 1 ]

	if lastChar == 'H':

		return int( s[ : - 1 ], 16 )

	elif lastChar == 'B':

		return int( s[ : - 1 ], 2 )

	elif lastChar == 'D':

		return int( s[ : - 1 ] )

	else:

		return int( s )

def parseString( s ):

	if len( s ) == 1:

		return ord( s )

	else:

		chars = []

		for c in s[ 1 : - 1 ]:

			chars.append( ord( c ) )

		return chars

def parseTerm( s ):

	# term -> register | integerConstant | asciiSequence | identifier | currentLocation

	global scheduleSecondPass

	c = s[ 0 ]

	if c == '$':

		return pc

	elif c.isdigit():

		return parseInt( s )

	elif c == '"' or c == "'":

		return parseString( s )

	elif s in registers:

		return s

	elif s in labels:

		return labels[ s ]

	elif s in variables:

		return variables[ s ]

	else:

		if completedPasses:

			raise Exception( "Don't know how to parseTerm - {}".format( s ) )

		elif not ranSecondPass:

			scheduleSecondPass = True  # maybe label assigned value later

			return None

def parseExpression( s ):

	# expression -> term ( op term )*

	# for compiler arithmetic, being lazy and assuming non-negative

	c = s[ 0 ]

	# string
	if c == '"' or c == "'":

		return parseString( s )

	exp = re.split( opsRe, s )

	# arithmetic
	if len( exp ) > 1:

		# print( pc, exp )

		val = parseTerm( exp[ 0 ] )

		if val:

			for i in range( 1, len( exp ), 2 ):

				op   = exp[ i ]
				term = parseTerm( exp[ i + 1 ] )

				if term:

					# print( val, op, term )

					if op == '+':

						val += term

					elif op == '-':

						val -= term

					elif op == '/':

						val = val // term

					elif op == '>>':

						val >>= term

					elif op == '&':

						val &= term

					else:

						raise Exception( 'derp' )

				else:

					val = None

					break

		return val

	#
	else:

		return parseTerm( s )

def parseArguments( s ):

	# arguments -> expression ( ',' expression )*

	args = s.split( ',' )

	byts = []

	for exp in args:

		byts.append( parseExpression( exp ) )
		# byts.extend( parseExpression( exp ) )

	return ( byts, len( args ) )


def compile_ ( inputFile, RAM_ = None ):

	global RAM

	if RAM_:

		RAM = RAM_

	else:

		RAM = [ None ] * 12000

	commands = extractCommands( inputFile )

	# for c in commands: print( c )

	commands_indexed = getLabels( commands )

	pPrintDict( labels )
	# for c in commands_indexed: print( c )

	compileCommands( commands_indexed )

	print( 'Assembly completed' )
	print( 'Program is about {} bytes long'.format( pc ) )  # + 0 or 1 or 2
	# print( RAM[ pc : pc + 5 ] )



# compile_( 'Programs/tinybasic-2.0-mod-mini85.asm' )
# compile_( '../cpm22_8080.asm' )

# compile_( 'Programs/sample_code.asm' )
# compile_( 'Programs/sample_code_3.asm' )
# compile_( 'Programs/sample_code_5.asm' )
# compile_( 'Programs/sample_code_6.asm' )
# compile_( 'Programs/sample_code_7a.asm' )

expected0 = [

	'00010110',
	'00101010',
	'00001110',
	'00111100',
	'00000110',
	'00000000',
	'00011110',
	'00001001',
	'01111001',
	'00011111',
	'01001111',
	'00011101',
	'11001010',
	'00011001',
	'00000000',
	'01111000',
	'11010010',
	'00010100',
	'00000000',
	'10000010',
	'00011111',
	'01000111',
	'11000011',
	'00001000',
	'00000000',
	'01110110',
]
expected3 = [

	'00000110',
	'00001100',
	'00100001',
	'00000000',
	'00000000',
	'00110110',
	'00000000',
	'00100011',
	'00110110',
	'00000001',
	'00101011',
	'01111110',
	'00100011',
	'10000110',
	'00100011',
	'01110111',
	'00000101',
	'11000010',
	'00001010',
	'00000000',
	'01110110',
]
expected5 = [

	'00000001',
	'11011011',
	'00100010',
	'00010001',
	'11111001',
	'00011010',
	'00110111',
	'00111111',
	'01111001',
	'10011011',
	'01101111',
	'01111000',
	'10011010',
	'01100111',
	'01110110',
]
expected6 = [

	'00010110',
	'00000011',
	'00000001',
	'00000000',
	'00000000',
	'00100001',
	'00001010',
	'00000000',
	'10101111',
	'00001010',
	'10001110',
	'00000010',
	'00010101',
	'11001010',
	'00010101',
	'00000000',
	'00000011',
	'00100011',
	'11000011',
	'00001001',
	'00000000',
	'01110110',
]
expected7a = [

	'00010110',
	'00000011',
	'11001101',
	'00000110',
	'00000000',
	'01110110',
	'00000001',
	'00000000',
	'00000000',
	'00100001',
	'00001010',
	'00000000',
	'10101111',
	'00001010',
	'10011110',
	'00000010',
	'00010101',
	'11001010',
	'00011001',
	'00000000',
	'00000011',
	'00100011',
	'11000011',
	'00001101',
	'00000000',
	'11001001',
]

def printRAM():

	for i in range( len( RAM ) ):
	# for i in range( len( expected ) ):
	# for i in range( 40 ):

		e = RAM[ i ]

		# if e == None: break

		if e != None:

			print( '{:4} {}'.format( i, bin( e )[2:].zfill( 8 ) ) )

		# b = bin( e )[2:].zfill( 8 )
		# print( '{:4} {} {}'.format( i, b, b == expected[ i ] ) )


# printRAM()