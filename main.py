import Tkinter as tk
from Tkinter import Menu
import ScrolledText
import sys
import threading
from parser import parse, error, ParserError,start
from interpreter import interpret
from lex import get_tokens
class StdoutRedirector(object):
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')

# http://knowpapa.com/text-editor/
root = tk.Tk(className="Best Language Ever")

textPad = ScrolledText.ScrolledText(root, width=300, height=30)
textPad.pack() # creates text area
textWidget = tk.Text(root,width=300, height=40,bg='black',fg='green',highlightcolor='yellow')
textWidget.pack()
sys.stdout = StdoutRedirector(textWidget)

# create a menu
def run():
    global dictionary, code
    # console.start()
    code = textPad.get("1.0",tk.END+'-1c')
    # print code
    filename = 'test.vote'
    newfile = open(filename,'w')
    newfile.write(code )
    newfile.close()
    dictionary = get_tokens(filename)

    if (dictionary):
        try:
            start
        except ParserError as e:
            error(e,code)
            return
    interpret()
    print 'done'
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Run", command=run)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=run)
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=run)
# end of menu creation

# textPad.pack()
root.mainloop()