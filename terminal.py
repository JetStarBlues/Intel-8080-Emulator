# ========================================================================================
# 
#  Description:
# 
#     Terminal Emulator
# 
#  Attribution:
# 
#     Code by www.jk-quantized.com
# 
#  Redistributions and use of this code in source and binary forms must retain
#  the above attribution notice and this condition.
# 
# ========================================================================================

''' 
Notes

	- Python 3 code
	- To exit cleanly use CTRL+Z.
	   CTRL+C doesn't cleanly kill threads (i.e you'll get an error message)
'''

import threading
from time import sleep


class Terminal:

	def __init__( self ):

		self.on = True

		self.tx = None
		self.rx = None

		# self.clockPeriod = 0.001  # seconds

		self.setupThreads()


	def setupThreads( self ):

		# Send and receive handled as threads to emulate concurrency of physical wires

		t1 = threading.Thread(

			name = 'tx_thread',
			target = self.send
		)

		t2 = threading.Thread(

			name = 'rx_thread',
			target = self.receive
		)

		t1.start()
		t2.start()


	def send( self ):

		while self.on:

			# Get user input
			try:

				user_input = input()

			# Exit conditions
			except EOFError:  # User pressed CTRL+C or CTRL+Z

				self.exit()
				break

			# Python input() can receive arbitrary length input from user
			#  We want to send it out one character at a time '''
			for c in user_input:

				# Drive TX line
				self.tx = c

				print( 'Transmitting {}'.format( c ) )  # debug

				# sleep( self.clockPeriod )

		print( '{} has exited'.format( threading.current_thread().getName() ) )  # debug


	def receive( self ):

		while self.on:

			# Sample RX line
			pass
			# print( self.rx, end = '' )

			# print( 'Receiving {}'.format( self.rx ) )  # debug

			# sleep( 2 )

		print( '{} has exited'.format( threading.current_thread().getName() ) )  # debug


	def exit( self ):

		self.on = False

		print( 'See you later!' )


# userTerm = Terminal()
