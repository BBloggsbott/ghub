from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import Terminal256Formatter

def printHighlightContent(fileName, content):
    lexer = get_lexer_for_filename(fileName)
    
    print(highlight(content, lexer, Terminal256Formatter()))
