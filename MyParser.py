from MyLexer import Lexer
import ply.yacc as yacc

class Parser(object):

    def __init__(self, lexer):
        print('---- Inicialización del Parser ----')
        self.parser = yacc.yacc(module=self)
        self.lexer = lexer
        self.metadata_block_matched = False  # Flag para rastrear si se ha encontrado el bloque de metadata
        self.defined_patterns = set()  # Conjunto para almacenar los nombres de patrones definidos

    tokens = Lexer.tokens

    print("TOKENS DEL LEXER!!", tokens)

    # Regla para la estructura general de una canción
    def p_song(self, p):
        '''song : metadata patterns song_block'''
        pass

    # Regla para el bloque de metadata
    def p_metadata(self, p):
        '''metadata : DASHES NEWLINE metadata_entries DASHES NEWLINE'''
        pass

    # Regla para las entradas de metadata
    def p_metadata_entries(self, p):
        '''metadata_entries : NAME ':' QUOTES NEWLINE
                            | ARTIST ':' QUOTES NEWLINE
                            | CHARTER ':' QUOTES NEWLINE
                            | ALBUM ':' QUOTES NEWLINE
                            | YEAR ':' QUOTES NEWLINE
                            | OFFSET ':' QUOTES NEWLINE
                            | DIFFICULTY ':' QUOTES NEWLINE
                            | PREVIEW_START ':' QUOTES NEWLINE
                            | PREVIEW_END ':' QUOTES NEWLINE
                            | GENRE ':' QUOTES NEWLINE
                            | MUSIC_STREAM ':' QUOTES NEWLINE'''
        pass

    # Regla para el bloque de patrones
    def p_patterns(self, p):
        '''patterns : ASTERISKS NEWLINE pattern_definitions ASTERISKS NEWLINE'''
        pass

    # Regla para las definiciones de patrones
    def p_pattern_definitions(self, p):
        '''pattern_definitions : pattern_definition
                               | pattern_definitions pattern_definition'''
        pass

    # Regla para la definición de un patrón
    def p_pattern_definition(self, p):
        '''pattern_definition : PAT PATTERN_NAME LBRACKET NEWLINE notes NEWLINE RBRACKET NEWLINE'''
        self.defined_patterns.add(p[2])  # Agregar el nombre del patrón al conjunto de patrones definidos

    # Regla para las notas dentro de un patrón
    def p_notes(self, p):
        '''notes : note
                 | notes NEWLINE note'''
        pass

    # Regla para una nota individual
    def p_note(self, p):
        '''note : NOTE
                | 'E' '''
        pass

    # Regla para el bloque de canción
    def p_song_block(self, p):
        '''song_block : ASTERISKS NEWLINE tempo_definitions ASTERISKS NEWLINE'''
        pass

    # Regla para las definiciones de tempo
    def p_tempo_definitions(self, p):
        '''tempo_definitions : tempo_definition
                             | tempo_definitions tempo_definition'''
        pass

    # Regla para la definición de un tempo
    def p_tempo_definition(self, p):
        '''tempo_definition : TEMPO LPAREN TEMPO_VAL RPAREN LBRACKET NEWLINE tempo_contents NEWLINE RBRACKET NEWLINE'''
        pass

    # Regla para los contenidos de un tempo
    def p_tempo_contents(self, p):
        '''tempo_contents : tempo_content
                          | tempo_contents tempo_content'''
        pass

    # Regla para un contenido individual de tempo
    def p_tempo_content(self, p):
        '''tempo_content : note
                         | PATTERN_NAME'''
        if p[1] in self.lexer.declaredPatterns:
            if p[1] not in self.defined_patterns:
                print(f"Error: El patrón '{p[1]}' se utiliza en un tempo pero no está definido en la sección de patrones.")
                raise SyntaxError(f"Patrón no definido '{p[1]}' utilizado en un tempo.")

    # Manejo de errores PANIC
    def p_error(self, p):
        if p:
            print("Error de sintaxis en el token", p.type)
            # Descartar el token y decirle al parser que está bien
            self.parser.errok()
        else:
            print("Error de sintaxis en EOF")