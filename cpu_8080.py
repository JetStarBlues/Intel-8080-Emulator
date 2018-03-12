# ========================================================================================
# 
#  Description:
# 
#     Intel 8080 Emulator
# 
#  Attribution:
# 
#     Code by www.jk-quantized.com
# 
#  Redistribution and use of this code in source and binary forms must retain
#  the above attribution notice and this condition.
# 
# ========================================================================================

'''
   Inspired by,
    - Game Boy Emulation
       https://www.youtube.com/watch?v=025tC0DcFUI
    - Minimal 8085 Single Board Computer - MiniMax8085
       http://www.malinov.com/Home/sergeys-projects/minimax8085

   References used,
    - 8080 Datasheet
       http://www.fecegypt.com/uploads/dataSheet/1481550148_8080.pdf
    - 8080 User Manual
       ftp://bitsavers.informatik.uni-stuttgart.de/pdf/intel/MCS80/98-153B_Intel_8080_Microcomputer_Systems_Users_Manual_197509.pdf
    - 8080 Assembly Language Manual
       http://altairclone.com/downloads/manuals/8080%20Programmers%20Manual.pdf

   Of interest,
    http://www.righto.com/search/label/8085
'''

'''
From 8080 Docs...

	Flags
		0 - carry,           set when addition result overflows or rotate/shift has shifted-out a '1'
		2 - parity,          set when modulo 2 sum of bits is zero
		4 - auxiliary carry, set when half carry occurs
		6 - zero,            set when result of operation is 0
		7 - sign,            set when MSB of result is 1

	OpCodes
		
		- Destination / Source
			. B      -> 000
			. C      -> 001
			. D      -> 010
			. E      -> 011
			. H      -> 100
			. L      -> 101
			. Memory -> 110
			. A      -> 111

		- Move, load, store
			. MOV R1,R2     -> 01DDDSSS -> 1 -> Move register to register
			. MOV M,R       -> 01110SSS -> 2 -> Move register to memory
			. MOV R,M       -> 01DDD110 -> 2 -> Move memory to register
			. MVI R,data    -> 00DDD110 -> 2 -> Move immediate to register
			. MVI M,data    -> 00110110 -> 3 -> Move immediate to memory
			. LXI BC,data16 -> 00000001 -> 3 -> Load immediate to register pair B & C
			. LXI DE,data16 -> 00010001 -> 3 -> Load immediate to register pair D & E
			. LXI HL,data16 -> 00100001 -> 3 -> Load immediate to register pair H & L
			. LXI SP,data16 -> 00110001 -> 3 -> Load immediate to stack pointer
			. LDA addr      -> 00111010 -> 4 -> Load A direct
			. STA addr      -> 00110010 -> 4 -> Store A direct
			. LHLD addr     -> 00101010 -> 5 -> Load H & L direct
			. SHLD addr     -> 00100010 -> 5 -> Store H & L direct
			. LDAX BC       -> 00001010 -> 2 -> Load A indirect
			. LDAX DE       -> 00011010 -> 2 -> Load A indirect
			. STAX BC       -> 00000010 -> 2 -> Store A indirect
			. STAX DE       -> 00010010 -> 2 -> Store A indirect
			. XCHG          -> 11101011 -> 1 -> Exchange register pair D & E with H & L

		- Stack ops
			. PUSH BC  -> 11000101 -> 3 -> Push register pair B & C on stack
			. PUSH DE  -> 11010101 -> 3 -> Push register pair D & E on stack
			. PUSH HL  -> 11100101 -> 3 -> Push register pair H & L on stack
			. PUSH PSW -> 11110101 -> 3 -> Push A and Flags on stack
			. POP BC   -> 11000001 -> 3 -> Pop top of stack onto register pair B & C
			. POP DE   -> 11010001 -> 3 -> Pop top of stack onto register pair D & E
			. POP HL   -> 11100001 -> 3 -> Pop top of stack onto register pair H & L
			. POP PSW  -> 11110001 -> 3 -> Pop top of stack onto A and Flags
			. XTHL     -> 11100011 -> 5 -> Exchange H & L with contents of location specified by stack pointer
			. SPHL     -> 11111001 -> 1 -> H & L to stack pointer

		- Jump
			. JMP addr -> 11000011 -> 3 -> Jump unconditional
			. JNZ addr -> 11000010 -> 3 -> Jump on not zero
			. JZ addr  -> 11001010 -> 3 -> Jump on zero
			. JNC addr -> 11010010 -> 3 -> Jump on no carry
			. JC addr  -> 11011010 -> 3 -> Jump on carry
			. JPO addr -> 11100010 -> 3 -> Jump on parity odd
			. JPE addr -> 11101010 -> 3 -> Jump on parity even
			. JP addr  -> 11110010 -> 3 -> Jump on positive
			. JM addr  -> 11111010 -> 3 -> Jump on minus
			. PCHL     -> 11101001 -> 1 -> H & L to program counter

		- Call
			. CALL addr -> 11001101 -> 5   -> Call unconditional
			. CNZ addr  -> 11000100 -> 3/5 -> Call on not zero
			. CZ addr   -> 11001100 -> 3/5 -> Call on zero
			. CNC addr  -> 11010100 -> 3/5 -> Call on no carry
			. CC addr   -> 11011100 -> 3/5 -> Call on carry
			. CPO addr  -> 11100100 -> 3/5 -> Call on parity odd
			. CPE addr  -> 11101100 -> 3/5 -> Call on parity even
			. CP addr   -> 11110100 -> 3/5 -> Call on positive
			. CM addr   -> 11111100 -> 3/5 -> Call on minus

		- Return
			. RET -> 11001001 -> 3   -> Return unconditional
			. RNZ -> 11000000 -> 1/3 -> Return on not zero
			. RZ  -> 11001000 -> 1/3 -> Return on zero
			. RNC -> 11010000 -> 1/3 -> Return on no carry
			. RC  -> 11011000 -> 1/3 -> Return on carry
			. RPO -> 11100000 -> 1/3 -> Return on parity odd
			. RPE -> 11101000 -> 1/3 -> Return on parity even
			. RP  -> 11110000 -> 1/3 -> Return on positive
			. RM  -> 11111000 -> 1/3 -> Return on minus

		- Restart
			. RST -> 11NNN111 -> 3 -> Restart

		- Increment and decrement
			. INR R  -> 00DDD100 -> 1 -> Increment register
			. INR M  -> 00110100 -> 3 -> Increment memory
			. INX BC -> 00000011 -> 1 -> Increment B & C registers
			. INX DE -> 00010011 -> 1 -> Increment D & E registers
			. INX HL -> 00100011 -> 1 -> Increment H & L registers
			. INX SP -> 00110011 -> 1 -> Increment stack pointer
			. DCR R  -> 00DDD101 -> 1 -> Decrement register
			. DCR M  -> 00110101 -> 3 -> Decrement memory
			. DCX BC -> 00001011 -> 1 -> Decrement B & C registers
			. DCX DE -> 00011011 -> 1 -> Decrement D & E registers
			. DCX HL -> 00101011 -> 1 -> Decrement H & L registers
			. DCX SP -> 00111011 -> 1 -> Decrement stack pointer

		- Add
			. ADD R    -> 10000SSS -> 1 -> Add register to A
			. ADD M    -> 10000110 -> 2 -> Add memory to A
			. ADI data -> 11000110 -> 2 -> Add immediate to A
			. ADC R    -> 10001SSS -> 1 -> Add register to A with carry
			. ADC M    -> 10001110 -> 2 -> Add memory to A with carry
			. ACI data -> 11001110 -> 2 -> Add immediate to A with carry
			. DAD BC   -> 00001001 -> 3 -> Add B & C to H & L
			. DAD DE   -> 00011001 -> 3 -> Add D & E to H & L
			. DAD HL   -> 00101001 -> 3 -> Add H & L to H & L
			. DAD SP   -> 00111001 -> 3 -> Add stack pointer to H & L

		- Subtract
			. SUB R    -> 10010SSS -> 1 -> Subtract register from A
			. SUB M    -> 10010110 -> 2 -> Subtract memory from A
			. SUI data -> 11010110 -> 2 -> Subtract immediate from A
			. SBB R    -> 10011SSS -> 1 -> Subtract register from A with borrow
			. SBB M    -> 10011110 -> 2 -> Subtract memory from A with borrow
			. SBI data -> 11011110 -> 2 -> Subtract immediate from A with borrow

		- Logical
			. ANA R    -> 10100SSS -> 1 -> And register with A
			. ANA M    -> 10100110 -> 2 -> And memory with A
			. ANI data -> 11100110 -> 2 -> And immediate with A
			. XRA R    -> 10101SSS -> 1 -> Exclusive or register with A
			. XRA M    -> 10101110 -> 2 -> Exclusive or memory with A
			. XRI data -> 11101110 -> 2 -> Exclusive or immediate with A
			. ORA R    -> 10110SSS -> 1 -> Or register with A
			. ORA M    -> 10110110 -> 2 -> Or memory with A
			. ORI data -> 11110110 -> 2 -> Or immediate with A
			. CMP R    -> 10111SSS -> 1 -> Compare register with A
			. CMP M    -> 10111110 -> 2 -> Compare memory with A
			. CPI data -> 11111110 -> 2 -> Compare immediate with A

		- Rotate
			. RLC -> 00000111 -> 1 -> Rotate A left
			. RRC -> 00001111 -> 1 -> Rotate A right
			. RAL -> 00010111 -> 1 -> Rotate A left through carry
			. RAR -> 00011111 -> 1 -> Rotate A right through carry

		- Specials
			. CMA -> 00101111 -> 1 -> Complement A
			. CMC -> 00111111 -> 1 -> Complement carry
			. STC -> 00110111 -> 1 -> Set carry
			. DAA -> 00100111 -> x -> Decimal adjust A

		- Input / Output
			. IN port  -> 11011011 -> 3 -> Input. Read byte from specified port and load to A
			. OUT port -> 11010011 -> 3 -> Output. Places contents of A onto data bus and the
			                                       selected port number onto the address bus

		- Control
			. EI  -> 11111011 -> 1 -> Enable interrupts
			. DI  -> 11110011 -> 1 -> Disable interrupt
			. HLT -> 01110110 -> 1 -> Halt
			. NOP -> 00000000 -> 1 -> No operation

		- 8085 instructions
			. SIM -> .. -> Set interrupt mask
			. RIM -> .. -> Read interrupt mask
			. review AND/ANI operation, which sets the AC flag differently

		- 8051 instructions
			. interrupts
			. timers

	Instructions greater than 8 bits

		There are times when execution of instruction requires more information than 8 bits can convey.
		In such a case, two or three byte instructions are used. Successive instruction bytes are stored
		sequentially in adjacent memory locations, and the processor performs two or three fetches in
		succession to obtain the full instruction. The first byte retrieved is placed in the instruction
		register and subsequent bytes in temporary storage. The processor then proceeds with execution.

	Control circuitry

		Using clock inputs, the cc maintains proper sequence of events required to process a task. After
		an instruction is fetched and decoded, the cc issues appropriate signals (internal and external to CPU)
		for initiating proper processing action.

		Signals:
		. Data bus in        (output) - indicates to external circuits that databus is in input mode
		. Ready              (input)  - indicates that valid data is available on the databus
		. Wait               (output) - indicates CPU is in a wait_state
		. Write              (output) - ?. Active low
		. Hold               (input)  - requests CPU to enter hold_state
		. Hold acknowledge   (output) - indicates ...
		. Interrupt enable   (output) - indicates content of interruptEn flipflop
		. Interrupts request (input)  - ...
		. Reset              (input)  - when toggles to high, PC address is cleared to 0.
		                                The interruptEn and holdAck flipflops are also reset.

	Interrupts
		An interrupt request will cause the control circuitry to temporarily
		interrupt main program execution, jump to a special routine to service the interrupting device,
		then automatically return to the main program.
		A wait request is often issued by a memory or IO device that operates slower than the CPU. The cc
		will idle the CPU until the memory or IO port device frees the WAIT line.
		In principle, an interrupt is similar to a subroutine call, except that the jump is initiated
		externally rather than by the program

	Direct Memory Access
		In ordinary IO operations, the processor supervises data transfer. Info to bo be placed in memory
		is transferred from input device to processor, then from processor to memory (and vis a vis output).
		If a large quantity of data must be transferred, it's ideal to have the device interface with memory
		directly. To achieve this, the processor must temporarily suspend its operation during such a transfer
		to prevent conflict. This is achieved via a HOLD signal sent to CPU.

	Instruction Cycle
		Instruction fetch
			- instruction retrieved from memory (address from PC) and store in instruction register
			- once fetched, pc incremented
		Instruction decode
			-
		Instruction execution
			- 
		A machine cycle is required each time the CPU accesses memory or an IO port.
		Thus duration of an instruction cycle consists of one machine cycle to fetch the instruction plus
		n machine cycles for subsequent mem / IO accesses needed to accomplish instruction.
	
	Stack pointer
		Decremented when data pushed onto stack, incremented when popped (i.e. grows downward)

	Registers
		PC, SP, BC, DE, HL, WZ
		Data bytes can be transferred from the internal bus (8bit) to a register via the
		register-select multiplexer.
		16 bit transfers can proceed between the register array and address buffer

	Instruction register
		During an instruction fetch, the first byte of an instruction is transfered to the
		instruction register. This is in turn available to the instruction decoder.

	Data bus buffer
		Bidirectional
		3-state
		Used to isolate the CPU's internal bus from the external data bus
		In output mode, internal bus content is loaded
		In input mode, external bus content is loaded

	Processor cycle
		Instruction cycle
			Time it takes to fetch and execute an instruction.
			Every instruction cycle consists of one to five machine cycles.
		Machine cycle
			Time it takes for CPU o access memory or an IO port.
			Fetching an instruction takes one machine cycle per byte
			Some instructions do not require additional machine cycles, while
			others do such as those reading/writing to memory/IO.
			Each machine cycle consists of three to five states
			Events with one machine cycle duration:
				instruction fetch, memory read, memory write, stack read, stack write,
				input, output, interrupt, halt
		States
			Smallest unit of processing activity.
			Duration is interval between two successive rising edges (i.e. one clock period) of the
			delta1 clock signal.
			Exceptions to the duration are wait_state, hold_state, and halt_state. All three 
			depend on external events and thusly are of indeterminate length.
		Machine cycle identification
			The processor identifies the machine cycle in progress by transmitting a status byte
			during the first state of each machine cycle.

				D7 - Indicates that databus will be used for memory read
				D6 - Indicates address bus contains address of an input device and input data should
				     be placed on the databus when DBIN (databusIn) is active
				D5 - Indicates CPU is in fetch cycle for first byte of instruction
				D4 - Indicates address bus contains address of an output device and the databus will
				     contain the output data when WR (write) is active
				D3 - Indicates acknowledge of HALT instruction
				D2 - Indicates address bus holds the pushdown? address from SP
				D1 - When low, indicates operation in current machine cycle will be a memory write or
				     output function. When high, memory read or input.
				D0 - Indicates acknowledge of interrupt request.

				Machine cycle              76543210
				-------------              --------
				Instruction fetch          10100010
				Memory read                10000010
				Memory write               00000000
				Stack read                 10000110
				Stack write                00000100
				Input read                 01000010
				Output write               00010000
				Interrupt Ack              00100011
				Halt Ack                   10001010
				Interrupt Ack while halt   00101011
		State Transition Sequence
			...

'''

from memory import *
from time import sleep


class CPU():

	def __init__( self, memory ):

		# Control signals (wip) ----------------------------------

		self.halt = False  # temp for now
		# self.hold = False  # input, facilitates DMA by peripherals

		# IO
		self.IO_RD = 0  # output
		self.IO_WR = 0  # output


		# Peripherals --------------------------------------
		self.memory = memory

		self.ioDevices = [  # index simulates port number

			# terminal,
		]


		# Components ---------------------------------------
		self.addressBus = None  # 16bit. However only using it for IO so treat as 8bit
		self.dataBus = None  # 8bit, bidirectional

		self.register_AF = Register()  # accumulator & flags
		self.register_BC = Register()  # general purpose
		self.register_DE = Register()  # general purpose
		self.register_HL = Register()  # general purpose
		self.register_SP = Register()  # stack pointer
		self.register_PC = Register()  # program counter


		# Helpers ------------------------------------------
		self.nBits = 8
		self.largestPositiveInt = 2 ** ( self.nBits - 1 ) - 1
		self.negativeOne = 2 ** self.nBits - 1  # two's complement

		self.flagALU_carry    = 0
		self.flagALU_parity   = 0
		self.flagALU_auxCarry = 0
		self.flagALU_zero     = 0
		self.flagALU_sign     = 0
		
		self.instruction = None


		# Instruction decode -------------------------------
		self.instructionLookup = {

			# Move, load, store ---

			# MOV R1,R2 -> 01DDDSSS -> Move register to register
			0b01000000 : ( self.MOV_R1R2, ( self.register_BC, self.register_BC, True, True  ) ),
			0b01000001 : ( self.MOV_R1R2, ( self.register_BC, self.register_BC, True, False ) ),
			0b01000010 : ( self.MOV_R1R2, ( self.register_BC, self.register_DE, True, True  ) ),
			0b01000011 : ( self.MOV_R1R2, ( self.register_BC, self.register_DE, True, False ) ),
			0b01000100 : ( self.MOV_R1R2, ( self.register_BC, self.register_HL, True, True  ) ),
			0b01000101 : ( self.MOV_R1R2, ( self.register_BC, self.register_HL, True, False ) ),
			0b01000111 : ( self.MOV_R1R2, ( self.register_BC, self.register_AF, True, True  ) ),

			0b01001000 : ( self.MOV_R1R2, ( self.register_BC, self.register_BC, False, True  ) ),
			0b01001001 : ( self.MOV_R1R2, ( self.register_BC, self.register_BC, False, False ) ),
			0b01001010 : ( self.MOV_R1R2, ( self.register_BC, self.register_DE, False, True  ) ),
			0b01001011 : ( self.MOV_R1R2, ( self.register_BC, self.register_DE, False, False ) ),
			0b01001100 : ( self.MOV_R1R2, ( self.register_BC, self.register_HL, False, True  ) ),
			0b01001101 : ( self.MOV_R1R2, ( self.register_BC, self.register_HL, False, False ) ),
			0b01001111 : ( self.MOV_R1R2, ( self.register_BC, self.register_AF, False, True  ) ),

			0b01010000 : ( self.MOV_R1R2, ( self.register_DE, self.register_BC, True, True  ) ),
			0b01010001 : ( self.MOV_R1R2, ( self.register_DE, self.register_BC, True, False ) ),
			0b01010010 : ( self.MOV_R1R2, ( self.register_DE, self.register_DE, True, True  ) ),
			0b01010011 : ( self.MOV_R1R2, ( self.register_DE, self.register_DE, True, False ) ),
			0b01010100 : ( self.MOV_R1R2, ( self.register_DE, self.register_HL, True, True  ) ),
			0b01010101 : ( self.MOV_R1R2, ( self.register_DE, self.register_HL, True, False ) ),
			0b01010111 : ( self.MOV_R1R2, ( self.register_DE, self.register_AF, True, True  ) ),

			0b01011000 : ( self.MOV_R1R2, ( self.register_DE, self.register_BC, False, True  ) ),
			0b01011001 : ( self.MOV_R1R2, ( self.register_DE, self.register_BC, False, False ) ),
			0b01011010 : ( self.MOV_R1R2, ( self.register_DE, self.register_DE, False, True  ) ),
			0b01011011 : ( self.MOV_R1R2, ( self.register_DE, self.register_DE, False, False ) ),
			0b01011100 : ( self.MOV_R1R2, ( self.register_DE, self.register_HL, False, True  ) ),
			0b01011101 : ( self.MOV_R1R2, ( self.register_DE, self.register_HL, False, False ) ),
			0b01011111 : ( self.MOV_R1R2, ( self.register_DE, self.register_AF, False, True  ) ),

			0b01100000 : ( self.MOV_R1R2, ( self.register_HL, self.register_BC, True, True  ) ),
			0b01100001 : ( self.MOV_R1R2, ( self.register_HL, self.register_BC, True, False ) ),
			0b01100010 : ( self.MOV_R1R2, ( self.register_HL, self.register_DE, True, True  ) ),
			0b01100011 : ( self.MOV_R1R2, ( self.register_HL, self.register_DE, True, False ) ),
			0b01100100 : ( self.MOV_R1R2, ( self.register_HL, self.register_HL, True, True  ) ),
			0b01100101 : ( self.MOV_R1R2, ( self.register_HL, self.register_HL, True, False ) ),
			0b01100111 : ( self.MOV_R1R2, ( self.register_HL, self.register_AF, True, True  ) ),

			0b01101000 : ( self.MOV_R1R2, ( self.register_HL, self.register_BC, False, True  ) ),
			0b01101001 : ( self.MOV_R1R2, ( self.register_HL, self.register_BC, False, False ) ),
			0b01101010 : ( self.MOV_R1R2, ( self.register_HL, self.register_DE, False, True  ) ),
			0b01101011 : ( self.MOV_R1R2, ( self.register_HL, self.register_DE, False, False ) ),
			0b01101100 : ( self.MOV_R1R2, ( self.register_HL, self.register_HL, False, True  ) ),
			0b01101101 : ( self.MOV_R1R2, ( self.register_HL, self.register_HL, False, False ) ),
			0b01101111 : ( self.MOV_R1R2, ( self.register_HL, self.register_AF, False, True  ) ),

			0b01111000 : ( self.MOV_R1R2, ( self.register_AF, self.register_BC, True, True  ) ),
			0b01111001 : ( self.MOV_R1R2, ( self.register_AF, self.register_BC, True, False ) ),
			0b01111010 : ( self.MOV_R1R2, ( self.register_AF, self.register_DE, True, True  ) ),
			0b01111011 : ( self.MOV_R1R2, ( self.register_AF, self.register_DE, True, False ) ),
			0b01111100 : ( self.MOV_R1R2, ( self.register_AF, self.register_HL, True, True  ) ),
			0b01111101 : ( self.MOV_R1R2, ( self.register_AF, self.register_HL, True, False ) ),
			0b01111111 : ( self.MOV_R1R2, ( self.register_AF, self.register_AF, True, True  ) ),

			# MOV M,R -> 01110SSS -> Move register to memory
			0b01110000 : ( self.MOV_MR, ( self.register_BC, True  ) ),
			0b01110001 : ( self.MOV_MR, ( self.register_BC, False ) ),
			0b01110010 : ( self.MOV_MR, ( self.register_DE, True  ) ),
			0b01110011 : ( self.MOV_MR, ( self.register_DE, False ) ),
			0b01110100 : ( self.MOV_MR, ( self.register_HL, True  ) ),
			0b01110101 : ( self.MOV_MR, ( self.register_HL, False ) ),
			0b01110111 : ( self.MOV_MR, ( self.register_AF, True  ) ),

			# MOV R,M -> 01DDD110 -> Move memory to register
			0b01000110 : ( self.MOV_RM, ( self.register_BC, True  ) ),
			0b01001110 : ( self.MOV_RM, ( self.register_BC, False ) ),
			0b01010110 : ( self.MOV_RM, ( self.register_DE, True  ) ),
			0b01011110 : ( self.MOV_RM, ( self.register_DE, False ) ),
			0b01100110 : ( self.MOV_RM, ( self.register_HL, True  ) ),
			0b01101110 : ( self.MOV_RM, ( self.register_HL, False ) ),
			0b01111110 : ( self.MOV_RM, ( self.register_AF, True  ) ),

			# MVI R,data -> 00DDD110 -> Move immediate to register
			0b00000110 : ( self.MVI_RData, ( self.register_BC, True  ) ),
			0b00001110 : ( self.MVI_RData, ( self.register_BC, False ) ),
			0b00010110 : ( self.MVI_RData, ( self.register_DE, True  ) ),
			0b00011110 : ( self.MVI_RData, ( self.register_DE, False ) ),
			0b00100110 : ( self.MVI_RData, ( self.register_HL, True  ) ),
			0b00101110 : ( self.MVI_RData, ( self.register_HL, False ) ),
			0b00111110 : ( self.MVI_RData, ( self.register_AF, True  ) ),

			# MVI M,data -> 00110110 -> Move immediate to memory
			0b00110110 : ( self.MVI_MData, () ),

			# LXI BC,data16 -> 00000001 -> Load immediate to register pair B & C
			0b00000001 : ( self.LXI_RData16, ( self.register_BC, ) ),
			# LXI DE,data16 -> 00010001 -> Load immediate to register pair D & E
			0b00010001 : ( self.LXI_RData16, ( self.register_DE, ) ),
			# LXI HL,data16 -> 00100001 -> Load immediate to register pair H & L
			0b00100001 : ( self.LXI_RData16, ( self.register_HL, ) ),
			# LXI SP,data16 -> 00110001 -> Load immediate to stack pointer
			0b00110001 : ( self.LXI_RData16, ( self.register_SP, ) ),

			# LDA addr -> 00111010 -> Load A direct
			0b00111010 : ( self.LDA_Addr, () ),

			# STA addr -> 00110010 -> Store A direct
			0b00110010 : ( self.STA_Addr, () ),

			# LHLD addr -> 00101010 -> Load H & L direct
			0b00101010 : ( self.LHLD_Addr, () ),

			# SHLD addr -> 00100010 -> Store H & L direct
			0b00100010 : ( self.SHLD_Addr, () ),

			# LDAX BC -> 00001010 -> Load A indirect
			# LDAX DE -> 00011010 -> Load A indirect
			0b00001010 : ( self.LDAX_R, ( self.register_BC, ) ),
			0b00011010 : ( self.LDAX_R, ( self.register_DE, ) ),

			# STAX BC -> 00000010 -> Store A indirect
			# STAX DE -> 00010010 -> Store A indirect
			0b00000010 : ( self.STAX_R, ( self.register_BC, ) ),
			0b00010010 : ( self.STAX_R, ( self.register_DE, ) ),

			# XCHG -> 11101011 -> Exchange register pair D & E with H & L
			0b11101011 : ( self.XCHG, () ),


			# Stack ops ---

			# PUSH BC -> 11000101 -> Push register pair B & C on stack
			0b11000101 : ( self.PUSH_R, ( self.register_BC, ) ),
			# PUSH DE -> 11010101 -> Push register pair D & E on stack
			0b11010101 : ( self.PUSH_R, ( self.register_DE, ) ),
			# PUSH HL -> 11100101 -> Push register pair H & L on stack
			0b11100101 : ( self.PUSH_R, ( self.register_HL, ) ),

			# PUSH PSW -> 11110101 -> Push A and Flags on stack
			0b11110101 : ( self.PUSH_PSW, () ),

			# POP BC -> 11000001 -> Pop top of stack onto register pair B & C
			0b11000001 : ( self.POP_R, ( self.register_BC, ) ),
			# POP DE -> 11010001 -> Pop top of stack onto register pair D & E
			0b11010001 : ( self.POP_R, ( self.register_DE, ) ),
			# POP HL -> 11100001 -> Pop top of stack onto register pair H & L
			0b11100001 : ( self.POP_R, ( self.register_HL, ) ),

			# POP PSW  -> 11110001 -> Pop top of stack onto A and Flags
			0b11110001 : ( self.POP_PSW, () ),

			# XTHL -> 11100011 -> Exchange H & L with contents of location specified by stack pointer
			0b11100011 : ( self.XTHL, () ),

			# SPHL -> 11111001 -> H & L to stack pointer
			0b11111001 : ( self.SPHL, () ),


			# Jump ---

			# JMP addr -> 11000011 -> Jump unconditional
			0b11000011 : ( self.JMP, () ),
			# JNZ addr -> 11000010 -> Jump on not zero
			0b11000010 : ( self.JNZ, () ),
			# JZ addr -> 11001010 -> Jump on zero
			0b11001010 : ( self.JZ, () ),
			# JNC addr -> 11010010 -> Jump on no carry
			0b11010010 : ( self.JNC, () ),
			# JC addr -> 11011010 -> Jump on carry
			0b11011010 : ( self.JC, () ),
			# JPO addr -> 11100010 -> Jump on parity odd
			0b11100010 : ( self.JPO, () ),
			# JPE addr -> 11101010 -> Jump on parity even
			0b11101010 : ( self.JPE, () ),
			# JP addr -> 11110010 -> Jump on positive
			0b11110010 : ( self.JP, () ),
			# JM addr -> 11111010 -> Jump on minus
			0b11111010 : ( self.JM, () ),

			# PCHL -> 11101001 -> H & L to program counter
			0b11101001 : ( self.PCHL, () ),


			# Call ---

			# CALL addr -> 11001101 -> Call unconditional
			0b11001101 : ( self.CALL, () ),
			# CNZ addr -> 11000100 -> Call on not zero
			0b11000100 : ( self.CNZ, () ),
			# CZ addr -> 11001100 -> Call on zero
			0b11001100 : ( self.CZ, () ),
			# CNC addr -> 11010100 -> Call on no carry
			0b11010100 : ( self.CNC, () ),
			# CC addr -> 11011100 -> Call on carry
			0b11011100 : ( self.CC, () ),
			# CPO addr -> 11100100 -> Call on parity odd
			0b11100100 : ( self.CPO, () ),
			# CPE addr -> 11101100 -> Call on parity even
			0b11101100 : ( self.CPE, () ),
			# CP addr -> 11110100 -> Call on positive
			0b11110100 : ( self.CP, () ),
			# CM addr -> 11111100 -> Call on minus
			0b11111100 : ( self.CM, () ),


			# Return ---

			# RET -> 11001001 -> Return unconditional
			0b11001001 : ( self.RET, () ),
			# RNZ -> 11000000 -> Return on not zero
			0b11000000 : ( self.RNZ, () ),
			# RZ -> 11001000 -> Return on zero
			0b11001000 : ( self.RZ, () ),
			# RNC -> 11010000 -> Return on no carry
			0b11010000 : ( self.RNC, () ),
			# RC -> 11011000 -> Return on carry
			0b11011000 : ( self.RC, () ),
			# RPO -> 11100000 -> Return on parity odd
			0b11100000 : ( self.RPO, () ),
			# RPE -> 11101000 -> Return on parity even
			0b11101000 : ( self.RPE, () ),
			# RP -> 11110000 -> Return on positive
			0b11110000 : ( self.RP, () ),
			# RM -> 11111000 -> Return on minus
			0b11111000 : ( self.RM, () ),


			# Restart ---

			# RST -> 11NNN111 -> Restart
			0b11000111 : ( self.RST, ( 0, ) ),
			0b11001111 : ( self.RST, ( 1, ) ),
			0b11010111 : ( self.RST, ( 2, ) ),
			0b11011111 : ( self.RST, ( 3, ) ),
			0b11100111 : ( self.RST, ( 4, ) ),
			0b11101111 : ( self.RST, ( 5, ) ),
			0b11110111 : ( self.RST, ( 6, ) ),
			0b11111111 : ( self.RST, ( 7, ) ),

			# Increment and decrement ---

			# INR R -> 00DDD100 -> Increment register
			0b00000100 : ( self.INR_R, ( self.register_BC, True  ) ),
			0b00001100 : ( self.INR_R, ( self.register_BC, False ) ),
			0b00010100 : ( self.INR_R, ( self.register_DE, True  ) ),
			0b00011100 : ( self.INR_R, ( self.register_DE, False ) ),
			0b00100100 : ( self.INR_R, ( self.register_HL, True  ) ),
			0b00101100 : ( self.INR_R, ( self.register_HL, False ) ),
			0b00111100 : ( self.INR_R, ( self.register_AF, True  ) ),

			# INR M -> 00110100 -> Increment memory
			0b00110100 : ( self.INR_M, () ),

			# INX BC -> 00000011 -> Increment B & C registers
			0b00000011 : ( self.INX_R, ( self.register_BC, ) ),
			# INX DE -> 00010011 -> Increment D & E registers
			0b00010011 : ( self.INX_R, ( self.register_DE, ) ),
			# INX HL -> 00100011 -> Increment H & L registers
			0b00100011 : ( self.INX_R, ( self.register_HL, ) ),
			# INX SP -> 00110011 -> Increment stack pointer
			0b00110011 : ( self.INX_R, ( self.register_SP, ) ),

			# DCR R -> 00DDD101 -> Decrement register
			0b00000101 : ( self.DCR_R, ( self.register_BC, True  ) ),
			0b00001101 : ( self.DCR_R, ( self.register_BC, False ) ),
			0b00010101 : ( self.DCR_R, ( self.register_DE, True  ) ),
			0b00011101 : ( self.DCR_R, ( self.register_DE, False ) ),
			0b00100101 : ( self.DCR_R, ( self.register_HL, True  ) ),
			0b00101101 : ( self.DCR_R, ( self.register_HL, False ) ),
			0b00111101 : ( self.DCR_R, ( self.register_AF, True  ) ),

			# DCR M -> 00110101 -> Decrement memory
			0b00110101 : ( self.DCR_M, () ),

			# DCX BC -> 00001011 -> Decrement B & C registers
			0b00001011 : ( self.DCX_R, ( self.register_BC, ) ),
			# DCX DE -> 00011011 -> Decrement D & E registers
			0b00011011 : ( self.DCX_R, ( self.register_DE, ) ),
			# DCX HL -> 00101011 -> Decrement H & L registers
			0b00101011 : ( self.DCX_R, ( self.register_HL, ) ),
			# DCX SP -> 00111011 -> Decrement stack pointer
			0b00111011 : ( self.DCX_R, ( self.register_SP, ) ),
	

			# Add ---

			# ADD R -> 10000SSS -> Add register to A
			0b10000000 : ( self.ADD_R, ( self.register_BC, True  ) ),
			0b10000001 : ( self.ADD_R, ( self.register_BC, False ) ),
			0b10000010 : ( self.ADD_R, ( self.register_DE, True  ) ),
			0b10000011 : ( self.ADD_R, ( self.register_DE, False ) ),
			0b10000100 : ( self.ADD_R, ( self.register_HL, True  ) ),
			0b10000101 : ( self.ADD_R, ( self.register_HL, False ) ),
			0b10000111 : ( self.ADD_R, ( self.register_AF, True  ) ),

			# ADD M -> 10000110 -> Add memory to A
			0b10000110 : ( self.ADD_M, () ),

			# ADI data -> 11000110 -> Add immediate to A
			0b11000110 : ( self.ADI_Data, () ),

			# ADC R -> 10001SSS -> Add register to A with carry
			0b10001000 : ( self.ADC_R, ( self.register_BC, True  ) ),
			0b10001001 : ( self.ADC_R, ( self.register_BC, False ) ),
			0b10001010 : ( self.ADC_R, ( self.register_DE, True  ) ),
			0b10001011 : ( self.ADC_R, ( self.register_DE, False ) ),
			0b10001100 : ( self.ADC_R, ( self.register_HL, True  ) ),
			0b10001101 : ( self.ADC_R, ( self.register_HL, False ) ),
			0b10001111 : ( self.ADC_R, ( self.register_AF, True  ) ),

			# ADC M -> 10001110 -> Add memory to A with carry
			0b10001110 : ( self.ADC_M, () ),

			# ACI data -> 11001110 -> Add immediate to A with carry
			0b11001110 : ( self.ACI_Data, () ),

			# DAD BC -> 00001001 -> Add B & C to H & L
			0b00001001 : ( self.DAD_R, ( self.register_BC, ) ),
			# DAD DE -> 00011001 -> Add D & E to H & L
			0b00011001 : ( self.DAD_R, ( self.register_DE, ) ),
			# DAD HL -> 00101001 -> Add H & L to H & L
			0b00101001 : ( self.DAD_R, ( self.register_HL, ) ),
			# DAD SP -> 00111001 -> Add stack pointer to H & L
			0b00111001 : ( self.DAD_R, ( self.register_SP, ) ),


			# Subtract ---

			# SUB R -> 10010SSS -> Subtract register from A
			0b10010000 : ( self.SUB_R, ( self.register_BC, True  ) ),
			0b10010001 : ( self.SUB_R, ( self.register_BC, False ) ),
			0b10010010 : ( self.SUB_R, ( self.register_DE, True  ) ),
			0b10010011 : ( self.SUB_R, ( self.register_DE, False ) ),
			0b10010100 : ( self.SUB_R, ( self.register_HL, True  ) ),
			0b10010101 : ( self.SUB_R, ( self.register_HL, False ) ),
			0b10010111 : ( self.SUB_R, ( self.register_AF, True  ) ),

			# SUB M -> 10010110 -> Subtract memory from A
			0b10010110 : ( self.SUB_M, () ),

			# SUI data -> 11010110 -> Subtract immediate from A
			0b11010110 : ( self.SUI_Data, () ),

			# SBB R -> 10011SSS -> Subtract register from A with borrow
			0b10011000 : ( self.SBB_R, ( self.register_BC, True  ) ),
			0b10011001 : ( self.SBB_R, ( self.register_BC, False ) ),
			0b10011010 : ( self.SBB_R, ( self.register_DE, True  ) ),
			0b10011011 : ( self.SBB_R, ( self.register_DE, False ) ),
			0b10011100 : ( self.SBB_R, ( self.register_HL, True  ) ),
			0b10011101 : ( self.SBB_R, ( self.register_HL, False ) ),
			0b10011111 : ( self.SBB_R, ( self.register_AF, True  ) ),

			# SBB M -> 10011110 -> Subtract memory from A with borrow
			0b10011110 : ( self.SBB_M, () ),

			# SBI data -> 11011110 -> Subtract immediate from A with borrow
			0b11011110 : ( self.SBI_Data, () ),


			# Logical ---
			
			# ANA R -> 10100SSS -> And register with A
			0b10100000 : ( self.ANA_R, ( self.register_BC, True  ) ),
			0b10100001 : ( self.ANA_R, ( self.register_BC, False ) ),
			0b10100010 : ( self.ANA_R, ( self.register_DE, True  ) ),
			0b10100011 : ( self.ANA_R, ( self.register_DE, False ) ),
			0b10100100 : ( self.ANA_R, ( self.register_HL, True  ) ),
			0b10100101 : ( self.ANA_R, ( self.register_HL, False ) ),
			0b10100111 : ( self.ANA_R, ( self.register_AF, True  ) ),

			# ANA M -> 10100110 -> And memory with A
			0b10100110 : ( self.ANA_M, () ),

			# ANI data -> 11100110 -> And immediate with A
			0b11100110 : ( self.ANI_Data, () ),

			# XRA R -> 10101SSS -> Exclusive or register with A
			0b10101000 : ( self.XRA_R, ( self.register_BC, True  ) ),
			0b10101001 : ( self.XRA_R, ( self.register_BC, False ) ),
			0b10101010 : ( self.XRA_R, ( self.register_DE, True  ) ),
			0b10101011 : ( self.XRA_R, ( self.register_DE, False ) ),
			0b10101100 : ( self.XRA_R, ( self.register_HL, True  ) ),
			0b10101101 : ( self.XRA_R, ( self.register_HL, False ) ),
			0b10101111 : ( self.XRA_R, ( self.register_AF, True  ) ),

			# XRA M -> 10101110 -> Exclusive or memory with A
			0b10101110 : ( self.XRA_M, () ),

			# XRI data -> 11101110 -> Exclusive or immediate with A
			0b11101110 : ( self.XRI_Data, () ),

			# ORA R -> 10110SSS -> Or register with A
			0b10110000 : ( self.ORA_R, ( self.register_BC, True  ) ),
			0b10110001 : ( self.ORA_R, ( self.register_BC, False ) ),
			0b10110010 : ( self.ORA_R, ( self.register_DE, True  ) ),
			0b10110011 : ( self.ORA_R, ( self.register_DE, False ) ),
			0b10110100 : ( self.ORA_R, ( self.register_HL, True  ) ),
			0b10110101 : ( self.ORA_R, ( self.register_HL, False ) ),
			0b10110111 : ( self.ORA_R, ( self.register_AF, True  ) ),

			# ORA M -> 10110110 -> Or memory with A
			0b10110110 : ( self.ORA_M, () ),

			# ORI data -> 11110110 -> Or immediate with A
			0b11110110 : ( self.ORI_Data, () ),

			# CMP R -> 10111SSS -> Compare register with A
			0b10111000 : ( self.CMP_R, ( self.register_BC, True  ) ),
			0b10111001 : ( self.CMP_R, ( self.register_BC, False ) ),
			0b10111010 : ( self.CMP_R, ( self.register_DE, True  ) ),
			0b10111011 : ( self.CMP_R, ( self.register_DE, False ) ),
			0b10111100 : ( self.CMP_R, ( self.register_HL, True  ) ),
			0b10111101 : ( self.CMP_R, ( self.register_HL, False ) ),
			0b10111111 : ( self.CMP_R, ( self.register_AF, True  ) ),

			# CMP M -> 10111110 -> Compare memory with A
			0b10111110 : ( self.CMP_M, () ),

			# CPI data -> 11111110 -> Compare immediate with A
			0b11111110 : ( self.CPI_Data, () ),


			# Rotate ---

			# RLC -> 00000111 -> Rotate A left
			0b00000111 : ( self.RLC, () ),
			# RRC -> 00001111 -> Rotate A right
			0b00001111 : ( self.RRC, () ),
			# RAL -> 00010111 -> Rotate A left through carry
			0b00010111 : ( self.RAL, () ),
			# RAR -> 00011111 -> Rotate A right through carry
			0b00011111 : ( self.RAR, () ),


			# Specials ---

			# CMA -> 00101111 -> Complement A
			0b00101111 : ( self.CMA, () ),
			# CMC -> 00111111 -> Complement carry
			0b00111111 : ( self.CMC, () ),
			# STC -> 00110111 -> Set carry
			0b00110111 : ( self.STC, () ),
			# DAA -> 00100111 -> Decimal adjust A
			0b00100111 : ( self.DAA, () ),

			# Input / Output ---

			# IN port -> 11011011 -> Input
			0b11011011 : ( self.IN, () ),
			# OUT port -> 11010011 -> Output
			0b11010011 : ( self.OUT, () ),


			# Control ---

			# EI -> 11111011 -> Enable interrupts
			0b11111011 : ( self.EI, () ),
			# DI -> 11110011 -> Disable interrupt
			0b11110011 : ( self.DI, () ),
			# HLT -> 01110110 -> Halt
			0b01110110 : ( self.HLT, () ),
			# NOP -> 00000000 -> No operation
			0b00000000 : ( self.NOP, () ),
		}


	# Serial simulation ----------------------------------------

	def receive( self ):  # IN command

		# Bypass need for UART and get data directly from IO device

		ioDevice = self.ioDevices[ self.addressBus ]

		data = ioDevice.transmit()

		return data

	def transmit( self, data ):

		# Bypass need for UART and send data directly to IO device

		ioDevice = self.ioDevices[ self.addressBus ]

		ioDevice.receive( data )

	def jumpToISR( self, loc ):

		# Simulate interrupt handling
		self.RST( loc )


	# Helpers --------------------------------------------------

	def toWord( self, lo, hi ):

		return ( hi << 8 ) | lo

	def getUpperByte( self, x ):

		return ( x >> 8 ) & 0xff

	def getLowerByte( self, x ):

		return x & 0xff

	def read_A( self ):

		return self.register_AF.readUpperByte()

	def write_A( self, value ):

		self.register_AF.writeUpperByte( value )

	def read_M( self, address ):

		return self.memory[ address ]

	def write_M( self, address, value ):

		self.memory[ address ] = value


	def toBin( self, x ):

		return bin( x )[ 2 : ].zfill( self.nBits )

	def toInt( self, x ):

		return int( x, 2 )

	def getParity( self, x ):

		# modulo 2 sum of bits
		return sum( map( int, self.toBin( x ) ) ) % 2

	def negate( self, x ):

		# two's complement
		if x == 0 :

			return x

		else:

			return ( abs( x ) ^ self.negativeOne ) + 1

	def add( self, a, b, c = 0 ):

		z = a + b + c

		# Update carry flag
		if z > self.negativeOne:

			self.flagALU_carry = 1

		else:

			self.flagALU_carry = 0

		z &= self.negativeOne  # discard overflow bits

		# Update parity, zero, sign flags
		self.updateALUFlags_PZS( z )

		return z

	def sub( self, a, b, c = 0 ):

		z = a + self.negate( b + c )

		# Update carry flag
		#  https://retrocomputing.stackexchange.com/a/5956/
		if ( b + c ) > a:

			self.flagALU_carry = 1

		else:

			self.flagALU_carry = 0

		z &= self.negativeOne  # discard overflow bits

		# Update parity, zero, sign flags
		self.updateALUFlags_PZS( z )

		return z

	def and_( self, a, b ):

		z = a & b

		# Update carry flag
		self.flagALU_carry = 0

		# Update parity, zero, sign flags
		self.updateALUFlags_PZS( z )

		return z

	def or_( self, a, b ):

		z = a | b

		# Update carry flag
		self.flagALU_carry = 0

		# Update parity, zero, sign flags
		self.updateALUFlags_PZS( z )

		return z

	def xor_( self, a, b ):

		z = a ^ b

		# Update carry flag
		self.flagALU_carry = 0

		# Update parity, zero, sign flags
		self.updateALUFlags_PZS( z )

		return z


	def skip2Bytes( self ):

		self.fetchInstruction()
		self.fetchInstruction()


	# Flags ----------------------------------------------------

	def genByteFromALUFlags( self ):

		# SZ0A0P1C  (Order as seen in pg.4-13 of 8080 User Manual)

		b = self.flagALU_carry
		b |= self.flagALU_parity   << 2
		b |= self.flagALU_auxCarry << 4
		b |= self.flagALU_zero     << 6
		b |= self.flagALU_sign     << 7

		return b

	def setALUFlagsFromByte( self, b ):

		self.flagALU_carry    = b & 1
		self.flagALU_parity   = ( b >> 2 ) & 1
		self.flagALU_auxCarry = ( b >> 4 ) & 1
		self.flagALU_zero     = ( b >> 6 ) & 1
		self.flagALU_sign     = ( b >> 7 ) & 1

	def updateALUFlags_Register( self ):

		self.register_AF.writeLowerByte( self.genByteFromALUFlags() )

	def updateALUFlags_Variables( self ):

		self.setALUFlagsFromByte( self.register_AF.readLowerByte() )

	def updateALUFlags_PZS( self, value ):

		# Called after arithmetic or logical operation performed by ALU
		#  i.e. flags set according to value ALU outputs

		self.flagALU_parity   = 0
		self.flagALU_zero     = 0
		self.flagALU_sign     = 0

		if self.getParity( value ) == 0:

			self.flagALU_parity = 1

		if value == 0:

			self.flagALU_zero = 1

		if value > self.largestPositiveInt:  # two's complement

			self.flagALU_sign = 1

		self.updateALUFlags_Register()

		# print( '{:<8}{}'.format( 'carry',  c.flagALU_carry ) )
		# print( '{:<8}{}'.format( 'zero',   c.flagALU_zero ) )
		# print( '{:<8}{}'.format( 'sign',   c.flagALU_sign ) )
		# print( '{:<8}{}'.format( 'parity', c.flagALU_parity ) )


	# Run ------------------------------------------------------

	def run( self ):

		while not self.halt:

			self.fetchInstruction()

			self.executeInstruction()

		print( '8080 has halted' )

	def step( self ):

		self.fetchInstruction()

		self.executeInstruction()


	# Fetch Instruction ----------------------------------------

	def fetchInstruction( self ):

		instructionAddress = self.register_PC.read()

		self.register_PC.write( instructionAddress + 1 )  # increment

		self.instruction = self.memory[ instructionAddress ]

		# print( instructionAddress, self.instruction )

		return self.instruction


	# Execute Instruction --------------------------------------

	def executeInstruction( self ):

		func, args = self.instructionLookup[ self.instruction ]

		# print( '>', func.__name__ )
		# print( func, args )

		func( *args )


	# Move, load, store ---

	# MOV R1,R2 -> 01DDDSSS -> 1 -> Move register to register
	def MOV_R1R2( self, R1, R2, R1_upper, R2_upper ):

		if R1_upper:

			if R2_upper:

				R1.writeUpperByte( R2.readUpperByte() )

			else:

				R1.writeUpperByte( R2.readLowerByte() )

		else:

			if R2_upper:

				R1.writeLowerByte( R2.readUpperByte() )

			else:

				R1.writeLowerByte( R2.readLowerByte() )

	# MOV M,R -> 01110SSS -> 2 -> Move register to memory
	def MOV_MR( self, R, R_upper ):

		address = self.register_HL.read()

		if R_upper:

			self.write_M( address, R.readUpperByte() )

		else:

			self.write_M( address, R.readLowerByte() )

	# MOV R,M -> 01DDD110 -> 2 -> Move memory to register
	def MOV_RM( self, R, R_upper ):

		address = self.register_HL.read()

		if R_upper:

			R.writeUpperByte( self.read_M( address ) )

		else:

			R.writeLowerByte( self.read_M( address ) )

	# MVI R,data -> 00DDD110 -> 2 -> Move immediate to register
	def MVI_RData( self, R, R_upper ):

		byte2 = self.fetchInstruction()

		if R_upper:

			R.writeUpperByte( byte2 )

		else:

			R.writeLowerByte( byte2 )

	# MVI M,data -> 00110110 -> 3 -> Move immediate to memory
	def MVI_MData( self ):

		byte2 = self.fetchInstruction()

		address = self.register_HL.read()
		self.write_M( address, byte2 )

	# LXI BC,data16 -> 00000001 -> 3 -> Load immediate to register pair B & C
	# LXI DE,data16 -> 00010001 -> 3 -> Load immediate to register pair D & E
	# LXI HL,data16 -> 00100001 -> 3 -> Load immediate to register pair H & L
	# LXI SP,data16 -> 00110001 -> 3 -> Load immediate to stack pointer
	def LXI_RData16( self, R ):

		byte2 = self.fetchInstruction()
		byte3 = self.fetchInstruction()

		R.writeLowerByte( byte2 )
		R.writeUpperByte( byte3 )

	# LDA addr -> 00111010 -> 4 -> Load A direct
	def LDA_Addr( self ):

		byte2 = self.fetchInstruction()
		byte3 = self.fetchInstruction()

		address = self.toWord( byte2, byte3 )
		self.write_A( self.read_M( address ) )

	# STA addr -> 00110010 -> 4 -> Store A direct
	def STA_Addr( self ):

		byte2 = self.fetchInstruction()
		byte3 = self.fetchInstruction()

		address = self.toWord( byte2, byte3 )
		self.write_M( address, self.read_A() )

	# LHLD addr -> 00101010 -> 5 -> Load H & L direct
	def LHLD_Addr( self ):

		byte2 = self.fetchInstruction()
		byte3 = self.fetchInstruction()

		address = self.toWord( byte2, byte3 )
		self.register_HL.writeLowerByte( self.read_M( address ) )

		address += 1
		self.register_HL.writeUpperByte( self.read_M( address ) )

	# SHLD addr -> 00100010 -> 5 -> Store H & L direct
	def SHLD_Addr( self ):

		byte2 = self.fetchInstruction()
		byte3 = self.fetchInstruction()

		address = self.toWord( byte2, byte3 )
		self.write_M( address, self.register_HL.readLowerByte() )

		address += 1
		self.write_M( address, self.register_HL.readUpperByte() )

	# LDAX BC -> 00001010 -> 2 -> Load A indirect
	# LDAX DE -> 00011010 -> 2 -> Load A indirect
	def LDAX_R( self, R ):

		address = R.read()
		self.write_A( self.read_M( address ) )

	# STAX BC -> 00000010 -> 2 -> Store A indirect
	# STAX DE -> 00010010 -> 2 -> Store A indirect
	def STAX_R( self, R ):

		address = R.read()
		self.write_M( address, self.read_A() )

	# XCHG -> 11101011 -> 1 -> Exchange register pair D & E with H & L
	def XCHG( self ):

		temp = self.register_HL.read()
		self.register_HL.write( self.register_DE.read() )
		self.register_DE.write( temp )


	# Stack ops ---

	# PUSH BC -> 11000101 -> 3 -> Push register pair B & C on stack
	# PUSH DE -> 11010101 -> 3 -> Push register pair D & E on stack
	# PUSH HL -> 11100101 -> 3 -> Push register pair H & L on stack
	def PUSH_R( self, R ):

		SP = self.register_SP.read()
		self.write_M( SP - 1, R.readUpperByte() )
		self.write_M( SP - 2, R.readLowerByte() )
		self.register_SP.write( SP - 2 )

	# PUSH PSW -> 11110101 -> 3 -> Push A and Flags on stack
	def PUSH_PSW( self ):

		SP = self.register_SP.read()
		self.write_M( SP - 1, self.register_AF.readUpperByte() )
		self.write_M( SP - 2, self.register_AF.readLowerByte() )
		self.register_SP.write( SP - 2 )

	# POP BC -> 11000001 -> 3 -> Pop top of stack onto register pair B & C
	# POP DE -> 11010001 -> 3 -> Pop top of stack onto register pair D & E
	# POP HL -> 11100001 -> 3 -> Pop top of stack onto register pair H & L
	def POP_R( self, R ):

		SP = self.register_SP.read()
		R.writeLowerByte( self.read_M( SP     ) )
		R.writeUpperByte( self.read_M( SP + 1 ) )
		self.register_SP.write( SP + 2 )

	# POP PSW -> 11110001 -> 3 -> Pop top of stack onto A and Flags
	def POP_PSW( self ):

		SP = self.register_SP.read()
		self.register_AF.writeLowerByte( self.read_M( SP     ) )
		self.register_AF.writeUpperByte( self.read_M( SP + 1 ) )
		self.register_SP.write( SP + 2 )

		self.updateALUFlags_Variables()

	# XTHL -> 11100011 -> 5 -> Exchange H & L with contents of location specified by stack pointer
	def XTHL( self ):

		SP = self.register_SP.read()

		temp_lo = self.read_M( SP     )
		temp_hi = self.read_M( SP + 1 )

		self.write_M( SP,     self.register_HL.readLowerByte() )
		self.write_M( SP + 1, self.register_HL.readUpperByte() )

		self.register_HL.writeLowerByte( temp_lo )
		self.register_HL.writeUpperByte( temp_hi )

	# SPHL -> 11111001 -> 1 -> H & L to stack pointer
	def SPHL( self ):

		self.register_SP.write( self.register_HL.read() )


	# Jump ---

	# JMP addr -> 11000011 -> 3 -> Jump unconditional
	def JMP( self ):

		byte2 = self.fetchInstruction()
		byte3 = self.fetchInstruction()

		address = self.toWord( byte2, byte3 )
		self.register_PC.write( address )

	# JNZ addr -> 11000010 -> 3 -> Jump on not zero
	def JNZ( self ):

		if self.flagALU_zero == 0: self.JMP()

		else: self.skip2Bytes()

	# JZ addr -> 11001010 -> 3 -> Jump on zero
	def JZ( self ):

		if self.flagALU_zero == 1: self.JMP()

		else: self.skip2Bytes()

	# JNC addr -> 11010010 -> 3 -> Jump on no carry
	def JNC( self ):

		if self.flagALU_carry == 0: self.JMP()

		else: self.skip2Bytes()

	# JC addr -> 11011010 -> 3 -> Jump on carry
	def JC( self ):

		if self.flagALU_carry == 1: self.JMP()

		else: self.skip2Bytes()

	# JPO addr -> 11100010 -> 3 -> Jump on parity odd
	def JPO( self ):

		if self.flagALU_parity == 0: self.JMP()

		else: self.skip2Bytes()

	# JPE addr -> 11101010 -> 3 -> Jump on parity even
	def JPE( self ):

		if self.flagALU_parity == 1: self.JMP()

		else: self.skip2Bytes()

	# JP addr -> 11110010 -> 3 -> Jump on positive
	def JP( self ):

		if self.flagALU_sign == 0: self.JMP()

		else: self.skip2Bytes()

	# JM addr -> 11111010 -> 3 -> Jump on minus
	def JM( self ):

		if self.flagALU_sign == 1: self.JMP()

		else: self.skip2Bytes()

	# PCHL -> 11101001 -> 1 -> H & L to program counter
	def PCHL( self ):

		self.register_PC.write( self.register_HL.read() )


	# Call ---

	# CALL addr -> 11001101 -> 5 -> Call unconditional
	def CALL( self ):

		byte2 = self.fetchInstruction()
		byte3 = self.fetchInstruction()

		# Save return address onto stack
		SP = self.register_SP.read()
		self.write_M( SP - 1, self.register_PC.readUpperByte() )
		self.write_M( SP - 2, self.register_PC.readLowerByte() )
		self.register_SP.write( SP - 2 )

		# Goto called address
		address = self.toWord( byte2, byte3 )
		self.register_PC.write( address )

	# CNZ addr -> 11000100 -> 3/5 -> Call on not zero
	def CNZ( self ):

		if self.flagALU_zero == 0: self.CALL()

		else: self.skip2Bytes()

	# CZ addr -> 11001100 -> 3/5 -> Call on zero
	def CZ( self ):

		if self.flagALU_zero == 1: self.CALL()

		else: self.skip2Bytes()

	# CNC addr -> 11010100 -> 3/5 -> Call on no carry
	def CNC( self ):

		if self.flagALU_carry == 0: self.CALL()

		else: self.skip2Bytes()

	# CC addr -> 11011100 -> 3/5 -> Call on carry
	def CC( self ):

		if self.flagALU_carry == 1: self.CALL()

		else: self.skip2Bytes()

	# CPO addr -> 11100100 -> 3/5 -> Call on parity odd
	def CPO( self ):

		if self.flagALU_parity == 0: self.CALL()

		else: self.skip2Bytes()

	# CPE addr -> 11101100 -> 3/5 -> Call on parity even
	def CPE( self ):

		if self.flagALU_parity == 1: self.CALL()

		else: self.skip2Bytes()

	# CP addr -> 11110100 -> 3/5 -> Call on positive
	def CP( self ):

		if self.flagALU_sign == 0: self.CALL()

		else: self.skip2Bytes()

	# CM addr -> 11111100 -> 3/5 -> Call on minus
	def CM( self ):

		if self.flagALU_sign == 1: self.CALL()

		else: self.skip2Bytes()


	# Return ---

	# RET -> 11001001 -> 3 -> Return 
	def RET( self ):

		# Goto return address saved on stack
		SP = self.register_SP.read()
		self.register_PC.writeLowerByte( self.read_M( SP     ) )
		self.register_PC.writeUpperByte( self.read_M( SP + 1 ) )
		self.register_SP.write( SP + 2 )

	# RNZ -> 11000000 -> 1/3 -> Return on not zero
	def RNZ( self ):

		if self.flagALU_zero == 0: self.RET()

	# RZ -> 11001000 -> 1/3 -> Return on zero
	def RZ( self ):

		if self.flagALU_zero == 1: self.RET()

	# RNC -> 11010000 -> 1/3 -> Return on no carry
	def RNC( self ):

		if self.flagALU_carry == 0: self.RET()

	# RC -> 11011000 -> 1/3 -> Return on carry
	def RC( self ):

		if self.flagALU_carry == 1: self.RET()

	# RPO -> 11100000 -> 1/3 -> Return on parity odd
	def RPO( self ):

		if self.flagALU_parity == 0: self.RET()

	# RPE -> 11101000 -> 1/3 -> Return on parity even
	def RPE( self ):

		if self.flagALU_parity == 1: self.RET()

	# RP -> 11110000 -> 1/3 -> Return on positive
	def RP( self ):

		if self.flagALU_sign == 0: self.RET()

	# RM -> 11111000 -> 1/3 -> Return on minus
	def RM( self ):

		if self.flagALU_sign == 1: self.RET()


	# Restart ---

	# RST -> 11NNN111 -> 3 -> Restart
	def RST( self, NNN ):

		# Save return address onto stack
		SP = self.register_SP.read()
		self.write_M( SP - 1, self.register_PC.readUpperByte() )
		self.write_M( SP - 2, self.register_PC.readLowerByte() )
		self.register_SP.write( SP - 2 )

		# Goto address 8 * NNN
		self.register_PC.write( 8 * NNN )


	# Increment and decrement ---

	# INR R -> 00DDD100 -> 1 -> Increment register
	def INR_R( self, R, R_upper ):

		savedCarry = self.flagALU_carry  # according to docs, all condition flags affected except carry
		
		if R_upper:

			z = self.add( R.readUpperByte(), 1 )
			R.writeUpperByte( z )

		else:

			z = self.add( R.readLowerByte(), 1 )
			R.writeLowerByte( z )

		self.flagALU_carry = savedCarry

		self.updateALUFlags_Register()

	# INR M -> 00110100 -> 3 -> Increment memory
	def INR_M( self ):

		savedCarry = self.flagALU_carry  # according to docs, all condition flags affected except carry
			
		address = self.register_HL.read()

		z = self.add( self.read_M( address ), 1 )
		self.write_M( address, z )

		self.flagALU_carry = savedCarry

		self.updateALUFlags_Register()

	# INX BC -> 00000011 -> 1 -> Increment B & C register pair
	# INX DE -> 00010011 -> 1 -> Increment D & E register pair
	# INX HL -> 00100011 -> 1 -> Increment H & L register pair
	# INX SP -> 00110011 -> 1 -> Increment stack pointer
	def INX_R( self, R ):

		z = R.read() + 1  # according to docs, no ALU flags are affected
		z &= 0xffff  # discard overflow bits
		R.write( z )

	# DCR R -> 00DDD101 -> 1 -> Decrement register
	def DCR_R( self, R, R_upper ):

		savedCarry = self.flagALU_carry  # according to docs, all condition flags affected except carry

		if R_upper:

			z = self.sub( R.readUpperByte(), 1 )
			R.writeUpperByte( z )

		else:

			z = self.sub( R.readLowerByte(), 1 )
			R.writeLowerByte( z )

		self.flagALU_carry = savedCarry

		self.updateALUFlags_Register()

	# DCR M -> 00110101 -> 3 -> Decrement memory
	def DCR_M( self ):

		savedCarry = self.flagALU_carry  # according to docs, all condition flags affected except carry

		address = self.register_HL.read()

		z = self.sub( self.read_M( address ), 1 )
		self.write_M( address, z )

		self.flagALU_carry = savedCarry

		self.updateALUFlags_Register()

	# DCX BC -> 00001011 -> 1 -> Decrement B & C register pair
	# DCX DE -> 00011011 -> 1 -> Decrement D & E register pair
	# DCX HL -> 00101011 -> 1 -> Decrement H & L register pair
	# DCX SP -> 00111011 -> 1 -> Decrement stack pointer
	def DCX_R( self, R ):

		curVal = R.read()

		# according to docs, no ALU flags are affected
		if curVal == 0:

			z = 0xffff  # two's complement negative one

		else:
			
			z = curVal - 1

		R.write( z )


	# Add ---

	# ADD R -> 10000SSS -> 1 -> Add register to A
	def ADD_R( self, R, R_upper ):

		curVal = self.read_A()

		if R_upper:

			z = self.add( curVal, R.readUpperByte() )

		else:

			z = self.add( curVal, R.readLowerByte() )
		
		self.write_A( z )

	# ADD M -> 10000110 -> 2 -> Add memory to A
	def ADD_M( self ):

		curVal = self.read_A()

		address = self.register_HL.read()

		z = self.add( curVal, self.read_M( address ) )
		self.write_A( z )

	# ADI data -> 11000110 -> 2 -> Add immediate to A
	def ADI_Data( self ):

		byte2 = self.fetchInstruction()

		curVal = self.read_A()

		z = self.add( curVal, byte2 )
		self.write_A( z )

	# ADC R -> 10001SSS -> 1 -> Add register to A with carry
	def ADC_R( self, R, R_upper ):

		curVal = self.read_A()

		if R_upper:

			z = self.add( curVal, R.readUpperByte(), self.flagALU_carry )

		else:

			z = self.add( curVal, R.readLowerByte(), self.flagALU_carry )
		
		self.write_A( z )

	# ADC M -> 10001110 -> 2 -> Add memory to A with carry
	def ADC_M( self ):

		curVal = self.read_A()

		address = self.register_HL.read()

		z = self.add( curVal, self.read_M( address ), self.flagALU_carry )
		self.write_A( z )

	# ACI data -> 11001110 -> 2 -> Add immediate to A with carry
	def ACI_Data( self ):

		byte2 = self.fetchInstruction()

		curVal = self.read_A()

		z = self.add( curVal, byte2, self.flagALU_carry )
		self.write_A( z )

	# DAD BC -> 00001001 -> 3 -> Add B & C to H & L
	# DAD DE -> 00011001 -> 3 -> Add D & E to H & L
	# DAD HL -> 00101001 -> 3 -> Add H & L to H & L
	# DAD SP -> 00111001 -> 3 -> Add stack pointer to H & L
	def DAD_R( self, R ):

		z = self.register_HL.read() + R.read()

		# according to docs, only carry flag is affected
		if z > 0xffff:

			self.flagALU_carry = 1

		else:

			self.flagALU_carry = 0

		z &= 0xffff  # discard overflow bits

		self.register_HL.write( z )

		self.updateALUFlags_Register()

	# Subtract ---

	# SUB R -> 10010SSS -> 1 -> Subtract register from A
	def SUB_R( self, R, R_upper ):

		curVal = self.read_A()

		if R_upper:

			z = self.sub( curVal, R.readUpperByte() )

		else:

			z = self.sub( curVal, R.readLowerByte() )
		
		self.write_A( z )

	# SUB M -> 10010110 -> 2 -> Subtract memory from A
	def SUB_M( self ):

		curVal = self.read_A()

		address = self.register_HL.read()

		z = self.sub( curVal, self.read_M( address ) )
		self.write_A( z )

	# SUI data -> 11010110 -> 2 -> Subtract immediate from A
	def SUI_Data( self ):

		byte2 = self.fetchInstruction()

		curVal = self.read_A()

		z = self.sub( curVal, byte2 )
		self.write_A( z )

	# SBB R -> 10011SSS -> 1 -> Subtract register from A with borrow
	def SBB_R( self, R, R_upper ):

		curVal = self.read_A()

		if R_upper:

			z = self.sub( curVal, R.readUpperByte(), self.flagALU_carry )

		else:

			z = self.sub( curVal, R.readLowerByte(), self.flagALU_carry )
		
		self.write_A( z )

	# SBB M -> 10011110 -> 2 -> Subtract memory from A with borrow
	def SBB_M( self ):

		curVal = self.read_A()

		address = self.register_HL.read()

		z = self.sub( curVal, self.read_M( address ), self.flagALU_carry )
		self.write_A( z )

	# SBI data -> 11011110 -> 2 -> Subtract immediate from A with borrow
	def SBI_Data( self ):

		byte2 = self.fetchInstruction()

		curVal = self.read_A()

		z = self.sub( curVal, byte2, self.flagALU_carry )
		self.write_A( z )


	# Logical ---

	# ANA R -> 10100SSS -> 1 -> And register with A
	def ANA_R( self, R, R_upper ):

		curVal = self.read_A()

		if R_upper:

			z = self.and_( curVal, R.readUpperByte() )

		else:

			z = self.and_( curVal, R.readLowerByte() )
		
		self.write_A( z )

	# ANA M -> 10100110 -> 2 -> And memory with A
	def ANA_M( self ):

		curVal = self.read_A()

		address = self.register_HL.read()

		z = self.and_( curVal, self.read_M( address ) )
		self.write_A( z )

	# ANI data -> 11100110 -> 2 -> And immediate with A
	def ANI_Data( self ):

		byte2 = self.fetchInstruction()

		curVal = self.read_A()

		z = self.and_( curVal, byte2 )
		self.write_A( z )

	# XRA R -> 10101SSS -> 1 -> Exclusive or register with A
	def XRA_R( self, R, R_upper ):

		curVal = self.read_A()

		if R_upper:

			z = self.xor_( curVal, R.readUpperByte() )

		else:

			z = self.xor_( curVal, R.readLowerByte() )
		
		self.write_A( z )

	# XRA M -> 10101110 -> 2 -> Exclusive or memory with A
	def XRA_M( self ):

		curVal = self.read_A()

		address = self.register_HL.read()

		z = self.xor_( curVal, self.read_M( address ) )
		self.write_A( z )

	# XRI data -> 11101110 -> 2 -> Exclusive or immediate with A
	def XRI_Data( self ):

		byte2 = self.fetchInstruction()

		curVal = self.read_A()

		z = self.xor_( curVal, byte2 )
		self.write_A( z )

	# ORA R -> 10110SSS -> 1 -> Or register with A
	def ORA_R( self, R, R_upper ):

		curVal = self.read_A()

		if R_upper:

			z = self.or_( curVal, R.readUpperByte() )

		else:

			z = self.or_( curVal, R.readLowerByte() )
		
		self.write_A( z )

	# ORA M -> 10110110 -> 2 -> Or memory with A
	def ORA_M( self ):

		curVal = self.read_A()

		address = self.register_HL.read()

		z = self.or_( curVal, self.read_M( address ) )
		self.write_A( z )

	# ORI data -> 11110110 -> 2 -> Or immediate with A
	def ORI_Data( self ):

		byte2 = self.fetchInstruction()

		curVal = self.read_A()

		z = self.or_( curVal, byte2 )
		self.write_A( z )

	# CMP R -> 10111SSS -> 1 -> Compare register with A
	def CMP_R( self, R, R_upper ):

		if R_upper:

			r = R.readUpperByte()

		else:

			r = R.readLowerByte()

		self.sub( self.read_A(), r )

	# CMP M -> 10111110 -> 2 -> Compare memory with A
	def CMP_M( self ):

		address = self.register_HL.read()

		self.sub( self.read_A(), self.read_M( address ) )

	# CPI data -> 11111110 -> 2 -> Compare immediate with A
	def CPI_Data( self ):

		byte2 = self.fetchInstruction()

		self.sub( self.read_A(), byte2 )


	# Rotate ---

	# RLC -> 00000111 -> 1 -> Rotate A left
	def RLC( self ):

		b = self.toBin( self.read_A() )

		sout = b[ 0 ]
		
		b = b[ 1 : ] + sout

		self.write_A( self.toInt( b ) )

		self.flagALU_carry = int( sout )

		self.updateALUFlags_Register()

	# RRC -> 00001111 -> 1 -> Rotate A right
	def RRC( self ):

		b = self.toBin( self.read_A() )

		sout = b[ self.nBits - 1 ]
		
		b = sout + b[ : - 1 ]

		self.write_A( self.toInt( b ) )

		self.flagALU_carry = int( sout )

		self.updateALUFlags_Register()

	# RAL -> 00010111 -> 1 -> Rotate A left through carry
	def RAL( self ):

		b = self.toBin( self.read_A() )

		sout = b[ 0 ]

		b = b[ 1 : ] + str( self.flagALU_carry )

		self.write_A( self.toInt( b ) )

		self.flagALU_carry = int( sout )

		self.updateALUFlags_Register()

	# RAR -> 00011111 -> 1 -> Rotate A right through carry
	def RAR( self ):

		b = self.toBin( self.read_A() )

		sout = b[ self.nBits - 1 ]

		b = str( self.flagALU_carry ) + b[ : - 1 ]

		self.write_A( self.toInt( b ) )

		self.flagALU_carry = int( sout )

		self.updateALUFlags_Register()


	# Specials ---

	# CMA -> 00101111 -> 1 -> Complement A
	def CMA( self ):

		self.write_A( self.read_A() ^ self.negativeOne )  # flip bits

	# CMC -> 00111111 -> 1 -> Complement carry
	def CMC( self ):

		self.flagALU_carry ^= 1  # flip

		self.updateALUFlags_Register()

	# STC -> 00110111 -> 1 -> Set carry
	def STC( self ):

		self.flagALU_carry = 1

		self.updateALUFlags_Register()

	# DAA -> 00100111 -> x -> Decimal adjust A
	def DAA( self ):

		raise Exception( 'DAA instruction not implemented' )

	# Input / Output ---

	# IN port -> 11011011 -> 3 -> Input. Read byte from specified port and load to A
	def IN( self ):

		byte2 = self.fetchInstruction()  # get port number. Used to select IO device
		self.addressBus = byte2

		# self.IO_WR = 1                   # signal IO device to write to databus
		# self.write_A( self.dataBus )     # get data placed on databus by IO device
		# self.IO_WR = 0                   # signal IO device to stop writing to databus

		data = self.receive()  # simulate
		self.write_A( data )

	# OUT port -> 11010011 -> 3 -> Output. Places contents of A onto data bus and the
	#                                      selected port number onto the address bus
	def OUT( self ):

		byte2 = self.fetchInstruction()  # get port number. Used to select IO device
		self.addressBus = byte2

		# self.dataBus = self.read_A()     # place contents of A onto databus
		# self.IO_RD = 1                   # signal IO device to read from databus
		# sleep( 0.1 )                     # wait for IO device to read?? one clock pulse??
		# self.IO_RD = 0                   # signal IO device to stop reading from databus

		# simulate
		data = self.read_A()
		self.transmit( data )



	# Control ---

	# EI -> 11111011 -> 1 -> Enable interrupts (takes effect next instruction)
	def EI( self ):

		# self.flagCC_interruptEnable = 1
		pass

	# DI -> 11110011 -> 1 -> Disable interrupt (takes effect immediately)
	def DI( self ):

		# self.flagCC_interruptEnable = 0
		pass

	# HLT -> 01110110 -> 1 -> Halt
	def HLT( self ):

		# Temp for now
		self.halt = True

		print( 'HLT instruction executed' )

	# NOP -> 00000000 -> 1 -> No operation
	def NOP( self ): pass
