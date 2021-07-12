import json
from selenium import webdriver

# EJECUTABLE QUE AYUDA A MANEJAR CHROME
driver = webdriver.Chrome('./chromedriver.exe')

def CrearJSON(href, text, proceso):
    # NAVEGAMOS POR LA PAGINA DE DETALLES DE LA LEY
    driver.get(href)

    # CREAMOS EL JSON
    data = {}

    # CLASE
    data['proyectos_ley'] = []

    # OBTENEMOS LAS FILAS DE LA TABLA EN UN ARREGLO
    tabla = driver.find_elements_by_xpath('//html/body/form/table/tbody/tr[2]/td/table/tbody/tr')

    # DATOS DEL ARCHIVO JSON
    numero = text
    proceso = proceso
    periodo_parlamentario = ""
    legislatura = ""
    fecha_presentacion = ""
    proponente = ""
    grupo_parlamentario_PartidoPolitico = []
    grupo_parlamentario_Congresistas = []
    titulo = ""
    objeto_del_proyecto = ""
    adherentes = []
    envio_a_comision = []
    proyectos_de_ley_agrupados = []

    # RECORREMOS LAS FILAS DE LAS TABLAS

    for tr in tabla:

        # MANEJAMOS UN TRY EXCEPT, POR SI RECIBIMOS UN ELEMENTO NO DESEADO
        try:
            title = tr.find_element_by_xpath('.//td[1]/b/font').text

            # COMPARAMOS LOS TITULOS, Y LOS ALMACENAMOS EN LAS VARIABLES

            if(title == "Período Parlamentario:"):
                periodo_parlamentario = tr.find_element_by_xpath('.//td[2]/font').text
            elif(title == "Legislatura:"):
                legislatura = tr.find_element_by_xpath('.//td[2]/font').text
            elif(title == "Fecha Presentación:"):
                fecha_presentacion = tr.find_element_by_xpath('.//td[2]/font').text
            elif(title == "Proponente:"):
                proponente = tr.find_element_by_xpath('.//td[2]/font').text

            elif(title == "Grupo Parlamentario:"):
                grupo_parlamentario_PartidoPolitico = str(tr.find_element_by_xpath('.//td/font').text).split(',')
                grupo_parlamentario_Congresistas = str(tr.find_element_by_xpath('.//td/p/font[1]').text).split(',')

            elif(title == "Título:"):
                titulo = tr.find_element_by_xpath('.//td/font').text
            elif(title == "Objeto del Proyecto de Ley:"):
                objeto_del_proyecto = tr.find_element_by_xpath('.//td/font').text

            elif(title == "Adherentes"):
                adherentes = str(tr.find_element_by_xpath('.//td/font').text).split(',')

            elif(title == "Envío a Comisión:"):
                envio_a_comision = str(tr.find_element_by_xpath('.//td/font').text).split('\n')

            elif(title == "Proyectos de Ley Agrupados:"):
                proyectos_de_ley_agrupados = str(tr.find_element_by_xpath('.//td[2]/font').text).split(',')
        except:
            pass


    # AGREGAMOS AL ARCHIVO JSON

    data['proyectos_ley'].append({
        'numero': numero,
        'proceso': proceso,
        'periodo_parlamentario': periodo_parlamentario,
        'legislatura': legislatura,
        'fecha_presentacion': fecha_presentacion,
        'proponente': proponente,
        'grupo_parlamentario_PartidoPolitico': grupo_parlamentario_PartidoPolitico,
        'grupo_parlamentario_Congresistas': grupo_parlamentario_Congresistas,
        'titulo': titulo,
        'objeto_del_proyecto': objeto_del_proyecto,
        'adherentes': adherentes,
        'envio_a_comision': envio_a_comision,
        'proyectos_de_ley_agrupados': proyectos_de_ley_agrupados
    })

    # CREAMOS EL ARCHIVO JSON CON EL CODIGO DE LA LEY
    archivo = "./CORPUS-JSON/"+str(numero).replace('/','-') + ".json"

    # ABRIMOS EL ARCHIVO JSON, Y LO MODIFICAMOS PARA QUE ACEPTE TILDES Y Ñ
    with open(archivo, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

#=====================================================================================================================#

url = 'https://www2.congreso.gob.pe/Sicr/TraDocEstProc/CLProLey2016.nsf/Local%20Por%20Numero%20Inverso?OpenView'

# NAVEGAREMOS HASTA UN ENLACE
driver.get(url)

# RECUPERAMOS LA TABLA CON LAS LEYES
select = driver.find_element_by_xpath('//html/body/form/table/tbody/tr/td/table[2]/tbody')

# RECUPERAMOS EL ENLACE A LA INFORMACION DE LA LEY
tr = select.find_elements_by_xpath('.//tr/td/font/a')

controlador = True

while controlador:

    driver.get(url)
    select = driver.find_element_by_xpath('//html/body/form/table/tbody/tr/td/table[2]/tbody')
    tr = select.find_elements_by_xpath('.//tr/td/font/a')

    for i in range(0, len(tr)):
        # RECUPERAMOS LA TABLA CON LAS LEYES, EL ENLACE A LA INFORMACION DE LA LEY
        select = driver.find_element_by_xpath('//html/body/form/table/tbody/tr/td/table[2]/tbody')
        tr = select.find_elements_by_xpath('.//tr/td/font/a')
        proceso = select.find_element_by_xpath('.//tr/td[5]/font').text


        # RECUPERAMOS LOS ATRIBUTOS HREF Y TEXTO (CODIGO)
        href = tr[i].get_attribute('href')
        text = tr[i].get_attribute('text')

        # CREAMOS EL ARCHIVO JSON
        CrearJSON(href, text, proceso)

        # NAVEGAREMOS AL ENLACE DE ORIGEN
        driver.get(url)

    # MANTENDREMOS LA URL ANTERIOR POR PRECAUCION YA QUE AL LLEGAR AL FINAL SE ORIGINA UN BUCLE INNECESARIO
    url_anterior = url

    # OBTENEMOS EL BOTON DE SIGUIENTE
    siguiente = driver.find_element_by_xpath('/html/body/form/table/tbody/tr/td/table[1]/tbody/tr/td[3]/a')

    # VAMOS A LA SIGUIENTE PAGINA DE TABLA DE LEYES
    siguiente.click()

    # OBETENEMOS EL NUEVO LINK PARA NAVEGAR EN ÉL
    url = driver.current_url

    # VERIFICAMOS SI EL BOTON DE SIGUIENTE NOS REGRESA A LA MISMA PAGINA
    if (url == url_anterior):
        controlador = False


