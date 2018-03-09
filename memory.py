class Register ():

	def __init__ ( self ):

		self.value = 0

	def read ( self ):

		return self.value

	def readUpperByte ( self ):

		return ( self.value >> 8 ) & 0xff

	def readLowerByte ( self ):

		return self.value & 0xff

	def write ( self, value ):

		self.value = value

	def writeUpperByte ( self, value ):

		self.value = ( self.value & 0x00ff ) | ( value << 8 )

	def writeLowerByte ( self, value ):

		self.value = ( self.value & 0xff00 ) | value
