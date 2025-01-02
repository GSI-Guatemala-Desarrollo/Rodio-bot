import time
import logging
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from datetime import datetime, timedelta

def harmony_introd_comprobantes_agregar_factura(driver, proveedor_id, no_factura, fecha_factura):
    """
    Ingresa al iframe principal (ptifrmtgtframe), llena los 3 campos
    y finaliza dando clic en el botón 'Añadir'.
    """

    try:
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
        logging.info("Iniciando 'harmony_introd_comprobantes_copiar_documento'...")
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
        input_uni_po.send_keys(uni_po)

        # 5. Ingresar número de pedido
        logging.info(f"Ingresando Número de Pedido: {no_pedido}")
        input_no_pedido = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "VCHR_PANELS_WRK_PO_ID"))
        )
        input_no_pedido.clear()
        input_no_pedido.send_keys(no_pedido)

        # 6. Clic en el botón 'Buscar'
        logging.info("Dando clic en el botón 'Buscar'.")
        btn_buscar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VCHR_PANELS_WRK_PB_GET_PO"))
        )
        time.sleep(1)
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
        #     - Removemos las comas de miles y reemplazamos comas decimales si fuera necesario
        #     - Ojo que Peoplesoft a veces muestra algo como "4,651.78" (coma para miles, punto para decimales)
        #       Simplemente removemos las comas y convertimos a float
        amount_no_commas = gross_amount_text.replace(",", "")  # "4651.78"
        try:
            gross_amount_float = float(amount_no_commas)
        except ValueError:
            logging.error("No se pudo parsear el valor bruto de la factura a float. Se usará 0.")
            gross_amount_float = 0.0

        #     Calculamos el IVA: (gross_amount * iva_percent) / 100
        iva_calculado = (gross_amount_float * iva_percent) / 100.0
        logging.info(f"IVA calculado: {iva_calculado:.2f} (usando {iva_percent}% de {gross_amount_float:.2f})")

        # 13. Ingresar el IVA en VOUCHER_VAT_ENTRD_AMT
        logging.info("Ingresando el valor del IVA en 'VOUCHER_VAT_ENTRD_AMT'.")
        vat_amount_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VOUCHER_VAT_ENTRD_AMT"))
        )
        vat_amount_element.clear()
        # Formateamos el IVA con dos decimales (o según tu caso). Ej: "465.18"
        vat_amount_element.send_keys(f"{iva_calculado:,.2f}")
        time.sleep(1)

        # 14. Ingresar número de factura y número de serie
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

    except Exception as e:
        logging.error("Error en 'harmony_introd_comprobantes_copiar_documento': %s", e, exc_info=True)
        # Manejo adicional de errores si fuera necesario

def harmony_introd_comprobantes_anexar_documento_y_comentario(
    driver, 
    pdf_dir, 
    pdf_filename, 
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
        logging.info("Iniciando 'harmony_introd_comprobantes_anexar_documento'...")

        # Ruta completa del PDF
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        logging.info(f"PDF path: {pdf_path}")

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

        #
        # == 2) "Añadir Anexo" (1ra ventana emergente) ==
        #
        logging.info("Haciendo clic en el botón 'Añadir Anexo'.")
        anadir_anexo_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VCHR_HDR_WRK_ATTACHADD"))
        )
        anadir_anexo_btn.click()
        time.sleep(1)

        #
        # == B) Cambiar al iframe de la segunda ventana emergente ==
        #
        logging.info("Cambiando al iframe de la segunda ventana emergente (Subir archivo).")
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, '/html/body/div[8]/div[3]/div/div[2]/iframe')
            )
        )

        #
        # == 3) Subir el PDF y "Cargar" ==
        #
        logging.info("Localizando <input type='file'> y enviando la ruta del PDF.")
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="win0divPSTOOLSHIDDENS"]/input[1]'))
        )
        file_input.send_keys(pdf_path)

        logging.info("Haciendo clic en el botón 'Cargar'.")
        cargar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "Upload"))
        )
        cargar_btn.click()

        logging.info("Esperando 3 seg a que finalice la subida y se cierre la ventana.")
        time.sleep(3)

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

        # 4) Ingresar texto f"-({numero_factura}) {nombre_proveedor}" en PV_ATTACH_WRK_ATTACH_DESCR$0 (si existe)
        logging.info("Ingresando la descripción del anexo (factura y proveedor).")
        try:
            desc_anexo_input = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "PV_ATTACH_WRK_ATTACH_DESCR$0"))
            )
            texto_anexo = f"f-{numero_factura} {nombre_proveedor}"
            logging.info(f"Texto a ingresar en anexo: {texto_anexo}")
            desc_anexo_input.clear()
            desc_anexo_input.send_keys(texto_anexo)
            time.sleep(1)
        except TimeoutException:
            logging.info("No se encontró el campo 'PV_ATTACH_WRK_ATTACH_DESCR$0'. "
                         "La ventana podría tener otra configuración.")

        # Clic en "#ICSave"
        logging.info("Haciendo clic en el botón 'Aceptar' (#ICSave).")
        aceptar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "#ICSave"))
        )
        aceptar_btn.click()

        #
        # == Esperar 3s para permitir que la ventana regrese a la página principal ==
        #
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


def harmony_introd_comprobantes_pagos(driver, fecha_factura):
    """
    1. Volver a default_content, cambiar al iframe "ptifrmtgtframe".
    2. Localizar el <a id="ICTAB_1"> (la pestaña 'Pagos') y hacer scroll.
    3. Intentar clic normal con Selenium y, si no funciona, clic por JavaScript.
    4. Esperar 4s a que cargue la pestaña de 'Pagos'.
    5. Calcular fecha de pago (viernes después de +30 días).
    6. Ingresar la fecha en "PYMNT_VCHR_XREF_SCHEDULED_PAY_DT$0".
    7. Regresar a la pestaña anterior (ID="ICTAB_0").
    8. Esperar 3s.
    9. Clic en "Retención" (ID="VCHR_HDR_WRK_XFR_WTHD_PB") para cargar nueva vista.
    """

    try:
        logging.info("Iniciando 'harmony_introd_comprobantes_pagos'...")

        #
        # [1] Asegurarse de estar en el iframe principal
        #
        driver.switch_to.default_content()
        logging.info("Cambiando al iframe principal 'ptifrmtgtframe'.")
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "ptifrmtgtframe"))
        )
        time.sleep(2)

        #
        # [2] Localizar la pestaña 'Pagos' (a#ICTAB_1)
        #
        logging.info("Localizando la pestaña 'Pagos' (id=ICTAB_1).")
        pagos_link = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "ICTAB_1"))
        )

        # Scroll
        logging.info("Haciendo scroll hasta la pestaña 'Pagos'.")
        driver.execute_script("arguments[0].scrollIntoView(true);", pagos_link)
        time.sleep(2)

        #
        # [3] Clic normal, fallback JS
        #
        try:
            logging.info("Intentando clic normal con Selenium en 'Pagos' (a#ICTAB_1).")
            pagos_link.click()
            time.sleep(1)
        except (ElementClickInterceptedException, TimeoutException) as e:
            logging.warning(f"El clic normal en 'Pagos' falló: {e}")
            logging.info("Intentando clic JS en 'Pagos' (a#ICTAB_1).")
            driver.execute_script("arguments[0].click();", pagos_link)
            time.sleep(1)

        #
        # [4] Esperar 4s a que cargue la pestaña
        #
        logging.info("Esperando 4 segundos para que se cargue la pestaña 'Pagos'.")
        time.sleep(4)

        #
        # [5] Calcular fecha de pago (viernes)
        #
        logging.info(f"Calculando fecha de pago a partir de la factura: {fecha_factura}")
        parsed_date = datetime.strptime(fecha_factura, "%d/%m/%Y")
        nueva_fecha = parsed_date + timedelta(days=30)
        while nueva_fecha.weekday() != 4:  # Friday=4
            nueva_fecha += timedelta(days=1)
        fecha_pago = nueva_fecha.strftime("%d/%m/%Y")
        logging.info(f"Fecha de pago calculada (viernes): {fecha_pago}")

        #
        # [6] Ingresar fecha en "PYMNT_VCHR_XREF_SCHEDULED_PAY_DT$0"
        #
        logging.info("Localizando e ingresando la fecha de pago en 'PYMNT_VCHR_XREF_SCHEDULED_PAY_DT$0'.")
        fecha_input = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "PYMNT_VCHR_XREF_SCHEDULED_PAY_DT$0"))
        )
        fecha_input.clear()
        fecha_input.send_keys(fecha_pago)
        time.sleep(1)

        #
        # [7] Regresar a la pestaña anterior: "ICTAB_0" (Información sobre Factura)
        #
        logging.info("Regresando a la pestaña anterior 'Información sobre Factura' (id=ICTAB_0).")
        info_factura_link = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "ICTAB_0"))
        )

        # Scroll y clic
        logging.info("Haciendo scroll hasta la pestaña 'Información sobre Factura'.")
        driver.execute_script("arguments[0].scrollIntoView(true);", info_factura_link)
        time.sleep(2)

        try:
            logging.info("Intentando clic normal con Selenium en 'Información sobre Factura' (a#ICTAB_0).")
            info_factura_link.click()
            time.sleep(1)
        except (ElementClickInterceptedException, TimeoutException) as e:
            logging.warning(f"El clic normal en 'Información sobre Factura' falló: {e}")
            logging.info("Intentando clic JS en 'Información sobre Factura' (a#ICTAB_0).")
            driver.execute_script("arguments[0].click();", info_factura_link)
            time.sleep(1)

        #
        # [8] Esperar 3s
        #
        logging.info("Esperando 3 segundos para que la pestaña 'Información sobre Factura' se cargue.")
        time.sleep(3)

        #
        # [9] Clic en "Retención" (ID="VCHR_HDR_WRK_XFR_WTHD_PB")
        #
        logging.info("Dando clic en 'Retención' (VCHR_HDR_WRK_XFR_WTHD_PB).")
        retencion_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "VCHR_HDR_WRK_XFR_WTHD_PB"))
        )

        # Scroll y clic
        logging.info("Haciendo scroll hasta el link 'Retención'.")
        driver.execute_script("arguments[0].scrollIntoView(true);", retencion_link)
        time.sleep(1)

        try:
            logging.info("Intentando clic normal con Selenium en 'Retención'.")
            retencion_link.click()
            time.sleep(1)
        except (ElementClickInterceptedException, TimeoutException) as e:
            logging.warning(f"El clic normal en 'Retención' falló: {e}")
            logging.info("Intentando clic JS en 'Retención'.")
            driver.execute_script("arguments[0].click();", retencion_link)
            time.sleep(1)

        logging.info("Función 'harmony_introd_comprobantes_pagos' finalizada correctamente.")

    except Exception as e:
        logging.error("Error en 'harmony_introd_comprobantes_pagos': %s", e, exc_info=True)
        # Manejo adicional de errores si fuera necesario