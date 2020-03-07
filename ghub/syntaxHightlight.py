from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import TerminalFormatter, Terminal256Formatter
import tempfile
import subprocess, sys, curses


def printHighlightContent(file_name, content):
    lexer = get_lexer_for_filename(file_name)
    if getTerminalColorSupport() == 256:
        paginate(highlight(content, lexer, Terminal256Formatter()))
    else:
        paginate(highlight(content, lexer, TerminalFormatter()))


def getTerminalColorSupport():
    curses.setupterm()
    return curses.tigetnum("colors")


def paginate(content):
    path = tempfile.mkstemp()[1]

    tmp_file = open(path, "a")
    sys.stdout = tmp_file

    print(content)

    tmp_file.flush()
    tmp_file.close()
    proc = subprocess.Popen(["less", "-R", path], stdin=subprocess.PIPE)
    proc.communicate()

    sys.stdout = sys.__stdout__
