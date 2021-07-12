# PREPROCESADO-LEYES

Este repositorio contiene los archivos necesarios para:
- [Creación de Corpus de Leyes](#creación-de-corpus)
- [Preprocesado de Leyes](#preprocesado-de-leyes)
- [Tratamiento con TF](#tratamiento-con-tf)
- [Tratamiento con TF Normalizado](#tratamiento-con-tf-normalizado)

* * *

### Creación de Corpus ###

El archivo `CorpusCreatorJSON.py` genera el Corpus de Leyes en archivos JSON, uno para cada proyecto de ley.

### Preprocesado de Leyes ###

El archivo `BagOfWordsJSON.py` genera un archivo JSON con un arreglo de términos preprocesados para cada proyecto de ley.

### Tratamiento con TF ###

El archivo `BagOfWordsJSON.py` genera:
- Excel de leyes * words, con el ponderado (TF).
- Excel del ponderado ordenado de las words. 
- Archivo .jpg de la nube de palabras basados en TF.

### Tratamiento con TF Normalizado###

El archivo `BagOfWordsTF.py` genera:
- Excel de leyes * words, con el ponderado (TF Normalizado).
- Excel del ponderado ordenado de las words. 
- Archivo .jpg de la nube de palabras basados en TF Normalizado.
