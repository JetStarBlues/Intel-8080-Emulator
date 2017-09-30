# ========================================================================================
# 
#  Description:
# 
#     UART Emulator
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


class UART:

	# Simple Intel 8251 emulation. Treat data as parallel

	def __init__( self ):

		self.name = ''  # debug
		
		self.on = True

		self.databus = None
		self.rxData = None
		self.txData = None

		self.rd  = 0
		self.wr  = 0
		self.clk = 0

		self.setupThreads()


	def setupThreads( self ):

		# Use of threads to emulate concurrency of physical wires

		t1 = threading.Thread(

			name = 'uart{}_rd_thread'.format( self.name ),
			target = self.sampleRD
		)

		t2 = threading.Thread(

			name = 'uart{}_wr_thread'.format( self.name ),
			target = self.sampleWR
		)

		t1.start()
		t2.start()


	def sampleRD( self ):

		while self.on:

			if self.clk and self.rd:

				self.receive()

		print( '{} has exited'.format( threading.current_thread().getName() ) )  # debug


	def sampleWR( self ):

		while self.on:

			if self.clk and self.wr:

				self.transmit()

		print( '{} has exited'.format( threading.current_thread().getName() ) )  # debug


	def transmit( self ):

		# Send data in databus
		self.txData = self.databus

		print( 'Transmitting {}'.format( self.databus ) )  # debug


	def receive( self ):

		# Read data onto databus
		self.databus = self.rxData

		print( 'Receiving {}'.format( self.rxData ) )  # debug


	def exit( self ):  # To cleanly close threads

		self.on = False



# Tests ------------------------------------------

from time import sleep, time

uart = UART()
uart.databus = 5
uart.wr = 1
# uart.rd = 1

clock = 0
startTime = time()
while True:

	elapsedTime = time() - startTime

	if elapsedTime >= 5:

		break

	clock ^= 1   # tick/tock

	uart.clk = clock

	print( clock, elapsedTime )

	sleep(1)  # pulse width

uart.on = False
