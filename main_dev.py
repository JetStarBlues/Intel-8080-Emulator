from computer import *

c = Computer( 65535 )

# programPath = 'Programs/sample_code.asm'
# programPath = 'Programs/sample_code_3.asm'
# programPath = 'Programs/sample_code_5.asm'
# programPath = 'Programs/sample_code_6.asm'
# programPath = 'Programs/sample_code_7a.asm'
# programPath = 'Programs/sample_code_7a.bin'
# programPath = 'Programs/smallest_number.asm'
# programPath = 'Programs/cpudiag_mod.asm'
# programPath = 'Programs/8080exerciser.asm'
programPath = 'Programs/tinybasic-2.0-mod.asm'
# programPath = 'Programs/tinybasic-2.0-mod.bin'
# programPath = 'Programs/tempTestComp.asm'
# programPath = '../cpm22_8080.asm'


c.loadProgram( programPath )
# c.loadProgram( programPath, isAssembly=False )


dumpFolderPath = '../../../tmp2/'
c.dumpFolderPath = dumpFolderPath

# c.dumpMemory()

# c.terminal.debugMode = True

c.breakpoint = 391
# c.breakpoint = 1e9  # infinity to allow stepping when reach HLT

# textSourcePath = 'Programs/tinybasic/needMoreSupport/TicTacToeTB.basic'
# textSourcePath = 'Programs/tinybasic/needMoreSupport/LifeTB.basic'
# textSourcePath = 'Programs/tinybasic/needMoreSupport/TinyAdventureTB.basic'
# textSourcePath = 'Programs/tinybasic/gcta.basic'
# textSourcePath = 'Programs/tinybasic/helloTB.basic'
# textSourcePath = 'Programs/tinybasic/EuphoriaTB_mod.basic'
textSourcePath = 'Programs/tinybasic/EuphoriaTB.basic'
# textSourcePath = 'Programs/tinybasic/tests/testPrint.basic'
# textSourcePath = 'Programs/tinybasic/wip/tictactoeTB.basic'


# c.terminal.tooLazyToType( textSourcePath )


c.run()
# c.run( step=True )  # debug
