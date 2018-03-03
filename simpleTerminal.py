# Scrollbar, https://stackoverflow.com/a/3092341
# Frame resize, https://stackoverflow.com/a/29322445

import tkinter

width = 400
height = 300
textColor = '#689497'
bgColor = '#fff4dc'

root = tkinter.Tk()
root.title( 'A Name' )
root.configure(

	# width = width,
	# height = height,
	# bg = bgColor
	bg = '#007700'
)


canvas = tkinter.Canvas( root )
canvas.pack( side = tkinter.LEFT, expand = True, fill = 'both' )
canvas.configure(

	width = width,
	height = height,
	highlightthickness = 0,
	bg = bgColor
	# bg = '#770000'
)


scrollbar = tkinter.Scrollbar( root )
scrollbar.pack( side = tkinter.RIGHT, fill = 'y' )
scrollbar.configure(

	orient = "vertical",
	command = canvas.yview
)

canvas.configure( yscrollcommand = scrollbar.set )


frame = tkinter.Frame( canvas )
frame.configure( bg = '#000077' )

canvasFrame = canvas.create_window( ( 0, 0 ), window = frame, anchor = 'nw' )


def onFrameConfigure( event ):

	# resize canvas
	canvas.configure( scrollregion = canvas.bbox( 'all' ) )

def onCanvasConfigure( event ):

	# resize frame
	canvas.itemconfigure( canvasFrame, width = event.width )

frame.bind( '<Configure>', onFrameConfigure )
canvas.bind( '<Configure>', onCanvasConfigure )


prompt = tkinter.Label( frame )
prompt.pack( expand = True, fill = 'both' )
prompt.configure(

	fg = textColor,
	bg = bgColor,
	anchor = 'nw',
	justify = tkinter.LEFT
	# wraplength = width - 5,
)


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
