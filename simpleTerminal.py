import tkinter

root = tkinter.Tk()
width = 400
height = 200
# root.geometry('{}x{}'.format( width , height ) )
root.config( width = width , height = height )
root.title( 'A Name' )


prompt = tkinter.Label( root )
# prompt.pack()
prompt.place( relx = 0, rely = 0 )
prompt.config( wraplength = width - 5, justify = tkinter.LEFT )


textColor = "#689497"
bgColor = "#fff4dc"
prompt.config( fg = textColor, bg = bgColor )
root.config( bg = bgColor )

# prompt[ 'text' ] = '> Hello!'
# prompt[ 'text' ] = 'You can also use elegant structures like tabs and marks to locate specific sections of the text, and apply changes to those areas. Moreover, you can embed windows and images in the text because this widget was designed to handle both plain and formatted text.'
# prompt[ 'text' ] = 'Youcanalsouseelegantstructuresliketabsandmarkstolocatespecificsectionsofthetext,andapplychangestothoseareas.Moreover,youcanembedwindowsandimagesinthetextbecausethiswidgetwasdesignedtohandlebothplainandformattedtext.'

promptText = '> _'  # for debug
prompt[ 'text' ] = promptText


codesOfInterest = [

	3,   # CTRL + C
	8,   # backspace
	10,  # newline
	13,  # newline
	15,  # CTRL + O
]


def getUserInput( event ):

	global promptText

	# print( event.char )
	# print( repr( event.char ) )

	if event.char:

		ccode = ord( event.char )

		if ccode in codesOfInterest:

			if ccode == 8:  # backspace

				promptText = promptText[ : - 2 ] + '_'  # for debug (TB will control display)

			elif ccode == 10 or ccode == 13:  # newline

				promptText = promptText[ : - 1 ] + '\n  _'  # for debug (TB will control display)

			elif ccode == 3:

				print( 'Hey, I recognized it' )

			prompt[ 'text' ] = promptText  # update
			return ccode

		elif ccode >= 32 and ccode <= 126:  # printable characters

			promptText = promptText[ : - 1 ] + str( event.char ) + '_'  # for debug (TB will control display)

			prompt[ 'text' ] = promptText  # update
			return ccode

		else: pass

def onClose():

	print( 'cya' )

	root.destroy()

root.bind( '<KeyPress>', getUserInput )

root.protocol( 'WM_DELETE_WINDOW', onClose )

root.mainloop()
