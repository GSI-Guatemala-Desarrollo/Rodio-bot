import logging
import time
from flujos import (
    configurar_driver,
    configurar_logging,
    caso_1_reten_IVA_GEN,
    caso_2_reten_IVA_e_ISR,
    caso_3_reten_IVA_PEQ,
    recepcion_OC
)

# Valores de las variables ya definidos, solo se utilizan para comprobar que el bot funcione correctamente. En casos reales se ingresan los valores en las funciones de los casos.
from constantes import (
    NUMERO_CASO,
    # SAT
    # Emisión constancias
    S_EMISION_CONSTANCIAS_EMISION_DEL,
    S_EMISION_CONSTANCIAS_EMISION_AL,
    S_EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_IVA,
    S_EMISION_CONSTANCIAS_REGIMEN_GEN,
    S_EMISION_CONSTANCIAS_TIPO_DOCUMENTO,
    S_EMISION_CONSTANCIAS_NIT_RETENIDO,
    S_EMISION_CONSTANCIAS_NO_AUTORIZACION_FEL,
    S_EMISION_CONSTANCIAS_SERIE_DE_FACTURA,
    S_EMISION_CONSTANCIAS_NO_DE_FACTURA,
    S_EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS,
    S_EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_IVA,
    S_EMISION_CONSTANCIAS_NOMBRE_PROVEEDOR,
    S_EMISION_CONSTANCIAS_FECHA_FACTURA,
    
    # Exclusivas del caso 2
    S_EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_ISR,
    S_EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_ISR,


    # Exclusivas del caso 3
    S_EMISION_CONSTANCIAS_REGIMEN_PEQ,

    # Categoría de rentas
    S_CATEGORIA_DE_RENTAS_NIT_RETENIDO,
    S_CATEGORIA_DE_RENTAS_PERIODO_DEL,
    S_CATEGORIA_DE_RENTAS_PERIODO_AL,
    S_CATEGORIA_DE_RENTAS_ESTADO_DE_ASIGNACION,
    S_CATEGORIA_DE_RENTAS_NO_DE_FACTURA,
    S_CATEGORIA_DE_RENTAS_OPCION_CATEGORIA_DE_RENTA, 
    S_CATEGORIA_DE_RENTAS_OPCION_REGIMEN,
    
    
    
    # Harmony
    # OC
    H_RECEPCIONES_UNI_PO,
    H_RECEPCIONES_ID_OC,
    # Facturas
    H_INTROD_COMPROBANTES_ID_PROVEEDOR,
    H_INTROD_COMPROBANTES_NO_DE_FACTURA,
    H_INTROD_COMPROBANTES_FECHA_FACTURA,
    
    H_INTROD_COMPROBANTES_UNI_PO,
    H_INTROD_COMPROBANTES_NO_PEDIDO,
    H_INTROD_COMPROBANTES_IVA,
    H_INTROD_COMPROBANTES_NO_DE_SERIE,
    
    H_INTROD_COMPROBANTES_PDF_PATH,
    H_INTROD_COMPROBANTES_NOMBRE_PDF,
    H_INTROD_COMPROBANTES_NOMBRE_PROVEEDOR,
    H_INTROD_COMPROBANTES_COMENTARIO,
    
    H_INTROD_COMPROBANTES_LISTA_PORCENTAJE_RETENCION,
    H_INTROD_COMPROBANTES_LISTA_IMPT_BASE_RETENCION_SUST_CASO_1y3,
    H_INTROD_COMPROBANTES_LISTA_IMPT_BASE_RETENCION_SUST_CASO_2,
    
    H_INTROD_COMPROBANTES_LISTA_DESCRIPCIONES,
    H_INTROD_COMPROBANTES_LISTA_IVA,
    
    # Cami
    CAMI_NOMBRE_EMPRESA,
)




# -x-x-x- CONFIGURACIÓN LOGGING Y DRIVER -x-x-x-

#driver = configurar_driver()  # Configurar el driver primero
#configurar_logging(driver)  # Pasar el driver al CriticalHandler




# -x-x-x- INICIO AUTOMATIZACIÓN -x-x-x-

# Órdenes de compra
"""
try:
    logging.info("INICIO DEL FLUJO: Órdenes de compra")
    recepcion_OC(
                NUMERO_CASO,
                # Valores Harmony
                H_RECEPCIONES_UNI_PO,
                H_RECEPCIONES_ID_OC,
                )
    logging.info("FLUJO COMPLETADO: Órdenes de compra")
except Exception as e:
    logging.critical(f"Error crítico en el flujo 'Órdenes de compra': {e}")
"""

# Facturas - Caso 1
#"""
try:
    logging.info("INICIO DEL FLUJO: Caso 1 - Reten IVA GEN")
    caso_1_reten_IVA_GEN(
                        NUMERO_CASO,
                         # SAT
                        S_EMISION_CONSTANCIAS_EMISION_DEL,
                        S_EMISION_CONSTANCIAS_EMISION_AL,
                        S_EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_IVA,
                        S_EMISION_CONSTANCIAS_REGIMEN_GEN,
                        S_EMISION_CONSTANCIAS_TIPO_DOCUMENTO,
                        S_EMISION_CONSTANCIAS_NIT_RETENIDO,
                        S_EMISION_CONSTANCIAS_NO_AUTORIZACION_FEL,
                        S_EMISION_CONSTANCIAS_SERIE_DE_FACTURA,
                        S_EMISION_CONSTANCIAS_NO_DE_FACTURA,
                        S_EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS,
                        S_EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_IVA,
                        S_EMISION_CONSTANCIAS_NOMBRE_PROVEEDOR,
                        S_EMISION_CONSTANCIAS_FECHA_FACTURA,
                        # HARMONY
                        H_INTROD_COMPROBANTES_ID_PROVEEDOR,
                        H_INTROD_COMPROBANTES_NO_DE_FACTURA,
                        H_INTROD_COMPROBANTES_FECHA_FACTURA,
                        
                        H_INTROD_COMPROBANTES_UNI_PO,
                        H_INTROD_COMPROBANTES_NO_PEDIDO,
                        H_INTROD_COMPROBANTES_IVA,
                        H_INTROD_COMPROBANTES_NO_DE_SERIE,
                        
                        H_INTROD_COMPROBANTES_PDF_PATH,
                        H_INTROD_COMPROBANTES_NOMBRE_PDF,
                        H_INTROD_COMPROBANTES_NOMBRE_PROVEEDOR,
                        H_INTROD_COMPROBANTES_COMENTARIO,
                        
                        H_INTROD_COMPROBANTES_LISTA_PORCENTAJE_RETENCION,
                        H_INTROD_COMPROBANTES_LISTA_IMPT_BASE_RETENCION_SUST_CASO_1y3,
                        
                        H_INTROD_COMPROBANTES_LISTA_DESCRIPCIONES,
                        H_INTROD_COMPROBANTES_LISTA_IVA,
                        # CAMI
                        CAMI_NOMBRE_EMPRESA
                        )
    logging.info("FLUJO FINALIZADO: Caso 1 - Reten IVA GEN")
except Exception as e:
    logging.critical(f"Error crítico en el flujo 'Caso 1 - Reten IVA GEN': {e}")
#"""

# Facturas - Caso 2
"""
try:
    logging.info("INICIO DEL FLUJO: Caso 2 - Reten IVA e ISR")
    caso_2_reten_IVA_e_ISR(
                        NUMERO_CASO,
                        # SAT
                        S_EMISION_CONSTANCIAS_EMISION_DEL,
                        S_EMISION_CONSTANCIAS_EMISION_AL,
                        S_EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_IVA,
                        S_EMISION_CONSTANCIAS_REGIMEN_GEN,
                        S_EMISION_CONSTANCIAS_TIPO_DOCUMENTO,
                        S_EMISION_CONSTANCIAS_NIT_RETENIDO,
                        S_EMISION_CONSTANCIAS_NO_AUTORIZACION_FEL,
                        S_EMISION_CONSTANCIAS_SERIE_DE_FACTURA,
                        S_EMISION_CONSTANCIAS_NO_DE_FACTURA,
                        S_EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS,
                        S_EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_IVA,
                        S_EMISION_CONSTANCIAS_NOMBRE_PROVEEDOR,
                        S_EMISION_CONSTANCIAS_FECHA_FACTURA,
                        S_CATEGORIA_DE_RENTAS_NIT_RETENIDO,
                        S_CATEGORIA_DE_RENTAS_PERIODO_DEL,
                        S_CATEGORIA_DE_RENTAS_PERIODO_AL,
                        S_CATEGORIA_DE_RENTAS_ESTADO_DE_ASIGNACION,
                        S_CATEGORIA_DE_RENTAS_NO_DE_FACTURA,
                        S_CATEGORIA_DE_RENTAS_OPCION_CATEGORIA_DE_RENTA,
                        S_CATEGORIA_DE_RENTAS_OPCION_REGIMEN,
                        S_EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_ISR,
                        S_EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_ISR,
                        # HARMONY
                        H_INTROD_COMPROBANTES_ID_PROVEEDOR,
                        H_INTROD_COMPROBANTES_NO_DE_FACTURA,
                        H_INTROD_COMPROBANTES_FECHA_FACTURA,
                            
                        H_INTROD_COMPROBANTES_UNI_PO,
                        H_INTROD_COMPROBANTES_NO_PEDIDO,
                        H_INTROD_COMPROBANTES_IVA,
                        H_INTROD_COMPROBANTES_NO_DE_SERIE,
                            
                        H_INTROD_COMPROBANTES_PDF_PATH,
                        H_INTROD_COMPROBANTES_NOMBRE_PDF,
                        H_INTROD_COMPROBANTES_NOMBRE_PROVEEDOR,
                        H_INTROD_COMPROBANTES_COMENTARIO,
                            
                        H_INTROD_COMPROBANTES_LISTA_PORCENTAJE_RETENCION,
                        H_INTROD_COMPROBANTES_LISTA_IMPT_BASE_RETENCION_SUST_CASO_2,
                            
                        H_INTROD_COMPROBANTES_LISTA_DESCRIPCIONES,
                        H_INTROD_COMPROBANTES_LISTA_IVA,
                           
                        # CAMI
                        CAMI_NOMBRE_EMPRESA
                        )
    logging.info("FLUJO FINALIZADO: Caso 2 - Reten IVA e ISR")
except Exception as e:
    logging.critical(f"Error crítico en el flujo 'Caso 2 - Reten IVA e ISR': {e}")
"""

# Facturas - Caso 3
"""
try:
    logging.info("INICIO DEL FLUJO: Caso 3 - Reten IVA PEQ")
    caso_3_reten_IVA_PEQ(
                        NUMERO_CASO,
                        # SAT
                        S_EMISION_CONSTANCIAS_EMISION_DEL,
                        S_EMISION_CONSTANCIAS_EMISION_AL,
                        S_EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_IVA,
                        S_EMISION_CONSTANCIAS_REGIMEN_PEQ,
                        S_EMISION_CONSTANCIAS_TIPO_DOCUMENTO,
                        S_EMISION_CONSTANCIAS_NIT_RETENIDO,
                        S_EMISION_CONSTANCIAS_NO_AUTORIZACION_FEL,
                        S_EMISION_CONSTANCIAS_SERIE_DE_FACTURA,
                        S_EMISION_CONSTANCIAS_NO_DE_FACTURA,
                        S_EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS,
                        S_EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_IVA,
                        S_EMISION_CONSTANCIAS_NOMBRE_PROVEEDOR,
                        S_EMISION_CONSTANCIAS_FECHA_FACTURA,
                        # HARMONY
                        H_INTROD_COMPROBANTES_ID_PROVEEDOR,
                        H_INTROD_COMPROBANTES_NO_DE_FACTURA,
                        H_INTROD_COMPROBANTES_FECHA_FACTURA,
                        
                        H_INTROD_COMPROBANTES_UNI_PO,
                        H_INTROD_COMPROBANTES_NO_PEDIDO,
                        H_INTROD_COMPROBANTES_IVA,
                        H_INTROD_COMPROBANTES_NO_DE_SERIE,
                        
                        H_INTROD_COMPROBANTES_PDF_PATH,
                        H_INTROD_COMPROBANTES_NOMBRE_PDF,
                        H_INTROD_COMPROBANTES_NOMBRE_PROVEEDOR,
                        H_INTROD_COMPROBANTES_COMENTARIO,
                        
                        H_INTROD_COMPROBANTES_LISTA_PORCENTAJE_RETENCION,
                        H_INTROD_COMPROBANTES_LISTA_IMPT_BASE_RETENCION_SUST_CASO_1y3,
                        
                        H_INTROD_COMPROBANTES_LISTA_DESCRIPCIONES,
                        H_INTROD_COMPROBANTES_LISTA_IVA,
                        # CAMI
                        CAMI_NOMBRE_EMPRESA
                        )
    logging.info("FLUJO FINALIZADO: Caso 3 - Reten IVA PEQ")
except Exception as e:
    logging.critical(f"Error crítico en el flujo 'Caso 3 - Reten IVA PEQ': {e}")
"""
