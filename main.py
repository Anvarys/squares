import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from PIL import Image, ImageTk
from collections import namedtuple
import webbrowser as wb
import re
from utilities import *
from code import command, interpret
from time import sleep

WIDTH_HEIGHT = 16

w = tk.Tk()
w.geometry("1240x840")
w.resizable(False, False)
w.title("Squares.io")


ColorTuple = namedtuple("Color",
                        ["bg", "pinky", "light_pinky", "dark_pinky", "green", "dark_lime", "neon_lime", "code_bg",
                         "blue_gray", "code_win_bg"])
ImageTuple = namedtuple("Image", ["start", "brush", "on", "off", "back", "logo"])

font = "Andale Mono"

color = ColorTuple("#4a0b8a", "#8a0091", "#da22e3", "#610066",
                   "#07753b", "#27ba6c", "#0af779", "#112e1e",
                   "#c8c8dc", "#2c6b2e")

image = ImageTuple(ImageTk.PhotoImage(Image.open("assets/start.png").resize((160, 160))),
                   ImageTk.PhotoImage(Image.open("assets/brush.png").resize((140, 140))),
                   ImageTk.PhotoImage(Image.open("assets/switch-on.png").resize((80, 80))),
                   ImageTk.PhotoImage(Image.open("assets/switch-off.png").resize((80, 80))),
                   ImageTk.PhotoImage(Image.open("assets/left-arrow.png").resize((80, 80))),
                   ImageTk.PhotoImage(Image.open("assets/logo.png")))

w.tk.call('wm', 'iconphoto', w, image.logo)

bg = tk.Frame(w, width=2000, height=2000, background=color.bg)
bg.place(x=-200, y=-200)

c = tk.Canvas(w, width=1210, height=810, highlightthickness=0, bd=0, relief='ridge', bg=color.bg)
c.place(x=20, y=20)

hover = Hover(c)

code_frame = tk.Frame(w, bg=color.code_bg)

code_c = tk.Canvas(code_frame, bg=color.code_bg, highlightthickness=0, bd=0, relief='ridge')
code_c.place(relheight=1,relwidth=1,relx=0,rely=0)

hover_code = Hover(code_c)

code_back = code_c.create_image(15,15, anchor=tk.NW, image=image.back)

hover_code.track(code_back)

text = tk.Text(
    code_frame, bg=color.code_win_bg, foreground=color.blue_gray, insertbackground=color.blue_gray, relief=tk.FLAT,
    font=(font, 20), pady=0, padx=0, highlightthickness=0, height=29
)

text.place(x=100, y=100)

repl = [
    [r'\b(square)(?:\(.*?\))', "#27F8FF"],
    [r'\b(squares)\b', "#27F8FF"],
    ['#.*?$', "#3b3b3b"],
    [r'\b(fill|rect)(?:\(.*?\))', "#23b9ff"],
    [r'\b(all)\b', "#23b9ff"],
    ['(\d+|\.)', "#ffaa4e"]
]


previousText = ''


def changes(widget):
    global previousText
    if widget.get('1.0', tk.END) == previousText:
        return
    for tag in widget.tag_names():
        widget.tag_remove(tag, "1.0", "end")

    i = 0
    for pattern, params in repl:
        if type(params) == str:
            params = {"foreground": params}
        for start, end in search_re(pattern, widget.get('1.0', tk.END)):
            widget.tag_add(f'{i}', start, end)
            widget.tag_config(f'{i}', **params)
            i += 1

    previousText = widget.get('1.0', tk.END)

def search_re(pattern, text):
    matches = []
    txt = text.splitlines()

    for i, line in enumerate(txt):
        for match in re.finditer(pattern, line):
            matches.append(
                (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
            )

    return matches


TILES_ID = []
TILES_DATA = [[{"fill": (255, 255, 255)} for _ in range(WIDTH_HEIGHT)] for __ in
              range(WIDTH_HEIGHT)]

for x in range(WIDTH_HEIGHT):
    TILES_COLUMN = []
    for y in range(WIDTH_HEIGHT):
        x0, y0 = (800 / WIDTH_HEIGHT * x), (800 / WIDTH_HEIGHT * y)
        TILES_COLUMN.append(
            c.create_rectangle(x0, y0, x0 + 800 / WIDTH_HEIGHT, y0 + 800 / WIDTH_HEIGHT, fill='white', outline='black'))
    TILES_ID.append(TILES_COLUMN)

# Default bar

width = 5
start_button = c.create_image(825, 5, anchor=tk.NW, image=image.start)
draw_button2 = c.create_rectangle(1025, 5, 1185, 160, fill=color.pinky, outline=color.dark_pinky, width=width)
draw_button = c.create_image(1035, 15, anchor=tk.NW, image=image.brush)
save_button2 = c.create_rectangle(825, 730, 1000, 800, fill=color.pinky, outline=color.dark_pinky, width=width)
load_button2 = c.create_rectangle(1025, 730, 1200, 800, fill=color.pinky, outline=color.dark_pinky, width=width)
doc_button2 = c.create_rectangle(825, 635, 1200, 705, fill=color.pinky, outline=color.dark_pinky, width=width)
outline_rect = c.create_rectangle(825, 540, 1200, 610, fill=color.pinky, outline=color.dark_pinky, width=width)
settings_rect = c.create_rectangle(825, 445, 1200, 515, fill=color.pinky, outline=color.dark_pinky, width=width)
code_rect = c.create_rectangle(825, 350, 1000, 420, fill=color.dark_lime, outline=color.green, width=width)
outline_text = c.create_text(1012, 575, text="OUTLINES   ", font=(font, 50), fill=color.light_pinky)
save_button = c.create_text(912, 765, text="SAVE", font=(font, 50), fill=color.light_pinky)
load_button = c.create_text(1112, 765, text="LOAD", font=(font, 50), fill=color.light_pinky)
doc_button = c.create_text(1012, 670, text="DOCUMENTATION", font=(font, 45), fill=color.light_pinky)
settings_button = c.create_text(1012, 480, text="SETTINGS", font=(font, 45), fill=color.light_pinky)
code_button = c.create_text(912, 385, text="CODE", font=(font, 50), fill=color.neon_lime)
outline_button = c.create_image(1100, 535, anchor=tk.NW, image=image.on)
outline_is_on = True

default_bar = (
    start_button, draw_button, draw_button2, save_button, save_button2, load_button, load_button2, doc_button,
    doc_button2, outline_button, outline_rect, outline_text, settings_button, settings_rect, code_button, code_rect)

cursor_hover = (
    start_button, draw_button, draw_button2, save_button, save_button2, load_button, load_button2, doc_button,
    doc_button2, outline_button, settings_button, settings_rect, code_button, code_rect
)

for i in cursor_hover:
    hover.track(i)


# Draw bar


def saveButton(event):
    filename = fd.asksaveasfilename(title="Save file", confirmoverwrite=True, defaultextension=".squares")
    if len(filename) == 0:
        return None

    with open(filename, "w") as file:
        file.write("Чел, это еще не готово пока что")

    '''
                 I will do it later 
    '''


def loadButton(event):
    filename = fd.askopenfilename(title="Load file", filetypes=([("Square files", "*.squares")]))
    if len(filename) == 0:
        return None

    '''
                 I will do it later 
    '''


def docButton(event):
    wb.open("https://docs.google.com/document/d/1IEAp5_gC-HUpNnwgQPvoXRFpTVlyt6ghPxPj6mnvYb8/edit?usp=sharing")


def outlineButton(event):
    global outline_is_on
    outline_is_on = not outline_is_on
    if outline_is_on:
        c.itemconfig(outline_button, image=image.on)
    else:
        c.itemconfig(outline_button, image=image.off)

    for x, column in enumerate(TILES_ID):
        for y, tile in enumerate(column):
            if outline_is_on:
                c.itemconfig(tile, outline='black')
            else:
                c.itemconfig(tile, outline='')
    w.update()


def drawButton(event):
    hideAll(c, default_bar)


def codeButton(event):
    code_frame.place(x=0, y=0, relheight=1, relwidth=1)


def codeBackButton(event):
    code_frame.place_forget()
    c.focus_set()


c.tag_bind(code_rect, "<Button>", codeButton)
c.tag_bind(code_button, "<Button>", codeButton)

code_c.tag_bind(code_back,"<Button>",codeBackButton)

c.tag_bind(save_button, "<Button>", saveButton)
c.tag_bind(save_button2, "<Button>", saveButton)

c.tag_bind(load_button, "<Button>", loadButton)
c.tag_bind(load_button2, "<Button>", loadButton)

c.tag_bind(doc_button, "<Button>", docButton)
c.tag_bind(doc_button2, "<Button>", docButton)

c.tag_bind(outline_button, "<Button>", outlineButton)

button_pressed = False


def runButton(event):
    commands = interpret(text.get("1.0", tk.END))
    if type(commands) == tuple:
        mb.showerror(message=f"Syntax Error in line {commands[0]+1}:\n{commands[1]}")
        return
    for cmd in commands:
        run_cmd(cmd)
        #update()
        #sleep(0.5)
    #update()

def ButtonPress(event):
    global button_pressed
    button_pressed = True


def ButtonRelease(event):
    global button_pressed
    button_pressed = False


w.bind_all("<Button>", ButtonPress)
w.bind_all("<ButtonRelease>", ButtonRelease)

c.tag_bind(start_button, "<Button>", runButton)


##########################################################################################


def run_cmd(cmd: tuple):
    global TILES_DATA

    cmd0 = cmd[0]

    if cmd0 == command.square.fill:
        TILES_DATA[cmd[1]][cmd[2]]['fill'] = cmd[3]
        update()

    if cmd0 == command.squares.rect.fill:
        for x in range(cmd[1],cmd[3]+1):
            for y in range(cmd[2],cmd[4]+1):
                TILES_DATA[x][y]["fill"] = cmd[5]
                update()

    if cmd0 == command.squares.all.fill:
        for x in range(WIDTH_HEIGHT):
            for y in range(WIDTH_HEIGHT):
                TILES_DATA[x][y]["fill"] = cmd[1]
                update()


##########################################################################################


def update():
    for x in range(WIDTH_HEIGHT):
        for y in range(WIDTH_HEIGHT):
            if outline_is_on:
                c.itemconfig(TILES_ID[x][y], outline='black', fill=rgb2hex(TILES_DATA[x][y]["fill"]))
            else:
                c.itemconfig(TILES_ID[x][y], fill=rgb2hex(TILES_DATA[x][y]["fill"]))
    w.update()


w.update()

try:
    while True:
        w.update()

        n = True
        if hover_code.get(code_back):
            n = False
            code_c.config(cursor='dot')
        for i in cursor_hover:
            if hover.get(i):
                c.config(cursor='dot')
                n = False
                break
        if n:
            c.config(cursor='')
            code_c.config(cursor='')
        if w.focus_get() != w:
            try:
                if w.focus_get() is not None:
                    changes(w.focus_get())
            except Exception as ex:
                pass
except Exception as ex:
    if str(ex) != 'invalid command name ".!canvas"':
        print("\033[91m" + str(ex))
finally:
    exit()
