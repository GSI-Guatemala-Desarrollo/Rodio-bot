import logging
import os
from datetime import datetime, timedelta
from selenium.common.exceptions import TimeoutException

from configuracion_bot import configurar_driver, finalizar_automatizacion
from modulos_cami.cami_ingreso_datos_harmony import cami_eleccion_funciono_harmony
from modulos_cami.cami_ingreso_datos_sat import cami_dirigir_a_pagina_y_verificar_estado_login, cami_eleccion_funciono_sat
from modulos_cami.cami_flujos import cami_elegir_flujo, cami_caso_iva_gen, cami_caso_iva_peq, cami_caso_isr
from constantes import CAMI_NOMBRE_EMPRESA

def notificar_y_subir_archivos_cami(mensaje_critico, creation_date_iso, modified_data):
    """
    Reabre el navegador, inicia sesión en CAMI, localiza el flujo por fecha y hora,
    y dispara la rutina de notificación específica según el tipo de retención y si declara ISR.
    
    Args:
        mensaje_critico: El mensaje CRITICAL capturado.
        creation_date_iso: Fecha original en formato ISO 8601, e.g. "2025-04-16T20:22:45.872Z".
        tipo_retencion: Cadena identificando el tipo de retención ("ISR TRIMESTRAL", etc.).
        declara_isr: "GEN" o "PEQ".
    """
    logging.info("===== Iniciando notificación por error crítico =====")
    if not mensaje_critico:
        logging.info("No hay mensaje crítico para notificar.")
        return
    logging.info(f"Mensaje crítico: {mensaje_critico}")

    # 1) Transformar la fecha ISO en "D/M/YYYY, H:MM:SS a. m./p. m."
    try:
        # parse ISO (con milisegundos)
        dt_utc = datetime.strptime(creation_date_iso, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        # sin milisegundos
        dt_utc = datetime.strptime(creation_date_iso, "%Y-%m-%dT%H:%M:%SZ")
    # ajustar a hora local GT (UTC-6)
    dt_local = dt_utc - timedelta(hours=6)
    hour = dt_local.hour
    ampm = "a. m." if hour < 12 else "p. m."
    hour12 = hour % 12 or 12
    fecha_target = f"{dt_local.day}/{dt_local.month}/{dt_local.year}, {hour12}:{dt_local.minute:02}:{dt_local.second:02} {ampm}"
    logging.info(f"Fecha para búsqueda en CAMI: {fecha_target}")

    # 2) Abrir navegador y loguearse en CAMI
    driver = configurar_driver()
    try:
        cami_dirigir_a_pagina_y_verificar_estado_login(driver, CAMI_NOMBRE_EMPRESA)
    except Exception as e:
        logging.error(f"Error en login para notificación: {e}", exc_info=True)
        finalizar_automatizacion(driver)
        return

    # 3) Buscar el flujo con esa fecha
    try:
        cami_elegir_flujo(driver, fecha_target)
    except Exception as e:
        logging.error(f"CAMI - No pude ubicar el flujo para notificación: {e}", exc_info=True)
        finalizar_automatizacion(driver)
        return

    # 4) Elige la opción de retención según el mensaje crítico
    try:
        cami_eleccion_funciono_sat(driver, mensaje_critico, modified_data)
        

    except Exception as e:
        logging.error(f"❌ Error al ejecutar caso de notificación en CAMI: {e}", exc_info=True)
    finally:
        # 5) Cerrar navegador al final
        finalizar_automatizacion(driver)
        logging.info("Notificación finalizada y navegador cerrado.")
