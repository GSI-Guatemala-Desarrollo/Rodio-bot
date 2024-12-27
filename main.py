import logging
import time
from configuracion_bot_y_flujos import (
    configurar_driver,
    configurar_logging,
    caso_1_reten_IVA_GEN,
    caso_2_reten_IVA_e_ISR,
    caso_3_reten_IVA_PEQ
)

# Valores de las variables ya definidos, solo se utilizan para comprobar que el bot funcione correctamente. En casos reales se ingresan los valores en las funciones de los casos.
from constantes import (
    # SAT
    # Emisión constancias
    EMISION_CONSTANCIAS_EMISION_DEL,
    EMISION_CONSTANCIAS_EMISION_AL,
    EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_IVA,
    EMISION_CONSTANCIAS_REGIMEN_GEN,
    EMISION_CONSTANCIAS_TIPO_DOCUMENTO,
    EMISION_CONSTANCIAS_NIT_RETENIDO,
    EMISION_CONSTANCIAS_NO_AUTORIZACION_FEL,
    EMISION_CONSTANCIAS_SERIE_DE_FACTURA,
    EMISION_CONSTANCIAS_NO_DE_FACTURA,
    EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS,
    EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_IVA,
    EMISION_CONSTANCIAS_NOMBRE_PROVEEDOR,
    EMISION_CONSTANCIAS_FECHA_FACTURA,
    
    # Exclusivas del caso 2
    EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_ISR,
    EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_ISR,


    # Exclusivas del caso 3
    EMISION_CONSTANCIAS_REGIMEN_PEQ,

    # Categoría de rentas
    CATEGORIA_DE_RENTAS_NIT_RETENIDO,
    CATEGORIA_DE_RENTAS_PERIODO_DEL,
    CATEGORIA_DE_RENTAS_PERIODO_AL,
    CATEGORIA_DE_RENTAS_ESTADO_DE_ASIGNACION,
    CATEGORIA_DE_RENTAS_NO_DE_FACTURA,
    CATEGORIA_DE_RENTAS_OPCION_CATEGORIA_DE_RENTA, 
    CATEGORIA_DE_RENTAS_OPCION_REGIMEN,
    
    
    
    # Harmony
    H_INTROD_COMPROBANTES_ID_PROVEEDOR,
    H_INTROD_COMPROBANTES_NO_DE_FACTURA,
    H_INTROD_COMPROBANTES_FECHA_FACTURA,
    
    H_INTROD_COMPROBANTES_UNI_PO,
    H_INTROD_COMPROBANTES_NO_PEDIDO,
    
    # Cami
    CAMI_NOMBRE_EMPRESA,
)




# -x-x-x- CONFIGURACIÓN LOGGING Y DRIVER -x-x-x-

driver = configurar_driver()  # Configurar el driver primero
configurar_logging(driver)  # Pasar el driver al CriticalHandler




# -x-x-x- INICIO AUTOMATIZACIÓN -x-x-x-

#"""
try:
    logging.info("INICIO DEL FLUJO: Caso 1 - Reten IVA GEN")
    caso_1_reten_IVA_GEN(driver,
                         # SAT
                        EMISION_CONSTANCIAS_EMISION_DEL,
                        EMISION_CONSTANCIAS_EMISION_AL,
                        EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_IVA,
                        EMISION_CONSTANCIAS_REGIMEN_GEN,
                        EMISION_CONSTANCIAS_TIPO_DOCUMENTO,
                        EMISION_CONSTANCIAS_NIT_RETENIDO,
                        EMISION_CONSTANCIAS_NO_AUTORIZACION_FEL,
                        EMISION_CONSTANCIAS_SERIE_DE_FACTURA,
                        EMISION_CONSTANCIAS_NO_DE_FACTURA,
                        EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS,
                        EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_IVA,
                        EMISION_CONSTANCIAS_NOMBRE_PROVEEDOR,
                        EMISION_CONSTANCIAS_FECHA_FACTURA,
                        # HARMONY
                        H_INTROD_COMPROBANTES_ID_PROVEEDOR,
                        H_INTROD_COMPROBANTES_NO_DE_FACTURA,
                        H_INTROD_COMPROBANTES_FECHA_FACTURA,
                        
                        H_INTROD_COMPROBANTES_UNI_PO,
                        H_INTROD_COMPROBANTES_NO_PEDIDO,
                        # CAMI
                        CAMI_NOMBRE_EMPRESA
                        )
    logging.info("FLUJO COMPLETADO: Caso 1 - Reten IVA GEN")
except Exception as e:
    logging.critical(f"Error crítico en el flujo 'Caso 1 - Reten IVA GEN': {e}")
#"""


"""
try:
    logging.info("INICIO DEL FLUJO: Caso 2 - Reten IVA e ISR")
    caso_2_reten_IVA_e_ISR(driver,
                           EMISION_CONSTANCIAS_EMISION_DEL,
                           EMISION_CONSTANCIAS_EMISION_AL,
                           EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_IVA,
                           EMISION_CONSTANCIAS_REGIMEN_GEN,
                           EMISION_CONSTANCIAS_TIPO_DOCUMENTO,
                           EMISION_CONSTANCIAS_NIT_RETENIDO,
                           EMISION_CONSTANCIAS_NO_AUTORIZACION_FEL,
                           EMISION_CONSTANCIAS_SERIE_DE_FACTURA,
                           EMISION_CONSTANCIAS_NO_DE_FACTURA,
                           EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS,
                           EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_IVA,
                           EMISION_CONSTANCIAS_NOMBRE_PROVEEDOR,
                           EMISION_CONSTANCIAS_FECHA_FACTURA,
                           CATEGORIA_DE_RENTAS_NIT_RETENIDO,
                           CATEGORIA_DE_RENTAS_PERIODO_DEL,
                           CATEGORIA_DE_RENTAS_PERIODO_AL,
                           CATEGORIA_DE_RENTAS_ESTADO_DE_ASIGNACION,
                           CATEGORIA_DE_RENTAS_NO_DE_FACTURA,
                           CATEGORIA_DE_RENTAS_OPCION_CATEGORIA_DE_RENTA,
                           CATEGORIA_DE_RENTAS_OPCION_REGIMEN,
                           EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_ISR,
                           EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_ISR,
                           CAMI_NOMBRE_EMPRESA
                           )
    logging.info("FLUJO COMPLETADO: Caso 2 - Reten IVA e ISR")
except Exception as e:
    logging.critical(f"Error crítico en el flujo 'Caso 2 - Reten IVA e ISR': {e}")
"""


"""
try:
    logging.info("INICIO DEL FLUJO: Caso 3 - Reten IVA PEQ")
    caso_3_reten_IVA_PEQ(driver,
                         EMISION_CONSTANCIAS_EMISION_DEL,
                         EMISION_CONSTANCIAS_EMISION_AL,
                         EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_IVA,
                         EMISION_CONSTANCIAS_REGIMEN_PEQ,
                         EMISION_CONSTANCIAS_TIPO_DOCUMENTO,
                         EMISION_CONSTANCIAS_NIT_RETENIDO,
                         EMISION_CONSTANCIAS_NO_AUTORIZACION_FEL,
                         EMISION_CONSTANCIAS_SERIE_DE_FACTURA,
                         EMISION_CONSTANCIAS_NO_DE_FACTURA,
                         EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS,
                         EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_IVA,
                         EMISION_CONSTANCIAS_NOMBRE_PROVEEDOR,
                         EMISION_CONSTANCIAS_FECHA_FACTURA,
                         CAMI_NOMBRE_EMPRESA
                         )
    logging.info("FLUJO COMPLETADO: Caso 3 - Reten IVA PEQ")
except Exception as e:
    logging.critical(f"Error crítico en el flujo 'Caso 3 - Reten IVA PEQ': {e}")
"""




# -x-x-x- FIN AUTOMATIZACIÓN -x-x-x-

# Eliminar la instancia
try:
    time.sleep(5)
    driver.close()
    driver.quit()
    logging.info("Automatización finalizada y navegador cerrado.")
except Exception as e:
    logging.error(f"Error al cerrar el navegador: {e}")