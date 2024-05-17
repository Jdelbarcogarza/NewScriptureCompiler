import ply.lex as lex

class Lexer(object):

  declaredPatterns = dict()

  # reserved words
  reserved = {
      'tempo': 'TEMPO',
      'pat': 'PAT',
      # ----- palabras reservadas de metadata --------
      'Name': 'NAME',
      'Artist': 'ARTIST',
      'Charter': 'CHARTER',
      'Album': 'ALBUM',
      'Year': 'YEAR',
      'Offset': 'OFFSET',
      'Difficulty': 'DIFFICULTY',
      'PreviewStart': 'PREVIEW_START',
      'PreviewEnd': 'PREVIEW_END',
      'Genre': 'GENRE',
      'MusicStream': 'MUSIC_STREAM',
  }

  # Token definitions
  tokens = [
    'NOTE',
    'COMMENTS',
    'NEWLINE',
    'EMPTY',
    'LBRACKET',
    'RBRACKET',
    'LPAREN',
    'RPAREN',
    'PATTERN_NAME', # token generico para aceptar nombres de patrones 
    # 'TEMPO_VAL', # valor dentro de parentesis de tempo
    # ----------- Tokens para metadata de cancion -----------
    'COLON',
    'QUOTES',
    'DASHES',
    'NUMBER' # alternativa a tempo val

  ] + list(reserved.values())

  # characters returned "as-is" by the lexer
  literals = [':']

  # whitespace
  t_ignore =' \t'

  # token regular expressions rules for simple tokens
  t_LPAREN = r'\('
  t_RPAREN = r'\)'
  t_LBRACKET = r'\{'
  t_RBRACKET = r'\}'
  # t_COLON = r':'
  t_DASHES = r'\-{3}'


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
     
  # Define regular expression rules for tokens
  def t_NUMBER(self, t):
      r'\d+'
      t.value = int(t.value)
      return t

  # regular expression rule with some action
  def t_NEWLINE(self, t):
      r'\n+'
      t.lexer.lineno += t.value.count('\n')

  def t_NOTE(self, t):
    r'N\d{1,2}(?:_\d{1,2})?'
    return t
  
  def t_NOTE(self, t):
    r'e\d{1,2}(?:_\d{1,2})?'
    return t
  
  #def t_COMMENT(self,t):
   #  r'\#.*'
    # t.lexer.lineno += t.value.count('\n')
     #return t
  def t_COMMENTS(self,t):
        r'\#.*'
        print('Comentario', t.value)
        pass 
  
  def t_TEMPO_VAL(self, t):
      r'\d+'
      t.value = int(t.value)
      return t
  

  
  '''
  Utilzado para extraer el valor en los atributos en la seccion de metadata. Lo que esta dentro de quotes
  puede tener acentos y otros caracteres no propios del ingles.
  '''
  def t_QUOTES(self, t):
    r'"[a-zA-Z0-9áéíóúüñ.\s]*"'
    # print('ATRIBUTO DE METADATA', t.value)
    t.value = t.value[1:-1]  # Remove quotation marks
    return t
      
  
  '''
  Este se utiliza para parsear palabras reservadas y aqui dentro se guardan los nombres de los patrones.
  '''
  def t_PATTERN_NAME(self, t):
      
      r'[a-zA-Z_][a-zA-Z_0-9]*'
      t.type = self.reserved.get(t.value, "PATTERN_NAME")

      '''
      1. Si t.type == PATTERN_NAME, significa que este es el string identificador del patron PAT declarado. Se guarda
      en los tokens para en un futuro parsearlo como debe ser.


      NOTA: es importante revisar que el nombre del patron no este ya en el diccionario de tokens.

      PREGUNTA: se deben guardar en el lexer las notas que contiene el patron?? AUN NO SE
      '''
      if t.type == "PATTERN_NAME" and t.value not in self.declaredPatterns:
          self.tokens.append(t.value)
          self.declaredPatterns[t.value] = [] # lista para en un futuro guardar todas las notas que contiene el patron.
          print('ahora esta es la lista de tokens', self.tokens)


      # print('el valor:', t.value)

      return t


    
  # Error handling rule
  def t_error(self, t):
      print("Illegal character '%s'" % t.value[0])
      t.lexer.skip(1)