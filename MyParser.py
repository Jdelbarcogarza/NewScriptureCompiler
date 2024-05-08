from MyLexer import Lexer
import ply.yacc as yacc

class Parser(object):

  def __init__(self, lexer):
    print('---- Parser Init ----')
    self.parser = yacc.yacc(module=self)
    self.lexer = lexer
    self.metadata_block_matched = False  # Flag to track rule match


  tokens = Lexer.tokens

  print("TOKENS FROM LEXERR!!",tokens)

  # puede ser start o end con los ---
  def p_metadata_block_limit(self, p):
    '''metadata_block_limit : metadata_attribute 
                            | DASHES
                            | metadata_block_limit metadata_attribute'''
                            
    if len(p) == 1:
      print("DASHES",p[0])
    if len(p) == 2:
            p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]
      
    

  def p_metadata_attribute(self, p):
    '''metadata_attribute : NAME COLON QUOTES
                           | ARTIST COLON QUOTES
                           | CHARTER COLON QUOTES
                           | ALBUM COLON QUOTES
                           | YEAR COLON QUOTES
                           | OFFSET COLON NUMBER
                           | DIFFICULTY COLON NUMBER
                           | PREVIEW_START COLON QUOTES
                           | PREVIEW_END COLON QUOTES
                           | GENRE COLON QUOTES
                           | MUSIC_STREAM COLON QUOTES'''
    p[0] = (p[1], p[3])
    print("atributo", p[1], p[3])
  
  def p_tempo_block(self, p):
    '''tempo_block : TEMPO LPAREN NUMBER RPAREN LBRACKET note_list RBRACKET'''    
    print("Tempo:", p[3])
    for note in p[6]:
        print("Note:", note)

  def p_note_list(self, p):
      '''note_list : note_list note
                  | note'''
      if len(p) == 2:
          p[0] = [p[1]]
      else:
          p[0] = p[1] + [p[2]]

  def p_note(self, p):
      '''note : NOTE
              | PATTERN_NAME'''
      p[0] = p[1]

  # PANIC error handling
  def p_error(self, p):
    if p:
      print("Syntax error at token", p.type)
          # Just discard the token and tell the parser it's okay.
      self.parser.errok()
    else:
        print("Syntax error at EOF")