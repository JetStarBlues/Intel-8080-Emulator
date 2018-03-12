from computer import *

c = Computer( 65535 )

# programPath = 'Programs/sample_code.asm'
# programPath = 'Programs/sample_code_5.asm'
# programPath = 'Programs/sample_code_6.asm'
# programPath = 'Programs/sample_code_7a.asm'
# programPath = 'Programs/sample_code_9.asm'
# programPath = 'Programs/smallest_number.asm'
# programPath = 'Programs/cpudiag_mod.asm'
programPath = 'Programs/tinybasic-2.0-mod.asm'
# programPath = '../cpm22_8080.asm'


c.loadProgram( programPath )


dumpFilePath = '../../../tmp2/'
c.dumpFilePath = dumpFilePath

# c.dumpMemory()

# c.terminal.debugMode = True

# c.breakpoint = 1360
# c.breakpoint = 1e9  # infinity to allow stepping when reach HLT

# textSourcePath = 'Programs/tinybasic/helloTB.basic'
# textSourcePath = 'Programs/tinybasic/TicTacToeTB.basic'
# textSourcePath = 'Programs/tinybasic/LifeTB.basic'
# textSourcePath = 'Programs/tinybasic/EuphoriaTB.basic'
# textSourcePath = 'Programs/tinybasic/TinyAdventureTB.basic'
textSourcePath = 'Programs/tinybasic/gcta.basic'


c.terminal.tooLazyToType( textSourcePath )


c.run()
# c.run( step=True )  # debug
