#### New scripture compiler

A compiler to read a Domain Specific Language to create [Clone Hero](https://clonehero.net/) song scriptures.


## Gramática BNF
Claro, puedo proporcionar una descripción detallada de cada parte de la gramática BNF que he propuesto para tu compilador. La gramática está diseñada para parsear un archivo con la estructura que has descrito en el ejemplo. Aquí está el desglose de cada componente:

### Gramática BNF Comentada

```bnf
<newscripture> ::= <metadata_block> <pattern_block> <tempo_block> <notes>
```
- **<newscripture>**: Este es el elemento raíz de la gramática y encapsula toda la estructura del archivo. Define que un archivo válido consiste en un bloque de metadatos, seguido de un bloque de patrones, un bloque de tempos y finalmente una lista de notas.

```bnf
<metadata_block> ::= '---' <metadata_entries> '---'
<metadata_entries> ::= <metadata_entry> <metadata_entries> | <metadata_entry>
<metadata_entry> ::= <key> ':' <value>
```
- **<metadata_block>**: Define el bloque de metadatos, que es encabezado y finalizado por tres guiones (`---`). Contiene una o más entradas de metadatos.
- **<metadata_entries>**: Una lista recursiva de entradas de metadatos. Puede consistir en una sola entrada o múltiples entradas.
- **<metadata_entry>**: Cada entrada de metadatos es un par clave-valor separado por dos puntos (`:`).

```bnf
<pattern_block> ::= '***' <pattern_definitions> '***'
<pattern_definitions> ::= <pattern_definition> <pattern_definitions> | <pattern_definition>
<pattern_definition> ::= 'pat' <pattern_name> '{' <note_sequence> '}'
```
- **<pattern_block>**: Define un bloque de patrones delimitado por tres asteriscos (`***`). Incluye una o más definiciones de patrones.
- **<pattern_definitions>**: Una lista recursiva de definiciones de patrones.
- **<pattern_definition>**: Define un patrón específico con un nombre y una secuencia de notas entre llaves.

```bnf
<tempo_block> ::= '+++' <tempo_definitions> '+++'
<tempo_definitions> ::= <tempo_definition> <tempo_definitions> | <tempo_definition>
<tempo_definition> ::= 'tempo(' <number> ')' '{' <tempo_contents> '}'
```
- **<tempo_block>**: Contiene definiciones de tempo encerradas entre tres signos de suma (`+++`). Define cómo las notas deben ser reproducidas a diferentes tempos.
- **<tempo_definitions>**: Una lista de definiciones de tempo.
- **<tempo_definition>**: Define un conjunto de notas o referencias a patrones que deben ser tocadas a un tempo específico, indicado por un número entre paréntesis.

```bnf
<notes> ::= <note_entry> <notes> | <note_entry>
<note_entry> ::= <timestamp> <note> | <timestamp> <pattern_name> | <timestamp> 'E'
```
- **<notes>**: Una lista recursiva de entradas de notas.
- **<note_entry>**: Define una nota individual, una referencia a un patrón, o una nota especial 'E', cada una asociada con un timestamp específico.

```bnf
<key> ::= 'Name' | 'Artist' | 'Charter' | 'Album' | 'Year' | 'Offset' | 'Difficulty' | 'PreviewStart' | 'PreviewEnd' | 'Genre' | 'MusicStream'
<value> ::= '"' <alphanumeric> '"'
<note_sequence> ::= <note> <note_sequence> | <note>
<note> ::= 'N' <digit> <optional_digit>
<optional_digit> ::= '_' <digit> | ε
<pattern_name> ::= <identifier>
<number> ::= <digit>+
<timestamp> ::= <number>
```
- **<key>** y **<value>**: Definen las claves y valores permitidos en las entradas de metadatos.
- **<note_sequence>**, **<note>**, **<optional_digit>**, **<pattern_name>**, **<number>**, **<timestamp>**: Estos elementos definen los componentes más fundamentales del archivo, como las notas, patrones, números, y marcas de tiempo.

Cada parte de la gramática está diseñada para ser lo suficientemente flexible para adaptarse a las estructuras más comunes que podrías necesitar, pero también lo suficientemente específica para asegurar que los datos se parseen de manera correcta y coherente. Si hay aspectos del lenguaje o estructuras

 de datos que necesitas modificar o expandir, podemos ajustar las definiciones acordemente.