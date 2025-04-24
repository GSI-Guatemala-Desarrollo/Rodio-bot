from datetime import datetime
import json
import logging

from conexion_y_manejo_datos.procesamiento_lineas_OC import iva_gen_calcular_linea_1, iva_peq_calcular_linea_1
from constantes import CAMI_NOMBRE_EMPRESA, H_INTROD_COMPROBANTES_PDF_PATH, H_INTROD_COMPROBANTES_UNI_PO, S_EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS, S_EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_IVA, S_EMISION_CONSTANCIAS_EMISION_AL, S_EMISION_CONSTANCIAS_EMISION_DEL, S_EMISION_CONSTANCIAS_NO_AUTORIZACION_FEL, S_EMISION_CONSTANCIAS_REGIMEN_GEN, S_EMISION_CONSTANCIAS_REGIMEN_PEQ, S_EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_IVA, S_EMISION_CONSTANCIAS_SERIE_DE_FACTURA, S_EMISION_CONSTANCIAS_TIPO_DOCUMENTO
from flujos import caso_1_reten_IVA_GEN, caso_3_reten_IVA_PEQ

def estandarizacion_de_datos(extracted_data):
    """Estandariza los datos de la lista, ajustando categorías y separando valores numéricos de descripciones."""

    # Convertir los valores de categoría a solo el número
    if "categoria_de_rentas_opcion_categoria_de_renta" in extracted_data:
        extracted_data["categoria_de_rentas_opcion_categoria_de_renta"] = extracted_data["categoria_de_rentas_opcion_categoria_de_renta"].split(".")[0]

    if "categoria_de_rentas_opcion_regimen" in extracted_data:
        extracted_data["categoria_de_rentas_opcion_regimen"] = extracted_data["categoria_de_rentas_opcion_regimen"].split(".")[0]

    # Convertir la fecha si existe en el diccionario
    if "s_emision_constancias_fecha_factura" in extracted_data:
        fecha_original = extracted_data["s_emision_constancias_fecha_factura"]
        
        try:
            # Convertir la fecha original de formato YYYY-MM-DD a un objeto datetime
            fecha_objeto = datetime.strptime(fecha_original, "%Y-%m-%d")
            
            # Convertir y actualizar la fecha original en formato DD/MM/YYYY
            fecha_original_formateada = fecha_objeto.strftime("%d/%m/%Y")
            extracted_data["s_emision_constancias_fecha_factura"] = fecha_original_formateada
            
            # Crear la nueva fecha en formato MM/DD/YYYY y agregarla al diccionario
            fecha_convertida = fecha_objeto.strftime("%m/%d/%Y")
            extracted_data["h_introd_comprobantes_fecha_factura"] = fecha_convertida
        
        except ValueError:
            logging.error(f"⚠️ Advertencia: Formato de fecha inválido en `s_emision_constancias_fecha_factura`: {fecha_original}")
            extracted_data["h_introd_comprobantes_fecha_factura"] = ""
            extracted_data["s_emision_constancias_fecha_factura"] = ""

    # Crear la lista con los nombres de los PDFs en minúsculas
    extracted_data["h_introd_comprobantes_nombre_pdf"] = [
        extracted_data.get("nombre_comprobante_entrega", "").lower(),
        extracted_data.get("nombre_factura", "").lower()
    ]

    # Separar valores numéricos y descripciones
    if "h_introd_comprobantes_lista_descripciones" in extracted_data:
        descripcion_dict = extracted_data["h_introd_comprobantes_lista_descripciones"]

        # Si es un string en formato JSON, convertirlo en un diccionario
        if isinstance(descripcion_dict, str):
            try:
                descripcion_dict = json.loads(descripcion_dict)
                logging.info("Convertido de string a diccionario.")
            except json.JSONDecodeError:
                logging.warning("No se pudo convertir a diccionario.")
                descripcion_dict = {}

        # Si es un diccionario y contiene 'COMENTARIO'
        if isinstance(descripcion_dict, dict) and "COMENTARIO" in descripcion_dict:
            datos_numericos = []
            descripciones = []

            for item in descripcion_dict["COMENTARIO"]:
                if isinstance(item, list) and len(item) == 2:  # Asegurar estructura válida
                    numero_convertido = convertir_a_numero(item[0])
                    if numero_convertido is not None:
                        datos_numericos.append(numero_convertido)  # Agregar el valor convertido
                        descripciones.append(item[1])  # Agregar la descripción

            # Guardar total_oc antes de procesar los datos
            extracted_data["total_oc"] = round(sum(datos_numericos), 2)

            # Reemplazar el diccionario por la lista de descripciones
            extracted_data["h_introd_comprobantes_lista_descripciones"] = descripciones
            extracted_data["procesamiento_datos_lineas"] = datos_numericos

        else:
            logging.warning("`h_introd_comprobantes_lista_descripciones` no es un diccionario válido.")
            extracted_data["h_introd_comprobantes_lista_descripciones"] = []
            extracted_data["procesamiento_datos_lineas"] = []
            extracted_data["total_oc"] = 0.0  # Si no hay datos, total_oc es 0

    return extracted_data

# Función auxiliar de estandarizacion_de_datos para cambiar formato
def convertir_a_numero(valor):
    """Convierte un string con formato '8.432,32' a float 8432.32"""
    if isinstance(valor, str):
        valor = valor.replace(".", "").replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            print(f"⚠️ Advertencia: No se pudo convertir '{valor}' a número.")
            return None
    return valor

def eleccion_caso_bot(modified_data, driver) :
    """Elige el caso adecuado según declara_isr y flujo_contribuyente."""

    tipo_retencion = modified_data.get("tipo_retencion", "").strip()
    flujo_contribuyente = modified_data.get("  flujo_contribuyente", "").strip()

    logging.info(f"`tipo_retencion`: '{tipo_retencion}'")
    logging.info(f"`flujo_contribuyente`: '{flujo_contribuyente}'")

    if tipo_retencion == "ISR TRIMESTRAL" and flujo_contribuyente == "GEN":
        ejecucion_caso_iva_gen(modified_data, driver)

    elif tipo_retencion == "RETENISR ROSSI" and flujo_contribuyente == "GEN":
        ejecucion_caso_iva_gen(modified_data, driver)

    elif tipo_retencion == "ISR TRIMESTRAL" and flujo_contribuyente == "PEQ":
        ejecucion_caso_iva_peq(modified_data, driver)

    else:
        logging.critical("API - Valores inesperados en tipo_retencion o flujo_contribuyente.")


# Caso 1 (Solo IVA, contribuyente GENERAL)
def ejecucion_caso_iva_gen(modified_data, driver):
    """Ejecuta el caso de Reten IVA GEN, calculando solo el IVA2."""

    try:
        logging.info("INICIO DEL FLUJO: Caso 1 - Reten IVA GEN")

        # Obtener la lista de valores numéricos procesados
        procesamiento_datos_lineas = modified_data.pop("procesamiento_datos_lineas", [])

        if not procesamiento_datos_lineas:
            logging.error("❌ Error: procesamiento_datos_lineas está vacío.")
            return

        retencion_iva = 0.15  # 15% de retención

        # Calcular IVA2 para cada valor
        lista_impt_base_retencion_sust = []
        for valor_numerico in procesamiento_datos_lineas:
            try:
                resultado = iva_gen_calcular_linea_1(valor_numerico, retencion_iva)["IVA2"]
                lista_impt_base_retencion_sust.append(round(resultado, 2))  # Redondear a 2 decimales
            except Exception as e:
                logging.error(f"❌ Error al calcular IVA2 para {valor_numerico}: {e}")

        # Guardar la lista procesada
        modified_data["h_introd_comprobantes_lista_impt_base_retencion_sust"] = lista_impt_base_retencion_sust

        # 📌 CREAR LISTAS ADICIONALES AQUÍ
        cantidad_elementos = len(procesamiento_datos_lineas)
        modified_data["h_introd_comprobantes_lista_porcentaje_retencion"] = ["TVA15"] * cantidad_elementos
        modified_data["h_introd_comprobantes_lista_iva"] = ["12.00"] * cantidad_elementos

        # Imprimir datos procesados antes de ejecutar el bot
        logging.info("\n\n Datos procesados antes de ejecutar el bot, después de estandarización:")
        for key, value in modified_data.items():
            logging.info(f"{key}: {value}")

        # Ejecutar el siguiente paso del flujo (activación del bot).
        caso_1_reten_IVA_GEN(
                            driver,
                            #NUMERO_CASO,
                            modified_data.get("numeracion_automatica", "0"),
                            
                            # SAT
                            S_EMISION_CONSTANCIAS_EMISION_DEL,
                            S_EMISION_CONSTANCIAS_EMISION_AL,
                            S_EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_IVA,
                            S_EMISION_CONSTANCIAS_REGIMEN_GEN,
                            S_EMISION_CONSTANCIAS_TIPO_DOCUMENTO,
                            #S_EMISION_CONSTANCIAS_NIT_RETENIDO,
                            modified_data.get("s_emision_constancias_nit_retenido", "0"),
                            S_EMISION_CONSTANCIAS_NO_AUTORIZACION_FEL, 
                            S_EMISION_CONSTANCIAS_SERIE_DE_FACTURA,
                            #S_EMISION_CONSTANCIAS_NO_DE_FACTURA,
                            modified_data.get(" s_emision_constancias_no_de_factura", "0"),
                            S_EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS,
                            S_EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_IVA,
                            #S_EMISION_CONSTANCIAS_NOMBRE_PROVEEDOR,
                            modified_data.get("s_emision_constancias_nombre_proveedor", "nombre_proveedor"),
                            #S_EMISION_CONSTANCIAS_FECHA_FACTURA,
                            modified_data.get("s_emision_constancias_fecha_factura", "0"),
                            
                            # HARMONY
                            #H_INTROD_COMPROBANTES_ID_PROVEEDOR,
                            modified_data.get("h_introd_comprobantes_id_proveedor", "0"),
                            #H_INTROD_COMPROBANTES_NO_DE_FACTURA,
                            modified_data.get(" s_emision_constancias_no_de_factura", "0"),
                            #H_INTROD_COMPROBANTES_FECHA_FACTURA,
                            modified_data.get("h_introd_comprobantes_fecha_factura", "0"),
                            
                            H_INTROD_COMPROBANTES_UNI_PO,
                            #H_INTROD_COMPROBANTES_NO_PEDIDO,
                            modified_data.get("h_introd_comprobantes_no_pedido", "0"),
                            #H_INTROD_COMPROBANTES_IVA,
                            modified_data.get("h_introd_comprobantes_iva", "0"),
                            #H_INTROD_COMPROBANTES_NO_DE_SERIE,
                            modified_data.get("s_emision_constancias_serie_de_factura", "0"),
                            
                            H_INTROD_COMPROBANTES_PDF_PATH,
                            #H_INTROD_COMPROBANTES_NOMBRE_PDF,
                            modified_data.get("h_introd_comprobantes_nombre_pdf", "0"),
                            #H_INTROD_COMPROBANTES_NOMBRE_PROVEEDOR,
                            modified_data.get("s_emision_constancias_nombre_proveedor", "0"),
                            #H_INTROD_COMPROBANTES_COMENTARIO,
                            modified_data.get("h_introd_comprobantes_comentario", "0"),
                            
                            #H_INTROD_COMPROBANTES_LISTA_PORCENTAJE_RETENCION,
                            modified_data.get("h_introd_comprobantes_lista_porcentaje_retencion", "0"),
                            #H_INTROD_COMPROBANTES_LISTA_IMPT_BASE_RETENCION_SUST_CASO_1y3,
                            modified_data.get("h_introd_comprobantes_lista_impt_base_retencion_sust", "0"),
                            
                            #H_INTROD_COMPROBANTES_LISTA_DESCRIPCIONES,
                            modified_data.get("h_introd_comprobantes_lista_descripciones", "0"),
                            #H_INTROD_COMPROBANTES_LISTA_IVA,
                            modified_data.get("h_introd_comprobantes_lista_iva", "0"),
                            # CAMI
                            CAMI_NOMBRE_EMPRESA
                            )
        logging.info("FLUJO FINALIZADO: Caso 1 - Reten IVA GEN")
    except Exception as e:
        logging.error(f"Error crítico en el flujo 'Caso 1 - Reten IVA GEN': {e}")
        


# Caso 2 (IVA e ISR, contribuyente GENERAL)
def ejecucion_caso_iva_isr(modified_data):
    
    
# Caso 3 (Solo IVA, contribuyente PEQUEÑO)
def ejecucion_caso_iva_peq(modified_data, driver):
    """Ejecuta el caso de Reten IVA PEQ, calculando solo el IVA2."""

    try:
        logging.info("INICIO DEL FLUJO: Caso 3 - Reten IVA PEQ")

        # Obtener la lista de valores numéricos procesados
        procesamiento_datos_lineas = modified_data.pop("procesamiento_datos_lineas", [])

        if not procesamiento_datos_lineas:
            logging.error("❌ Error: procesamiento_datos_lineas está vacío.")
            return

        retencion_iva = 0.05  # 5% de retención

        # Calcular IVA2 para cada valor
        lista_impt_base_retencion_sust = []
        for valor_numerico in procesamiento_datos_lineas:
            try:
                resultado = iva_peq_calcular_linea_1(valor_numerico, retencion_iva)["IVA2"]
                lista_impt_base_retencion_sust.append(round(resultado, 2))  # Redondear a 2 decimales
            except Exception as e:
                logging.error(f"❌ Error al calcular IVA2 para {valor_numerico}: {e}")

        # Guardar la lista procesada
        modified_data["h_introd_comprobantes_lista_impt_base_retencion_sust"] = lista_impt_base_retencion_sust

        # 📌 CREAR LISTAS ADICIONALES AQUÍ
        cantidad_elementos = len(procesamiento_datos_lineas)
        modified_data["h_introd_comprobantes_lista_porcentaje_retencion"] = ["TVA05"] * cantidad_elementos
        modified_data["h_introd_comprobantes_lista_iva"] = ["5.00"] * cantidad_elementos

        # Imprimir datos procesados antes de ejecutar el bot
        print("\n\n📌 Datos procesados antes de ejecutar el bot:")
        for key, value in modified_data.items():
            print(f"{key}: {value}")

        # Ejecutar el siguiente paso del flujo (activación del bot).
        caso_3_reten_IVA_PEQ(
                            driver,
                            #NUMERO_CASO,
                            modified_data.get("numeracion_automatica", "0"),
                            
                            # SAT
                            S_EMISION_CONSTANCIAS_EMISION_DEL,
                            S_EMISION_CONSTANCIAS_EMISION_AL,
                            S_EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA_IVA,
                            S_EMISION_CONSTANCIAS_REGIMEN_PEQ,
                            S_EMISION_CONSTANCIAS_TIPO_DOCUMENTO,
                            #S_EMISION_CONSTANCIAS_NIT_RETENIDO,
                            modified_data.get("s_emision_constancias_nit_retenido", "0"),
                            S_EMISION_CONSTANCIAS_NO_AUTORIZACION_FEL, 
                            S_EMISION_CONSTANCIAS_SERIE_DE_FACTURA,
                            #S_EMISION_CONSTANCIAS_NO_DE_FACTURA,
                            modified_data.get(" s_emision_constancias_no_de_factura", "0"),
                            S_EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS,
                            S_EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS_IVA,
                            #S_EMISION_CONSTANCIAS_NOMBRE_PROVEEDOR,
                            modified_data.get("s_emision_constancias_nombre_proveedor", "nombre_proveedor"),
                            #S_EMISION_CONSTANCIAS_FECHA_FACTURA,
                            modified_data.get("s_emision_constancias_fecha_factura", "0"),
                            
                            # HARMONY
                            #H_INTROD_COMPROBANTES_ID_PROVEEDOR,
                            modified_data.get("h_introd_comprobantes_id_proveedor", "0"),
                            #H_INTROD_COMPROBANTES_NO_DE_FACTURA,
                            modified_data.get(" s_emision_constancias_no_de_factura", "0"),
                            #H_INTROD_COMPROBANTES_FECHA_FACTURA,
                            modified_data.get("h_introd_comprobantes_fecha_factura", "0"),
                            
                            H_INTROD_COMPROBANTES_UNI_PO,
                            #H_INTROD_COMPROBANTES_NO_PEDIDO,
                            modified_data.get("h_introd_comprobantes_no_pedido", "0"),
                            #H_INTROD_COMPROBANTES_IVA,
                            modified_data.get("h_introd_comprobantes_iva", "0"),
                            #H_INTROD_COMPROBANTES_NO_DE_SERIE,
                            modified_data.get("s_emision_constancias_serie_de_factura", "0"),
                            
                            H_INTROD_COMPROBANTES_PDF_PATH,
                            #H_INTROD_COMPROBANTES_NOMBRE_PDF,
                            modified_data.get("h_introd_comprobantes_nombre_pdf", "0"),
                            #H_INTROD_COMPROBANTES_NOMBRE_PROVEEDOR,
                            modified_data.get("s_emision_constancias_nombre_proveedor", "0"),
                            #H_INTROD_COMPROBANTES_COMENTARIO,
                            modified_data.get("h_introd_comprobantes_comentario", "0"),
                            
                            #H_INTROD_COMPROBANTES_LISTA_PORCENTAJE_RETENCION,
                            modified_data.get("h_introd_comprobantes_lista_porcentaje_retencion", "0"),
                            #H_INTROD_COMPROBANTES_LISTA_IMPT_BASE_RETENCION_SUST_CASO_1y3,
                            modified_data.get("h_introd_comprobantes_lista_impt_base_retencion_sust", "0"),
                            
                            #H_INTROD_COMPROBANTES_LISTA_DESCRIPCIONES,
                            modified_data.get("h_introd_comprobantes_lista_descripciones", "0"),
                            #H_INTROD_COMPROBANTES_LISTA_IVA,
                            modified_data.get("h_introd_comprobantes_lista_iva", "0"),
                            # CAMI
                            CAMI_NOMBRE_EMPRESA
                            )
        logging.info("FLUJO FINALIZADO: Caso 3 - Reten IVA PEQ")
    except Exception as e:
        logging.error(f"Error crítico en el flujo 'Caso 3 - Reten IVA PEQ': {e}")
        
        