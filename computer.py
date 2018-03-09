from cpu_8080 import *
from memory import *
from terminal import *

from assembler import compile_
from disassembler import instructionLookup, instructionsWithData

from time import sleep
import sys

class Computer ():

	def __init__ ( self, memorySize ):

		self.memory = [ 0 ] * memorySize

		self.CPU = CPU( self.memory )

		self.terminal = Terminal()

		self.CPU.ioDevices.append( self.terminal )

		self.dumpFilePath = None


	def loadProgram ( self, programPath ):

		compile_( programPath, self.memory )


	def run ( self, step=False ):

		cpuThreadTarget = self.CPU.run

		if step: cpuThreadTarget = self.run_debugMode

		tkThread = threading.Thread(

			target = self.terminal.setupTkinter,
			name = 'tk_thread'
		)

		cpuThread = threading.Thread(

			# target = self.CPU.run,
			target = cpuThreadTarget,
			name = 'cpu_thread',
			daemon = True  # so that closing tk also closes cpu
		)

		tkThread.start()
		sleep( 0.1 )  # wait for tk to setup
		cpuThread.start()

		tkThread.join()  # wait for tk to be closed
		self.onStop()


	def onStop ( self ):

		print( 'See you later!' )

		# self.dumpStatus()  # debug


	def run_debugMode ( self ):

		self.prevInstruction = None
		self.prevPC = None

		self.dumpStatus()

		while True:

			uinput = input( '> ' )

			if uinput == 'n':

				self.CPU.step()

				self.dumpStatus()

			elif uinput == 'quit':

				break


	def dumpStatus ( self ):

		if self.dumpFilePath:  # redirect stdout

			sys.stdout = open( self.dumpFilePath, 'w' )


		print( '\nMemory...' )
		self.dumpMemory()

		print( '\nRegisters...' )
		print( 'A  :', self.CPU.register_AF.readUpperByte() )
		print( 'B  :', self.CPU.register_BC.readUpperByte() )
		print( 'C  :', self.CPU.register_BC.readLowerByte() )
		print( 'BC :', self.CPU.register_BC.read() )
		print( 'D  :', self.CPU.register_DE.readUpperByte() )
		print( 'E  :', self.CPU.register_DE.readLowerByte() )
		print( 'DE :', self.CPU.register_DE.read() )
		print( 'H  :', self.CPU.register_HL.readUpperByte() )
		print( 'L  :', self.CPU.register_HL.readLowerByte() )
		print( 'HL :', self.CPU.register_HL.read() )
		print( 'SP :', self.CPU.register_SP.read() )

		print( '\nFlags...' )
		f = self.CPU.register_AF.readLowerByte()
		f = bin( f )[ 2 : ].zfill( 8 )
		f = f[ : : - 1 ]
		print( 'carry  :', self.CPU.flagALU_carry , f[ 0 ] )
		print( 'parity :', self.CPU.flagALU_parity, f[ 2 ] )
		print( 'zero   :', self.CPU.flagALU_zero  , f[ 6 ] )
		print( 'sign   :', self.CPU.flagALU_sign  , f[ 7 ] )

		print( '\nInstruction...' )
		if self.prevInstruction in instructionsWithData:
			print( 'instruction      :', self.prevInstruction )
			nBytes = instructionsWithData[ self.prevInstruction ]
			for i in range( nBytes ):
				print( 'data             :', self.CPU.read_M( self.prevPC + 1 + i ) )
		else:
			print( 'instruction      :', instructionLookup[ self.CPU.instruction ] )  # disassemble
		nextPC = self.CPU.register_PC.read()
		nextInstr = instructionLookup[ self.CPU.read_M( nextPC ) ]
		print( 'PC_next          :', nextPC )
		print( 'instruction_next :', nextInstr )

		self.prevPC = nextPC
		self.prevInstruction = nextInstr

		if self.dumpFilePath:  # restore stdout

			sys.stdout = sys.__stdout__


	def dumpMemory ( self, start=None, end=None ):

		if start and end:

			range_ = range( start, end + 1 )

		else:

			range_ = range( len( self.memory ) )

		for i in range_:

			r = self.memory[ i ]

			b = bin( r )[ 2 : ].zfill( 8 )
			# b = '{:08b}'.format( r )

			if r != 0:

				c = None
				if r > 127: c = chr( r )

				# print( '{:5x}  {:08b}  {:5}  {}'.format( i, r, r, c ) )
				print( '{:5x}  {:08b}  {:5}  {}'.format( i, r, r, c ).encode( 'utf-8' ) )

