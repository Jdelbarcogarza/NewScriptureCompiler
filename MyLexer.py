import ply.lex as lex

class Lexer(object):

    declaredPatterns = dict()  # Diccionario para almacenar los patrones declarados

    # Palabras reservadas
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

    # Definición de tokens
    tokens = [
        'NOTE',
        'COMMENT',
        # 'EMPTY',
        'LBRACKET',
        'RBRACKET',
        'LPAREN',
        'RPAREN',
        'PATTERN_NAME', # Token genérico para aceptar nombres de patrones 
        'TEMPO_VAL', # Valor dentro de paréntesis de tempo
        'QUOTES',
        'DASHES',
        'NEWLINE',
        'ASTERISKS',
        'PLUS'
    ] + list(reserved.values())

    # Caracteres devueltos "tal cual" por el lexer
    literals = [':']

    # Caracteres ignorados (espacios en blanco)
    t_ignore = ' \t'

    # Reglas de expresiones regulares para tokens simples
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\{'
    t_RBRACKET = r'\}'
    # t_COLON = r':'
    t_DASHES = r'\-{3}'

    def build(self, **kwargs):
        # Construir el lexer utilizando las reglas definidas en la clase
        self.lexer = lex.lex(module=self, **kwargs)

    # Función para probar la salida del lexer
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

    # Regla de expresión regular con acción para el token NEWLINE
    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')
        return t

    # Regla para el token NOTE
    def t_NOTE(self, t):
        r'N\d{1,2}(?:_\d{1,2})?'
        return t

    # Regla para el token TEMPO_VAL
    def t_TEMPO_VAL(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    '''
    Utilizado para extraer el valor en los atributos en la sección de metadata. Lo que está dentro de quotes
    puede tener acentos y otros caracteres no propios del inglés.
    '''
    def t_QUOTES(self, t):
        r'"[a-zA-Z0-9áéíóúüñ.\s]*"'
        return t

    '''
    Este se utiliza para parsear palabras reservadas y aquí dentro se guardan los nombres de los patrones.
    '''
    def t_PATTERN_NAME(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, "PATTERN_NAME")

        '''
        1. Si t.type == PATTERN_NAME, significa que este es el string identificador del patrón PAT declarado. Se guarda
        en los tokens para en un futuro parsearlo como debe ser.

        NOTA: es importante revisar que el nombre del patrón no esté ya en el diccionario de tokens.

        PREGUNTA: ¿se deben guardar en el lexer las notas que contiene el patrón? AÚN NO SE
        '''
        if t.type == "PATTERN_NAME" and t.value not in self.declaredPatterns:
            self.tokens.append(t.value)
            self.declaredPatterns[t.value] = []

        return t

    # Regla para el token ASTERISKS
    def t_ASTERISKS(self, t):
        r'\*{3}'
        return t
    
    # Regla para el token PLUS
    def t_PLUS(self, t):
        r'\+{3}'
        return t

    # Regla para manejo de errores
    def t_error(self, t):
        print("Carácter ilegal '%s'" % t.value[0])
        t.lexer.skip(1)