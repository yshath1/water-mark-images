from tkinter import font
from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import colorchooser

win = Tk()
win.title('watermark image app')
win.geometry("1200x650")
## tool_bar
my_tool_bar = Frame(win)
my_tool_bar.pack(pady=5)
# main Frame
my_frame = Frame(win)
my_frame.pack(fill=X)

# scroll bar
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)
# horizontal scroll
hori_scroll = Scrollbar(my_frame, orient='horizontal')
hori_scroll.pack(side=BOTTOM, fill=X, pady=5)
# text box
my_text = Text(my_frame, width=97, height=25, font=('exo2', 18), selectbackground="yellow", selectforeground="black",
               undo=True, yscrollcommand=text_scroll.set, wrap='none', xscrollcommand=hori_scroll.set)
my_text.pack(pady=5)
text_scroll.config(command=my_text.yview)
hori_scroll.config(command=my_text.xview)


# ADD IMAGE
def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global image
    file_path = filedialog.askopenfilename()

    if file_path:
        image = Image.open(file_path)
        # create the image object, and save it so that it
        # won't get deleted by the garbage collector
        my_text.image_tk = ImageTk.PhotoImage(image)
        my_text.image_create(END, image=my_text.image_tk)


# CHANGE SELECTED IMAGE COLOR

# MECHANISM

global current_status_name
current_status_name = False

global selected
selected = False


def new_image():
    my_text.delete("1.0", END)
    # update status
    win.title("New Image- Image collage")
    status_bar.config(text="New image")
    global current_status_name
    current_status_name = False


def open_image():
    # remove previous image
    my_text.delete("1.0", END)
    # grab file from local directory
    image_file = filedialog.askopenfilename(title="Open File", filetypes=(
        ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Image Files", "*.jpeg"), ("All Files", "*.*")))
    if image_file:
        global current_status_name
        current_status_name = image_file

    name = image_file
    status_bar.config(text=f'{name}                 ')
    win.title(f"{name}")

    # open the file
    image_file = open(image_file, 'r')
    stuff = image_file.read()
    # Add file to text box
    my_text.insert(END, stuff)
    image_file.close()


def save_as_image():
    image_file = filedialog.asksaveasfilename(defaultextension=".*", title="Save File", filetypes=(
        ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Image Files", "*.jpeg"), ("All Files", "*.*")))
    print(image_file)
    if image_file:
        # update status bar
        name = image_file
        status_bar.config(text=f'Saved: {name}                 ')
        win.title(f"{name}")
        # save file
        image_file = open(image_file, 'w')
        image_file.write(my_text.get(1.0, END))
        # close file
        image_file.close()


def cut_image(e):
    global selected
    # check to see keyboard shortcut used
    if e:
        selected = win.clipboard_get()
    else:
        if my_text.selection_get():
            # select text
            selected = my_text.selection_get()
            # delete selected
            my_text.delete("sel.first", "sel.last")
            # clear the keyboard
            win.clipboard_clear()
            win.clipboard_append(selected)


def copy_image(e):
    global selected
    if e:
        selected = win.clipboard_get()
    if my_text.selection_get():
        # select text
        selected = my_text.selection_get()
        # clear the keyboard
        win.clipboard_clear()
        win.clipboard_append(selected)


def paste_image(e):
    global selected
    # check to see keyboard shortcut
    if e:
        selected = win.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)  # get postion of the mouse
            my_text.insert(position, selected)


def save_file():
    global current_status_name
    if current_status_name:
        # save the file
        image_file = open(current_status_name, "w")
        image_file.write(my_text.get(1.0, END))
        # close file
        image_file.close()
        # notification
        status_bar.config(text=f'Saved: {current_status_name}                 ')
    else:
        save_as_image()


def text_color():
    # pick a color
    my_color = colorchooser.askcolor()[1]

    color_font = font.Font(my_text, my_text.cget('font'))

    # configure tag
    my_text.tag_configure("colored", font=color_font, foreground=my_color)

    # define current tags
    current_tags = my_text.tag_names("sel.first")

    # if statement to see if tag as being set
    if "colored" in current_tags:
        my_text.tag_remove("colored", "sel.first", "sel.last")
    else:
        my_text.tag_add("colored", "sel.first", "sel.last")


def back_ground_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(bg=my_color)


def all_text():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(bg=my_color)


# night mode on
def night_mode_on():
    main_color = "#000000"
    second_color = "#373737"
    text_cl = "green"

    win.config(bg=main_color)
    status_bar.config(bg=main_color, fg=text_cl)
    my_text.config(bg=second_color)
    my_tool_bar.config(by=main_color)


# night mode off
def night_mode_off():
    main_color = "SystemButtonFace"
    second_color = "SystemButtonFace"
    text_cl = "black"

    win.config(bg=main_color)
    status_bar.config(bg=main_color, fg=text_cl)
    my_text.config(bg=second_color)
    my_tool_bar.config(by=main_color)




# Image color
color_button = Button(my_tool_bar, text="Image color", command=text_color)
color_button.grid(row=0, column=0)

win.bind('<Control-Key-x>', cut_image)
win.bind('<Control-Key-v>', paste_image)
win.bind('<Control-Key-c>', copy_image)

# menu
my_menu = Menu(win)
win.config(menu=my_menu)

# add image menu
image_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Image", menu=image_menu)
image_menu.add_command(label="new", command=new_image)
image_menu.add_command(label="add image", command=open_image)
image_menu.add_command(label="add logo", command=browse_button)
image_menu.add_command(label="add text", )
image_menu.add_command(label="save", command=save_file)
image_menu.add_command(label="save as", command=save_as_image)
image_menu.add_separator()
image_menu.add_command(label="Exit", command=win.quit)
# edit photo
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="edit", menu=edit_menu)
edit_menu.add_command(label="cut ", command=lambda: cut_image(False), accelerator="Ctrl+x")
edit_menu.add_command(label="copy ", command=lambda: copy_image(False), accelerator="Ctrl+c")
edit_menu.add_command(label="paste ", command=lambda: paste_image(False), accelerator="Ctrl+v")
edit_menu.add_command(label="undo", command=lambda: my_text.edit_undo, accelerator="Ctrl+z")
edit_menu.add_command(label="Redo", command=lambda: my_text.edit_redo, accelerator="Ctrl+y")
# color Menu
color_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Colors", menu=color_menu)
color_menu.add_command(label="Background ", command=back_ground_color)
color_menu.add_command(label="change select image ", command=text_color)
color_menu.add_command(label="All text  ", command=all_text)

# Add image Menu
# image_menu = Menu(my_menu, tearoff=False)
# image_menu.add_cascade(label="Images", menu=image_menu)
# image_menu.add_command(label="Add+ ", )
# Options Menu
option_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Options", menu=option_menu)
option_menu.add_command(label="Night Mode On ", command=night_mode_on)
option_menu.add_command(label="Night Mode Off ", command=night_mode_on)

# status bar
status_bar = Label(win, text='Ready                        ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)
win.mainloop()
