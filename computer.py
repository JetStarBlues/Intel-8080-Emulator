from cpu_8080 import *
from memory import *
from terminal import *

from assembler import compile_

class Computer ():

	def __init__ ( self, memorySize ):

		self.memory = [ 0 ] * memorySize

		self.terminal = Terminal()

		self.CPU = CPU( self.memory, self.terminal )

	def loadProgram ( self, program ):

		compile_( program, self.memory )

	def run ( self ):

		self.CPU.run()

	def dumpMemory ( self ):

		for i in range( len( self.memory ) ):

			r = self.memory[ i ]

			b = bin( r )[ 2 : ].zfill( 8 )

			print( '{:5} {}'.format( i, b ) )

