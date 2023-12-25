import re
from collections import namedtuple
from tkinter import Tk, Canvas

Command = namedtuple("Command", ["square", "squares"])
square_ = namedtuple("square", ["fill"])("square.fill")
rect_, all_ = namedtuple("rect", ["fill"])("squares.rect.fill"), namedtuple("all", ["fill"])("squares.all.fill")
squares_ = namedtuple("squares", ["rect", "all"])(rect_, all_)
command = Command(square_, squares_)

Error = namedtuple("Error", ["squareArgs", "squareAfter", "fillArgs", "rectArgs", "rectAfter", "allAfter"])

error = Error(
    "function \"square\" have 2 number arguments: X, Y (Position of square)",
    "function \"square\" must have function after it (fill)",
    "function \"fill\" must have 3 number arguments: Red (0-255), Green (0-255), Blue (0-255)",
    "function \"rect\" have 4 number arguments: X1, Y1, X2, Y2 (Positions of rectangle angles)",
    "function \"rect\" must have function after it (fill)",
    "function \"all\" must have function after it (fill)"
)


def interpret(code: str):
    commands = []
    lines = code.splitlines()

    # Remove not useful text
    for i in range(len(lines)):
        comment = lines[i].find("#")
        if comment != -1:
            lines[i] = lines[i][:lines[i].find("#")]
        spaces = re.search(r"\s*$", lines[i]).span()
        if spaces[0] != spaces[1]:
            lines[i] = lines[i][:spaces[0]]

    for i in range(len(lines)):
        line = lines[i]
        if re.match("square\(.*\)", line) is not None:
            if re.match("square\(\d+,\d+\)", line) is None:
                return i, error.squareArgs
            x, y = map(int, re.match("square\((\d+),(\d+)\)", line).groups())
            line = line.removeprefix(re.match("square\(\d+,\d+\).", line).group(0))

            if re.match("fill", line) is not None:
                args = re.match("fill\((\d+),(\d+),(\d+)\)", line)
                if args is None:
                    return i, error.fillArgs
                rgb = tuple(map(int, args.groups()))
                commands.append((command.square.fill, x - 1, y - 1, rgb))

            else:
                return i, error.squareAfter

        elif re.match("squares", line) is not None:
            line = line.removeprefix("squares.")

            if re.match("rect", line) is not None:
                if re.match("rect\(\d+,\d+,\d+,\d+\)", line) is None:
                    return i, error.rectArgs
                x0, y0, x1, y1 = map(int, re.match("rect\((\d+),(\d+),(\d+),(\d+)\).", line).groups())
                line = line.removeprefix(re.match("rect\(\d+,\d+,\d+,\d+\).", line).group(0))
                if re.match("fill", line) is not None:
                    args = re.match("fill\((\d+),(\d+),(\d+)\)", line)
                    if args is None:
                        return i, error.fillArgs
                    rgb = tuple(map(int, args.groups()))
                    commands.append((command.squares.rect.fill, x0-1, y0-1, x1-1, y1-1, rgb))

                else:
                    return i, error.rectAfter

            if re.match("all", line) is not None:
                line = line.removeprefix(re.match("all.", line).group(0))
                if re.match("fill", line) is not None:
                    args = re.match("fill\((\d+),(\d+),(\d+)\)", line)
                    if args is None:
                        return i, error.fillArgs
                    rgb = tuple(map(int, args.groups()))
                    commands.append((command.squares.all.fill, rgb))
                else:
                    return i, error.allAfter

    return commands
