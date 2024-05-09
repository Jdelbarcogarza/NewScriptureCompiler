from MyLexer import Lexer
from MyParser import Parser

# Token definitions
# t_NOTE=r'N\d{1,2}(?:_\d{1,2})?$'
# t_TEMPO=r'tempo\(\d+\)\s*{\s*.*\s*}'

def main():
    # Solicitar al usuario el nombre del archivo
    filename = input("Ingrese el nombre del archivo: ")

    try:
      # Abrir el archivo en modo lectura
      with open(filename, 'r') as file:
        # Leer el contenido del archivo
        data = file.read()

      # Crear el lexer
      lexer = Lexer()

      # Construir el lexer
      lexer.build()

      # Probar el lexer con el contenido del archivo
      lexer.test(data)

    except FileNotFoundError:
        print(f"El archivo '{filename}' no existe.")
    except IOError:
        print(f"Error al leer el archivo '{filename}'.")


    def test_note(noteString)-> bool:
      pattern = re.compile(t_NOTE)
      if pattern.match(noteString):

        print(noteString, 'valid input')

      else:
        print(noteString, 'not valid')


# ----- PROGRAM ------

if __name__ == "__main__":
  main()