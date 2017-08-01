# ========================================================================================
# 
#  Description:
# 
#     Compiles Intel 8080 assembly code to binary
# 
#  Attribution:
# 
#     Code by www.jk-quantized.com
# 
#  Redistributions and use of this code in source and binary forms must retain
#  the above attribution notice and this condition.
# 
# ========================================================================================

''' TODO

 - Pad code based on commands and compare generated line numbers
   with listing
	
	Load immediates
	  - data16, +2
	  - data, +1

	JMP
		+2

	DB
		+len( list )

	DW
		+2 * len( list )
	
	DS
		+arg
		Ignore??, seems to be outside code



'''


'''

	Skip END cmd

'''

# == Imports =================================================

# Built ins
import re
import os


# == Helpers =================================================

dataBase = 0


# def DB( self, base = dataBase, x ) :  # define byte(s)

# 	if isinstance( x, str ):

# 		x = map( ord, x )

# 	for i in range( len( x ) ):

# 		self.write_M( base + i, x[ i ] )

# 	dataBase = base + i + 1


# def DW( self, base = dataBase, x ) :  # define word(s)

# 	for i in range( len( x ) ):

# 		j = i * 2

# 		self.write_M( base + j    , self.getLowerByte( x[ i ] ) )
# 		self.write_M( base + j + 1, self.getUpperByte( x[ i ] ) )

# 	dataBase = base + j + 2

# def DS( self, base = dataBase, x ) : # define storage (nBytes)

# 	''' the value of x specifies the number of memory bytes to
# 	    reserve for data storage '''

# 	dataBase += x

# 	pass

def MACRO(): pass  # looks like not included in line count

def toInt( s ):

	if s[ - 1 : ] == 'H':

		return int( s[ : - 1 ], 16 )

	else:

		return int( s )

def EQU( cmd ):

	knownVars[ cmd[ 0 ] ] = toInt( cmd[ 2 ] )


# == Main ====================================================


# -- Extraction -------------------------------------

# Select everything that is not a comment
cmdPattern = '''
	^                # from beginning of string
	.*?              # select all characters until
	(?=;|[\r\n])     # reach start of a comment or the string's end
'''
cmdPattern = re.compile( cmdPattern, re.X )

def extractCmd( line ):

	# line = line.replace( ' ', '' )   # remove spaces
	# line = line.replace( '\t', '' )  # remove tabs
	# line = line.upper()              # upper case everything

	found = re.search( cmdPattern, line ) 	# select everything that is not a comment
	cmd = found.group( 0 )

	if cmd:

		return re.findall( r':|"?\'?\S+"?\'?', cmd )  # extract words

		# return re.findall( r':|"?\'?(\w+|\$|\-|\+)"?\'?', cmd )  # extract words
		 # DB   PR2-$-1

		# TODO, scrap this and use tokenizer approach

	else:

		return None

def extractCmds( inputFile ):

	commands = []

	with open( inputFile, 'r' ) as input_file:
		
		for line in input_file:

			cmd = extractCmd( line )

			if cmd:

				commands.append( cmd )

				print( cmd )

	return commands


# -- Translation -------------------------------------





def translateCmds( cmdList ):

	''' Translate assembly to binary '''

	cmdList = handleLabels( cmdList )
	cmdList = handleVariables( cmdList[0], cmdList[1] )
	binCmdList = translateInstructions( cmdList )


# -- Output --------------------------------------

def writeToOutputFile( binCmdList, outputFile ):

	''' Generate an output file containing the binary commands '''

	with open( outputFile, 'w' ) as output_file:

		firstLine = True # workaround to avoid extra blank line at end of output file, http://stackoverflow.com/a/18139440
		
		for cmd_binary in binCmdList:
				
			if firstLine: firstLine = False
			else: output_file.write( '\n' )

			output_file.write( cmd_binary )


# -- Run ------------------------------------------

def asm_to_bin( inputFile, outputFile ):

	# Read
	cmds_assembly = extractCmds( inputFile )

	# Translate
	# cmds_binary = translateCmds( cmds_assembly )

	# Write
	# writeToOutputFile( cmds_binary, outputFile )

	# print( 'Done' )

inputFile = 'C:/Users/Janet/Desktop/Hack/gb_emul/tinybasic/tinybasic-2.0.asm'
outputFile = 'C:/Users/Janet/Desktop/Hack/gb_emul/Emulator/tinybasic.bin'
asm_to_bin( inputFile, outputFile )