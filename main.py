import pathlib
import tkinter as tk
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import ttk

from speak import SpeakMain
from comment import comment_or_uncomment
from show_help import HelpWindow
from LineNumber import LineMain
from syntax_highlight import SyntaxHighlight
from textarea import MyText
from findwindow import Finder
from run_file import run_command
from changefont import bold_it, italics_it, bg_color, all_text_color, text_color

window = Tk(className='PyCoder')
window.title("Untitled - Python PyCode Tkeditor")
window.attributes('-zoomed', True)
window.style = ttk.Style()
window.style.theme_use('default')
window.attributes('-zoomed', True)
window.minsize(670, 450)
window.iconphoto(False, PhotoImage(file="/home/mw/Desktop/progamming/my python editor/icon.png"))

# hide hidden files in filedialog
try:
    try:
        window.tk.call('tk_getOpenFile', '-foobarbaz')
    except TclError:
        pass
    # now set the magic variables accordingly
    window.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
    window.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
except TclError:
    pass


def newfile(event=None):
    window.title("Untitled - Python PyCode TkEditor")
    textarea.delete(1.0, END)

    file_label["text"] = "Untitled.py"
    update_index()
    # reset undo and redo
    textarea.edit_reset()


def openfile(event=None):
    global file
    file = askopenfilename(initialdir="/home/mw",
                           filetypes=[("Python Files", "*.py"),
                                      ("All Files", "*.*"),
                                      ("Html Files", "*.html"),
                                      ("CSS Files", "*.css"),
                                      ("JavaScript Files", "*.js")])

    if file == "":
        file = None

    else:
        window.title(os.path.basename(file) + " - Python PyCode TkEditor")
        textarea.delete(1.0, END)
        openedfile = open(file, "r")
        try:
            textarea.insert(END, openedfile.read())
        except UnicodeDecodeError as error:
            showerror("Unicode Error!", error)
        openedfile.close()

    file_label["text"] = file

    # reset undo and redo
    textarea.edit_reset()
    update_index()


def savefile(event=None):
    global file
    if file == None:
        # save as new file
        file = asksaveasfilename(initialfile='Untitled',
                                 filetypes=[("Python Files", "*.py"),
                                            ("All Files", "*.*"),
                                            ("Html Files", "*.html"),
                                            ("CSS Files", "*.css"),
                                            ("JavaScript Files", "*.js")])

        if file == "":
            file = None
        else:
            window.title(os.path.basename(file) + " - Python PyCode TkEditor")
            savedfile = open(file, "w")
            savedfile.write(textarea.get(1.0, END))
            savedfile.close()
    else:
        savedfile = open(file, "w")
        savedfile.write(textarea.get(1.0, END))
        savedfile.close()

        file_label["text"] = os.path.basename(file)
        update_index()


def savefileas(event=None):
    global file
    file = asksaveasfilename(initialfile='Untitled',
                             filetypes=[("Python Files", "*.py"),
                                        ("All Files", "*.*"),
                                        ("Html Files", "*.html"),
                                        ("CSS Files", "*.css"),
                                        ("JavaScript Files", "*.js")])
    if file == "":
        file = None
    else:
        window.title(os.path.basename(file) + " - Python PyCode TkEditor")
        savedasfile = open(file, "w")
        savedasfile.write(textarea.get(1.0, END))
        savedasfile.close()

        file_label["text"] = file
        update_index()


def copy():
    textarea.event_generate("<<Copy>>")


def cut():
    textarea.event_generate("<<Cut>>")
    update_index()


def paste():
    textarea.event_generate("<<Paste>>")
    update_index()


def undo():
    textarea.event_generate("<<Undo>>")


def redo():
    textarea.event_generate("<<Redo>>")


def select_all(event=None):
    # textarea.tag_add("sel", '1.0', 'end')
    textarea.event_generate("<<SelectAll>>")


def deselect_all(event=None):
    textarea.tag_remove("sel", '1.0', 'end')


def speak(event=None):
    SpeakMain()


def showfindwindow(event=None):
    Finder(window, textarea).pack(fill=X)


def runfile(event=None):
    run_command("running" + file + "...", pathlib.Path, ["python3", file])


def comment_uncomment():
    comment_or_uncomment(textarea)


def light_theme(event=None):
    textarea.configure(insertbackground='black', bg="white", fg="black")
    menubar.configure(bg="lightgrey", fg="black")
    themevar.set("light")


def dark_theme(event=None):
    textarea.configure(insertbackground='white', bg="#232342", fg="white")
    menubar.configure(bg="lightgrey", fg="black")
    themevar.set("dark")


def classic_theme(event=None):
    textarea.configure(insertbackground='white', bg="#2b2b2b", fg="white")
    menubar.configure(bg="darkgrey", fg="black")
    themevar.set("classic")


def showhelp(event=None):
    # showinfo("Help", "my python editor made using python's tkinter module!")
    HelpWindow()


def show_right_click_menu(event):
    right_click_menu.tk_popup(event.x_root, event.y_root)

    return


def autoindent(event=None):
    # the text widget that received the event
    widget = event.widget

    # get current line
    line = widget.get("insert linestart", "insert lineend")

    # compute the indentation of the current line
    match = re.match(r'^(\s+)', line)
    current_indent = len(match.group(0)) if match else 0

    # compute the new indentation
    new_indent = current_indent + 4

    # insert the character that triggered the event,
    # a newline, and then new indentation
    widget.insert("insert", event.char + "\n" + " " * new_indent)

    # return 'break' to prevent the default behavior
    return "break"


def tab(event=None):
    textarea.insert(INSERT, "   ")
    return 'break'


def on_closing(event=None):
    leave = showwarning("Exit?", "Are you sure you want to quit?", type="yesno")
    if leave == "yes":
        window.destroy()
    else:
        pass


window.protocol("WM_DELETE_WINDOW", on_closing)


def update_index(event=None):
    cursor_position = textarea.index(INSERT)
    cursor_position_pieces = str(cursor_position).split('.')

    cursor_line = cursor_position_pieces[0]
    cursor_column = cursor_position_pieces[1]

    current_index.set(f'Ln: {cursor_line}, Col: {cursor_column}')


file = None

status_bar = tk.Frame(window, bg="#404040", bd=2)
status_bar.pack(fill=X, side=BOTTOM)

current_index = StringVar()
index_label = Label(status_bar, textvar=current_index, font=(None, 8))
index_label.configure(foreground="white", background="#404040")
index_label.pack(side=RIGHT)

file_label = Label(status_bar, text="Untitled.py", font=(None, 8))
file_label.configure(foreground="white", background="#404040")
file_label.pack(side=LEFT)

topscrollbar = ttk.Scrollbar(window)
topscrollbar.pack(fill=Y, side=RIGHT)

bottomscrollbar = ttk.Scrollbar(window, orient='horizontal')
bottomscrollbar.pack(fill=X, side=BOTTOM)

textarea = MyText(window, font=("Ubuntu Mono", 14), undo=True, yscrollcommand=topscrollbar.set,
                  xscrollcommand=bottomscrollbar.set)
textarea.configure(wrap=NONE, insertbackground="white", selectforeground="white",
                   selectbackground="#595959",
                   bg="#2b2b2b", fg="white")

linenumbers = LineMain(textarea)

textarea.pack(fill=BOTH, expand=True)
textarea.focus_set()

topscrollbar.config(command=textarea.yview)
bottomscrollbar.config(command=textarea.xview)

SyntaxHighlight(textarea)

menubar = Menu(window, activebackground="#bfbfbf")
menubar.configure(bg="darkgrey", fg="black")
window.configure(menu=menubar)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=newfile, accelerator="Ctrl+N")
filemenu.add_command(label="Open", command=openfile, accelerator="Ctrl+O")
filemenu.add_command(label="Save", command=savefile, accelerator="Ctrl+S")
filemenu.add_command(label="Save As", command=savefileas, accelerator="Ctrl+Shift+S")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=on_closing, accelerator="Ctrl+Q")

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Copy", command=copy, accelerator="Ctrl+C")
editmenu.add_command(label="Cut", command=cut, accelerator="Ctrl+X")
editmenu.add_command(label="Paste", command=paste, accelerator="Ctrl+V")
editmenu.add_separator()
editmenu.add_command(label="Find and Replace", command=showfindwindow,
                     accelerator="Ctrl+F")
editmenu.add_separator()
editmenu.add_command(label="Undo", command=undo, accelerator="Ctrl+Z")
editmenu.add_command(label="Redo", command=redo, accelerator="Ctrl+Shift+z")
editmenu.add_separator()
editmenu.add_command(label="Select All", command=select_all, accelerator="Ctrl+A")
editmenu.add_command(label="Deselect All", command=deselect_all)
editmenu.add_separator()
editmenu.add_command(label="Bold Selected Text", command=lambda: bold_it(textarea),
                     accelerator="Ctrl+B")
editmenu.add_command(label="Italics Selected Text", command=lambda: italics_it(textarea),
                     accelerator="Ctrl+Shift+I")

runmenu = Menu(menubar, tearoff=0)
runmenu.add_command(label="Run File in Terminal", command=runfile, accelerator="F5")

toolsmenu = Menu(menubar, tearoff=0)
themevar = StringVar()
themevar.set("classic")
toolsmenu.add_radiobutton(label="Toggle Classic Theme Recommended", variable=themevar,
                          value="classic",
                          command=classic_theme, accelerator="Alt+T")
toolsmenu.add_radiobutton(label="Toggle Light Theme", variable=themevar, value="light",
                          command=light_theme,
                          accelerator="Alt+L")
toolsmenu.add_radiobutton(label="Toggle Dark Theme", variable=themevar, value="dark",
                          command=dark_theme,
                          accelerator="Alt+D")
toolsmenu.add_separator()
toolsmenu.add_command(label="Change Selected Text Colour", command=lambda: text_color(textarea))
toolsmenu.add_command(label="Change Textarea Background Colour", command=lambda: bg_color(textarea))
toolsmenu.add_command(label="Change Textarea Foreground Colour", command=lambda: all_text_color(textarea))
toolsmenu.add_separator()
toolsmenu.add_command(label="Enter Text To Speak", command=speak, accelerator="Alt+S")

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=showhelp, accelerator="F1")

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Edit", menu=editmenu)
menubar.add_cascade(label="Run", menu=runmenu)
menubar.add_cascade(label="Tools", menu=toolsmenu)
menubar.add_cascade(label="Help", menu=helpmenu)

right_click_menu = Menu(textarea, tearoff=0)
right_click_menu.add_command(label='Copy', command=copy)
right_click_menu.add_command(label='Cut', command=cut)
right_click_menu.add_command(label='Paste', command=paste)
right_click_menu.add_separator()
right_click_menu.add_command(label="Undo", command=undo)
right_click_menu.add_command(label="Redo", command=redo)
right_click_menu.add_separator()
right_click_menu.add_command(label="Select All", command=select_all)
right_click_menu.add_command(label="Deselect All", command=deselect_all)


window.bind("<Control-n>", newfile)
window.bind("<Control-o>", openfile)
window.bind("<Control-s>", savefile)
window.bind('<Control-S>', savefileas)
window.bind("<Control-f>", showfindwindow)
window.bind('<F5>', runfile)
window.bind("<Alt-t>", classic_theme)
window.bind("<Alt-l>", light_theme)
window.bind("<Alt-d>", dark_theme)
window.bind("<Alt-s>", speak)
window.bind("<F1>", showhelp)
window.bind('<Control-a>', select_all)
window.bind("<Control-q>", on_closing)
textarea.bind("<Button-2>", paste)
textarea.bind("<Button-3>", show_right_click_menu)
textarea.bind('<KeyRelease>', update_index)
textarea.bind("<Control-b>", lambda event=None: bold_it(textarea))
textarea.bind("<Control-I>", lambda event=None: italics_it(textarea))
textarea.bind("<Tab>", tab)
textarea.bind("<Control-slash>", lambda e: comment_or_uncomment(textarea))

# textarea.bind(":", autoindent)

update_index()

window.mainloop()
