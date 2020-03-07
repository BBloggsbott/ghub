from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import TerminalFormatter, Terminal256Formatter
import curses


def printHighlightContent(fileName, content):
    lexer = get_lexer_for_filename(fileName)
    if getTerminalColorSupport() == 256:
        print(highlight(content, lexer, Terminal256Formatter()))
    else:
        print(highlight(content, lexer, TerminalFormatter()))


def getTerminalColorSupport():
    curses.setupterm()
    return curses.tigetnum("colors")
