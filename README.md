# Documentación Técnica: Proyecto Vigenère

## Estructura del Directorio
El proyecto consta de un único script principal ubicado en `fjperezdev-vigenere-cypher/main.py`.

## Clase: `CriptoanalisisVigenere`
Esta clase contiene todas las constantes y métodos necesarios para el cifrado, descifrado y criptoanálisis.

### Constantes
* **`ALFABETO`**: Lista que contiene las letras mayúsculas de la 'A' a la 'Z'.
* **`FRECUENCIAS`**: Diccionario con las frecuencias porcentuales de aparición de letras (basado en estadísticas de idioma, incluyendo inglés/español).

### Métodos Principales

#### 1. `formateoDeTexto(self, texto: str) -> str`
Prepara el texto para ser procesado.
* Convierte el texto a mayúsculas.
* Reemplaza la letra 'Ñ' por el dígrafo 'GN'.
* Elimina cualquier carácter que no se encuentre en `ALFABETO`.

#### 2. `vigenere(self, mensaje: str, clave: str, cifrado: bool) -> str`
Ejecuta el algoritmo de Vigenère.
* Formatea la clave antes de usarla.
* **Cifrado (`cifrado=True`)**: Suma el índice de la letra del mensaje con el de la clave: `(Msg + Clave) % LongitudAlfabeto`.
* **Descifrado (`cifrado=False`)**: Resta el índice de la clave al del mensaje: `(Msg - Clave) % LongitudAlfabeto`.

#### 3. `calcularIndiceDeCoincidencias(self, texto)`
Calcula el Índice de Coincidencia (IC) de un texto para evaluar si se comporta como lenguaje natural.
* Utiliza la fórmula: Sumatoria de `n*(n-1)` dividido por `Total*(Total-1)`.

#### 4. `calcularChiCuadrado(self, text)`
Calcula el valor Chi-cuadrado para comparar la frecuencia de letras del texto con las `FRECUENCIAS` esperadas.
* Itera sobre cada letra y aplica la fórmula: `((Observado - Esperado)^2) / Esperado`.
* Un valor más bajo indica mayor similitud con el idioma objetivo.

#### 5. `longitudClave(self, textoCifrado: str, maximaLongitud: int = 20) -> int`
Estima la longitud de la clave utilizada para cifrar.
*Prueba longitudes desde 1 hasta `maximaLongitud`.
* Para cada longitud, divide el texto en columnas y calcula el IC promedio de estas.
* Retorna la longitud que produce el IC promedio más alto.

#### 6. `encontrarClave(self, textoCifrado: str, longitudClave: int) -> str`
Recupera la clave de cifrado sin conocerla previamente.
* Divide el texto en columnas según la `longitudClave` detectada.
* Para cada columna, prueba las 26 letras posibles como clave (Cifrado César).
* Selecciona la letra que genera el menor valor Chi-cuadrado al descifrar la columna.
* Concatena las mejores letras para formar la clave final.

## Flujo de Ejecución (`main`)
El script ejecuta las siguientes pruebas al iniciarse:
1.  **Demostración**: Cifra y descifra un texto de ejemplo (`TEXTO_EJEMPLO_CLARO`) usando la clave "SECRETO".
2.  **Criptoanálisis**:
    * Toma la variable `TEXTOAROMPER`.
    * Calcula la longitud de la clave automáticamente.
    * Encuentra la clave utilizando análisis de frecuencias.
    * Muestra el texto descifrado final.
