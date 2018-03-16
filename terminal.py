# ========================================================================================
# 
#  Description:
# 
#     Simple Terminal Emulator
#
#     Interface:
#       Input  -> keyboard
#       Output -> screen
# 
#  Attribution:
# 
#     Code by www.jk-quantized.com
# 
#  Redistribution and use of this code in source and binary forms must retain
#  the above attribution notice and this condition.
# 
# ========================================================================================

import tkinter
import threading

class Terminal():

	def __init__ ( self, width=400, height=400 ):

		self.keyBuffer = []
		self.displayBuffer = ''

		self.K_CTRL_C    = 0x03
		self.K_BACKSPACE = 0x08
		self.K_LF        = 0x0A
		self.K_CR        = 0x0D  # used as end-of-(line,string,input) marker in TB
		self.K_RUB_OUT   = 0x7F  # backspace

		self.debugMode = False

		self.width = width
		self.height = height
		self.textColor = '#689497'
		self.bgColor = '#fff4dc'
		self.tkRoot = None
		self.tkTextBox = None
		self.tkCanvas = None
		self.tkCanvasFrame = None

		# self.tkThread = threading.Thread(

		# 	target = self.setupTkinter,
		# 	name = 'tk_thread'

		# ).start()


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


	# Helper ------------------------------------------

	def tooLazyToType ( self, filepath ):

		with open( filepath, 'r' ) as file:

			for line in file:

				for char in line:

					keyCode = ord( char )

					if keyCode == self.K_LF:

						keyCode = self.K_CR  # tiny basic expects CR as delimiter

					# print( char, keyCode )

					self.addKeyToBuffer( keyCode )


	# Keypress ----------------------------------------

	def addKeyToBuffer ( self, key ):

		self.keyBuffer.insert( 0, key )

		# self.sendInterrupt()  # interrupt vs waiting for poll
		

	def handleKeypress ( self, event ):

		if event.char:  # modifier keys like SHIFT are None?

			char = event.char
			keyCode = ord( char )

			# print( char, keyCode )

			if keyCode == self.K_CTRL_C:

				self.addKeyToBuffer( keyCode )

			elif keyCode == self.K_BACKSPACE:  

				self.addKeyToBuffer( self.K_RUB_OUT )

			elif keyCode == self.K_CR or keyCode == self.K_LF:

				self.addKeyToBuffer( self.K_CR )

			elif keyCode >= 32 and keyCode <= 126:

				self.addKeyToBuffer( keyCode )

			else:

				# print( 'Key not handled - {}'.format( keyCode ) )
				pass


	# Display -----------------------------------------

	def displayCharacter ( self, keyCode ):

		if self.debugMode:

			print( 'tkRaw ->', keyCode )

		if keyCode == 0:

			return

		if keyCode >= 32 and keyCode <= 126:

			self.displayBuffer += chr( keyCode )

		elif keyCode == self.K_CR:

			pass

		elif keyCode == self.K_LF:

			self.displayBuffer += '\n'

		elif keyCode == self.K_BACKSPACE:  

			if len( self.displayBuffer ) > 0:

				self.displayBuffer = self.displayBuffer[ : - 1 ]  # remove from display buffer


		self.updateDisplay()

	def tk_onFrameConfigure( self, event ):

		# resize canvas
		self.tkCanvas.configure( scrollregion = self.tkCanvas.bbox( 'all' ) )

	def tk_onCanvasConfigure( self, event ):

		# resize frame
		self.tkCanvas.itemconfigure( self.tkCanvasFrame, width = event.width )

	def setupTkinter( self ):

		self.tkRoot = tkinter.Tk()
		self.tkRoot.title( '8080 Sim' )

		self.tkCanvas = tkinter.Canvas( self.tkRoot )
		self.tkCanvas.pack( side = tkinter.LEFT, expand = True, fill = 'both' )
		self.tkCanvas.configure(

			width = self.width,
			height = self.height,
			highlightthickness = 0,
			bg = self.bgColor
		)

		scrollbar = tkinter.Scrollbar( self.tkRoot )
		scrollbar.pack( side = tkinter.RIGHT, fill = 'y' )
		scrollbar.configure(

			orient = 'vertical',
			command = self.tkCanvas.yview
		)
		self.tkCanvas.configure( yscrollcommand = scrollbar.set )

		frame = tkinter.Frame( self.tkCanvas )
		self.tkCanvasFrame = self.tkCanvas.create_window(

			( 0, 0 ),
			window = frame,
			anchor = 'nw'
		)

		self.tkTextBox = tkinter.Label( frame )
		self.tkTextBox.pack( expand = True, fill = 'both' )
		self.tkTextBox[ 'text' ] = self.displayBuffer
		self.tkTextBox.config(

			fg = self.textColor,
			bg = self.bgColor,
			anchor = 'nw',
			justify = tkinter.LEFT,
			wraplength = self.width - 5
		)

		frame.bind( '<Configure>', self.tk_onFrameConfigure )
		self.tkCanvas.bind( '<Configure>', self.tk_onCanvasConfigure )

		self.tkRoot.bind( '<KeyPress>', self.handleKeypress )

		self.tkRoot.protocol( 'WM_DELETE_WINDOW', self.quitTkinter )
		
		self.tkRoot.mainloop()

	def quitTkinter( self ):

		self.tkRoot.quit()

		print( 'Tkinter has exited' )

	def updateDisplay( self ):

		self.tkTextBox[ 'text' ] = self.displayBuffer

		self.tkCanvas.yview_moveto( 1 )  # scroll to bottom (show latest)


# t = Terminal()
