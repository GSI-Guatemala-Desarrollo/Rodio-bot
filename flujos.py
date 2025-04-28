
# Imports configuracion
import logging
from configuracion_bot import configurar_driver, configurar_logging, finalizar_automatizacion

# Imports SAT
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

# Imports Harmony
from modulos_harmony.harmony_login import harmony_dirigir_a_pagina_y_verificar_estado_login
from modulos_harmony.harmony_navegar_a_modulo import harmony_navegar_a_modulo

from modulos_harmony.harmony_modulo_recepciones import harmony_recepciones_agregar_valor_y_busqueda_oc, harmony_recepciones_guardar

from modulos_harmony.harmony_modulo_introd_comprobantes import (
    harmony_introd_comprobantes_agregar_factura,
    harmony_introd_comprobantes_anexar_documento_y_comentario,
    harmony_introd_comprobantes_copiar_documento,
    harmony_introd_comprobantes_descripcion_e_iva,
    harmony_introd_comprobantes_guardar,
    harmony_introd_comprobantes_pagos_y_retencion,
    )

#          -x-x- FLUJOS -x-x-

# Flujo Ordenes de compra: Harmony
def recepcion_OC (
    numero_caso, # Usuario
    # Valores Harmony
    h_recepciones_uni_po,
    h_recepciones_id_oc, # Usuario
    
):

# --------------------- CONFIGURACIÓN LOGGING Y DRIVER ---------------------
    driver = configurar_driver()  # Configurar el driver primero
    configurar_logging(driver, numero_caso)  # Pasar el driver al CriticalHandler
    
    
# --------------------- Funciones Harmony ---------------------
    # Paso 1
    harmony_dirigir_a_pagina_y_verificar_estado_login(driver)
    # Paso 2
    harmony_navegar_a_modulo(driver, indices=(7, 2, 3))
    # Pasos (a)-(d)
    harmony_recepciones_agregar_valor_y_busqueda_oc(driver, h_recepciones_uni_po, h_recepciones_id_oc)
    # Paso (e)
    harmony_recepciones_guardar(driver)
    
    
# --------------------- Fin Automatización ---------------------
    finalizar_automatizacion(driver)


# Flujo Caso 1: SAT-Harmony-CAMI
def caso_1_reten_IVA_GEN (
    driver,
    numero_caso, # Usuario
    # Valores SAT            
    s_emision_constancias_emision_del,
    s_emision_constancias_emision_al,
    s_emision_constancias_retenciones_que_declara_iva,
    s_emision_constancias_regimen_gen,
    s_emision_constancias_tipo_documento,
    s_emision_constancias_nit_retenido, # Usuario
    s_emision_constancias_no_autorizacion_fel,
    s_emision_constancias_serie_de_factura, # Usuario
    s_emision_constancias_no_de_factura, # Usuario
    s_emision_constancias_directorio_descargas,
    s_emision_constancias_directorio_facturas_iva,
    s_emision_constancias_nombre_proveedor, # Usuario
    s_emision_constancias_fecha_factura, # Usuario
    
    # Valores Harmony
    h_introd_comprobantes_id_proveedor, # Usuario
    h_introd_comprobantes_no_de_factura, # Repetido
    h_introd_comprobantes_fecha_factura, # Repetido
    
    h_introd_comprobantes_uni_po,
    h_introd_comprobantes_no_pedido, # Usuario
    h_introd_comprobantes_iva, # Usuario
    h_introd_comprobantes_no_serie, # Repetido
    
    h_introd_comprobantes_pdf_path,
    h_introd_comprobantes_nombre_pdf, # Usuario (lista)
    h_introd_comprobantes_nombre_proveedor, # Repetido
    h_introd_comprobantes_comentario, # Usuario
    
    h_introd_comprobantes_lista_porcentaje_retencion, # Usuario (lista)
    h_introd_comprobantes_lista_impt_base_retencion_sust, # Usuario (lista)
    
    h_introd_comprobantes_lista_descripciones, # Usuario (lista)
    h_introd_comprobantes_lista_iva, # Usuario (lista)
    ):
    
    MAX_INTENTOS_LOGIN = 3
    intento_login = 0

    while intento_login < MAX_INTENTOS_LOGIN:
        intento_login += 1

# --------------------- CONFIGURACIÓN LOGGING Y DRIVER ---------------------
       #driver = configurar_driver() # Configurar el driver primero
        #configurar_logging(driver, numero_caso)  # Manejo de logs críticos con el driver actual
        logging.info(f"==== Intento de login #{intento_login} para SAT ====")

# --------------------- Caso 1 - Funciones SAT ---------------------
    
        try:
            # Pasos 1-3
            sat_dirigir_a_pagina_y_verificar_estado_login(driver)
            break
        except Exception as e:
            logging.warning(f"Error en intento de login #{intento_login}, la página no cargó a tiempo.")
            finalizar_automatizacion(driver)

            if intento_login == MAX_INTENTOS_LOGIN:
                logging.error("Se alcanzó el máximo de intentos de login. Abortando el flujo. Revise estado de la página SAT")
                return
    # Pasos 4-7
    sat_navegar_por_busqueda(driver, "Emision constancias de retencion")
    # Pasos 8-10
    sat_emision_constancias_de_retencion_busqueda_parametros(driver, s_emision_constancias_emision_del, s_emision_constancias_emision_al, s_emision_constancias_retenciones_que_declara_iva, s_emision_constancias_regimen_gen, s_emision_constancias_tipo_documento, s_emision_constancias_nit_retenido, s_emision_constancias_no_autorizacion_fel, s_emision_constancias_serie_de_factura, s_emision_constancias_no_de_factura)
    # Pasos 11-18 (Sin impresión)
    numero_retencion_iva = sat_emision_constancias_de_retencion_generar_retencion_y_cambiar_directorio_pdf(driver, s_emision_constancias_retenciones_que_declara_iva, s_emision_constancias_directorio_descargas, s_emision_constancias_directorio_facturas_iva, s_emision_constancias_nombre_proveedor, s_emision_constancias_no_de_factura, s_emision_constancias_fecha_factura)
    h_introd_comprobantes_nombre_pdf = h_introd_comprobantes_nombre_pdf + (numero_retencion_iva,)
    
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
    
# --------------------- Fin Automatización ---------------------
    if driver.service.process is not None:  # Solo cerrar si el proceso sigue activo
        finalizar_automatizacion(driver)


# Flujo Caso 2: SAT-Harmony-CAMI
def caso_2_reten_IVA_e_ISR (
    driver,
    numero_caso, # Usuario
    # Variables pasos 1-18
    s_emision_constancias_emision_del,
    s_emision_constancias_emision_al,
    s_emision_constancias_retenciones_que_declara_iva,
    s_emision_constancias_regimen_gen,
    s_emision_constancias_tipo_documento,
    s_emision_constancias_nit_retenido, # Usuario
    s_emision_constancias_no_autorizacion_fel,
    s_emision_constancias_serie_de_factura, # Usuario
    s_emision_constancias_no_de_factura, # Usuario
    s_emision_constancias_directorio_descargas,
    s_emision_constancias_directorio_facturas_iva,
    s_emision_constancias_nombre_proveedor, # Usuario
    s_emision_constancias_fecha_factura, # Usuario
    
    # Variables pasos 19-29
    categoria_de_rentas_nit_retenido, # Repetido
    categoria_de_rentas_periodo_del,
    categoria_de_rentas_periodo_al,
    categoria_de_rentas_estado_de_asignacion,
    categoria_de_rentas_no_de_factura, # Repetido
    categoria_de_rentas_opcion_categoria_de_renta, # Usuario
    categoria_de_rentas_opcion_regimen, # Usuario
    
    # Variables pasos 30-...
    s_emision_constancias_retenciones_que_declara_isr,
    s_emision_constancias_directorio_facturas_isr,
    
    # Valores Harmony
    h_introd_comprobantes_id_proveedor, # Usuario
    h_introd_comprobantes_no_de_factura, # Repetido
    h_introd_comprobantes_fecha_factura, # Repetido
    
    h_introd_comprobantes_uni_po,
    h_introd_comprobantes_no_pedido, # Usuario
    h_introd_comprobantes_iva, # Usuario
    h_introd_comprobantes_no_serie, # Repetido
    
    h_introd_comprobantes_pdf_path,
    h_introd_comprobantes_nombre_pdf, # Usuario (lista)
    h_introd_comprobantes_nombre_proveedor, # Repetido
    h_introd_comprobantes_comentario, # Usuario
    
    h_introd_comprobantes_lista_porcentaje_retencion, # Usuario (lista)
    h_introd_comprobantes_lista_impt_base_retencion_sust, # Usuario (lista)
    
    h_introd_comprobantes_lista_descripciones, # Usuario (lista)
    h_introd_comprobantes_lista_iva, # Usuario (lista)
    
    ):

    MAX_INTENTOS_LOGIN = 3
    intento_login = 0

    while intento_login < MAX_INTENTOS_LOGIN:
        intento_login += 1

# --------------------- CONFIGURACIÓN LOGGING Y DRIVER ---------------------
        #driver = configurar_driver() # Configurar el driver primero
        #configurar_logging(driver, numero_caso)  # Manejo de logs críticos con el driver actual
        logging.info(f"==== Intento de login #{intento_login} para SAT ====")

# --------------------- Caso 1 - Funciones SAT ---------------------
        try:
            # Pasos 1-3
            sat_dirigir_a_pagina_y_verificar_estado_login(driver)
            break
        except Exception as e:
            logging.warning(f"Error en intento de login #{intento_login}, la página no cargó a tiempo.")
            finalizar_automatizacion(driver)

            if intento_login == MAX_INTENTOS_LOGIN:
                logging.error("Se alcanzó el máximo de intentos de login. Abortando el flujo.")
                return
    # Pasos 4-7
    sat_navegar_por_busqueda(driver, "Emision constancias de retencion")
    # Pasos 8-10
    sat_emision_constancias_de_retencion_busqueda_parametros(driver, s_emision_constancias_emision_del, s_emision_constancias_emision_al, s_emision_constancias_retenciones_que_declara_iva, s_emision_constancias_regimen_gen, s_emision_constancias_tipo_documento, s_emision_constancias_nit_retenido, s_emision_constancias_no_autorizacion_fel, s_emision_constancias_serie_de_factura, s_emision_constancias_no_de_factura)
    # Pasos 11-18 (Sin impresión)
    numero_retencion_iva = sat_emision_constancias_de_retencion_generar_retencion_y_cambiar_directorio_pdf(driver, s_emision_constancias_retenciones_que_declara_iva, s_emision_constancias_directorio_descargas, s_emision_constancias_directorio_facturas_iva, s_emision_constancias_nombre_proveedor, s_emision_constancias_no_de_factura, s_emision_constancias_fecha_factura)
    h_introd_comprobantes_nombre_pdf = h_introd_comprobantes_nombre_pdf + (numero_retencion_iva,)


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
    numero_retencion_isr = sat_emision_constancias_de_retencion_generar_retencion_y_cambiar_directorio_pdf(driver, s_emision_constancias_retenciones_que_declara_isr, s_emision_constancias_directorio_descargas, s_emision_constancias_directorio_facturas_isr, s_emision_constancias_nombre_proveedor, s_emision_constancias_no_de_factura, s_emision_constancias_fecha_factura)
    h_introd_comprobantes_nombre_pdf = h_introd_comprobantes_nombre_pdf + (numero_retencion_isr,)

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

# --------------------- Fin Automatización ---------------------
    if driver.service.process is not None:  # Solo cerrar si el proceso sigue activo
        finalizar_automatizacion(driver)


# Flujo Caso 3: SAT-Harmony-CAMI
def caso_3_reten_IVA_PEQ (
    driver,
    numero_caso, # Usuario
    # Valores SAT
    s_emision_constancias_emision_del,
    s_emision_constancias_emision_al,
    s_emision_constancias_retenciones_que_declara_iva,
    s_emision_constancias_regimen_peq,
    s_emision_constancias_tipo_documento,
    s_emision_constancias_nit_retenido, # Usuario
    s_emision_constancias_no_autorizacion_fel,
    s_emision_constancias_serie_de_factura, # Usuario
    s_emision_constancias_no_de_factura, # Usuario
    s_emision_constancias_directorio_descargas,
    s_emision_constancias_directorio_facturas_iva,
    s_emision_constancias_nombre_proveedor, # Usuario
    s_emision_constancias_fecha_factura, # Usuario
    
    # Valores Harmony
    h_introd_comprobantes_id_proveedor, # Usuario
    h_introd_comprobantes_no_de_factura, # Repetido
    h_introd_comprobantes_fecha_factura, # Repetido
    
    h_introd_comprobantes_uni_po,
    h_introd_comprobantes_no_pedido, # Usuario
    h_introd_comprobantes_iva, # Usuario
    h_introd_comprobantes_no_serie, # Repetido
    
    h_introd_comprobantes_pdf_path,
    h_introd_comprobantes_nombre_pdf, # Usuario (lista)
    h_introd_comprobantes_nombre_proveedor, # Repetido
    h_introd_comprobantes_comentario, # Usuario
    
    h_introd_comprobantes_lista_porcentaje_retencion, # Usuario (lista)
    h_introd_comprobantes_lista_impt_base_retencion_sust, # Usuario (lista)
    
    h_introd_comprobantes_lista_descripciones, # Usuario (lista)
    h_introd_comprobantes_lista_iva, # Usuario (lista)
    
    ):

    MAX_INTENTOS_LOGIN = 3
    intento_login = 0

    while intento_login < MAX_INTENTOS_LOGIN:
        intento_login += 1

# --------------------- CONFIGURACIÓN LOGGING Y DRIVER ---------------------
        #driver = configurar_driver() # Configurar el driver primero
        #configurar_logging(driver, numero_caso)  # Manejo de logs críticos con el driver actual
        logging.info(f"==== Intento de login #{intento_login} para SAT ====")

# --------------------- Caso 1 - Funciones SAT ---------------------
        try:
            # Pasos 1-3
            sat_dirigir_a_pagina_y_verificar_estado_login(driver)
            break
        except Exception as e:
            logging.warning(f"Error en intento de login #{intento_login}, la página no cargó a tiempo.")
            finalizar_automatizacion(driver)

            if intento_login == MAX_INTENTOS_LOGIN:
                logging.error("Se alcanzó el máximo de intentos de login. Abortando el flujo.")
                return
    # Pasos 4-7
    sat_navegar_por_busqueda(driver, "Emision constancias de retencion")
    # Pasos 8-10 (Cambiar gen por peq en constantes antes de ejecutar caso 3 completo)
    sat_emision_constancias_de_retencion_busqueda_parametros(driver, s_emision_constancias_emision_del, s_emision_constancias_emision_al, s_emision_constancias_retenciones_que_declara_iva, s_emision_constancias_regimen_peq, s_emision_constancias_tipo_documento, s_emision_constancias_nit_retenido, s_emision_constancias_no_autorizacion_fel, s_emision_constancias_serie_de_factura, s_emision_constancias_no_de_factura)
    # Pasos 11-18
    numero_retencion_iva = sat_emision_constancias_de_retencion_generar_retencion_y_cambiar_directorio_pdf(driver, s_emision_constancias_retenciones_que_declara_iva, s_emision_constancias_directorio_descargas, s_emision_constancias_directorio_facturas_iva, s_emision_constancias_nombre_proveedor, s_emision_constancias_no_de_factura, s_emision_constancias_fecha_factura)
    h_introd_comprobantes_nombre_pdf = h_introd_comprobantes_nombre_pdf + (numero_retencion_iva,)

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

# --------------------- Fin Automatización ---------------------
    if driver.service.process is not None:  # Solo cerrar si el proceso sigue activo
        finalizar_automatizacion(driver)