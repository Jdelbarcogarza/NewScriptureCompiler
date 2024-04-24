from MyLexer import Lexer

# yacc unsued so far
import ply.yacc as yacc






# Token definitions
# t_NOTE=r'N\d{1,2}(?:_\d{1,2})?$'
# t_TEMPO=r'tempo\(\d+\)\s*{\s*.*\s*}'


data = '''


pat hardPattern {

  N4
  N4
  N3
  N21
  N21

}


tempo(34) {

  N4
  N5
  hardPattern
  N34_5
  N2

}

'''

lexer = Lexer()

lexer.build() #  build the lexer

lexer.test(data)




def test_note(noteString)-> bool:
  pattern = re.compile(t_NOTE)
  if pattern.match(noteString):

    print(noteString, 'valid input')

  else:
    print(noteString, 'not valid')


# ----- PROGRAM ------

