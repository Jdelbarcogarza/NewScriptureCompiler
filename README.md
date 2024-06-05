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


## Manual de Usuario

### Formato del Archivo de Entrada

El archivo de entrada (`test2.txt`) debe seguir un formato específico para ser procesado correctamente. A continuación se presenta un ejemplo del formato requerido:

```txt
---
Name: "77"
Artist: "Peso Pluma"
Album: "Génesis"
Charter: "CX404"
Year: "2023"
Offset: 0
Difficulty: 3
PreviewStart: 15
PreviewEnd: 35
Genre: "Regional Mexicano"
MusicStream: "song.mp3"
---
pat patJuna {
    N1
    N2
    N3
    N654
}

pat patHactor {
    N5
    N6
    N3
    N12345_123456
}
---
tempos(23) {
N2
N12
N123
patHactor
N12345_1234
N12345_12345
N12345_123456
}

tempos(543) {
N1234
N12345
N12345_1
N12345_12
N12345_123
patJuna
}
```

### Instrucciones

1. **Creación del Archivo de Entrada**:
   - Asegúrese de que su archivo de entrada siga el formato descrito anteriormente.
   - Incluya todos los metadatos necesarios en el primer bloque del archivo.
   - Defina los patrones y tempos en los bloques subsecuentes.

2. **Ejecución del Compilador**:
   - Ejecute el script `NewScripture.py` usando Python.
   - El archivo `notes.chart` se generará en el mismo directorio que el script.

### Salida

El archivo de salida `notes.chart` tendrá un formato compatible con varios programas de edición y reproducción de música. Contendrá secciones con metadatos de la canción, sincronización de pistas y notas musicales.

### Errores Comunes

- **Error 101**: Indica que el archivo de entrada no tiene el número correcto de bloques de datos. Asegúrese de seguir el formato especificado.
- **Error de Sintaxis**: Puede ocurrir si los patrones y tempos no están correctamente definidos en el archivo de entrada.

---

Este README proporciona la información necesaria para comprender y utilizar el compilador NewScripture de manera efectiva. Si encuentra algún problema o tiene alguna pregunta, no dude en contactar al desarrollador.
