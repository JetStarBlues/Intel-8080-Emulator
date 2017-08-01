from memory import *
from cpu_8080 import *

class Computer():

	def __init__( self ):

		self.dataMemory = RAM( 200 )
		self.programMemory = RAM( 100 )

		self.CPU = CPU( self.dataMemory, self.programMemory )
