import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# -x-x-x- DATOS SAT -x-x-x-

# URL de la Agencia Virtual SAT
SAT_URL = "https://farm3.sat.gob.gt/menu/portada.jsf"

# Variables de entorno
SAT_USER_EMAIL = os.getenv("SAT_USER", "")
SAT_USER_PASSWORD = os.getenv("SAT_PASSWORD", "")

# Rutas y configuraciones del driver

# Linux
# CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
# BRAVE_BINARY_PATH = "/snap/brave/current/opt/brave.com/brave/brave-browser"

# Windows
CHROMEDRIVER_PATH = r"C:\Users\ads_edgar.menendez\Desktop\RPA\auto-SAT\drivers\chromedriver.exe"
BRAVE_BINARY_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"


# -x- modulo_emision_constancias_de_retencion.py -x-

EMISION_CONSTANCIAS_EMISION_DEL = "04/12/2024" # Opcional
EMISION_CONSTANCIAS_EMISION_AL = "20/12/2024" # Opcional
EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_IVA = 1
EMISION_CONSTANCIAS_REGIMEN_GEN = 1
EMISION_CONSTANCIAS_TIPO_DOCUMENTO = 1
EMISION_CONSTANCIAS_NIT_RETENIDO = "12345678"
EMISION_CONSTANCIAS_NO_AUTORIZACION_FEL = "" # Opcional
EMISION_CONSTANCIAS_SERIE_DE_FACTURA = "" # Opcional
EMISION_CONSTANCIAS_NO_DE_FACTURA = "1234567890"
EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS = "/home/diego/Downloads"
EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_IVA = "/home/diego/Documents"
EMISION_CONSTANCIAS_NOMBRE_PROVEEDOR = "Kevin"
EMISION_CONSTANCIAS_FECHA_FACTURA = "20/12/2024"

# Datos de prueba que cambian luego para el caso 2, despúes de terminar la asignación de categoría se vuelve a generar la retención pero del ISR en lugar del IVA.
EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_ISR = 2
EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_ISR = "/home/diego/Music"

# Datos de prueba que cambian luego para el caso 3 (pequeño contribuyente).
EMISION_CONSTANCIAS_REGIMEN_PEQ = 2

# Variables de impresión (función pendiente):
EMISION_CONSTANCIAS_NOMBRE_IMPRESORA = "RICOH_MP_C307_002673EBD502"
EMISION_CONSTANCIAS_CANTIDAD_COPIAS = 3



# -x- modulo_categoria_de_rentas.py -x-

CATEGORIA_DE_RENTAS_PERIODO_DEL = "03/12/2024" # Opcional
CATEGORIA_DE_RENTAS_PERIODO_AL = "19/12/2024" # Opcional
CATEGORIA_DE_RENTAS_NIT_RETENIDO = "12723770"
CATEGORIA_DE_RENTAS_ESTADO_DE_ASIGNACION = 1
CATEGORIA_DE_RENTAS_NO_DE_FACTURA = "1234567890"
CATEGORIA_DE_RENTAS_OPCION_CATEGORIA_DE_RENTA = 1
CATEGORIA_DE_RENTAS_OPCION_REGIMEN = 9

# opciones de CATEGORIA_DE_RENTAS_OPCION_REGIMEN, colocar en la variable el numero correspondiente.
"""
1.Compras o Servicios Gravados, adquiridos de Entidades Exentas
2.Materias Primas
3.Productos Terminados
4.Transporte de carga y de personas dentro o fuera del territorio
5.Telecomunicaciones
6.Servicios Bancarios, Seguros y Financieros
7.Servicios Informáticos
8.Suministro de Energía Eléctrica y Agua
9.Servicios Técnicos
10. Arrendamiento y Subarrendamiento de Bienes Muebles
11. Arrendamiento y Subarrendamiento de Bienes Inmuebles
12.Servicios Profesionales
13.Dietas a asistentes eventuales a consejos y otros órganos directivos
14.Espectáculos Públicos, Culturales y Deportivos
15.Subsidios Públicos
16.Subsidios Privados
17.Otros Bienes y/o Servicios
18.Películas Cinematográficas, TV y similares
19.Dietas
20.Otras Remuneraciones (Viáticos no comprobables, comisiones, Gastos de Representación
"""



# -x-x-x- DATOS HARMONY -x-x-x-

# Variables de entorno
HARMONY_USER_EMAIL = os.getenv("HARMONY_USER", "")
HARMONY_USER_PASSWORD = os.getenv("HARMONY_PASSWORD", "")

# URL de la APP (aqui se cambia de test a app si es necesario)
HARMONY_URL = "https://dailyprd.soletanchefreyssinet.net/psp/DAILYPRD/?&cmd=login&languageCd=ESP&"

# -x- harmony_modulo_introd_comprobantes.py -x-
H_INTROD_COMPROBANTES_ID_PROVEEDOR = "0000000246"
H_INTROD_COMPROBANTES_NO_DE_FACTURA = "1744130018"
H_INTROD_COMPROBANTES_FECHA_FACTURA = "04/11/2024"

H_INTROD_COMPROBANTES_UNI_PO = "23796"
H_INTROD_COMPROBANTES_NO_PEDIDO = "7962401726"
H_INTROD_COMPROBANTES_IVA = 12
H_INTROD_COMPROBANTES_NO_DE_SERIE = "16dcc25da"

H_INTROD_COMPROBANTES_PDF_PATH = r"C:\Users\ads_edgar.menendez\Desktop"
H_INTROD_COMPROBANTES_NOMBRE_PDF = "test 1.pdf"
H_INTROD_COMPROBANTES_NOMBRE_PROVEEDOR = "Nombre Proveedor"
H_INTROD_COMPROBANTES_COMENTARIO = "Comentario"

H_INTROD_COMPROBANTES_LISTA_PORCENTAJE_RETENCION = ("TVA15", "GT050", "TVA15", "GT070", "TVA15", "GT070")

H_INTROD_COMPROBANTES_LISTA_DESCRIPCIONES = ("Desc 1", "Desc 2", "Desc 3")
H_INTROD_COMPROBANTES_LISTA_IVA = ("12.00", "12.00", "12.00")
# -x-x-x- DATOS CAMI -x-x-x-

# Variables de entorno
CAMI_USER_EMAIL = os.getenv("CAMI_USER", "")
CAMI_USER_PASSWORD = os.getenv("CAMI_PASSWORD", "")

# URL de la APP (aqui se cambia de test a app si es necesario)
CAMI_URL = "https://test.camiapp.net/"

# Nombre de la empresa a la que se quiere ingresar después del login
CAMI_NOMBRE_EMPRESA = "QA Cami"


# -x- TRAB_INSERCION_DOCS -x-

INSERCION_TIPODOC = "SeleniumTest"

INSERCION_VALORES_POR_TIPO = {
    "text": "Texto",
    "number": "123",
    "phone": "+12345678901",
    "date": "12315678",
    "email": "test@example.com",
    "time": "12341",
    "select": "0",  # Valor del option que queremos seleccionar en una lista
}

# -x- TRAB_CONSULTA_DOCS -x-

CONSULTA_TIPODOC = "SeleniumTest"

CONSULTA_VALORES_POR_TIPO = {
    "text": "Texto",
    "number": "123",
    "phone": "+12345678901",
    "date": "12315678",
    "email": "test@example.com",
    "time": "12341",
    "select": "0",  # Valor del option que queremos seleccionar en una lista
}