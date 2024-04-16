import re
import ply.lex as lex
import ply.yacc as yacc

# Token definitions
tokens = (
  'NOTE',
  'TEMPO',
  'PAT',
  'COMMENT',
  # 'EMPTY',
  'LBRACKET',
  'RBRACKET',
  'LPAREN',
  'RPAREN'
)

# whitespace
t_ignore =' \t'

# token regular expressions rules for simple tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\{'
t_RBRACKET = r'\}'


# Token definitions
# t_NOTE=r'N\d{1,2}(?:_\d{1,2})?$'
# t_TEMPO=r'tempo\(\d+\)\s*{\s*.*\s*}'


# regular expression rule with some action
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_NOTE(t):
   r'N\d{1,2}(?:_\d{1,2})?'
   return t

def t_TEMPO(t):
   r'tempo\(\d+\)' # tempo(34) {
   t.value = re.search(r'\d+', t.value).group(0)
   print(t.value, 'THIS IS THE VALUE')
   return t
   
# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
  
data = '''

tempo(34) {

  N4
  N5
  N34_5
  N2

}

'''

lexer.input(data)

while True:
   tok = lexer.token()
   if not tok:
      break
   print(tok)


def test_note(noteString)-> bool:
  pattern = re.compile(t_NOTE)
  if pattern.match(noteString):

    print(noteString, 'valid input')

  else:
    print(noteString, 'not valid')


# ----- PROGRAM ------

