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

---

### Parámetros (eda_params.json):

* α - Porcentaje de parabras a cambiar por frase.
  * Cada una de las 4 técnicas tiene su propio α (alpha_sr, alpha_ri, alpha_rs, alpha_rd)
  * Para α = 0, esa técnica no se aplica
* n_aug - Número de frases nuevas a generar por frase original
* input_conll: path al fichero conll con los datos a aumentar
  - Formato:
    ```
    File [FileName] -
    [word] [InitOffset]-[EndOffset] [tag]-[class]
    ...
    
    File [FileName2] -
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

 
