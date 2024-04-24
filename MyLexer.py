import re
import ply.lex as lex


class Lexer(object):

  declaredPatterns = dict()

  # reserved words
  reserved = {
      "tempo": "TEMPO",
      "pat": "PAT",
  }

  # Token definitions
  tokens = [
    'NOTE',
    'COMMENT',
    # 'EMPTY',
    'LBRACKET',
    'RBRACKET',
    'LPAREN',
    'RPAREN',
    'PATTERN_NAME',# token generico para aceptar nombres de patrones 
    'TEMPO_VAL' # valor dentro de parentesis de tempo
  ] + list(reserved.values())



  # whitespace
  t_ignore =' \t'

  # token regular expressions rules for simple tokens
  t_LPAREN = r'\('
  t_RPAREN = r'\)'
  t_LBRACKET = r'\{'
  t_RBRACKET = r'\}'

  def build(self, **kwargs):
     self.lexer = lex.lex(module=self, **kwargs)

  # Test it output
  def test(self,data):
      self.lexer.input(data)
      while True:
            tok = self.lexer.token()
            if not tok: 
                break
            print(tok)
     

  # regular expression rule with some action
  def t_NEWLINE(self, t):
      r'\n+'
      t.lexer.lineno += t.value.count('\n')

  def t_NOTE(self, t):
    r'N\d{1,2}(?:_\d{1,2})?'
    return t
  
  def t_TEMPO_VAL(self, t):
      r'\d+'
      t.value = int(t.value)
      return t
  
  def t_PATTERN_NAME(self, t):
      
      r'[a-zA-Z_][a-zA-Z_0-9]*'
      t.type = self.reserved.get(t.value, "PATTERN_NAME")

      '''
      1. Si t.type == PATTERN_NAME, significa que este es el string identificador del patron PAT declarado. Se guarda
      en los tokens para en un futuro parsearlo como debe ser.


      NOTA: es importante revisar que el nombre del patron no este ya en el diccionario de tokens.
      PREGUNTA: se deben guardar en el lexer las notas que contiene el patron?? AUN NO SE
      '''
      if t.type == "PATTERN_NAME":
          self.tokens.append(t.value)
          print('ahora esta es la lista de tokens', self.tokens)


      print('el valor:', t.value)

      return t


  # def t_PATTERN_NAME(self, t):
  #     r'[a-zA-Z_][a-zA-Z_0-9]*'
  #     print(t.value)
  #     return t

  # def t_TEMPO(self, t):
  #   r'tempo\(\d+\)' # tempo(34) {
  #   t.value = re.search(r'\d+', t.value).group(0)
  #   print(t.value, 'THIS IS THE VALUE')
  #   return t
    
  # Error handling rule
  def t_error(self, t):
      print("Illegal character '%s'" % t.value[0])
      t.lexer.skip(1)

