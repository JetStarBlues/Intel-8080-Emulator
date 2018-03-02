'''
	input  -> keyboard
	output -> display
'''

import tkinter
import threading

class Terminal():

	def __init__ ( self, width=400, height=400, CPU=None ):

		self.CPU = CPU

		self.keyBuffer = []
		self.displayBuffer = ''

		self.K_CTRL_C    = 0x03
		self.K_BACKSPACE = 0x08
		self.K_ENTER     = 0x0A

		# teletype keys?
		self.K_CR      = 0x0D  # used as end-of-(line,string,input) marker in TB
		self.K_RUB_OUT = 0x7F  # backspace

		self.debugMode = False

		self.tkRoot = None
		self.tkWidth = width
		self.tkHeight = height
		self.tkTextBox = None

		threading.Thread(

			target = self.setupTkinter,
			name = 'tk_thread'

		).start()


	# Communication -----------------------------------

	def transmit ( self ):

		# Send data to CPU

		if len( self.keyBuffer ) > 0:

			return self.keyBuffer.pop()

		else:

			return 0

	def receive ( self, data ):

		# Receive data from CPU

		self.displayCharacter( data )

	def sendInterrupt ( self, isrLoc ):

		'''
			Real procedure,
			  set INT high
			  send RST instr
			  set INT low
			  ISR code will call IN to get data
		'''

		self.CPU.jumpToISR( isrLoc )


	# Keypress ----------------------------------------

	def addKeyToBuffer ( self, key ):

		self.keyBuffer.insert( 0, key )

		# self.sendInterrupt()  # interrupt vs waiting for poll
		

	def handleKeypress ( self, event ):

		char = event.char
		keyCode = ord( char )

		if keyCode == self.K_CTRL_C:

			self.addKeyToBuffer( keyCode )  # send to TB

			return

		elif keyCode == self.K_BACKSPACE:  

			self.addKeyToBuffer( self.K_RUB_OUT )  # send to TB

			if len( self.displayBuffer ) > 0:

				self.displayBuffer = self.displayBuffer[ : - 1 ]  # remove from display buffer

		elif keyCode == self.K_ENTER:

			self.addKeyToBuffer( self.K_CR )  # send to TB

			self.displayBuffer += char  # echo

		elif keyCode >= 32 and keyCode <= 126:

			self.addKeyToBuffer( keyCode )  # send to TB

			self.displayBuffer += char  # echo

		else:

			# print( 'Key not handled - {}'.format( keyCode ) )

			return

		self.updateDisplay()


	# Display -----------------------------------------

	def displayCharacter ( self, data ):

		if self.debugMode:

			print( 'tkRaw ->', data )

		if data >= 32 and data <= 126:

			self.displayBuffer += chr( data )

		elif data == self.K_CR:

			self.displayBuffer += '\n'

		self.updateDisplay()

	def setupTkinter( self ):

		self.tkRoot = tkinter.Tk()

		self.tkRoot.config( width = self.tkWidth, height = self.tkHeight )
		self.tkRoot.title( '8080 Sim' )

		self.tkTextBox = tkinter.Label( self.tkRoot )
		self.tkTextBox.place( relx = 0, rely = 0 )
		self.tkTextBox.config(
			wraplength = self.tkWidth - 5,
			justify = tkinter.LEFT
		)

		textColor = "#689497"
		bgColor = "#fff4dc"
		self.tkTextBox.config( fg = textColor, bg = bgColor )
		self.tkRoot.config( bg = bgColor )

		self.tkTextBox[ 'text' ] = self.displayBuffer

		self.tkRoot.bind( '<KeyPress>', self.handleKeypress )

		self.tkRoot.protocol( 'WM_DELETE_WINDOW', self.quitTkinter )

		self.tkRoot.mainloop()

	def quitTkinter( self ):

		self.tkRoot.quit()

		# print( 'See you later!' )
		print( 'Tkinter has exited' )

	def updateDisplay( self ):

		self.tkTextBox[ 'text' ] = self.displayBuffer
