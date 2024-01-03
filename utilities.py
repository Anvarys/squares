def rgb2hex(rgb: tuple):
    return "#%02x%02x%02x" % (round(rgb[0]),round(rgb[1]),round(rgb[2]))


def hex2rgb(hex0: str):
    return tuple(int(hex0.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))


def hideAll(canvas, l, remove=True):
    for i in l:
        if remove:
            canvas.itemconfig(i, state='hidden')
        else:
            canvas.itemconfig(i, state='normal')


class Hover:
    def __init__(self, canvas):
        self.canvas = canvas
        self.hover = {}

    def get(self, target):
        return self.hover[target]

    def track(self, target):
        self.hover[target] = False

        def onLeave(event):
            self.hover[target] = False

        def onEnter(event):
            self.hover[target] = True

        self.canvas.tag_bind(target, "<Leave>", onLeave)
        self.canvas.tag_bind(target, "<Enter>", onEnter)

    def getAll(self):
        return self.hover
