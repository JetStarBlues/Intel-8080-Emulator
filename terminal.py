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

'''
     ________                 _________
    |        |               |         |
    |        |               |         |   txData
    |        |    databus    |         | ----------->
    | DEVICE | <-----------> |         |
    |        |               |         |   rxData
    |        |    rd         |         | <----------
    |        | ------------> |  UART   |
    |        |               |         |
    |        |    wr         |         |
    |        | ------------> |         |
    |        |               |         |
    |        |               |         |
    |________|               |_________|
                                  ^
                                  |
                                  |
                                  clk
'''


import threading


class Terminal:

	def __init__( self ):

		self.on = True

		self.txData = None
		self.rxData = None

		self.rxReady = 0
		self.clk     = 0

		# self.sampleFrequency = 2  # seconds

		self.setupThreads()


	def setupThreads( self ):

		# Handle as threads to emulate concurrency of physical wires

		t1 = threading.Thread(

			name = 'tx_thread',
			target = self.transmit
		)

		# t2 = threading.Thread(

		# 	name = 'rx_thread',
		# 	target = self.receive
		# )

		t3 = threading.Thread(

			name = 'rxReady_thread',
			target = self.sampleRxReady
		)

		t1.start()
		# t2.start()
		t3.start()


	def sampleRxReady( self ):

		while self.on:

			if self.clk and self.rxReady:

				self.receive()

		print( '{} has exited'.format( threading.current_thread().getName() ) )  # debug


	def receive( self ):

		# print( self.rx, end = '' )
		print( 'Receiving {}'.format( self.rxData ) )  # debug


	def transmit( self ):

		while self.on:

			# Get user input
			try:

				user_input = input()

			# Exit conditions
			except EOFError:  # User pressed CTRL+C or CTRL+Z

				self.exit()
				break

			# Append newline character (omitted by input())
			user_input += '\n'

			# Python input() can receive arbitrary length input from user
			#  We want to send it out one character at a time '''
			for c in user_input:

				# Drive TX line
				self.txData = c

				print( 'Transmitting {}'.format( c ) )  # debug

				# sleep( self.clockPeriod )

		print( '{} has exited'.format( threading.current_thread().getName() ) )  # debug


	def exit( self ):

		self.on = False

		print( 'See you later!' )



# Tests ------------------------------------------

from time import sleep, time

term = Terminal()
term.rxReady = 1
# term.rxData = "greetings"

clock = 0
startTime = time()
while time() - startTime < 1:
	
	clock ^= 1   # tick/tock

	sleep( 0.5 )  # pulse width

	term.clk = clock

term.exit()
