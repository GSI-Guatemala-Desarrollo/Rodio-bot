import logging
import time
import sys
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from constantes import (
    CHROMEDRIVER_PATH,
    BRAVE_BINARY_PATH,
)

from modulos_harmony.harmony_modulo_introd_comprobantes import (
    harmony_introd_comprobantes_agregar_factura,
    harmony_introd_comprobantes_anexar_documento_y_comentario,
    harmony_introd_comprobantes_copiar_documento,
    harmony_introd_comprobantes_descripcion_e_iva,
    harmony_introd_comprobantes_guardar,
    harmony_introd_comprobantes_pagos_y_retencion,
    )
from modulos_harmony.harmony_modulo_recepciones import harmony_recepciones_agregar_valor_y_busqueda_oc, harmony_recepciones_guardar
from modulos_sat.sat_login import sat_dirigir_a_pagina_y_verificar_estado_login
from modulos_sat.sat_navegar_a_modulo import sat_navegar_por_busqueda
from modulos_sat.sat_modulo_emision_constancias_de_retencion import (
    sat_emision_constancias_de_retencion_busqueda_parametros,
    sat_emision_constancias_de_retencion_generar_retencion_y_cambiar_directorio_pdf,
    sat_pdf_imprimir_factura,
    )
from modulos_sat.sat_modulo_categoria_de_rentas import (
    sat_categoria_de_rentas_busqueda_parametros,
    sat_categoria_de_rentas_buscar_en_tabla, 
    sat_categoria_de_rentas_asignar_categoria_y_regimen
    )

from modulos_harmony.harmony_login import harmony_dirigir_a_pagina_y_verificar_estado_login
from modulos_harmony.harmony_navegar_a_modulo import harmony_navegar_a_modulo

from modulos_cami.cami_login import cami_dirigir_a_pagina_y_verificar_estado_login
from modulos_cami.cami_navegar_a_modulo import cami_navegar_a_modulo



# -x-x-x- INICIO CONFIGURACIÓN -x-x-x-

#          -x-x- FLUJOS -x-x-


# Flujo Ordenes de compra: Harmony
def recepcion_OC (
    # Valores Harmony
    driver,
    h_recepciones_uni_po,
    h_recepciones_id_oc,
    
    h_recepciones_comentario
    
):
    # --------------------- Caso 1 - Funciones Harmony ---------------------
    # Paso 1
    harmony_dirigir_a_pagina_y_verificar_estado_login(driver)
    # Paso 2
    harmony_navegar_a_modulo(driver, indices=(7, 2, 3))
    # Pasos (a)-(d)
    harmony_recepciones_agregar_valor_y_busqueda_oc(driver, h_recepciones_uni_po, h_recepciones_id_oc)
    # Paso (e)
    # harmony_recepciones_guardar(driver, h_recepciones_comentario)

# Flujo Caso 1: SAT-Harmony-CAMI
def caso_1_reten_IVA_GEN (     
    # Valores SAT            
    driver,
    s_emision_constancias_emision_del,
    s_emision_constancias_emision_al,
    s_emision_constancias_retenciones_que_declara_iva,
    s_emision_constancias_regimen_gen,
    s_emision_constancias_tipo_documento,
    s_emision_constancias_nit_retenido,
    s_emision_constancias_no_autorizacion_fel,
    s_emision_constancias_serie_de_factura,
    s_emision_constancias_no_de_factura, 
    s_emision_constancias_directorio_descargas,
    s_emision_constancias_directorio_facturas_iva,
    s_emision_constancias_nombre_proveedor,
    s_emision_constancias_fecha_factura,
    
    # Valores Harmony
    h_introd_comprobantes_id_proveedor,
    h_introd_comprobantes_no_de_factura,
    h_introd_comprobantes_fecha_factura,
    
    h_introd_comprobantes_uni_po,
    h_introd_comprobantes_no_pedido,
    h_introd_comprobantes_iva,
    h_introd_comprobantes_no_serie,
    
    h_introd_comprobantes_pdf_path,
    h_introd_comprobantes_nombre_pdf,
    h_introd_comprobantes_nombre_proveedor,
    h_introd_comprobantes_comentario,
    
    h_introd_comprobantes_lista_porcentaje_retencion,
    h_introd_comprobantes_lista_impt_base_retencion_sust,
    
    h_introd_comprobantes_lista_descripciones,
    h_introd_comprobantes_lista_iva,
    # Valores Cami
    cami_nombre_empresa
    ):
    
    """
# --------------------- Caso 1 - Funciones SAT ---------------------
    # Pasos 1-3
    sat_dirigir_a_pagina_y_verificar_estado_login(driver)
    # Pasos 4-7
    sat_navegar_por_busqueda(driver, "Emision constancias de retencion")
    # Pasos 8-10
    sat_emision_constancias_de_retencion_busqueda_parametros(driver, s_emision_constancias_emision_del, s_emision_constancias_emision_al, s_emision_constancias_retenciones_que_declara_iva, s_emision_constancias_regimen_gen, s_emision_constancias_tipo_documento, s_emision_constancias_nit_retenido, s_emision_constancias_no_autorizacion_fel, s_emision_constancias_serie_de_factura, s_emision_constancias_no_de_factura)
    # Pasos 11-18 (Sin impresión)
    sat_emision_constancias_de_retencion_generar_retencion_y_cambiar_directorio_pdf(driver, s_emision_constancias_directorio_descargas, s_emision_constancias_directorio_facturas_iva, s_emision_constancias_nombre_proveedor, s_emision_constancias_no_de_factura, s_emision_constancias_fecha_factura)
    """
    
# --------------------- Caso 1 - Funciones Harmony ---------------------
    # Paso 1
    harmony_dirigir_a_pagina_y_verificar_estado_login(driver)
    # Paso 1
    harmony_navegar_a_modulo(driver, indices=(13, 1, 1, 1))
    # Paso 2
    harmony_introd_comprobantes_agregar_factura(driver, h_introd_comprobantes_id_proveedor, h_introd_comprobantes_no_de_factura, h_introd_comprobantes_fecha_factura)
    # Pasos 3-6
    harmony_introd_comprobantes_copiar_documento(driver, h_introd_comprobantes_uni_po, h_introd_comprobantes_no_pedido, h_introd_comprobantes_iva, h_introd_comprobantes_no_de_factura, h_introd_comprobantes_no_serie)
    # Pasos 7-8
    harmony_introd_comprobantes_anexar_documento_y_comentario(driver, h_introd_comprobantes_pdf_path, h_introd_comprobantes_nombre_pdf, h_introd_comprobantes_no_de_factura, h_introd_comprobantes_nombre_proveedor, h_introd_comprobantes_comentario)
    # Pasos 9-10
    harmony_introd_comprobantes_pagos_y_retencion(driver, h_introd_comprobantes_fecha_factura, h_introd_comprobantes_lista_impt_base_retencion_sust, h_introd_comprobantes_lista_porcentaje_retencion)
    # Pasos 11-12
    harmony_introd_comprobantes_descripcion_e_iva(driver, h_introd_comprobantes_lista_descripciones, h_introd_comprobantes_lista_iva)
    # Paso 13
    # harmony_introd_comprobantes_guardar(driver) # Comentar la llamada a esta funcion en caso de pruebas para que no realice los cambios en harmony.


# --------------------- Caso 1 - Funciones Cami ---------------------
    # Pasos
    cami_dirigir_a_pagina_y_verificar_estado_login(driver, cami_nombre_empresa)
    # Pasos
    cami_navegar_a_modulo(driver, "Relaciones Comerciales")


# Flujo Caso 2: SAT-Harmony-CAMI
def caso_2_reten_IVA_e_ISR (
    driver,
    # Variables pasos 1-18
    s_emision_constancias_emision_del,
    s_emision_constancias_emision_al,
    s_emision_constancias_retenciones_que_declara_iva,
    s_emision_constancias_regimen_gen,
    s_emision_constancias_tipo_documento,
    s_emision_constancias_nit_retenido,
    s_emision_constancias_no_autorizacion_fel,
    s_emision_constancias_serie_de_factura,
    s_emision_constancias_no_de_factura, 
    s_emision_constancias_directorio_descargas,
    s_emision_constancias_directorio_facturas_iva,
    s_emision_constancias_nombre_proveedor,
    s_emision_constancias_fecha_factura,
    
    # Variables pasos 19-29
    categoria_de_rentas_nit_retenido,
    categoria_de_rentas_periodo_del,
    categoria_de_rentas_periodo_al,
    categoria_de_rentas_estado_de_asignacion,
    categoria_de_rentas_no_de_factura,
    categoria_de_rentas_opcion_categoria_de_renta,
    categoria_de_rentas_opcion_regimen,
    
    # Variables pasos 30-...
    s_emision_constancias_retenciones_que_declara_isr,
    s_emision_constancias_directorio_facturas_isr,
    
    # Valores Harmony
    h_introd_comprobantes_id_proveedor,
    h_introd_comprobantes_no_de_factura,
    h_introd_comprobantes_fecha_factura,
    
    h_introd_comprobantes_uni_po,
    h_introd_comprobantes_no_pedido,
    h_introd_comprobantes_iva,
    h_introd_comprobantes_no_serie,
    
    h_introd_comprobantes_pdf_path,
    h_introd_comprobantes_nombre_pdf,
    h_introd_comprobantes_nombre_proveedor,
    h_introd_comprobantes_comentario,
    
    h_introd_comprobantes_lista_porcentaje_retencion,
    h_introd_comprobantes_lista_impt_base_retencion_sust,
    
    h_introd_comprobantes_lista_descripciones,
    h_introd_comprobantes_lista_iva,
    
    # Valores Cami
    cami_nombre_empresa
    ):
    
# --------------------- Caso 2 - Funciones SAT ---------------------
    # Pasos 1-3
    sat_dirigir_a_pagina_y_verificar_estado_login(driver)
    # Pasos 4-7
    sat_navegar_por_busqueda(driver, "Emision constancias de retencion")
    # Pasos 8-10
    sat_emision_constancias_de_retencion_busqueda_parametros(driver, s_emision_constancias_emision_del, s_emision_constancias_emision_al, s_emision_constancias_retenciones_que_declara_iva, s_emision_constancias_regimen_gen, s_emision_constancias_tipo_documento, s_emision_constancias_nit_retenido, s_emision_constancias_no_autorizacion_fel, s_emision_constancias_serie_de_factura, s_emision_constancias_no_de_factura)
    # Pasos 11-18 (Sin impresión)
    sat_emision_constancias_de_retencion_generar_retencion_y_cambiar_directorio_pdf(driver, s_emision_constancias_directorio_descargas, s_emision_constancias_directorio_facturas_iva, s_emision_constancias_nombre_proveedor, s_emision_constancias_no_de_factura, s_emision_constancias_fecha_factura)


    # Pasos 19-22
    sat_navegar_por_busqueda(driver, "Categoría de Rentas")
    # Pasos 23-24
    sat_categoria_de_rentas_busqueda_parametros(driver, categoria_de_rentas_nit_retenido, categoria_de_rentas_periodo_del, categoria_de_rentas_periodo_al, categoria_de_rentas_estado_de_asignacion)
    # Pasos 25-26
    sat_categoria_de_rentas_buscar_en_tabla(driver, categoria_de_rentas_no_de_factura)
    # Pasos 27-29
    sat_categoria_de_rentas_asignar_categoria_y_regimen(driver, categoria_de_rentas_opcion_categoria_de_renta, categoria_de_rentas_opcion_regimen)


    # (se repiten pasos 1-18 con datos de ISR)
    # Pasos 30-33 (4-7)
    sat_navegar_por_busqueda(driver, "Emision constancias de retencion")
    # Paso 34 (8-10)
    sat_emision_constancias_de_retencion_busqueda_parametros(driver, s_emision_constancias_emision_del, s_emision_constancias_emision_al, s_emision_constancias_retenciones_que_declara_isr, s_emision_constancias_regimen_gen, s_emision_constancias_tipo_documento, s_emision_constancias_nit_retenido, s_emision_constancias_no_autorizacion_fel, s_emision_constancias_serie_de_factura, s_emision_constancias_no_de_factura)
    # Pasos 11-18 (Sin impresión)
    sat_emision_constancias_de_retencion_generar_retencion_y_cambiar_directorio_pdf(driver, s_emision_constancias_directorio_descargas, s_emision_constancias_directorio_facturas_isr, s_emision_constancias_nombre_proveedor, s_emision_constancias_no_de_factura, s_emision_constancias_fecha_factura)

# --------------------- Caso 2 - Funciones Harmony ---------------------
    # Paso 1
    harmony_dirigir_a_pagina_y_verificar_estado_login(driver)
    # Paso 1
    harmony_navegar_a_modulo(driver, indices=(13, 1, 1, 1))
    # Paso 2
    harmony_introd_comprobantes_agregar_factura(driver, h_introd_comprobantes_id_proveedor, h_introd_comprobantes_no_de_factura, h_introd_comprobantes_fecha_factura)
    # Pasos 3-6
    harmony_introd_comprobantes_copiar_documento(driver, h_introd_comprobantes_uni_po, h_introd_comprobantes_no_pedido, h_introd_comprobantes_iva, h_introd_comprobantes_no_de_factura, h_introd_comprobantes_no_serie)
    # Pasos 7-8
    harmony_introd_comprobantes_anexar_documento_y_comentario(driver, h_introd_comprobantes_pdf_path, h_introd_comprobantes_nombre_pdf, h_introd_comprobantes_no_de_factura, h_introd_comprobantes_nombre_proveedor, h_introd_comprobantes_comentario)
    # Pasos 9-10
    harmony_introd_comprobantes_pagos_y_retencion(driver, h_introd_comprobantes_fecha_factura, h_introd_comprobantes_lista_impt_base_retencion_sust, h_introd_comprobantes_lista_porcentaje_retencion)
    # Pasos 11-12
    harmony_introd_comprobantes_descripcion_e_iva(driver, h_introd_comprobantes_lista_descripciones, h_introd_comprobantes_lista_iva)
    # Paso 13
    # harmony_introd_comprobantes_guardar(driver) # Comentar la llamada a esta funcion en caso de pruebas para que no realice los cambios en harmony.


    
# --------------------- Caso 2 - Funciones Cami ---------------------
    # Pasos
    cami_dirigir_a_pagina_y_verificar_estado_login(driver, cami_nombre_empresa)
    # Pasos
    cami_navegar_a_modulo(driver, "Relaciones Comerciales")


# Flujo Caso 3: SAT-Harmony-CAMI
def caso_3_reten_IVA_PEQ (
    driver,
    s_emision_constancias_emision_del,
    s_emision_constancias_emision_al,
    s_emision_constancias_retenciones_que_declara_iva,
    s_emision_constancias_regimen_peq,
    s_emision_constancias_tipo_documento,
    s_emision_constancias_nit_retenido,
    s_emision_constancias_no_autorizacion_fel,
    s_emision_constancias_serie_de_factura,
    s_emision_constancias_no_de_factura, 
    s_emision_constancias_directorio_descargas,
    s_emision_constancias_directorio_facturas_iva,
    s_emision_constancias_nombre_proveedor,
    s_emision_constancias_fecha_factura,
    # Valores Harmony
    h_introd_comprobantes_id_proveedor,
    h_introd_comprobantes_no_de_factura,
    h_introd_comprobantes_fecha_factura,
    
    h_introd_comprobantes_uni_po,
    h_introd_comprobantes_no_pedido,
    h_introd_comprobantes_iva,
    h_introd_comprobantes_no_serie,
    
    h_introd_comprobantes_pdf_path,
    h_introd_comprobantes_nombre_pdf,
    h_introd_comprobantes_nombre_proveedor,
    h_introd_comprobantes_comentario,
    
    h_introd_comprobantes_lista_porcentaje_retencion,
    h_introd_comprobantes_lista_impt_base_retencion_sust,
    
    h_introd_comprobantes_lista_descripciones,
    h_introd_comprobantes_lista_iva,
    # Valores Cami
    cami_nombre_empresa
    ):
    
# --------------------- Caso 3 - Funciones SAT ---------------------
    # Pasos 1-3
    sat_dirigir_a_pagina_y_verificar_estado_login(driver)
    # Pasos 4-7
    sat_navegar_por_busqueda(driver, "Emision constancias de retencion")
    # Pasos 8-10 (Cambiar gen por peq en constantes antes de ejecutar caso 3 completo)
    sat_emision_constancias_de_retencion_busqueda_parametros(driver, s_emision_constancias_emision_del, s_emision_constancias_emision_al, s_emision_constancias_retenciones_que_declara_iva, s_emision_constancias_regimen_peq, s_emision_constancias_tipo_documento, s_emision_constancias_nit_retenido, s_emision_constancias_no_autorizacion_fel, s_emision_constancias_serie_de_factura, s_emision_constancias_no_de_factura)
    # Pasos 11-18
    sat_emision_constancias_de_retencion_generar_retencion_y_cambiar_directorio_pdf(driver, s_emision_constancias_directorio_descargas, s_emision_constancias_directorio_facturas_iva, s_emision_constancias_nombre_proveedor, s_emision_constancias_no_de_factura, s_emision_constancias_fecha_factura)

# --------------------- Caso 3 - Funciones Harmony ---------------------
    # Paso 1
    harmony_dirigir_a_pagina_y_verificar_estado_login(driver)
    # Paso 1
    harmony_navegar_a_modulo(driver, indices=(13, 1, 1, 1))
    # Paso 2
    harmony_introd_comprobantes_agregar_factura(driver, h_introd_comprobantes_id_proveedor, h_introd_comprobantes_no_de_factura, h_introd_comprobantes_fecha_factura)
    # Pasos 3-6
    suma_total_iva = () # Paso exclusivo del caso 3, recibe el total de la factura y lo guarda en el primer indice de una lista para la funcion "harmony_introd_comprobantes_pagos_y_retencion"
    suma_total_iva.insert(0, harmony_introd_comprobantes_copiar_documento(driver, h_introd_comprobantes_uni_po, h_introd_comprobantes_no_pedido, h_introd_comprobantes_iva, h_introd_comprobantes_no_de_factura, h_introd_comprobantes_no_serie))
    # Pasos 7-8
    harmony_introd_comprobantes_anexar_documento_y_comentario(driver, h_introd_comprobantes_pdf_path, h_introd_comprobantes_nombre_pdf, h_introd_comprobantes_no_de_factura, h_introd_comprobantes_nombre_proveedor, h_introd_comprobantes_comentario)
    # Pasos 9-10
    # Se utiliza "suma_total_iva" en lugar de "h_introd_comprobantes_lista_impt_base_retencion_sust"
    harmony_introd_comprobantes_pagos_y_retencion(driver, h_introd_comprobantes_fecha_factura, suma_total_iva, h_introd_comprobantes_lista_porcentaje_retencion)
    # Pasos 11-12
    harmony_introd_comprobantes_descripcion_e_iva(driver, h_introd_comprobantes_lista_descripciones, h_introd_comprobantes_lista_iva)
    # Paso 13
    # harmony_introd_comprobantes_guardar(driver) # Comentar la llamada a esta funcion en caso de pruebas para que no realice los cambios en harmony.

    
# --------------------- Caso 3 - Funciones Cami ---------------------
    # Pasos
    cami_dirigir_a_pagina_y_verificar_estado_login(driver, cami_nombre_empresa)
    # Pasos
    cami_navegar_a_modulo(driver, "Relaciones Comerciales")




#          -x-x- CONFIGURACIONES ADICIONALES -x-x-

class CriticalHandler(logging.Handler):
    """Detiene la ejecución al detectar un log CRITICAL para que el bot no pueda continuar (p. e. cuando la factura no existe o no logró iniciar sesión)."""

    def __init__(self, driver=None):
        super().__init__()
        self.driver = driver

    def emit(self, record):
        if record.levelno == logging.CRITICAL:
            print("Se detectó un error crítico. Cerrando el navegador...")
            if self.driver:
                try:
                    self.driver.close()
                    self.driver.quit()
                    print("Navegador cerrado correctamente.")
                except Exception as e:
                    print(f"Error al cerrar el navegador: {e}")
            else:
                print("Driver no disponible. Intenta verificar el flujo.")
            sys.exit(1)

def configurar_logging(driver=None):
    """
    Configura el logging para registrar mensajes en terminal y archivo.
    Crea un archivo de log único por ejecución con un nombre basado en la fecha y hora.
    Los logs se guardan en la carpeta 'logs' en la raíz del proyecto.
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Formato del log
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Crear la carpeta 'logs' si no existe
    logs_directory = "logs"
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    # Generar nombre único para el archivo de log basado en fecha y hora
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    log_filename = os.path.join(logs_directory, f"log_RPA_{timestamp}.log")

    # Manejador para archivo
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Manejador para terminal
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    # Limpiar manejadores existentes (evitar duplicados)
    if logger.hasHandlers():
        logger.handlers.clear()

    # Agregar manejadores
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # Agregar manejador personalizado para errores críticos
    if driver is not None:
        critical_handler = CriticalHandler(driver)
        logger.addHandler(critical_handler)

def configurar_driver():
    """
    Configura el driver de Selenium para Brave y lo inicializa sin cargar una URL.
    Returns:
        driver: WebDriver configurado.
    """
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-gpu")

    # Evitar problemas de sandbox en contenedores
    options.add_argument("--no-sandbox")

    # Limitar logs
    options.add_argument("--log-level=3")

    # Aumentar memoria compartida en Docker u otras VMs
    options.add_argument("--disable-dev-shm-usage")

    options.binary_location = BRAVE_BINARY_PATH
    options.add_argument("--start-maximized")  # Pantalla completa
    service = Service(CHROMEDRIVER_PATH)

    try:
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("Navegador inicializado correctamente.")
        time.sleep(2)
        return driver
    except Exception as e:
        logging.error(f"Error al inicializar el navegador: {e}")
        raise  # Re-lanza el error para obtener trazas completas si es necesario.
