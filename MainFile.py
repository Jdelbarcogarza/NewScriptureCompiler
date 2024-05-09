from MyLexer import Lexer
from MyParser import Parser






# Token definitions
# t_NOTE=r'N\d{1,2}(?:_\d{1,2})?$'
# t_TEMPO=r'tempo\(\d+\)\s*{\s*.*\s*}'

def main():

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

    pat easyPattern {
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
    easyPattern
    N2

  }

  '''

  # create lexer
  lexer = Lexer()

  # build the lexer
  lexer.build()

  # test method for input (deprecated)
  lexer.test(data)

  # create parser
  # yaccParser = Parser(lexer)

  # yaccParser.parser.parse(data)


  def test_note(noteString)-> bool:
    pattern = re.compile(t_NOTE)
    if pattern.match(noteString):

      print(noteString, 'valid input')

    else:
      print(noteString, 'not valid')


# ----- PROGRAM ------

if __name__ == "__main__":
  main()