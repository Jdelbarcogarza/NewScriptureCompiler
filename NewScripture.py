from sly import Lexer, Parser


#  NOTES MANAGER - - - - - - - - - - - - - - - - - -

#La clase noteLexer inicia el lexer para definir las notas
class noteLexer(Lexer):
    tokens = { 'NOTE', 'LONG_NOTE' } #Especificamos los tokens que lexer puede producir.
    ignore = ' \t' #Define caracteres a ignorar durante la tokenizacion

    # Se capturan los caracteres de salto de linea
    @_(r'\n')
    def NEWLINE(self, t):
        self.lineno += len(t.value) #Actualiza el numero de saltos de linea para cada salto de linea encontrado
        return t
    
    #Se capturan nuestras notas largas con regrex
    @_(r'N\d{1,5}_\d{1,6}')
    def LONG_NOTE(self, t):
        return t

    #Se capturan nuestras notas regrex
    @_(r'N\d{1,5}')
    def NOTE(self, t):
        return t
    
    #Imprime un mensjae de error cuando encuentra caracteres ilegales
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
  
 #Procesamos los tokens generados con el lexer con el Parser 
class noteParser(Parser):
    tokens = noteLexer.tokens #Utilizmaos los tokens definidos en notelexer

    #Inicializamos una lista vacia para guardar los valores que analizemos con el parser.
    def __init__(self):
        self.out = []
    #Guardamos la nota en self.out
    @_('NOTE')
    def notes(self, p):
        self.out.append(p.NOTE)
        return
    
    #Guardamos la nota larga en self.out
    @_('LONG_NOTE')
    def notes(self, p):
        self.out.append(p.LONG_NOTE)
        return
    #LLama al metodo de parser padre y regresa la lista self.out
    def parse(self, tokens):
        super().parse(tokens)
        return self.out  #Return self.out after parsing
    
    #Manda un mensaje cuando ocurre un error
    def error(self, t):
        print(f'Syntax error at line {t.lineno}')


#  METADATA  - - - - - - - - - - - - - - - - - - - - 
#Declaramos los tipos de tokens que el lexer puede producir
class metaLexer(Lexer):
    tokens = { 'NAME', 'ARTIST', 'CHARTER', 'ALBUM', 'YEAR', 'OFFSET', 'DIFFICULTY', 'PREVIEWSTART', 'PREVIEWEND', 'GENRE', 'MUSICSTREAM', 'NUMBER', 'STRING' }
    ignore = ' \t'
    
    #Tenemos las palabras clave de la metadata
    NAME = r'Name:'
    ARTIST = r'Artist:'
    CHARTER = r'Charter:'
    ALBUM = r'Album:'
    YEAR = r'Year:'
    OFFSET = r'Offset:'
    DIFFICULTY = r'Difficulty:'
    PREVIEWSTART = r'PreviewStart:'
    PREVIEWEND = r'PreviewEnd:'
    GENRE = r'Genre:'
    MUSICSTREAM = r'MusicStream:'

    #Convertimos numeros a enteros
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t
    #Extraemos valores de string con doble comilla
    @_(r'"([^"]*)"')
    def STRING(self, t):
        t.value = t.value[1:-1]  #Quita las comillas
        return t
    #Ignoramos saltos de linea y actualizamos el valor
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)
        return None
    #Avanzamos el indice del lexer y mandamos mensaje cuando tenemos caracteres ilegales
    def error(self, t):
        print(f'Illegal character {t.value[0]!r} at line {self.lineno}')
        self.index += 1
    
    #Definimos funcion del parser y usamos los tokens que usamos en el metaparser.
class metaParser(Parser):
    tokens = metaLexer.tokens
   
    #Incializamos una lista vacia para guardar lo que hagamos parser de la metadata
    def __init__(self):
        self.result = []
    #Una regla de atributo donde empezamos nuestro parser
    @_('attributes')
    def program(self, p):
        pass
    #Hace match con una secuencia de atributos vacio.
    @_('attribute attributes',
       'empty')
    def attributes(self, p):
        pass

    #Hace match con las vairables de la metdata y los retorna en self.result
    @_('NAME STRING',
       'ARTIST STRING',
       'CHARTER STRING',
       'ALBUM STRING',
       'YEAR STRING',
       'GENRE STRING',
       'MUSICSTREAM STRING',
       'OFFSET NUMBER',
       'DIFFICULTY NUMBER',
       'PREVIEWSTART NUMBER',
       'PREVIEWEND NUMBER')
    def attribute(self, p):
        self.result.append(f'{p[0]} {p[1]}')
     
    #Es una producion vacia
    @_('')
    def empty(self, p):
        pass
   #LLama al metodo de parser padre y regresa la lista self.out
    def parse(self, tokens):
        super().parse(tokens)
        return self.result  #Regresa sle.result despues del parsing

   #Manda un mensaje cuando ocurre un error y en que linea ocurrio
    def error(self, t):
        if t:
            print(f'Syntax error at line {t.lineno}')
        else:
            print('Syntax error at EOF')













def substitute_patterns(input_string, patterns):
    result_lines = []
    for line in input_string.splitlines(): #Itera sobre cada linea de los string del archivo
        for pattern_name, pattern_data in patterns.items(): #Itera sobre cada patron en los diccionarios de los patrones por eso el .items()
            if pattern_name in line:
                #Remplaza pattern_name con pattern_data y manda lo remplazado a la lista
                replaced_line = line.replace(pattern_name, f"{' '.join(pattern_data)}")
                result_lines.append(replaced_line)
                break
        else:
            result_lines.append(line) #Manda las lineas resultantes a la lista
    s = str('\n'.join(result_lines))
    return s



def pattern_maker(data):
    patterns = {}
    lines = data.split() #Separa la informacion en lineas
    cont = 0
    aux = ''
    naux = ''''''
    for w in lines:
        if w == 'pat': #Revisa si el nombre del patron empieza con pat
            cont += 1
        elif cont > 0:
            if w == '}': #Revisa si se encuentra con el que se termina el bloque de los patrones
                lex = noteLexer() #Incializa el lexer para ver los patrones
                par = noteParser() #Incializa el paser para analizar los patrones
                patterns[aux] = par.parse(lex.tokenize(naux))
                cont = 0
                naux = ''''''
            elif cont >= 3:
                naux += w + '\n'
            elif cont == 1:
                aux = w
                cont += 1
            elif cont == 2 and w == '{': #Revisa si se encuentra con el que se inicia el bloque de los patrones
                cont += 1
            else:
                raise ValueError('Error in pattern defining not starting properly with { value: ' + w)
        else:
            raise ValueError('Error in pattern function not starting with \"pat\": ' + w) #Establece error cuando el nombre del patron no empieza con pat
    return patterns


def write_file(data_parts):
    m_lexer = metaLexer() #Incializa el lexer para ver la metadata
    m_parser = metaParser() #Incializa el parser para analizar la metadata
    meta = m_parser.parse(m_lexer.tokenize(data_parts[1]))  #Analiza la metadatade de data_parts[1]

    # Patterns
    patterns = pattern_maker(data_parts[2]) #Genera los patrones 
    
    # Tempos
    tempo_data = substitute_patterns(data_parts[3], patterns) #Genera la informacion de los tempos

    
    with open('notes.chart', 'w', encoding='utf-8') as outfile:
        outfile.write('[Song]\n{\n')
        for value in meta:
            outfile.write(f'{value}\n')

        #Generaliza caracteristicas extras ignoradas por el compilador
        outfile.write('}\n\n[SyncTrack]\n{\n  0 = TS 4\n}\n\n[Events]\n{\n}\n\n[ExpertSingle]\n{\n')

        naux = '' #Inicializamos un string vacio para acumular los datos de las notas dentro de un bloque de tempo
        time = 1000 #Establece un tiempo default
        current_tempo = 0 #Incializamos el tiempo actual del tempo
        inside = 0 #Vemos si el parser esta dentro de un bloque de tempo
        notes = tempo_data.split() #Dividimos la informacion del tempo en notas individuales

        for x in notes:
            if inside > 0: #Checa si el parser esta adentro de la nota de tiempo
                if inside == 1:
                    if x == '{':
                        inside += 1
                    else:
                        raise ValueError('Error in tempo function, not initializing properly with \"{\", given:', x)
                elif inside >= 2 and x != '}':
                    naux += x + '\n'
                elif x == '}':
                                    
                    lex = noteLexer() #Incializa el lexer para ver las notas
                    par = noteParser() #Incializa el parser para analizar los patrones
                    # Ajustamos nuestras notas basandonos en el tempo
                    note_naux = par.parse(lex.tokenize(naux))  
                    for y in note_naux:
                        time += int(current_tempo)
                        z = y.replace('N', '')
                        if '_' in z:
                            n = z.split('_')
                            for ind in n[0]:
                                outfile.write(f'{time} N {ind} {n[1]}\n')
                        else:
                            for ind in z:
                                outfile.write(f'{time} N {ind} 0\n')
                        

                    inside = 0
            #Revisa si se empieza un nuevo bloque de tempo
            elif x[:7] == 'tempos(' and inside == 0:
                if (x[7:])[:-1]:
                    current_tempo = x[7:][:-1]
                    inside += 1
            else:
                raise ValueError('Value not expected, expected tempo function. Given:', x)

        outfile.write('}\n') #Escribe el final de la seccion de notas




# MAIN - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def main():
   filename = input()  #Estableciendo la variable para recibir el input del archivo
   try:
        with open(filename, 'r', encoding='utf-8') as file: #Leyendo el archivo
            data = str(file.read())
        
        data_parts = ("useless space" + data).split('---') #Separa la informacion en el texto siempre que se encuentre con este string ---
        
        if len(data_parts) == 4 or len(data_parts) == 5: #Revisa si el numero de partes es 4 o 5
            write_file(data_parts)
        else:
            print('Error 101: Fewer component blocks not properly made (wrong length size)') #Da error si el numero de parte no es valido
            return None










   except FileNotFoundError:
        print(f"El archivo '{filename}' no existe.") #Imprime error si el nombre del archivo no exite
   except IOError:
        print(f"Error al leer el archivo '{filename}'.") #Imprime error si no puede leer el archivo

# ----- PROGRAM ------
#Solo se imprime main cuando el codigo esta ejecutando
if __name__ == "__main__":
    main()