from computer import *

c = Computer( 65535 )


programPath = 'Programs/tinybasic-2.0-mod.asm'


c.loadProgram( programPath )


# textSourcePath = 'Programs/tinybasic/helloTB.basic'
# textSourcePath = 'Programs/tinybasic/EuphoriaTB.basic'


# c.terminal.tooLazyToType( textSourcePath )


c.run()
