################################################## IMPORTACIONES #######################################################
import os

import json

# LIBRERIA PARA STOPWORDS Y TOKENIZER
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# LIBRERIA PARA ANALISIS LE LENGUAJE NATURAL DESARROLLADA CON REDES NEURONALES
import stanza

# INSTALANDO DEPENDENCIAS PARA PODER OPERAR CON EL LENGUAJE ESPAÑOL
stanza.download('es', package='ancora', processors='tokenize,mwt,pos,lemma', verbose=True)
stNLP = stanza.Pipeline(processors='tokenize,mwt,pos,lemma', lang='es', use_gpu=True)

############################################### FUNCIONES ADICIONALES ##################################################

# FUNCION QUE AYUDA A PREVENIR LA MALA IDENTIFICACION DEL PESO, CON EL 'TITULO' Y 'OBJETO DE LEY'
def UnirVariables(array1, array2):
    array=[]
    for word in array2:
        if (i not in array1):
            array.append(word)
    return array

################################################# LIMPIEZA DE RUIDO ####################################################

def Lematizar(word):
    # LEMATIZAMOS EL PARAMETRO (PALABRA)
    doc = stNLP(word)
    # RECUPERAMOS EL LEMA DEL WORD
    aux = doc.sentences[0].words[0]
    return (aux.lemma)

def Preproccessing_Personalizado(filtered):

    important_word = ["ley", "legislativo", "supremo", "urgencia"]
    final = []
    controlador = False
    word = ""
    # ARREGLO PERSONALIZADO LEYES
    for i in range(0, len(filtered)):
        if controlador == False:
            if (filtered[i] in important_word):
                if (filtered[i] == "legislativo" or filtered[i] == "supremo" or "urgencia"):
                    if (filtered[i - 1] == "resolución"):
                        word = "resolución legislativa"
                    if (filtered[i - 1] == "decreto"):
                        word = "decreto " + filtered[i]
                    else:
                        word = filtered[i]
                controlador = True
            else:
                final.append(filtered[i])

        else:
            if (any(chr.isdigit() for chr in filtered[i])):
                new_word = word + "(" + filtered[i] + ")"
                final.append(new_word)
                final.append(new_word)
                final.append(new_word)
                controlador = False
            else:
                controlador = False
    return final

def Preprocessing(texto):
    # TOKENIZAMOS EL TEXTO
    word_tokens = word_tokenize(texto)

    # RECUPERAMOS LOS STOP_WORDS DE LA LIBRERIA NLTK.CORPUS
    stop_words = set(stopwords.words('spanish'))

    # NUESTROS STOPWORDS
    our_stopwords = {"propone", "así","uso","u","art","numeral","general","regl","prov","núm","mediante",
                     "comision", "titulo","pasa","artítulo","artitulo","oficio","pleno","texto","aras",
                     "aquella", "tiene", "expresamente", "pequeña","ser","y/o","cada","parte", "lay",
                     "nacional","interés","interes","público","publico","constitución", "declarar","necesidad",
                     "perú","proceso","disposición","forma","año","bien","mínimo","mínimo","alto","artículo","articulo",
                     "provincia","región", "objeto", "nuevo","permitir","vida","centro","función","funcion",
                     "objeto","medida","caso","peruano","departamento","san","ubicado","regional","nivel","marco",
                     "actividad","país","día","inciso","valor","plazo","red","básico","literal","libre","medio","dentro",
                     "santo","código","vía","río","recurso","villa","miembro","área","primero","segundo","tercero",
                     "zona","distrito","pago","crisis","fin","post"}

    # UNIMOS LOS STOPWORDS DE LA LIBRERIA CON NUESTROS STOPWORDS
    stop_words = stop_words.union(our_stopwords)

    # FILTRAMOS EL ARREGLO TOKENIZADO
    filtered = []
    for i in range(1, len(word_tokens)):
        # CONVERTIMOS A MINUSCULA
        word_tokens[i] = word_tokens[i].lower()

        # ELIMINAMOS NÚMEROS
        # word_tokens[i] = re.sub("\d+", ' ',word_tokens[i])

        # ELIMINAMOS SIGNOS DE PUNTUACION
        signos = ["?", "¿", "¡", "!", " ", ",", ".", ";", ":"]
        if (word_tokens[i] in signos): word_tokens[i] = ' '

        # ELIMINAMOS ESPACIOS
        word_tokens[i] = re.sub('\s+', ' ',word_tokens[i])

        # VALIDAMOS QUE SEAN DIFERENTES A VACIO POR LA FUNCION R.SUB
        if ( word_tokens[i] != ' ' ):
            # ELIMINAMOS LOS STOPWORDS
            if ( word_tokens[i] not in stop_words):

                # REALIZAMOS LA LEMATIZACION
                word_tokens[i] = Lematizar(word_tokens[i])
                if (word_tokens[i] not in stop_words):

                    # VALIDAMOS QUE SEAN MAYORES A UNO YA QUE SE NOMBRAN ARTICULOS '4-A, 4-B'
                    if (len(str (word_tokens[i]))>2):
                        # AGREGAMOS AL VECTOR FINAL PREPROCESADO
                        filtered.append(word_tokens[i])

    # PREPROCESADO PERSONALIZADO (PARA VISUALIZAR LEYES MODIFICADAS)
    final_filtered = Preproccessing_Personalizado(filtered)

    # RETORNAMOS EL ARREGLO PREPROCESADO
    return final_filtered


################################################## RECORRER JSONS ######################################################

# LISTAR DIRECTORIOS DE NUESTRO CORPUS
url_JSONs = os.listdir('./CORPUS-JSON')

#### CREAMOS EL JSON (LEY <==> ARREGLO DE PALABRAS PREPROCESADAS)
data1 = {}
data1['leyes'] = []

#DEFINIMOS PARAMETROS SUPERIOR Y INFERIOR, PARA LA EXTRACCION DE LEYES DEL CORPUS
inferior = 4849
superior = 6634

# RECORRER ARCHIVOS JSON RECUPERADOS DEL CORPUS
for i in range( inferior , superior ):
    url = str ('./CORPUS-JSON/' + url_JSONs[i])

    # ABRIR ARCHIVO JSON (TENER MUY EN CUENTA EL ENCODING)
    with open(url, encoding="utf-8") as file:
        data = json.load(file)

        # RECUPERAMOS ATRIBUTOS IMPORTANTES DEL JSON '(TITULO, OBJETO DEL PROYECTO)'
        for ley in data['proyectos_ley']:
            titulo = ley['titulo']
            objeto_proyecto = ley['objeto_del_proyecto']

            print(url)

            ### REALIZAMOS EL PREPROCESADO DE TITULO Y OBJETO DE LEY
            pre_titulo = Preprocessing( titulo )
            pre_objeto = Preprocessing( objeto_proyecto )

            # UNIR AMBOS PREPROCESADOS YA QUE EXISTEN TERMINOS QUE SE REPITEN EN TITULO Y OBJETO DEL PROYECTO
            preprocesado = UnirVariables( pre_titulo, pre_objeto )

            # AGREGAMOS AL ARCHIVO JSON (LEY <==> ARREGLO DE PALABRAS PREPROCESADAS)
            data1['leyes'].append({
                'ley': str(url_JSONs[i].replace(".json", "")),
                'words': preprocesado
            })

# GUARDAMOS EL JSON (LEY <==> ARREGLO DE PALABRAS PREPROCESADAS)
nombre_archivo = "./PREPROCESADO-LEYES/JSON/" + str(inferior) + "-" + str(superior) + ".json"
with open(nombre_archivo, 'w', encoding="utf-8") as file:
    json.dump(data1, file, indent=4, ensure_ascii=False)




