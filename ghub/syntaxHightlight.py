from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import TerminalFormatter, Terminal256Formatter
import tempfile
import subprocess, sys, curses


def highlight_and_paginate_content(file_name, content):
    lexer = get_lexer_for_filename(file_name)
    if get_terminal_color_support() == 256:
        paginate(highlight(content, lexer, Terminal256Formatter()))
    else:
        paginate(highlight(content, lexer, TerminalFormatter()))


def get_terminal_color_support():
    curses.setupterm()
    return curses.tigetnum("colors")


def paginate(content):
    path = tempfile.mkstemp()[1]

    tmp_file = open(path, "a")
    sys.stdout = tmp_file

    print(content)

    tmp_file.flush()
    tmp_file.close()
    p = subprocess.Popen(["less", "-R", path], stdin=subprocess.PIPE)
    p.communicate()

    sys.stdout = sys.__stdout__
