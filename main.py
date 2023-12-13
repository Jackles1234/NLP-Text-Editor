from tkinter import *
from tkinter import filedialog
from tkinter import font
import os
import side_menu
import spell_check
from PIL import ImageTk,Image
import ws
import model
root = Tk()
root.title('Textpad')
root.geometry('1200x660')


global open_status_name
open_status_name = False

global selected
selected = False

global definition
definition = ""

global thes
thes = [""]
#Create new File
def new_file():
    my_text.delete("1.0", END)
    root.title('New File - Textpad')
    status_bar.config(text="New File        ")

def open_file(): 
    my_text.delete("1.0", END)
    text_file = filedialog.askopenfile(initialdir="C:/Users/jackw/PyCharm_Projects/files", title="Open File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*py"), ("All Files", "*.*")))
    name = str(os.path.abspath(text_file.name))
    if text_file:
        global open_status_name
        open_status_name = name
    
    status_bar.config(text=f'{name}      ')
    name.replace("C:/Users/jackw/PyCharm_Projects/files", "")
    root.title(f'{name} - Textpad')

    with open(name, 'r', encoding='utf-8-sig') as text_file2:
        stuff = text_file2.read()

        my_text.insert(END, stuff)
        text_file2.close()

def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/Users/jackw/PyCharm_Projects/files", title="Save File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))

    if text_file:
        name = text_file
        status_bar.config(text=f'{name}      ')
        name = name.replace("C:/Users/jackw/PyCharm_Projects/files", "")
        root.title(f'{name} - Textpad')

        with open(text_file, 'w', encoding='utf-8-sig') as text_file:
            text_file.write(my_text.get(1.0, END))
            text_file.close()

def save_file():
    global open_status_name
    if open_status_name:
        with open(open_status_name, 'w', encoding='utf-8-sig') as text_file:
            text_file.write(my_text.get(1.0, END))
            text_file.close()
            status_bar.config(text=f'Saved: {open_status_name}      ')

    else:
        save_as_file()


def cut_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            #grab text
            selected = my_text.selection_get()
            #delete text
            my_text.delete("sel.first", "sel.last")
            
            root.clipboard_clear()
            root.clipboard_append(selected)


def copy_text(e):
    global selected
    #check for keyboard shortcuts
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        selected = my_text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)



def paste_text(e):
    global selected
    if e:
        selected = root.clipboard_get
    else:
        if selected:
            postition = my_text.index(INSERT)
            my_text.insert(postition, selected)
def thesaurize():
    global thes
    if my_text.selection_get():
        # grab text
        selected = my_text.selection_get()
        thes = ws.thesaurus(selected)
        thes = list(set(thes))
        print(thes)
    else:
        print("ERROR")
    side_menu.sidebar_act(root, definition, thes)

def define_word():
    global selected
    global definition
    if my_text.selection_get():
        # grab text
        selected = my_text.selection_get()
        context = (my_text.get(1.0, END))
        definition = ws.simplified_lesk(selected, context)
        #NEED TRY STATEMENT
    else:
        print("ERROR")
    side_menu.sidebar_act(root, definition, thes)

def predict():
    my_text.tag_config('prediction', background="yellow", foreground="grey")
    postition = my_text.index(INSERT)
    words = model.generate_text(my_text.get(1.0, END), 1)
    my_text.insert(postition, words, 'prediction')

def clear_format():
    my_text.tag_config(background="white", foreground="black")

#Spell Checker
#spell_check.SpellingChecker()

my_frame = Frame(root)
my_frame.pack(pady=5)
#Scrollbar

text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)
#Textbox
my_text = Text(my_frame, width=97, height=25, font=("Helvetica", 16), selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set)
my_text.pack()
#Config scrollbar
text_scroll.config(command=my_text.yview)
#spell
#Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

#Add file meunu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)

file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

#add Edit Menu

edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command= lambda: cut_text(False))
edit_menu.add_command(label="Copy", command= lambda: copy_text(False))
edit_menu.add_command(label="Paste", command= lambda: paste_text(False))
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")

my_menu.add_command(label="Define", command= define_word)

my_menu.add_command(label="Thesaurus", command= thesaurize)

my_menu.add_command(label="Fill", command= predict)
status_bar = Label(root, text='Ready    ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)
print(thes)
side_menu.sidebar_act(root, definition, thes)

#Edit Bindings
root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)
root.bind('<Tab>', clear_format)
#.bind('<Tab>', accept_txt)
spell_check.SpellingChecker(my_text)
root.mainloop()
