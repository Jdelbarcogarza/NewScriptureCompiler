from sly import Lexer, Parser

class makeLexer(Lexer):
    tokens = {
        'NOTE',
        'COMMENTS',
        'NEWLINE',
        'EMPTY',
        'LBRACKET',
        'RBRACKET',
        'LPAREN',
        'RPAREN',
        'PATTERN_NAME',  # token generico para aceptar nombres de patrones
        'TEMPO_VAL',  # valor dentro de parentesis de tempo
        'QUOTES',
        'DASHES',
        'TEMPO',
        'PAT',
        'ASTERISKS',
        'PLUS',
        # ----- palabras reservadas de metadata --------
        'NAME',
        'ARTIST',
        'CHARTER',
        'ALBUM',
        'YEAR',
        'OFFSET',
        'DIFFICULTY',
        'PREVIEW_START',
        'PREVIEW_END',
        'GENRE',
        'MUSIC_STREAM',
        # 'ID'
    }

    ignore = ' \t'
    literals = {'+', '-', '*', '/', '(', ')', '{', '}', ':', '"', '*'}

    # Base ID rule
    # ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # # Special cases
    # ID['tempo'] = 'TEMPO'
    # ID['pat'] = 'PAT'
    # ID['Name'] = 'NAME'
    # ID['Artist'] = 'ARTIST'
    # ID['Charter'] = 'CHARTER'
    # ID['Album'] = 'ALBUM'
    # ID['Year'] = 'YEAR'
    # ID['Offset'] = 'OFFSET'
    # ID['Difficulty'] = 'DIFFICULTY'
    # ID['PreviewStart'] = 'PREVIEW_START'
    # ID['PreviewEnd'] = 'PREVIEW_END'
    # ID['Genre'] = 'GENRE'
    # ID['MusicStream'] = 'MUSIC_STREAM'

    # Tokens
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACKET = r'\{'
    RBRACKET = r'\}'
    DASHES = r'\-{3}'
    ASTERISKS = r'\*{3}'
    PLUS = r'\+'

    declaredPatterns = {}  # Definir el diccionario para almacenar patrones

    # regular expression rule with some action
    @_(r'\n+')
    def NEWLINE(self, t):
        self.lineno += len(t.value)
        return t

    @_(r'N\d{1,2}(?:_\d{1,2})?')
    def NOTE(self, t):
        return t

    # @_(r'\#.*')
    # def COMMENTS(self, t):
    #     print('Comentario', t.value)
    #     pass

    @_(r'\d+')
    def TEMPO_VAL(self, t):
        t.value = int(t.value)
        return t

    @_(r'"[a-zA-Z0-9áéíóúüñ.\s]*"')
    def QUOTES(self, t):
        print('ATRIBUTO DE METADATA', t.value)
        return t

    @_(r'[a-zA-Z][a-zA-Z_0-9]*')
    def PATTERN_NAME(self, t):
        if t.value not in self.declaredPatterns and t.type == 'PATTERN_NAME':
            self.declaredPatterns[t.value] = []  # lista para en un futuro guardar todas las notas que contiene el patron.
            self.tokens.add(t.value)
            print('ahora esta es la lista de tokens', self.tokens)
        print('el valor:', t.value)
        return t

    # Error handling rule
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class makeParser(Parser):
    start = 'metadata_entries'

    tokens = makeLexer.tokens

    def __init__(self, lexer):
        print('---- Inicialización del Parser ----')
        self.lexer = lexer
        self.metadata_block_matched = False  # Flag para rastrear si se ha encontrado el bloque de metadata
        self.defined_patterns = set()  # Conjunto para almacenar los nombres de patrones definidos

    @_('DASHES NEWLINE metadata_entries DASHES NEWLINE')
    def metadata(self, p):
        print("HALLOOOOOO")
        return p[0]

    @_('metadata_entry NEWLINE metadata_entries',
       'metadata_entry NEWLINE')
    def metadata_entries(self, p):
        print("HALLOOOOOO")
        return p[0]

    @_('NAME ":" QUOTES',
       'ARTIST ":" QUOTES',
       'CHARTER ":" QUOTES',
       'ALBUM ":" QUOTES',
       'YEAR ":" QUOTES',
       'OFFSET ":" QUOTES',
       'DIFFICULTY ":" QUOTES',
       'PREVIEW_START ":" QUOTES',
       'PREVIEW_END ":" QUOTES',
       'GENRE ":" QUOTES',
       'MUSIC_STREAM ":" QUOTES')
    def metadata_entry(self, p):
        print("HALLOOOOOO")
        return p[0]

    @_('ASTERISKS NEWLINE pattern_definitions ASTERISKS NEWLINE')
    def patterns(self, p):
        print("HALLOOOOOO")
        return p[0]

    @_('pattern_definition pattern_definitions',
       'pattern_definition')
    def pattern_definitions(self, p):
        print("HALLOOOOOO")
        return p[0]

    @_('PAT PATTERN_NAME LBRACKET NEWLINE notes NEWLINE RBRACKET NEWLINE')
    def pattern_definition(self, p):
        self.defined_patterns.add(p.PATTERN_NAME)  # Agregar el nombre del patrón al conjunto de patrones definidos
        return p[0]

    @_('note NEWLINE notes',
       'note')
    def notes(self, p):
        print("HALLOOOOOO")
        return p[0]

    @_('NOTE',
       '"E"')
    def note(self, p):
        print("HALLOOOOOO")
        return p[0]

    @_('PLUS NEWLINE tempo_definitions PLUS NEWLINE')
    def song_block(self, p):
        print("HALLOOOOOO")
        return p[0]

    @_('tempo_definition tempo_definitions',
       'tempo_definition')
    def tempo_definitions(self, p):
        print("HALLOOOOOO")
        return p[0]

    @_('TEMPO LPAREN TEMPO_VAL RPAREN LBRACKET NEWLINE tempo_contents NEWLINE RBRACKET NEWLINE')
    def tempo_definition(self, p):
        print("HALLOOOOOO")
        return p[0]

    @_('tempo_content tempo_contents',
       'tempo_content')
    def tempo_contents(self, p):
        print("HALLOOOOOO")
        return p[0]

    @_('note',
       'PATTERN_NAME')
    def tempo_content(self, p):
        if p[0] in self.lexer.declaredPatterns:
            if p[0] not in self.defined_patterns:
                print(f"Error: El patrón '{p[0]}' se utiliza en un tempo pero no está definido en la sección de patrones.")
                raise SyntaxError(f"Patrón no definido '{p[0]}' utilizado en un tempo.")
            return p[0]

    def error(self, p):
        if not p:
            print("Error de sintaxis en el token", p.type)
            self.errok()
        else:
            print("Error de sintaxis en EOF")
            
        # self.index += 1

if __name__ == '__main__':
    lexer = makeLexer()
    parser = makeParser(lexer)
    with open('mySong.txt', 'r') as file:
            text = file.read()
            
            if text:
                parser.parse(lexer.tokenize(text))
