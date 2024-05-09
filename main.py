from MyLexer import Lexer
import re

# yacc unsued so far
import ply.yacc as yacc






# Token definitions
# t_NOTE=r'N\d{1,2}(?:_\d{1,2})?$'


data = '''



---
Name: "77"
Artist: "Peso Pluma"
Charter: "CX404"
Album: "Génesis"
Year: "2023"
Offset: 0
Difficulty: 3
PreviewStart: 15
PreviewEnd: 35
Genre: "Regional Mexicano"
MusicStream: "song.mp3"
---


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

