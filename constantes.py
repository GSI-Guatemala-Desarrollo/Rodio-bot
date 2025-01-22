import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()
NUMERO_CASO = "TEST"

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


# -x- modulo_emision_constancias_de_retencion.py (Facturas) -x-

S_EMISION_CONSTANCIAS_EMISION_DEL = "" # Opcional
S_EMISION_CONSTANCIAS_EMISION_AL = "" # Opcional
S_EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_IVA = 1
S_EMISION_CONSTANCIAS_REGIMEN_GEN = 1
S_EMISION_CONSTANCIAS_TIPO_DOCUMENTO = 1
S_EMISION_CONSTANCIAS_NIT_RETENIDO = ""
S_EMISION_CONSTANCIAS_NO_AUTORIZACION_FEL = "" # Opcional
S_EMISION_CONSTANCIAS_SERIE_DE_FACTURA = "" # Opcional
S_EMISION_CONSTANCIAS_NO_DE_FACTURA = ""
S_EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS = r"C:\Users\ads_edgar.menendez\Downloads"
S_EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_IVA = r"C:\Users\ads_edgar.menendez\Desktop\docs\constancia_iva" # Constancia IVA
S_EMISION_CONSTANCIAS_NOMBRE_PROVEEDOR = "JORGE AUGUSTO, RODRIGUEZ GONZALEZ"
S_EMISION_CONSTANCIAS_FECHA_FACTURA = "14/01/2025" # Formato español: dd/mm/yyyy

# Datos de prueba que cambian luego para el caso 2, despúes de terminar la asignación de categoría se vuelve a generar la retención pero del ISR en lugar del IVA.
S_EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_ISR = 2
S_EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_ISR = r"C:\Users\ads_edgar.menendez\Desktop\docs\constancia_isr" # Constancia ISR

# Datos de prueba que cambian luego para el caso 3 (pequeño contribuyente).
S_EMISION_CONSTANCIAS_REGIMEN_PEQ = 2


# -x- modulo_categoria_de_rentas.py (ISR) -x-

S_CATEGORIA_DE_RENTAS_PERIODO_DEL = "" # Opcional
S_CATEGORIA_DE_RENTAS_PERIODO_AL = "" # Opcional
S_CATEGORIA_DE_RENTAS_NIT_RETENIDO = "17047455"
S_CATEGORIA_DE_RENTAS_ESTADO_DE_ASIGNACION = 1
S_CATEGORIA_DE_RENTAS_NO_DE_FACTURA = "2076264085"
S_CATEGORIA_DE_RENTAS_OPCION_CATEGORIA_DE_RENTA = 1
S_CATEGORIA_DE_RENTAS_OPCION_REGIMEN = 9

# opciones de S_CATEGORIA_DE_RENTAS_OPCION_CATEGORIA_DE_RENTA, colocar en la variable el numero correspondiente.
"""
1. RÉGIMEN OPCIONAL SIMPLIFICADO SOBRE INGRESOS DE ACTIVIDADES LUCRATIVAS  
2. RENTAS DE CAPITAL INMOBILIARIO  
3. RENTAS DE CAPITAL MOBILIARIO  
"""

# opciones de CATEGORIA_DE_RENTAS_OPCION_REGIMEN, colocar en la variable el numero correspondiente.
"""
1. RÉGIMEN OPCIONAL SIMPLIFICADO SOBRE INGRESOS DE ACTIVIDADES LUCRATIVAS 
    1. Compras o Servicios Gravados, adquiridos de Entidades Exentas
    2. Materias Primas
    3. Productos Terminados
    4. Transporte de carga y de personas dentro o fuera del territorio
    5. Telecomunicaciones
    6. Servicios Bancarios, Seguros y Financieros
    7. Servicios Informáticos
    8. Suministro de Energía Eléctrica y Agua
    9. Servicios Técnicos
    10. Arrendamiento y Subarrendamiento de Bienes Muebles
    11. Arrendamiento y Subarrendamiento de Bienes Inmuebles
    12. Servicios Profesionales
    13. Dietas a asistentes eventuales a consejos y otros órganos directivos
    14. Espectáculos Públicos, Culturales y Deportivos
    15. Subsidios Públicos
    16. Subsidios Privados
    17. Otros Bienes y/o Servicios
    18. Películas Cinematográficas, TV y similares
    19. Dietas
    20. Otras Remuneraciones (Viáticos no comprobables, comisiones, Gastos de Representación


2. RENTAS DE CAPITAL INMOBILIARIO  
    1. Arrendamiento y Subarrendamientos de Bienes Inmuebles  
    2. Constitución Cesión de Derechos o Facultades de Uso o Goce de Bienes Inmuebles


3. RENTAS DE CAPITAL MOBILIARIO 
    1. Intereses y Rentas de Dinero o en Especie Provenientes de Créditos de Cualquier Naturaleza
    2. Arrendamiento y Subarrendamientos de Bienes Muebles
    3. Constitución o Cesión de derechos, facultades de uso o goce de bienes tangibles
    4. Constitución o Cesión de derechos, facultades de uso o goce de bienes intangibles
    5. Rentas derivadas de contratos de seguros
    6. Rentas Vitalicias o temporales originadas de inversión de capital
    7. Rentas Originadas en donaciones condicionadas
    8. Distribución de dividendos, ganancias y utilidades
"""





# -x-x-x- DATOS HARMONY -x-x-x-

# Variables de entorno
HARMONY_USER_EMAIL = os.getenv("HARMONY_USER", "")
HARMONY_USER_PASSWORD = os.getenv("HARMONY_PASSWORD", "")

# URL de la APP (aqui se cambia de test a app si es necesario)
HARMONY_URL = "https://dailyprd.soletanchefreyssinet.net/psp/DAILYPRD/?&cmd=login&languageCd=ESP&"


# -x- harmony_modulo_recepciones.py (Recepción OC) -x-

H_RECEPCIONES_UNI_PO = "23796"
H_RECEPCIONES_ID_OC = "7962407338"


# -x- harmony_modulo_introd_comprobantes.py (Facturas) -x-
H_INTROD_COMPROBANTES_ID_PROVEEDOR = "0000000114"
H_INTROD_COMPROBANTES_NO_DE_FACTURA = "2076264085"
H_INTROD_COMPROBANTES_FECHA_FACTURA = "01/14/2025" # Formato ingles: mm/dd/yyyy

H_INTROD_COMPROBANTES_UNI_PO = "23796"
H_INTROD_COMPROBANTES_NO_PEDIDO = "7962407338"
H_INTROD_COMPROBANTES_IVA = 15
H_INTROD_COMPROBANTES_NO_DE_SERIE = "F48E8E98"


H_INTROD_COMPROBANTES_PDF_PATH = (
    r"C:\Users\ads_edgar.menendez\Desktop\docs\comprobante",
    r"C:\Users\ads_edgar.menendez\Desktop\docs\facturas",
    r"C:\Users\ads_edgar.menendez\Desktop\docs\oc",
    r"C:\Users\ads_edgar.menendez\Desktop\docs\constancia_iva",
    r"C:\Users\ads_edgar.menendez\Desktop\docs\constancia_isr", # Esta linea solo se utiliza en el caso 2.
    )

H_INTROD_COMPROBANTES_NOMBRE_PDF = (
    "comprobante test.pdf",
    "factura test.pdf",
    "oc test.pdf",
    "f-2076264085 JORGE AUGUSTO, RODRIGUEZ GONZALEZ.pdf",
    )

H_INTROD_COMPROBANTES_NOMBRE_PROVEEDOR = "JORGE AUGUSTO, RODRIGUEZ GONZALEZ"
H_INTROD_COMPROBANTES_COMENTARIO = "Comentario"

# Dato exclusivo del caso 2, usan la misma funcion pero se pasa la lista vacía en los casos 1 y 3.
H_INTROD_COMPROBANTES_LISTA_IMPT_BASE_RETENCION_SUST_CASO_1y3 = ("")

# en caso 1 y 3, cada línea de la OC es un dato en cada lista (IVA)
# en caso 2, cada línea de la OC son dos datos en cada lista (IVA e ISR)
H_INTROD_COMPROBANTES_LISTA_IMPT_BASE_RETENCION_SUST_CASO_2 = ("1111", "2222")
H_INTROD_COMPROBANTES_LISTA_PORCENTAJE_RETENCION = ("TVA15", "GT050")

# en estas listas siempre es un dato por línea sin importar el caso.
H_INTROD_COMPROBANTES_LISTA_DESCRIPCIONES = ("Desc 1")
H_INTROD_COMPROBANTES_LISTA_IVA = ("15.00")



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