# NewScripture Compiler

El **NewScripture Compiler** es una herramienta que convierte archivos de texto con información de canciones en un formato específico en archivos `.chart` compatibles con varios programas de edición y reproducción de música. Este README proporciona tanto el manual técnico como el manual de usuario del compilador.

## Manual Técnico

### Estructura del Proyecto

El proyecto se compone de los siguientes archivos:
- `NewScripture.py`: El script principal del compilador.
- `test2.txt`: Archivo de entrada con la información de la canción.
- `notes.chart`: Archivo de salida generado por el compilador.

### Descripción de los Componentes

#### Lexer y Parser
El proyecto utiliza la biblioteca `sly` para la creación de lexers y parsers.

- **noteLexer** y **noteParser**:
  - Estos componentes manejan la tokenización y el análisis de notas musicales dentro del archivo de entrada.
  - `noteLexer` reconoce tokens como `NOTE` y `LONG_NOTE`.
  - `noteParser` procesa estos tokens y los organiza en una lista de notas.

- **metaLexer** y **metaParser**:
  - Estos componentes manejan la tokenización y el análisis de metadatos de las canciones.
  - `metaLexer` reconoce tokens como `NAME`, `ARTIST`, `ALBUM`, `YEAR`, entre otros.
  - `metaParser` procesa estos tokens y los organiza en una lista de atributos.

#### Funciones Clave

- `substitute_patterns(input_string, patterns)`: Sustituye patrones definidos en el archivo de entrada por sus valores correspondientes.
- `pattern_maker(data)`: Genera patrones a partir de las definiciones encontradas en el archivo de entrada.
- `write_file(data_parts)`: Escribe el archivo de salida `.chart` utilizando los metadatos y notas procesadas.
- `main()`: Función principal que coordina la lectura del archivo de entrada, el procesamiento de datos y la escritura del archivo de salida.

### Ejecución

Para ejecutar el compilador, simplemente ejecute el script `NewScripture.py`:
```sh
python NewScripture.py <y el nombre del archivo de entrada, ejemplo: inputSample.ns>
