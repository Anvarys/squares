import collections


ColorTuple = collections.namedtuple("Color",
                        ["bg", "pinky", "light_pinky", "dark_pinky", "green", "dark_lime", "neon_lime", "code_bg",
                         "blue_gray", "code_win_bg", "light_yellow", "apple_juice", "light_blue", "medium_blue",
                         "settings_bg", "light_magenta"])

ImageTuple = collections.namedtuple("Image",
                        ["start", "brush", "on", "off", "back", "logo", "pencil", "bucket", "square_rounded",
                         "return0", "imageicon"])

CursorTuple = collections.namedtuple("Cursor", ["hand", "grab", "open", "cross"])


cursor = CursorTuple("@assets/handpointing.svg", "@assets/handopen.svg", "@assets/handgrabbing.svg",
                     "@assets/cross.svg")

color = ColorTuple("#4a0b8a", "#8a0091", "#da22e3", "#610066",
                   "#07753b", "#27ba6c", "#0af779", "#112e1e",
                   "#c8c8dc", "#2c6b2e", "#fff76e", "#d0cb22",
                   "#84ffff", "#24cfd0", "#653cff", "#653cff")