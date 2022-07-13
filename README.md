# EDA: Easy Data Augmentation para tareas NER

***

### Técnicas:

* Synonym Replacement (SR):
  1. Se obtiene una palabra aleatoria
  2. Se sustituye por un sinónimo
  3. Repetir n veces (n = α · l, siendo l la longitud de la frase en palabras)


* Random Insertion (RI):
  1. Se obtiene una palabra aleatoria
  2. Se inserta el sinónimo de la palabra en una posicioón aleatoria de la frase
  3. Repetir n veces (n = α · l, siendo l la longitud de la frase en palabras)

* Random Swap (RS):
  1. Se obtienen 2 palabras aleatorias
  2. Se intercambian sus posiciones
  3. Repetir n veces (n = α · l, siendo l la longitud de la frase en palabras)

* Random Deletion (RD):
  1. Eliminar cada palabra con probabilidad p (p = α)


Estas técnicas mantienen las entidades intactas, es decir:
* Las entidades NO se reemplazan por sinónimos en SR.
* Las entidades NO se insertan en otras zonas del texto en RI.
* Las entidades compuestas por más de un token NO se dividen (no se insertan palabras en medio) en RI.
* Las entidades NO son eliminadas en RD.
* Las entidades NO se intercambian de posición en RS.

---

### Parámetros (eda_params.json):

* α - Porcentaje de parabras a cambiar por frase.
  * Cada una de las 4 técnicas tiene su propio α (alpha_sr, alpha_ri, alpha_rs, alpha_rd)
  * Para α = 0, esa técnica no se aplica
* n_aug - Número de frases nuevas a generar por frase original (ha de ser múltiplo del número de técnicas a utilizar)
* input_conll: path al fichero conll con los datos a aumentar
  - Formato:
    ```
    File [FileName] -
    [word] [InitOffset]-[EndOffset] [tag]-[class]
    ...
    
    File [FileName2] -
    ...
    ```
   - Ejemplo:
      ```
      File 16472 -    
      Could 0-5 O    
      I 6-7 O    
      have 8-12 O    
      reflux 13-19 B-finding    
      ? 20-21 O    

      File 18659 -    
      I 0-1 O    
      also 2-6 O    
      have 7-11 O    
      a 12-13 O    
      temperature 14-25 O    
      and 26-29 O    
      my 30-32 O    
      throat 33-39 B-finding
      hurts 40-45 I-finding
      . 46-47 O
      ```
* output_conll: path al fichero conll con los datos aumentados (mismo formato que el input_conll)
* language: lenguaje del corpus a aumentar ("spanish" o "english")

 ---
 
 ### Recursos (resources.json):
 
 Contiene los recursos del idioma del corpus a aumentar (solo se han añadido inglés y español)
 
 * stopswords: Las stopwords del idioma que NO se desean reemplazar ni insertar.
 * characters: Los caracteres que contienen las palabras del idioma.
 * abbreviation: Abreviación del nombre del idioma en wordnet (3 letras).
