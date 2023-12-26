"""

    Requires pillow library

"""

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import colorchooser as cch
from PIL import Image, ImageTk
from collections import namedtuple
import webbrowser as wb
import re
from utilities import *
from code import command, interpret

WIDTH_HEIGHT = 16

w = tk.Tk()
w.geometry("1240x840")
w.resizable(False, False)
w.title("Squares.io")

ColorTuple = namedtuple("Color",
                        ["bg", "pinky", "light_pinky", "dark_pinky", "green", "dark_lime", "neon_lime", "code_bg",
                         "blue_gray", "code_win_bg", "light_yellow", "apple_juice"])
ImageTuple = namedtuple("Image",
                        ["start", "brush", "on", "off", "back", "logo", "pencil", "bucket", "square_rounded", "return0"])
CursorTuple = namedtuple("Cursor", ["hand", "grab", "open", "cross"])

font = "Andale Mono"

color = ColorTuple("#4a0b8a", "#8a0091", "#da22e3", "#610066",
                   "#07753b", "#27ba6c", "#0af779", "#112e1e",
                   "#c8c8dc", "#2c6b2e", "#fff76e", "#d0cb22")

image = ImageTuple(ImageTk.PhotoImage(Image.open("assets/start.png").resize((160, 160))),
                   ImageTk.PhotoImage(Image.open("assets/brush.png").resize((140, 140))),
                   ImageTk.PhotoImage(Image.open("assets/switch-on.png").resize((80, 80))),
                   ImageTk.PhotoImage(Image.open("assets/switch-off.png").resize((80, 80))),
                   ImageTk.PhotoImage(Image.open("assets/left-arrow.png").resize((80, 80))),
                   ImageTk.PhotoImage(Image.open("assets/logo.png")),
                   ImageTk.PhotoImage(Image.open("assets/pencil.png").resize((80, 80))),
                   ImageTk.PhotoImage(Image.open("assets/paint-bucket.png").resize((80, 80))),
                   ImageTk.PhotoImage(Image.open("assets/square_rounded.png").resize((70, 70))),
                   ImageTk.PhotoImage(Image.open("assets/return.png").resize((50, 50))))

cursor = CursorTuple("@assets/handpointing.svg", "@assets/handopen.svg", "@assets/handgrabbing.svg",
                     "@assets/cross.svg")

w.tk.call('wm', 'iconphoto', w, image.logo)

bg = tk.Frame(w, width=2000, height=2000, background=color.bg)
bg.place(x=-200, y=-200)

c = tk.Canvas(w, width=1210, height=810, highlightthickness=0, bd=0, relief='ridge', bg=color.bg)
c.place(x=20, y=20)

hover = Hover(c)

code_frame = tk.Frame(w, bg=color.code_bg)

code_c = tk.Canvas(code_frame, bg=color.code_bg, highlightthickness=0, bd=0, relief='ridge')
code_c.place(relheight=1, relwidth=1, relx=0, rely=0)

hover_code = Hover(code_c)

code_back = code_c.create_image(15, 15, anchor=tk.NW, image=image.back)

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


def onTileClick(event):
    global TILES_DATA, button_pressed
    if current_bar == 2:
        new_layer = []
        for i1 in range(WIDTH_HEIGHT):
            ll = []
            for i2 in range(WIDTH_HEIGHT):
                ll.append(layers[-1][i1][i2])
            new_layer.append(ll)
        if current_tool == 1:
            button_pressed = True
            while button_pressed:
                update()
                try:
                    tile_x, tile_y = round((mouseX / 800 * WIDTH_HEIGHT) // 1), round((mouseY / 800 * WIDTH_HEIGHT) // 1)
                    if tile_x < 0 or tile_y < 0:
                        continue
                    new_layer[tile_x][tile_y] = current_color
                    TILES_DATA[tile_x][tile_y]["fill"] = current_color
                    update()
                except Exception as ex:
                    pass
            update()
        layers.append(new_layer)


TILES_ID = []
TILES_DATA = [[{"fill": (255, 255, 255)} for _ in range(WIDTH_HEIGHT)] for __ in
              range(WIDTH_HEIGHT)]

for x_ in range(WIDTH_HEIGHT):
    TILES_COLUMN = []
    for y_ in range(WIDTH_HEIGHT):
        x0, y0 = (800 / WIDTH_HEIGHT * x_), (800 / WIDTH_HEIGHT * y_)
        TILES_COLUMN.append(
            c.create_rectangle(x0, y0, x0 + 800 / WIDTH_HEIGHT, y0 + 800 / WIDTH_HEIGHT, fill='white', outline='black'))
        hover.track(TILES_COLUMN[-1])

        c.tag_bind(TILES_COLUMN[-1],"<Button>",onTileClick)
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

# Draw bar

color_button = c.create_rectangle(825, 5, 985, 165, fill="white", outline="black", width=10)
back_default_bar_button = c.create_image(825, 705, image=image.back, anchor=tk.NW)
return_button = c.create_image(825,175,image=image.return0,anchor=tk.NW)
draw_tools_images = (
    image.pencil,
    image.bucket,
    (image.square_rounded, (15, 15))
)

current_color = (255,255,255)
current_tool = 1
layers = []
for i0 in range(WIDTH_HEIGHT):
    lll = []
    for i1 in range(WIDTH_HEIGHT):
        lll.append((255,255,255))
    layers.append(lll)
layers = [layers]
draw_bar = [color_button, back_default_bar_button, return_button]

for y in range(5):
    for x in range(3):
        if y * 3 + x >= len(draw_tools_images):
            break
        y0, x0 = y * 130 + 300, x * 130 + 830
        color_tool_rect = c.create_rectangle(x0, y0, x0 + 100, y0 + 100, fill=color.light_yellow,
                                             outline=color.apple_juice, width=10)
        if type(draw_tools_images[y * 3 + x]) != tuple:
            color_tool = c.create_image(x0 + 10, y0 + 10, image=draw_tools_images[y * 3 + x], anchor=tk.NW)
        else:
            color_tool = c.create_image(x0 + draw_tools_images[y * 3 + x][1][0],
                                        y0 + draw_tools_images[y * 3 + x][1][1],
                                        image=draw_tools_images[y * 3 + x][0], anchor=tk.NW)
        draw_bar.append(color_tool_rect)
        draw_bar.append(color_tool)


c.itemconfig(draw_bar[3], fill=color.neon_lime, outline=color.dark_lime)

hideAll(c, draw_bar)

cursor_hover = [
    start_button, draw_button, draw_button2, save_button, save_button2, load_button, load_button2, doc_button,
    doc_button2, outline_button, settings_button, settings_rect, code_button, code_rect
]
cursor_hover.extend(draw_bar)

current_bar = 1

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


def colorSelectButton(event):
    global current_color
    askcolor = cch.askcolor(title="Choose color")
    if askcolor[0] is None:
        return
    current_color = askcolor[0]
    c.itemconfig(color_button, fill=rgb2hex(current_color))
    if askcolor[0][0] < 100 and askcolor[0][1] < 100 and askcolor[0][2] < 100:
        c.itemconfig(color_button, outline="white")
    else:
        c.itemconfig(color_button, outline="black")


def drawButton(event):
    global current_bar
    hideAll(c, default_bar)
    hideAll(c, draw_bar, False)
    current_bar = 2


def codeButton(event):
    code_frame.place(x=0, y=0, relheight=1, relwidth=1)


def codeBackButton(event):
    code_frame.place_forget()
    c.focus_set()


def backDefaultBarButton(event):
    global current_bar
    hideAll(c, default_bar, False)
    hideAll(c, draw_bar)
    current_bar = 1


def returnPrevLayerButton(event):
    global TILES_DATA
    global layers
    if len(layers) > 1:
        layers = layers[:-1]
    for x in range(WIDTH_HEIGHT):
        for y in range(WIDTH_HEIGHT):
            TILES_DATA[x][y]["fill"] = layers[-1][x][y]
    update()


c.tag_bind(return_button, "<Button>", returnPrevLayerButton)

c.tag_bind(code_rect, "<Button>", codeButton)
c.tag_bind(code_button, "<Button>", codeButton)

code_c.tag_bind(code_back, "<Button>", codeBackButton)

c.tag_bind(save_button, "<Button>", saveButton)
c.tag_bind(save_button2, "<Button>", saveButton)

c.tag_bind(load_button, "<Button>", loadButton)
c.tag_bind(load_button2, "<Button>", loadButton)

c.tag_bind(doc_button, "<Button>", docButton)
c.tag_bind(doc_button2, "<Button>", docButton)

c.tag_bind(outline_button, "<Button>", outlineButton)

c.tag_bind(draw_button, "<Button>", drawButton)
c.tag_bind(draw_button2, "<Button>", drawButton)

c.tag_bind(back_default_bar_button, "<Button>", backDefaultBarButton)

c.tag_bind(color_button, "<Button>", colorSelectButton)

button_pressed = False


def runButton(event):
    commands = interpret(text.get("1.0", tk.END))
    if type(commands) == tuple:
        mb.showerror(message=f"Syntax Error in line {commands[0] + 1}:\n{commands[1]}")
        return
    for cmd in commands:
        run_cmd(cmd)
        # update()
        # sleep(0.5)
    # update()


def ButtonPress(event):
    global button_pressed
    button_pressed = True


def ButtonRelease(event):
    global button_pressed
    button_pressed = False


nn = False
mouseX, mouseY = -1, -1


def motion(event):
    global nn, mouseY, mouseX
    mouseX, mouseY = event.x, event.y


w.bind_all("<Button>", ButtonPress)
w.bind_all("<ButtonRelease>", ButtonRelease)

c.tag_bind(start_button, "<Button>", runButton)

c.bind("<Motion>", motion)


##########################################################################################


def run_cmd(cmd: tuple):
    global TILES_DATA

    cmd0 = cmd[0]

    if cmd0 == command.square.fill:
        TILES_DATA[cmd[1]][cmd[2]]['fill'] = cmd[3]
        update()

    if cmd0 == command.squares.rect.fill:
        for x in range(cmd[1], cmd[3] + 1):
            for y in range(cmd[2], cmd[4] + 1):
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
            code_c.config(cursor=cursor.hand)
        for i in cursor_hover:
            if hover.get(i):
                c.config(cursor=cursor.hand)
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
