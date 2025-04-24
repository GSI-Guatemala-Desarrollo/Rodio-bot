import time
import logging
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
from datetime import datetime, timedelta

# Paso 2
def harmony_introd_comprobantes_agregar_factura(driver, proveedor_id, no_factura, fecha_factura):
    """
    Ingresa al iframe principal (ptifrmtgtframe), llena los 3 campos
    y finaliza dando clic en el botón 'Añadir'.
    """

    try:
        logging.info("\n\n\n-x-x-x- (PASO 2) harmony_introd_comprobantes_agregar_factura -x-x-x-\n")
        # 1. Cambiar al iframe principal donde están los inputs
        logging.info("Cambiando al iframe principal (ptifrmtgtframe).")
        WebDriverWait(driver, 15).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "ptifrmtgtframe"))
        )
        time.sleep(1)  # Pausa para asegurar que el iframe cargó

        # 2. Ingresar Proveedor ID
        logging.info(f"Ingresando Proveedor ID: {proveedor_id}")
        input_proveedor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="VCHR_ADDSRCH_VW_VENDOR_ID"]'))
        )
        input_proveedor.clear()
        input_proveedor.send_keys(proveedor_id)
        time.sleep(2)  
        # ↑ Damos tiempo a Peoplesoft para que complete cualquier recarga automática tras ingresar el Proveedor

        # 3. Realiza la búsqueda del proveedor al interactuar con otro input
        input_no_factura = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="VCHR_ADDSRCH_VW_INVOICE_ID"]'))
        )
        input_no_factura.clear()
        input_no_factura.send_keys(" ")
        time.sleep(1)
        
        # 4. Ingresar Fecha de la factura
        logging.info(f"Ingresando Fecha de la Factura: {fecha_factura}")
        input_fecha_factura = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="VCHR_ADDSRCH_VW_INVOICE_DT"]'))
        )
        input_fecha_factura.clear()
        input_fecha_factura.send_keys(fecha_factura)
        time.sleep(1)

        # 5. Ingresar Número de factura
        logging.info(f"Ingresando Número de Factura: {no_factura}")
        input_no_factura = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="VCHR_ADDSRCH_VW_INVOICE_ID"]'))
        )
        input_no_factura.clear()
        time.sleep(1)
        input_no_factura.send_keys(no_factura)
        time.sleep(1)

        # 6. Clic en el botón "Añadir"
        logging.info("Dando clic en el botón 'Añadir'.")
        btn_anadir = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="#ICSearch"]'))
        )
        btn_anadir.click()
        logging.info("Factura añadida correctamente.")

    except Exception as e:
        logging.error("Error al agregar la factura: %s", e, exc_info=True)
        # Manejo adicional de errores si fuera necesario

# Pasos 3-6
def harmony_introd_comprobantes_copiar_documento(
    driver,
    uni_po,
    no_pedido,
    iva_percent,
    factura_num,
    factura_serie
):
    """
    1. Selecciona 'N Recepción Ped' en el select (VCHR_PANELS_WRK_VCHRWS_CPY_OPT).
    2. Da clic en el link 'Ir'.
    3. Espera 2 segundos para que cargue la página.
    4. Ingresa en el campo UNI PO.
    5. Ingresa el número de pedido.
    6. Da clic en el botón 'Buscar'.
    7. Espera a que se cargue la tabla.
    8. 'Scroll' al botón 'Selec Todo' y clic en él.
    9. Clic en el botón 'Copiar Líneas Seleccionadas'.
    10. Espera a que cargue la página anterior.
    11. Copia el total de la factura (VOUCHER_GROSS_AMT).
    12. Calcula el IVA según iva_percent.
    13. Ingresa el valor del IVA en VOUCHER_VAT_ENTRD_AMT.
    14. Ingresa número de factura y número de serie.
    """

    try:
        logging.info("\n\n\n-x-x-x- (PASOS 3-6) harmony_introd_comprobantes_copiar_documento -x-x-x-\n")

        # --- Nuevo Paso: Esperar a que aparezca el componente
        #     <div id="win0divVOUCHER_BUSINESS_UNIT">, que indica que la siguiente página ya cargó ---
        logging.info("Esperando a que aparezca 'win0divVOUCHER_BUSINESS_UNIT' antes de continuar...")
        start_time = time.time()
        timeout_segundos = 60  # Ajusta el tiempo máximo según tu escenario

        while True:
            if (time.time() - start_time) > timeout_segundos:
                logging.critical("HARMONY - No apareció 'win0divVOUCHER_BUSINESS_UNIT' antes de timeout. Abortando flujo.")
                return 
            
            try:
                driver.find_element(By.ID, "win0divVOUCHER_BUSINESS_UNIT")
                logging.info("'win0divVOUCHER_BUSINESS_UNIT' encontrado. Continuando con el flujo.")
                break  # Rompe el bucle si lo encontramos
            except:
                pass  # Si no está, lo reintentamos en el siguiente ciclo

            time.sleep(1)
        # --- Fin Nuevo Paso ---

        time.sleep(5)
        # 1. Seleccionar la opción 'N Recepción Ped' (value='PORV') en el select
        logging.info("Seleccionando opción 'N Recepción Ped' en el select.")
        select_cpy_opt = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VCHR_PANELS_WRK_VCHRWS_CPY_OPT"))
        )
        Select(select_cpy_opt).select_by_value("PORV")  # <option value="PORV">N Recepción Ped</option>
        time.sleep(1)

        # 2. Clic en el link 'Ir'
        logging.info("Haciendo clic en el link 'Ir'.")
        ir_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="VCHR_PANELS_WRK_PB_GO$span"]'))
        )
        ir_link.click()

        # 3. Espera 2s para que cargue la nueva pantalla
        logging.info("Esperando 2 segundos para que la página se recargue...")
        time.sleep(2)

        # 4. Ingresar UNI PO
        logging.info(f"Ingresando UNI PO: {uni_po}")
        input_uni_po = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "VCHR_PANELS_WRK_BUSINESS_UNIT_PO"))
        )
        input_uni_po.clear()
        time.sleep(1)
        input_uni_po.send_keys(uni_po)

        # 5. Ingresar número de pedido
        logging.info(f"Ingresando Número de Pedido: {no_pedido}")
        input_no_pedido = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "VCHR_PANELS_WRK_PO_ID"))
        )
        input_no_pedido.clear()
        time.sleep(1)
        input_no_pedido.send_keys(no_pedido)
        time.sleep(1)
        # 6. Clic en el botón 'Buscar'
        logging.info("Dando clic en el botón 'Buscar'.")
        btn_buscar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VCHR_PANELS_WRK_PB_GET_PO"))
        )
        time.sleep(2)
        btn_buscar.click()

        # 7. Esperamos a que la tabla se cargue.
        logging.info("Esperando a que la tabla se cargue...")
        time.sleep(2)  # Ajustar si la carga tarda más

        # 8. 'Scroll' al botón 'Selec Todo' y clic
        logging.info("Haciendo scroll hacia el botón 'Selec Todo'.")
        select_todo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VCHR_PANELS_WRK_SELECT_ALL$0"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", select_todo)
        select_todo.click()
        time.sleep(1)

        # 9. Clic en el botón 'Copiar Líneas Seleccionadas'
        logging.info("Haciendo clic en el botón 'Copiar Líneas Seleccionadas'.")
        btn_copiar_lineas = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VCHR_PANELS_WRK_VCHR_COPY_HDR"))
        )
        btn_copiar_lineas.click()

        # 10. Esperar a que cargue la página anterior
        logging.info("Esperando 2 segundos mientras carga la página anterior...")
        time.sleep(2)

                # 11. Copiar el total de la factura (VOUCHER_GROSS_AMT)
        logging.info("Obteniendo el total de la factura (VOUCHER_GROSS_AMT).")
        gross_amount_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "VOUCHER_GROSS_AMT"))
        )
        gross_amount_text = gross_amount_element.get_attribute("value")  # Ej: "4,651.78"
        logging.info(f"Valor bruto recuperado: {gross_amount_text}")

        # 12. Parsear y calcular IVA
        amount_no_commas = gross_amount_text.replace(",", "")  # "4651.78"
        try:
            gross_amount_float = float(amount_no_commas)
        except ValueError:
            logging.error("No se pudo parsear el valor bruto de la factura a float. Se usará 0.")
            gross_amount_float = 0.0

        iva_calculado = (gross_amount_float * iva_percent) / 100.0
        logging.info(f"IVA calculado: {iva_calculado:.2f} (usando {iva_percent}% de {gross_amount_float:.2f})")

        # 13. Ingresar el IVA en VOUCHER_VAT_ENTRD_AMT
        logging.info("Ingresando el valor del IVA en 'VOUCHER_VAT_ENTRD_AMT'.")
        vat_amount_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VOUCHER_VAT_ENTRD_AMT"))
        )
        vat_amount_element.clear()
        vat_amount_element.send_keys(f"{iva_calculado:,.2f}")
        time.sleep(1)

        # 14. Sumar total + IVA y ponerlo de nuevo en 'VOUCHER_GROSS_AMT'
        suma_total_iva = gross_amount_float + iva_calculado
        logging.info(f"Suma del total + IVA = {suma_total_iva:.2f}")
        logging.info("Reingresando la suma en 'VOUCHER_GROSS_AMT'.")
        # Volvemos a tomar el elemento (o reubicarlo) para asegurar que esté interactuable
        new_gross_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VOUCHER_GROSS_AMT"))
        )
        new_gross_element.clear()
        new_gross_element.send_keys(f"{suma_total_iva:,.2f}")
        time.sleep(1)

        # 15. Ingresar número de factura y número de serie
        logging.info(f"Ingresando número de factura: {factura_num}")
        factura_num_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VCHR_UUID_SBF_UUID_AC_SBF"))
        )
        factura_num_element.clear()
        factura_num_element.send_keys(factura_num)
        time.sleep(1)

        logging.info(f"Ingresando número de serie: {factura_serie}")
        factura_serie_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VCHR_UUID_SBF_SERIES_AC_SBF"))
        )
        factura_serie_element.clear()
        factura_serie_element.send_keys(factura_serie)

        logging.info("Función 'harmony_introd_comprobantes_copiar_documento' finalizada correctamente.")
        
        return suma_total_iva
        
    except Exception as e:
        logging.error("Error en 'harmony_introd_comprobantes_copiar_documento': %s", e, exc_info=True)
        # Manejo adicional de errores si fuera necesario

# Pasos 7-8
def harmony_introd_comprobantes_anexar_documento_y_comentario(
    driver, 
    pdf_dirs, 
    pdf_filenames, 
    numero_factura, 
    nombre_proveedor, 
    comentario
):
    """
    1) Clic en "Anexos (0)" -> abre 1ra ventana emergente.
    2) "Añadir Anexo" -> abre 2da ventana emergente.
    3) Subir archivo PDF y "Cargar".
    4) Volver a la 1ra ventana emergente, ingresar texto f"-({numero_factura}) {nombre_proveedor}"
       en "PV_ATTACH_WRK_ATTACH_DESCR$0" (si existe) y dar clic en "#ICSave".
    5) Esperar 3s, luego volver a "ptifrmtgtframe" (iframe principal) para
       hacer clic en la sección de comentarios "Coment(0)".
    6) Cambiar al iframe de comentarios y escribir `comentario` en "VOUCHER_DESCR254_MIXED".
    7) Clic en "Acep" para cerrar la ventana de comentarios.
    """

    try:
        logging.info("\n\n\n-x-x-x- (PASOS 7-8) harmony_introd_comprobantes_anexar_documento_y_comentario -x-x-x-\n")

        #
        # == Construir las rutas completas para múltiples PDFs ==
        #
        pdf_paths = []
        for i in range(len(pdf_dirs)):
            ruta_pdf = os.path.join(pdf_dirs[i], pdf_filenames[i])
            pdf_paths.append(ruta_pdf)
            logging.info(f"PDF path #{i+1}: {ruta_pdf}")

        #
        # == 1) Clic en "Anexos (0)" (main page/iframe principal) ==
        #
        logging.info("Haciendo clic en el link 'Anexos (0)'.")
        anexos_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VCHR_HDR_WRK_ATTACHMENTS_PB"))
        )
        anexos_link.click()
        time.sleep(1)

        #
        # == A) Cambiar al iframe de la primera ventana emergente ==
        #
        logging.info("Cambiando al iframe de la primera ventana emergente (Anexos).")
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, '/html/body/div[8]/div[2]/div/div[2]/iframe')
            )
        )


        cantidad_archivos = len(pdf_dirs)
        start_index = 0

        while start_index < cantidad_archivos:
            # 1) Determinar cuántos quedan por subir
            archivos_restantes = cantidad_archivos - start_index
            # 2) Definir bloque de 4 archivos máximo
            bloque_size = min(archivos_restantes, 4)

            logging.info(f"Subiendo bloque de {bloque_size} archivos, desde índice {start_index}.")

            # 3) Clic en "Añadir Anexo" para abrir la segunda ventana (si ya no está abierta)
            logging.info("Haciendo clic en el botón 'Añadir Anexo'.")
            anadir_anexo_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "VCHR_HDR_WRK_ATTACHADD"))
            )
            anadir_anexo_btn.click()
            time.sleep(1)

            # 4) Cambiar al iframe de la segunda ventana emergente
            logging.info("Cambiando al iframe de la segunda ventana emergente (Subir archivo).")
            driver.switch_to.default_content()
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.XPATH, '/html/body/div[8]/div[3]/div/div[2]/iframe')
                )
            )

            logging.info("Subiendo múltiples PDFs en esta ventana emergente.")

            # Definir nombres de los inputs de archivo
            file_input_names = [
                "#ICOrigFileName",
                "#ICOrigFileName1",
                "#ICOrigFileName2",
                "#ICOrigFileName3"
            ]

            # Para este bloque, subimos hasta 'bloque_size' archivos
            for i in range(bloque_size):
                idx = start_index + i
                pdf_path = os.path.join(pdf_dirs[idx], pdf_filenames[idx])
                logging.info(f"Archivo #{idx+1} => {pdf_path}")

                try:
                    input_name = file_input_names[i]  # 0..3
                    file_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, input_name))
                    )
                    file_input.send_keys(pdf_path)
                    logging.info(f"Archivo '{pdf_path}' asignado al input '{input_name}'.")
                except Exception as e:
                    logging.warning(f"No se pudo asignar archivo #{idx+1}: {e}")

            # 5) Clic en el botón "Cargar"
            logging.info("Haciendo clic en el botón 'Cargar'.")
            cargar_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "Upload"))
            )
            cargar_btn.click()

            logging.info("Esperando a que finalice la subida de archivos y se cierre la ventana.")
            time.sleep(8)

            # 6) Volver al primer iframe de "Anexos" para, en caso de que
            #    queden más archivos, repetir el bucle
            driver.switch_to.default_content()
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.XPATH, '/html/body/div[8]/div[2]/div/div[2]/iframe')
                )
            )

            # Avanzar para el siguiente bloque de archivos
            start_index += bloque_size

        logging.info("Se completó la carga de TODOS los PDFs exitosamente.")
        #
        # == C) Volver a la 1ra ventana emergente para ingresar descripción y Aceptar ==
        #
        logging.info("Regresando al iframe de la 1ra ventana emergente (Anexos) para continuar.")
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, '/html/body/div[8]/div[2]/div/div[2]/iframe')
            )
        )

        # Construir la descripción para cada archivo
        texto_anexo = f"f-{numero_factura} {nombre_proveedor}"
        logging.info(f"Texto a ingresar en cada anexo: {texto_anexo}")

        # Supongamos que conoces cuántos anexos (líneas) hay que rellenar.
        # Por ejemplo, si subiste 'n_archivos' con "Añadir Anexo", lo normal es
        # que existan 'n_archivos' líneas. Hasta 5 si son 5 archivos.
        num_lineas = 5  # Ajusta la lógica o determina en función del número real de archivos

        for i in range(num_lineas):
            desc_id = f"PV_ATTACH_WRK_ATTACH_DESCR${i}"
            try:
                logging.info(f"Ingresando descripción en el campo '{desc_id}'...")
                desc_input = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, desc_id))
                )
                desc_input.clear()
                desc_input.send_keys(texto_anexo)
                time.sleep(1)
            except TimeoutException:
                logging.info(f"No se encontró el campo '{desc_id}'. "
                            "La ventana podría tener otra configuración.")
            except Exception as e:
                logging.warning(f"Error asignando descripción en '{desc_id}': {e}")

        # Finalmente, clic en "#ICSave"
        logging.info("Haciendo clic en el botón 'Aceptar' (#ICSave).")
        aceptar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "#ICSave"))
        )
        aceptar_btn.click()

        logging.info("Esperando 3 segundos para que se procese el Aceptar.")
        time.sleep(3)

        #
        # == D) Regresar al iframe principal ptifrmtgtframe y dar clic en 'Coment(0)' ==
        #
        logging.info("Cambiando a default_content y luego al iframe principal 'ptifrmtgtframe'.")
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.ID, "ptifrmtgtframe")  # O el XPATH /html/body/div[4]/div[2]/iframe
            )
        )

        logging.info("Haciendo clic en la sección de comentarios 'Coment(0)'.")
        coment_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VCHR_PANELS_WRK_VCHR_COMMENTS"))
        )
        coment_link.click()
        time.sleep(1)

        #
        # == E) Cambiar al iframe de la ventana emergente de comentarios ==
        #
        logging.info("Regresando a default_content y abriendo el iframe de comentarios.")
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, '/html/body/div[8]/div[2]/div/div[2]/iframe')
            )
        )

        # Ingresar el `comentario`
        logging.info(f"Ingresando comentario: {comentario}")
        textarea_coment = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "VOUCHER_DESCR254_MIXED"))
        )
        textarea_coment.clear()
        textarea_coment.send_keys(comentario)
        time.sleep(1)

        # Botón "Acep" (VCHR_PANELS_WRK_OK_PB)
        logging.info("Haciendo clic en el botón 'Acep' de la ventana de comentarios.")
        btn_coment_acep = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VCHR_PANELS_WRK_OK_PB"))
        )
        btn_coment_acep.click()
        time.sleep(1)

        logging.info("Función 'harmony_introd_comprobantes_anexar_documento' finalizada con éxito.")

    except Exception as e:
        logging.error("Error en 'harmony_introd_comprobantes_anexar_documento': %s", e, exc_info=True)
        # Manejo adicional de errores si fuera necesario

# Pasos 9-10
def harmony_introd_comprobantes_pagos_y_retencion(driver, fecha_factura, total_retencion_por_articulo, porcentaje_retencion):
    """
    1. Cambiar al iframe "ptifrmtgtframe".
    2. Localizar la pestaña 'Pagos' (id=ICTAB_1), hacer scroll y dar clic.
    3. Esperar 4s a que cargue la pestaña.
    4. Calcular fecha de pago (viernes a partir de +30 días).
    5. Ingresar la fecha en 'PYMNT_VCHR_XREF_SCHEDULED_PAY_DT$0'.
    6. Volver a la pestaña 'Información sobre Factura' (id=ICTAB_0), esperar 3s.
    7. Clic en 'Retención' (id=VCHR_HDR_WRK_XFR_WTHD_PB) => Carga la vista de retención.
    8. LEER "X de Y" en '//*[@id="win0div$ICField$4$GP$0"]/table/tbody/tr/td[2]/span[2]' 
       y, para cada página i en [0..(Y-1)]:
         - Completar 2 inputs (VCHR_LINE_WTHD_WTHD_RULE$0 y $1) con 2 valores de 'porcentaje_retencion'
         - Si i < Y-1 => clic en "Siguiente" ($ICField$4$$hdown$0) y espera 3s
    9. Clic en "Volver a Factura" (id=VCHR_PANELS_WRK_GOTO_VCHR_HDR) y esperar 3s.
    """

    try:
        logging.info("\n\n\n-x-x-x- (PASOS 9-10) harmony_introd_comprobantes_pagos_y_retencion -x-x-x-\n")

        # [1] Cambiar al iframe principal
        driver.switch_to.default_content()
        logging.info("Cambiando al iframe principal 'ptifrmtgtframe'.")
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "ptifrmtgtframe"))
        )
        time.sleep(2)

        # [2] Localizar la pestaña 'Pagos' (a#ICTAB_1)
        logging.info("Localizando la pestaña 'Pagos' (a#ICTAB_1).")
        pagos_link = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "ICTAB_1"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", pagos_link)
        time.sleep(2)

        # Clic normal / fallback JS
        try:
            logging.info("Intentando clic Selenium en 'Pagos'.")
            pagos_link.click()
            time.sleep(1)
        except (ElementClickInterceptedException, TimeoutException) as e:
            logging.warning(f"Clic normal en 'Pagos' falló: {e}")
            logging.info("Intentando clic JS en 'Pagos'.")
            driver.execute_script("arguments[0].click();", pagos_link)
            time.sleep(1)

        # [3] Esperar 4s para cargar la pestaña
        logging.info("Esperando 4 segundos para que se cargue la pestaña 'Pagos'.")
        time.sleep(4)

        # [4] Calcular fecha de pago (+30 dias +viernes)
        parsed_date = datetime.strptime(fecha_factura, "%m/%d/%Y") # Lectura de la fecha con formato en inglés
        nueva_fecha = parsed_date + timedelta(days=30)
        while nueva_fecha.weekday() != 4:  # Friday=4
            nueva_fecha += timedelta(days=1)
        fecha_pago = nueva_fecha.strftime("%m/%d/%Y") # Fecha nueva con formato en español
        logging.info(f"Fecha de pago calculada (viernes): {fecha_pago}")

        # [5] Ingresar la fecha en 'PYMNT_VCHR_XREF_SCHEDULED_PAY_DT$0'
        fecha_input = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "PYMNT_VCHR_XREF_SCHEDULED_PAY_DT$0"))
        )
        fecha_input.clear()
        fecha_input.send_keys(fecha_pago)
        time.sleep(1)


        # [6] Volver a 'Información sobre Factura' (a#ICTAB_0)
        factura_tab = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "ICTAB_0"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", factura_tab)
        time.sleep(1)
        try:
            factura_tab.click()
            time.sleep(1)
        except (ElementClickInterceptedException, TimeoutException) as e:
            driver.execute_script("arguments[0].click();", factura_tab)
            time.sleep(1)

        logging.info("Esperando 3 segundos para que se cargue la pestaña 'Información sobre Factura'.")
        time.sleep(3)

        # [7] Clic en 'Retención' (id=VCHR_HDR_WRK_XFR_WTHD_PB)
        retencion_link = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "VCHR_HDR_WRK_XFR_WTHD_PB"))
        )
        try:
            retencion_link.click()
            time.sleep(1)
        except (ElementClickInterceptedException, TimeoutException) as e:
            driver.execute_script("arguments[0].click();", retencion_link)
            time.sleep(1)

        logging.info("Vista de Retención cargada (dentro del mismo iframe principal).")

        # [8] ITERAR páginas de Retención
        #     1) Leer "X de Y" en '//*[@id="win0div$ICField$4$GP$0"]/table/tbody/tr/td[2]/span[2]'
        #        => Y = total de páginas
        #     2) Para i en [0..Y-1], llenar 2 inputs de "porcentaje_retencion" (VCHR_LINE_WTHD_WTHD_RULE$0/$1)
        #        y 2 inputs de "total_retencion_por_articulo" (VCHR_LINE_WTHD_WTHD_BASIS_AMT$0/$1).
        #        Luego, si i < Y-1 => clic en "Siguiente".

        logging.info("Leyendo cantidad de páginas de retención en 'win0div$ICField$4$GP$0'...")

        # --- Asegurar que 'porcentaje_retencion' sea una tupla/lista ---
        if isinstance(porcentaje_retencion, str):
            logging.info(f"'porcentaje_retencion' llegó como cadena: '{porcentaje_retencion}'")
            if porcentaje_retencion.strip():
                porcentaje_retencion = (porcentaje_retencion,)
            else:
                porcentaje_retencion = ()

        # --- Asegurar que 'total_retencion_por_articulo' sea tupla/lista ---
        if isinstance(total_retencion_por_articulo, str):
            logging.info(f"'total_retencion_por_articulo' llegó como cadena: '{total_retencion_por_articulo}'")
            if total_retencion_por_articulo.strip():
                total_retencion_por_articulo = (total_retencion_por_articulo,)
            else:
                total_retencion_por_articulo = ()

        try:
            txt_pages = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="win0div$ICField$4$GP$0"]/table/tbody/tr/td[2]/span[2]')
                )
            ).text  # Ejemplo: "1 de 3"
        except TimeoutException:
            logging.warning("No se encontró '1 de X' en retención. Asumimos 1 de 1.")
            txt_pages = "1 de 1"

        # Parsear Y
        try:
            partes = txt_pages.split(" de ")
            total_pages = int(partes[1])
        except (IndexError, ValueError):
            logging.warning(f"No se pudo parsear '{txt_pages}'. Asumimos 1 de 1.")
            total_pages = 1

        logging.info(
            f"Hay {total_pages} página(s) de retención. "
            f"La lista de retenciones tiene {len(porcentaje_retencion)} elementos. "
            f"La lista de totales tiene {len(total_retencion_por_articulo)} elementos."
        )

        ret_index = 0
        for i in range(total_pages):
            logging.info(f"== Retención - Página {i+1} de {total_pages} ==")

            for sub_idx in range(2):  # 0..1
                logging.info(f"Procesando sub_idx = {sub_idx}, ret_index = {ret_index}")

                # 1) Porcentaje de retención
                rule_input_id = f"VCHR_LINE_WTHD_WTHD_RULE${sub_idx}"
                try:
                    logging.info(f"Buscando el input de porcentaje '{rule_input_id}'...")
                    rule_input = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID, rule_input_id))
                    )
                    logging.info(f"Encontrado '{rule_input_id}'. Haciendo .clear()")
                    rule_input.clear()
                    time.sleep(1.5)

                    if ret_index < len(porcentaje_retencion):
                        valor_porcentaje = porcentaje_retencion[ret_index]
                        logging.info(f"Ingresando valor '{valor_porcentaje}' en '{rule_input_id}'...")
                        rule_input.send_keys(valor_porcentaje)
                        logging.info(f"Asignado '{valor_porcentaje}' en {rule_input_id}.")
                    else:
                        logging.info(f"No hay más elementos en porcentaje_retencion. Dejando '{rule_input_id}' en blanco.")
                except TimeoutException:
                    logging.warning(f"No se encontró el campo '{rule_input_id}'. No se pudo ingresar retención.")
                    break
                except StaleElementReferenceException as e:
                    logging.warning(f"StaleElementReference al interactuar con '{rule_input_id}': {e}")
                    break

                # Espera un poco tras ingresar la retención (PeopleSoft refresca a veces).
                time.sleep(2)

                # 2) Total retención por artículo
                basis_input_id = f"VCHR_LINE_WTHD_WTHD_BASIS_AMT${sub_idx}"

                # Mecanismo de reintento para posible "stale element reference"
                reintentos = 3
                while reintentos > 0:
                    try:
                        logging.info(f"Intentando localizar '{basis_input_id}' (reintentos={reintentos})")
                        basis_input = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.ID, basis_input_id))
                        )
                        logging.info(f"Encontrado '{basis_input_id}'. Haciendo scrollIntoView...")
                        driver.execute_script("arguments[0].scrollIntoView(true);", basis_input)
                        time.sleep(1)

                        logging.info("Haciendo click() en basis_input...")
                        basis_input.click()
                        time.sleep(1)

                        logging.info("Haciendo clear() en basis_input...")
                        basis_input.clear()
                        time.sleep(1)

                        if ret_index < len(total_retencion_por_articulo):
                            valor_total = total_retencion_por_articulo[ret_index]
                            logging.info(f"Ingresando valor '{valor_total}' en '{basis_input_id}'...")
                            basis_input.send_keys(valor_total)
                            logging.info(f"Asignado '{valor_total}' en {basis_input_id}.")
                        else:
                            logging.info(f"No hay más elementos en total_retencion_por_articulo. "
                                        f"Dejando '{basis_input_id}' en blanco.")

                        # Si todo va bien, rompemos el while
                        break
                    except StaleElementReferenceException as e:
                        logging.warning(f"STALE reference en '{basis_input_id}': {e}. Reintentando...")
                        reintentos -= 1
                        time.sleep(2)
                    except TimeoutException:
                        logging.warning(f"No se encontró el campo '{basis_input_id}'. No se pudo ingresar el total.")
                        break
                    except Exception as ex:
                        logging.warning(f"Error inesperado con '{basis_input_id}': {ex}")
                        break

                # Avanzar al siguiente índice en ambas listas
                ret_index += 1
                time.sleep(1)

            # Si no es la última página => clic en Siguiente
            if i < (total_pages - 1):
                logging.info(f"Página {i+1} completada. Avanzando a la página {i+2} de retención.")
                try:
                    btn_siguiente = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="$ICField$4$$hdown$0"]'))
                    )
                    btn_siguiente.click()
                    time.sleep(3)
                except TimeoutException:
                    logging.warning("No se encontró el botón 'Siguiente' en retención. Abortando.")
                    break


        # [9] Clic en "Volver a Factura" (id=VCHR_PANELS_WRK_GOTO_VCHR_HDR)
        logging.info("Presionando 'Volver a Factura' para regresar a la pantalla anterior.")
        volver_factura_link = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "VCHR_PANELS_WRK_GOTO_VCHR_HDR"))
        )
        try:
            volver_factura_link.click()
            time.sleep(1)
        except (ElementClickInterceptedException, TimeoutException) as e:
            logging.warning(f"Clic en 'Volver a Factura' falló: {e}")
            driver.execute_script("arguments[0].click();", volver_factura_link)

        logging.info("Esperando 3 segundos para que se cargue la pantalla anterior...")
        time.sleep(3)

        logging.info("Función 'harmony_introd_comprobantes_pagos' finalizada correctamente.")


    except Exception as e:
        logging.error("Error en 'harmony_introd_comprobantes_pagos': %s", e, exc_info=True)
        # Manejo adicional de errores si fuera necesario

# Pasos 11-12
def harmony_introd_comprobantes_descripcion_e_iva(driver, descripciones, ivas):
    """
    Ingreso de descripciones e IVA para cada artículo de la factura.
    Se replica la forma de acceder a ventanas emergentes,
    igual que en la función de anexar documentos y comentarios.

    Pasos:
      1) Lee "X de Y" (ej. "1 de 3") para saber cuántos artículos hay (Y).
      2) Para i en [0..Y-1] (o hasta min(Y, len(descripciones), len(ivas))):
         a) Escribe descripciones[i] en VOUCHER_LINE_DESCR$0
         b) Clic en "IVA Línea Factura" -> abre ventana emergente
            - Esperar 3s
            - switch_to.default_content()
            - Cambiar al iframe emergente con XPATH '/html/body/div[8]/div[2]/div/div[2]/iframe'
            - **Clic en "Contraer Todas Secciones"** (nuevo)
            - Clic en la flecha "VAT_LABEL_WRK_VAT_DETAILS" para (des)plegar la sección
            - Espera 2s
            - Escribe ivas[i] en 'VAT_FIELDS_WRK_TAX_CD_VAT'
            - Clic en "Ir a Línea Factura" -> cierra la ventana
            - Regresar a default_content() -> ptifrmtgtframe
         c) Si i < último, clic en "Siguiente" y esperar 3s
    """

    logging.info("\n\n\n-x-x-x- (PASOS 11-12) harmony_introd_comprobantes_descripcion_e_iva -x-x-x-\n")

    # --- Asegurar que 'descripciones' sea tupla/lista ---
    if isinstance(descripciones, str):
        logging.info(f"Se recibió 'descripciones' como cadena: '{descripciones}'")
        if descripciones.strip():
            descripciones = (descripciones,)
        else:
            descripciones = ()
    else:
        logging.info(f"'descripciones' es lista/tupla con {len(descripciones)} elemento(s).")

    # --- Asegurar que 'ivas' sea tupla/lista ---
    if isinstance(ivas, str):
        logging.info(f"Se recibió 'ivas' como cadena: '{ivas}'")
        if ivas.strip():
            ivas = (ivas,)
        else:
            ivas = ()
    else:
        logging.info(f"'ivas' es lista/tupla con {len(ivas)} elemento(s).")
        
    # --- Paso previo: Ir a la primera página ---
    try:
        # Localizar el botón "Primero"
        primero_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="$ICField1$htop$0"]'))
        )
        # Hacer scroll
        driver.execute_script("arguments[0].scrollIntoView(true);", primero_btn)
        time.sleep(1)

        # Clic en "Primero"
        primero_btn.click()
        logging.info("Clic en 'Primero' para regresar a la primera página de artículos.")
    except TimeoutException:
        logging.warning("No se encontró el botón 'Primero'. Continuamos de todas formas.")

    # Esperar 2s tras presionar "Primero"
    time.sleep(2)

    # 1) Leer "X de Y" (ej. "1 de 3")
    try:
        texto_items = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="win0div$ICField1GP$0"]/table/tbody/tr/td[2]/span[2]')
            )
        ).text  # Ej. "1 de 3"
    except TimeoutException:
        logging.warning("No se encontró 'X de Y' al inicio. Se asume '1 de 1'.")
        texto_items = "1 de 1"

    # Parsear Y
    try:
        partes = texto_items.split(" de ")
        Y = int(partes[1])
    except (IndexError, ValueError):
        logging.warning(f"No se pudo parsear '{texto_items}'. Se asume 1 de 1.")
        Y = 1

    n_desc = len(descripciones)
    n_ivas = len(ivas)
    max_articulos = min(Y, n_desc, n_ivas)

    logging.info(
        f"La página indica {Y} artículo(s). Hay {n_desc} descripciones y {n_ivas} IVAs. "
        f"Se llenarán {max_articulos} artículo(s)."
    )

    if max_articulos == 0:
        logging.info("max_articulos = 0. Nada por llenar. Terminando función.")
        return

    # 2) Iterar sobre cada artículo
    for i in range(max_articulos):
        desc = descripciones[i]
        iva_val = ivas[i]
        logging.info(f"== ARTÍCULO {i+1} de {max_articulos} ==")

        # 2.a) Ingresar la descripción en VOUCHER_LINE_DESCR$0
        try:
            desc_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "VOUCHER_LINE_DESCR$0"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", desc_input)
            time.sleep(1)
            desc_input.clear()
            desc_input.send_keys(desc)
            logging.info(f"Descripción '{desc}' ingresada en VOUCHER_LINE_DESCR$0.")
        except TimeoutException:
            logging.error("No se encontró el campo 'VOUCHER_LINE_DESCR$0'. Terminando.")
            break

        # 2.b) Clic en "IVA Línea Factura"
        try:
            iva_linea_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="VCHR_PANELS_WK1_VAT_PB$0"]'))
            )
            iva_linea_link.click()
            logging.info("Clic en 'IVA Línea Factura'. Se abre ventana emergente.")
        except (TimeoutException, ElementClickInterceptedException) as e:
            logging.warning(f"No se pudo hacer clic en 'IVA Línea Factura': {e}")
            break

        # Esperar 3s a que aparezca la ventana emergente
        time.sleep(3)

        # Salir al contenido principal
        driver.switch_to.default_content()

        # Cambiar al iframe emergente con la ruta
        try:
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.XPATH, '/html/body/div[8]/div[2]/div/div[2]/iframe')
                )
            )
            logging.info("Dentro del iframe emergente para Detalles IVA.")
        except TimeoutException:
            logging.error("No se pudo cambiar al iframe emergente. Terminando.")
            break

        # (Nuevo) Clic en "Contraer Todas Secciones"
        # XPATH: '//*[@id="win0divVAT_SUBPAGE_WRK_COLLAPSE_SECTIONS"]/a'
        try:
            contraer_secciones_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="win0divVAT_SUBPAGE_WRK_COLLAPSE_SECTIONS"]/a'))
            )
            contraer_secciones_btn.click()
            logging.info("Clic en 'Contraer Todas Secciones'.")
        except TimeoutException:
            logging.warning("No se encontró el botón 'Contraer Todas Secciones'. Continuamos de todas formas.")

        time.sleep(1)  # Breve espera tras contraer secciones

        # Flecha "VAT_LABEL_WRK_VAT_DETAILS"
        try:
            detalles_iva_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "VAT_LABEL_WRK_VAT_DETAILS"))
            )
            detalles_iva_btn.click()
            logging.info("Clic en la flecha 'VAT_LABEL_WRK_VAT_DETAILS' (Detalles IVA).")
        except TimeoutException:
            logging.warning("No se encontró 'VAT_LABEL_WRK_VAT_DETAILS'.")
        time.sleep(2)

        # Ingresar el IVA en "VAT_FIELDS_WRK_TAX_CD_VAT"
        try:
            iva_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="VAT_FIELDS_WRK_TAX_CD_VAT"]'))
            )
            iva_input.clear()
            iva_input.send_keys(str(iva_val))
            logging.info(f"IVA '{iva_val}' ingresado en 'VAT_FIELDS_WRK_TAX_CD_VAT'.")
        except TimeoutException:
            logging.warning("No se encontró 'VAT_FIELDS_WRK_TAX_CD_VAT'. No se pudo ingresar el IVA.")

        # Clic en "Ir a Línea Factura"
        try:
            volver_linea_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="VCHR_PANELS_WK1_GOTO_VCHRLN"]'))
            )
            volver_linea_btn.click()
            logging.info("Clic en 'Ir a Línea Factura' para regresar al iframe principal.")
        except TimeoutException:
            logging.warning("No se encontró 'Ir a Línea Factura'. No se pudo regresar.")
            break

        # Regresamos a default_content y luego al iframe principal
        driver.switch_to.default_content()
        # ... luego de "Ir a Línea Factura" y driver.switch_to.default_content()

        try:
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "ptifrmtgtframe"))
            )
            logging.info("Regresando al iframe principal 'ptifrmtgtframe'.")
        except TimeoutException:
            logging.error("No se pudo volver al iframe principal. Terminando.")
            break

        # Espera extra para que PeopleSoft termine de dibujar la página
        time.sleep(2)

        if i < max_articulos - 1:
            logging.info(f"Artículo {i+1} completado. Avanzando al siguiente (i={i+1}).")
            
            # Localizar el botón “Siguiente” con WebDriverWait
            try:
                btn_siguiente = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="$ICField1$hdown$0"]'))
                )
                btn_siguiente.click()
                logging.info("Botón 'Siguiente' presionado. Esperando 3s...")
                time.sleep(3)
            except TimeoutException:
                logging.warning("No se encontró el botón 'Siguiente'. No se puede avanzar.")
                break


    logging.info("Función 'harmony_introd_comprobantes_descripcion_e_iva' finalizada correctamente.")

# Paso 13
def harmony_introd_comprobantes_guardar(driver):
    """
    1) Scroll al botón 'Guardar' (//*[@id="win0divVCHR_PANELS_WRK_VCHR_SAVE_PB"]/a) y clic.
    2) Espera 3s.
    3) Clic en el botón final 'Guardar' (#ICSave).
    """

    try:
        logging.info("\n\n\n-x-x-x- (PASO 13) harmony_introd_comprobantes_comprobantes_guardar -x-x-x-\n")
        # 1) Ubicar y hacer scroll al botón "Guardar" (VCHR_PANELS_WRK_VCHR_SAVE_PB)
        primer_guardar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="win0divVCHR_PANELS_WRK_VCHR_SAVE_PB"]/a'))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", primer_guardar_btn)
        time.sleep(1)
        primer_guardar_btn.click()
        logging.info("Clic en el primer botón 'Guardar' (VCHR_PANELS_WRK_VCHR_SAVE_PB).")

    except TimeoutException:
        logging.warning("No se encontró el primer botón 'Guardar' (VCHR_PANELS_WRK_VCHR_SAVE_PB). Continuamos sin él.")

    # 2) Esperar 3s tras presionar el primer botón
    logging.info("Esperando 3 segundos tras el primer 'Guardar'...")
    time.sleep(3)

    try:
        # 3) Clic en el botón final 'Guardar' (#ICSave)
        guardar_final_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "#ICSave"))
        )
        guardar_final_btn.click()
        logging.info("Clic en el botón final 'Guardar' (#ICSave).")

    except TimeoutException:
        logging.warning("No se encontró el botón final '#ICSave'. No se pudo guardar definitivamente.")

    logging.info("Función 'harmony_introd_comprobantes_guardar' finalizada correctamente.")

