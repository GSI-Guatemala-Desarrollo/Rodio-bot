import logging
import os
from datetime import datetime, timedelta
from selenium.common.exceptions import TimeoutException

from configuracion_bot import configurar_driver, finalizar_automatizacion
from modulos_cami.cami_ingreso_datos_harmony import cami_eleccion_funciono_harmony
from modulos_cami.cami_ingreso_datos_sat import cami_eleccion_funciono_sat, cami_elegir_flujo
from constantes import CAMI_NOMBRE_EMPRESA
from modulos_cami.cami_login import cami_dirigir_a_pagina_y_verificar_estado_login
def notificar_y_subir_archivos_cami(mensaje_critico, creation_date_iso, modified_data):
    """
    Reabre el navegador, inicia sesión en CAMI, localiza el flujo por fecha y hora,
    y dispara la rutina de notificación específica según el tipo de retención y si declara ISR.

    Args:
        mensaje_critico: El mensaje CRITICAL capturado.
        creation_date_iso: Fecha original en formato ISO 8601, e.g. "2025-04-16T20:22:45.872Z".
        modified_data: Diccionario con los datos modificados.
    """
    logging.info("===== Iniciando notificación por error crítico =====")
    if not mensaje_critico:
        logging.info("No hay mensaje crítico para notificar.")
        return
    logging.info(f"Mensaje crítico: {mensaje_critico}")

    try:
        try:
            dt_utc = datetime.strptime(creation_date_iso, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            dt_utc = datetime.strptime(creation_date_iso, "%Y-%m-%dT%H:%M:%SZ")

        dt_local = dt_utc - timedelta(hours=4)

        # Desglosar manualmente los componentes para evitar el cero inicial en la hora
        mes = str(dt_local.month)
        dia = str(dt_local.day)
        anio = dt_local.year
        hora = dt_local.strftime("%I").lstrip("0")  # quitar cero inicial solo en la hora
        minuto_segundo = dt_local.strftime(":%M:%S")
        am_pm = dt_local.strftime(" %p")
        
        fecha_target = f"{mes}/{dia}/{anio}, {hora}{minuto_segundo}{am_pm}"
        logging.info(f"Fecha para búsqueda en CAMI: {fecha_target}")

    except Exception as e:
        logging.error(f"Error al procesar la fecha")
        return

    
    # 2) Abrir navegador y loguearse en CAMI
    driver = configurar_driver()
    try:
        cami_dirigir_a_pagina_y_verificar_estado_login(driver, CAMI_NOMBRE_EMPRESA)
    except Exception as e:
        logging.error(f"Error en login para notificación", exc_info=True)
        finalizar_automatizacion(driver)
        return

    # 3) Buscar el flujo con esa fecha
    try:
        cami_elegir_flujo(driver, fecha_target)
    except Exception as e:
        logging.error(f"CAMI - No pude ubicar el flujo para notificación", exc_info=True)
        finalizar_automatizacion(driver)
        return

    # 4) Elige la opción de retención según el mensaje crítico
    try:
        cami_eleccion_funciono_sat(driver, mensaje_critico, modified_data)
        

    except Exception as e:
        logging.error(f"❌ Error al ejecutar caso de notificación en CAMI", exc_info=True)
    finally:
        # 5) Cerrar navegador al final
        finalizar_automatizacion(driver)
        logging.info("Notificación finalizada y navegador cerrado.")
