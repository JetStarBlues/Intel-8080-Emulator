from computer import *

c = Computer( 65535 )

# programPath = 'Programs/sample_code.asm'
# programPath = 'Programs/sample_code_5.asm'
# programPath = 'Programs/sample_code_6.asm'
# programPath = 'Programs/sample_code_7a.asm'
programPath = 'Programs/tinybasic-2.0-mod.asm'
# programPath = '../cpm22_8080.asm'


c.loadProgram( programPath )

# c.dumpMemory()

c.terminal.debugMode = True

c.run()

# print( '>>', c.CPU.register_BC.read() )
# print( '>>', c.CPU.register_AF.readUpperByte() )
