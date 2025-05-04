import logging
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import shutil

def sat_emision_constancias_de_retencion_busqueda_parametros(
    driver,
    EMISION_CONSTANCIAS_EMISION_DEL,
    EMISION_CONSTANCIAS_EMISION_AL,
    EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA,
    EMISION_CONSTANCIAS_REGIMEN,
    EMISION_CONSTANCIAS_TIPO_DOCUMENTO,
    EMISION_CONSTANCIAS_NIT_RETENIDO,
    EMISION_CONSTANCIAS_NO_AUTORIZACION_FEL,
    EMISION_CONSTANCIAS_SERIE_DE_FACTURA,
    EMISION_CONSTANCIAS_NO_DE_FACTURA,
):
    try:
        _ = driver.title
    except Exception as e:
        logging.info("El navegador no está disponible. Se detiene la ejecución de la función.")
        return
    
    logging.info(f"\n\n\n-x-x-x- (PASOS 8-10) sat_emision_constancias_de_retencion_busqueda_parametros -x-x-x-\n")
    # Esperar a que cargue la tabla.
    time.sleep(3)
    EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA = EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA - 1
    EMISION_CONSTANCIAS_REGIMEN = EMISION_CONSTANCIAS_REGIMEN - 1
    EMISION_CONSTANCIAS_TIPO_DOCUMENTO = EMISION_CONSTANCIAS_TIPO_DOCUMENTO - 1
            
    # Verificar si el elemento está dentro de un iframe
    try:
        driver.switch_to.default_content()
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            driver.switch_to.frame(iframe)
            if driver.find_elements(
                By.XPATH, "//input[contains(@id, 'itDel_input')]"
            ):
                logging.info(
                    "Elemento encontrado dentro del iframe, cambiando de contexto."
                )
                break
            driver.switch_to.default_content()
    except Exception as e:
        logging.warning(f"No se encontró el elemento en ningún iframe. Error: {e}")
    
    # EMISION DEL:
    if EMISION_CONSTANCIAS_EMISION_DEL.strip():
        try:

            # Intentar localizar y hacer click en el input usando XPath relativo
            input_xpath_relativo = "//span/input[contains(@id, 'itDel_input')]"
            boton_xpath_relativo = (
                "//span/button[contains(@class, 'ui-datepicker-trigger')]"
            )

            elementos_encontrados = driver.find_elements(By.XPATH, input_xpath_relativo)

            fecha_input = None
            try:
                fecha_input = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, input_xpath_relativo))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", fecha_input)
                time.sleep(1)  # Pausa para asegurar visibilidad
                fecha_input.click()
            except Exception as e:
                logging.warning(
                    f"No se pudo hacer click en el input. Intentando con el botón. Error: {e}"
                )

            # Intentar localizar y hacer click en el botón usando XPath relativo
            if fecha_input is None:
                try:
                    boton_calendario = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, boton_xpath_relativo))
                    )
                    driver.execute_script(
                        "arguments[0].scrollIntoView(true);", boton_calendario
                    )
                    time.sleep(1)  # Pausa para asegurar visibilidad
                    boton_calendario.click()
                except Exception as e:
                    logging.warning(
                        f"No se pudo hacer click en el botón con XPath relativo. Error: {e}"
                    )

            # Dividir la fecha en día, mes y año
            dia, mes, anio = EMISION_CONSTANCIAS_EMISION_DEL.split("/")

            if dia.startswith("0"):
                dia = dia[1:]

            # Seleccionar año
            select_anio = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ui-datepicker-year"))
            )
            Select(select_anio).select_by_visible_text(anio)

            # Seleccionar mes
            select_mes = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ui-datepicker-month"))
            )
            Select(select_mes).select_by_index(int(mes) - 1)

            # Seleccionar día
            calendario_tabla = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ui-datepicker-calendar"))
            )
            dias = calendario_tabla.find_elements(By.TAG_NAME, "td")
            for dia_elemento in dias:
                if dia_elemento.text == dia and dia_elemento.is_enabled():
                    dia_elemento.click()
                    break

            logging.info(f"Fecha EMISIÓN DEL '{EMISION_CONSTANCIAS_EMISION_DEL}' seleccionada correctamente.")
            time.sleep(1)

        except Exception as e:
            logging.error(f"Error al seleccionar la fecha EMISIÓN DEL: {e}")
    else:
        logging.info("La variable EMISION_CONSTANCIAS_EMISION_DEL está vacía, se omite la selección de fecha DEL.")

    # EMISION AL (opcional)
    if EMISION_CONSTANCIAS_EMISION_AL.strip():
        try:
            input_al_xpath_relativo = "//span/input[contains(@id, 'itAl_input')]"
            fecha_input_al = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, input_al_xpath_relativo))
            )

            # Desplazamos el elemento a la vista si es necesario
            driver.execute_script("arguments[0].scrollIntoView(true);", fecha_input_al)
            time.sleep(1)  # Pequeña espera para estabilidad

            # Eliminamos los '/' de la fecha
            fecha_sin_slash = EMISION_CONSTANCIAS_EMISION_AL.replace("/", "")

            # Asignamos la fecha directamente por JavaScript y forzamos eventos de cambio
            driver.execute_script("""
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('change'));
                arguments[0].dispatchEvent(new Event('blur'));
            """, fecha_input_al, fecha_sin_slash)

            logging.info(
                f"Fecha EMISIÓN AL '{EMISION_CONSTANCIAS_EMISION_AL}' transformada a '{fecha_sin_slash}' e ingresada vía JavaScript."
            )
            time.sleep(1)

        except Exception as e:
            logging.error(f"Error al ingresar la fecha EMISIÓN AL: {e}")
    else:
        logging.info("La variable EMISION_CONSTANCIAS_EMISION_AL está vacía, se omite la selección de fecha AL.")


    # RETENCIONES QUE DECLARA:
    try:
        logging.info("Intentando seleccionar RENCIONES QUE DECLARA")
        dropdown_label_xpath = "//label[contains(@id, 'modoServe_label')]"
        dropdown_items_xpath = "//ul[contains(@id, 'modoServe_items')]//li"
        # Hacer clic en el label para abrir el menú desplegable
        dropdown_label = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, dropdown_label_xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_label)
        dropdown_label.click()

        # Seleccionar el ítem correspondiente por índice
        dropdown_items = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.XPATH, dropdown_items_xpath))
        )
        if 0 <= EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA < len(dropdown_items):
            dropdown_items[EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA].click()
            time.sleep(1)
        else:
            logging.warning(
                f"Índice {EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA} fuera de rango en el menú desplegable."
            )

    except Exception as e:
        logging.error(f"Error al seleccionar RETENCIONES QUE DECLARA: {e}")

    # REGIMEN
    try:
        logging.info("Intentando seleccionar REGIMEN")

        dropdown_label_xpath = "//label[contains(@id, 'paramServe_label')]"
        dropdown_items_xpath = "//ul[contains(@id, 'paramServe_items')]//li"

        # Hacer clic en el label para abrir el menú desplegable
        dropdown_label = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, dropdown_label_xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_label)
        dropdown_label.click()

        # Seleccionar el ítem correspondiente por índice
        dropdown_items = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.XPATH, dropdown_items_xpath))
        )
        if 0 <= EMISION_CONSTANCIAS_REGIMEN < len(dropdown_items):
            dropdown_items[EMISION_CONSTANCIAS_REGIMEN].click()
            time.sleep(1)
        else:
            logging.warning(
                f"Índice {EMISION_CONSTANCIAS_REGIMEN} fuera de rango en el menú desplegable."
            )

    except Exception as e:
        logging.info(
            f"Error al seleccionar REGIMEN, comprobando si es RETENCION A DECLARAR"
        )
        try:
            logging.info("Intentando seleccionar RETENCION A DECLARAR")

            dropdown_label_xpath = "//label[contains(@id, 'paramMode_label')]"
            dropdown_items_xpath = "//ul[contains(@id, 'paramMode_items')]//li"

            # Hacer clic en el label para abrir el menú desplegable
            dropdown_label = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, dropdown_label_xpath))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_label)
            dropdown_label.click()

            # Seleccionar el ítem correspondiente por índice
            dropdown_items = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.XPATH, dropdown_items_xpath))
            )
            if 0 <= EMISION_CONSTANCIAS_REGIMEN < len(dropdown_items):
                dropdown_items[EMISION_CONSTANCIAS_REGIMEN].click()
                time.sleep(1)
            else:
                logging.warning(
                    f"Índice {EMISION_CONSTANCIAS_REGIMEN} fuera de rango en el menú desplegable."
                )
        except Exception as e:
            logging.error(f"Error al seleccionar RETENCION A DECLARAR: {e}")

    # TIPO DOCUMENTO
    try:
        logging.info("Intentando seleccionar TIPO DOCUMENTO")

        dropdown_label_xpath = "//label[contains(@id, 'tipoDocto_label')]"
        dropdown_items_xpath = "//ul[contains(@id, 'tipoDocto_items')]//li"

        # Hacer clic en el label para abrir el menú desplegable
        dropdown_label = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, dropdown_label_xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_label)
        dropdown_label.click()

        # Seleccionar el ítem correspondiente por índice
        dropdown_items = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.XPATH, dropdown_items_xpath))
        )
        if 0 <= EMISION_CONSTANCIAS_TIPO_DOCUMENTO < len(dropdown_items):
            dropdown_items[EMISION_CONSTANCIAS_TIPO_DOCUMENTO].click()
            time.sleep(1)
        else:
            logging.warning(
                f"Índice {EMISION_CONSTANCIAS_TIPO_DOCUMENTO} fuera de rango en el menú desplegable."
            )

    except Exception as e:
        logging.error(f"Error al seleccionar TIPO DOCUMENTO: {e}")

    # NIT RETENIDO
    try:
        logging.info("Intentando ingresar NIT RETENIDO")
        input_nit_xpath = "//input[@id='formContent:itNitRetenido']"
        input_nit = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, input_nit_xpath))
        )
        input_nit.clear()
        input_nit.send_keys(EMISION_CONSTANCIAS_NIT_RETENIDO)
        logging.info(
            f"NIT RETENIDO {EMISION_CONSTANCIAS_NIT_RETENIDO} ingresado correctamente."
        )
    except Exception as e:
        logging.error(f"Error al ingresar NIT RETENIDO: {e}")

    # NUMERO DE AUTORIZACION FEL
    try:
        logging.info("Intentando ingresar NUMERO DE AUTORIZACION FEL")
        input_auth_xpath = "//input[@id='formContent:itNumAuth']"
        input_auth = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, input_auth_xpath))
        )
        input_auth.clear()
        input_auth.send_keys(EMISION_CONSTANCIAS_NO_AUTORIZACION_FEL)
        logging.info(
            f"NUMERO DE AUTORIZACION FEL {EMISION_CONSTANCIAS_NO_AUTORIZACION_FEL} ingresado correctamente."
        )
    except Exception as e:
        logging.error(f"Error al ingresar NUMERO DE AUTORIZACION FEL: {e}")

    # SERIE DE FACTURA
    try:
        logging.info("Intentando ingresar SERIE DE FACTURA")
        input_serie_xpath = "//input[@id='formContent:itSerieFactura']"
        input_serie = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, input_serie_xpath))
        )
        input_serie.clear()
        input_serie.send_keys(EMISION_CONSTANCIAS_SERIE_DE_FACTURA)
        logging.info(
            f"SERIE DE FACTURA {EMISION_CONSTANCIAS_SERIE_DE_FACTURA} ingresada correctamente."
        )
    except Exception as e:
        logging.error(f"Error al ingresar SERIE DE FACTURA: {e}")

    # NUMERO DE FACTURA
    try:
        logging.info("Intentando ingresar NUMERO DE FACTURA")
        input_num_factura_xpath = "//input[@id='formContent:itNumFactura']"
        input_num_factura = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, input_num_factura_xpath))
        )
        input_num_factura.clear()
        input_num_factura.send_keys(EMISION_CONSTANCIAS_NO_DE_FACTURA)
        logging.info(
            f"NUMERO DE FACTURA {EMISION_CONSTANCIAS_NO_DE_FACTURA} ingresado correctamente."
        )
    except Exception as e:
        logging.error(f"Error al ingresar NUMERO DE FACTURA: {e}")
    
    # Hacer clic en el botón de "Buscar"
    try:
        logging.info("Intentando hacer clic en el botón Buscar")
        boton_buscar_xpath = "//button[@id='formContent:btnBuscar']"
        boton_buscar = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, boton_buscar_xpath))
        )
        boton_buscar.click()
        logging.info("Botón Buscar presionado correctamente.")
        # Espera a que cargue la tabla
        time.sleep(4)
    except Exception as e:
        logging.error(f"Error al hacer clic en el botón Buscar: {e}")

    # Hacer clic en el checkbox para confirmar fecha emisión constancia utilizando JavaScript
    try:
        logging.info("Intentando hacer clic en el checkbox para confirmar fecha emisión constancia")

        # Intentar con el primer checkbox
        checkbox_input_xpath = "//input[@id='formContent:idGenReten_input']"
        checkbox_input = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, checkbox_input_xpath))
        )
        driver.execute_script("arguments[0].click();", checkbox_input)
        logging.info("Checkbox 'Confirme fecha emisión constancia' seleccionado correctamente.")

    except Exception as e:
        logging.info(f"No se pudo hacer clic en el primer checkbox (IVA). Intentando con el segundo (ISR).")

        try:
            # Intentar con el segundo checkbox
            checkbox_input_alternative_xpath = "//input[@id='formContent:idGenRetenISR_input']"
            checkbox_input_alternative = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, checkbox_input_alternative_xpath))
            )
            driver.execute_script("arguments[0].click();", checkbox_input_alternative)
            logging.info("Checkbox alternativo seleccionado correctamente.")
        except Exception as e:
            logging.error(f"Error al hacer clic en el checkbox alternativo: {e}")


    # === Esperar hasta 15s a que cargue la tabla ===
    logging.info("Esperando hasta 15 segundos para que cargue la tabla.")
    start_time = time.time()
    found_div = False

    while True:
        if time.time() - start_time > 15:
            logging.critical("SAT - No se encontró el div 'formContent:pnlFacturas' antes de 15s. Finalizando flujo, revise los datos.")
            return
        try:
            # Verificar si el div aparece y está visible
            div_facturas = driver.find_element(By.ID, "formContent:pnlFacturas")
            if div_facturas.is_displayed():
                found_div = True
                logging.info("Div 'formContent:pnlFacturas' encontrado y visible. Continuando...")
                break
        except Exception:
            # Ignorar para reintentar
            pass
        time.sleep(1)

    if not found_div:
        logging.critical("SAT - No se encontró el div 'formContent:pnlFacturas'. Se detiene la ejecución. Revise los datos ingresados.")
        return
    

def sat_emision_constancias_de_retencion_generar_retencion_y_cambiar_directorio_pdf(
    driver,
    EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA,
    EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS,
    EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS,
    EMISION_CONSTANCIAS_NOMBRE_PROVEEDOR,
    EMISION_CONSTANCIAS_NO_DE_FACTURA,
    EMISION_CONSTANCIAS_FECHA_FACTURA
):
    try:
        # Verificar si el navegador sigue disponible
        try:
            _ = driver.title
        except Exception as e:
            logging.info("El navegador no está disponible. Se detiene la ejecución de la función.")
            return
        
        logging.info(f"\n\n\n-x-x-x- (PASOS 11-14) sat_emision_constancias_de_retencion_generar_retencion_y_cambiar_directorio_pdf -x-x-x-\n")
        # Verificar si existe el primer checkbox en la tabla
        checkbox_xpath_1 = "//*[@id='formContent:tblFacturas_data']/tr/td[1]/div/div[1]/input"
        checkbox_xpath_2 = "//*[@id='formContent:tblFacturas_data']/tr[1]/td[1]/div/div[1]/input"
        
        # Intentar localizar el primer checkbox
        try:
            checkbox_element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, checkbox_xpath_1))
            )
            logging.info("Primer checkbox localizado.")
        except Exception as e:
            logging.warning("No se pudo localizar el primer checkbox. Intentando con el segundo.")
            try:
                checkbox_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, checkbox_xpath_2))
                )
                logging.info("Segundo checkbox localizado.")
            except Exception as e:
                logging.critical("SAT - No se pudo localizar ningún checkbox en la tabla, revise que la factura exista para crear una retención o que los parametros ingresados sean correctos para la búsqueda.")
                raise e  # Detiene el flujo lanzando el error


        # Hacer scroll y clic en el checkbox seleccionado
        driver.execute_script("arguments[0].scrollIntoView();", checkbox_element)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", checkbox_element)
        logging.info("Checkbox seleccionado correctamente.")

        # Asignar el número de factura proporcionado como argumento
        numero_de_factura_retenida = EMISION_CONSTANCIAS_NO_DE_FACTURA
        logging.info(f"Número de factura retenida: {numero_de_factura_retenida}")

        # Localizar el botón 'Generar retención'
        generar_retencion_xpath = "//button[span[text()='Generar retención']]"
        intentos = 3

        while intentos > 0:
            try:
                generar_retencion_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, generar_retencion_xpath))
                )
                driver.execute_script("arguments[0].scrollIntoView();", generar_retencion_button)
                time.sleep(1)
                generar_retencion_button.click()
                logging.info("Clic estándar en el botón 'Generar retención' realizado con éxito.")
                break
            except Exception as e:
                logging.warning("Intento fallido para hacer clic en el botón. Reintentando.")
                intentos -= 1
                time.sleep(2)

        if intentos == 0:
            try:
                logging.info("Intentando clic con JavaScript...")
                generar_retencion_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, generar_retencion_xpath))
                )
                driver.execute_script("arguments[0].click();", generar_retencion_button)
                logging.info("Clic con JavaScript realizado con éxito.")
            except Exception as js_error:
                logging.error(f"Error al intentar clic con JavaScript: {js_error}")
                return

        # Esperar que la ventana emergente aparezca
        time.sleep(3)

        # Obtener el texto del link que contiene el número de constancia
        constancia_xpath = "//*[@id='formContent:tblConst:0:blConstancia']"
        constancia_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, constancia_xpath))
        )
        numero_constancia_de_retencion_y_nombre_pdf = constancia_element.text.strip()
        logging.info(f"Número de constancia de retención y nombre del PDF: {numero_constancia_de_retencion_y_nombre_pdf}")

        # Hacer clic en el link para descargar el PDF
        constancia_element.click()
        logging.info(f"Descargando PDF con número de constancia: {numero_constancia_de_retencion_y_nombre_pdf}")

        # Esperar a que se descargue el archivo
        time.sleep(5)

        # Presionar el botón "Cerrar"
        cerrar_boton_xpath = "//*[@id='formContent:j_idt226']"
        cerrar_boton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, cerrar_boton_xpath))
        )
        cerrar_boton.click()
        logging.info("Botón 'Cerrar' presionado. Ventana emergente cerrada.")

        # Llamar a la función para cambiar el nombre y directorio del PDF
        
        numero_retencion = cambiar_nombre_y_directorio_pdf(
            driver,
            EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA,
            EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS,
            EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS,
            EMISION_CONSTANCIAS_NOMBRE_PROVEEDOR,
            EMISION_CONSTANCIAS_FECHA_FACTURA,
            numero_constancia_de_retencion_y_nombre_pdf,
            numero_de_factura_retenida
        )
        
        return numero_retencion  # Regresar el nombre final (con .pdf)
    
    except Exception as e:
        logging.error(f"Error en el proceso de generar retención y descargar PDF: {e}")
        return None

# Función auxiliar de la anterior, no se encuentra en la configuración de los flujos porque necesita el numero de constancia que se genera en la anterior función
# solamente existe para simplificar y separar los procesos de descargar pdf y de cambiar directorio y nombre. (Pasos 16-17)
def cambiar_nombre_y_directorio_pdf(
    driver,
    EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA,
    EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS,
    EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS,
    EMISION_CONSTANCIAS_NOMBRE_PROVEEDOR,
    EMISION_CONSTANCIAS_FECHA_FACTURA,
    numero_constancia_de_retencion_y_nombre_pdf,
    numero_de_factura_retenida
):
    """
    Si EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA == 1 => renombra el PDF.
    Si EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA != 1 => mantiene el nombre original.
    Retorna el nombre final del archivo (incluyendo '.pdf').
    """
    try:
        logging.info("\n\n\n-x-x-x- (PASOS 15-18) cambiar_nombre_y_directorio_pdf -x-x-x-\n")

        # Nombre original (el generado al descargar):
        archivo_pdf_nombre = f"{numero_constancia_de_retencion_y_nombre_pdf}.pdf"
        ruta_descargas_pdf = os.path.join(EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS, archivo_pdf_nombre)

        # Verificar si existe el archivo en descargas
        if not os.path.exists(ruta_descargas_pdf):
            logging.error(f"El archivo {archivo_pdf_nombre} no se encontró en el directorio de descargas.")
            return None  # o raise Exception, según tu manejo de errores

        # Dependiendo del valor de EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA, renombrar o no
        if EMISION_CONSTANCIAS_RETENCIONES_QUE_DECLARA == 1:
            # Renombrar el PDF
            nuevo_nombre_pdf = f"f-{numero_de_factura_retenida} {EMISION_CONSTANCIAS_NOMBRE_PROVEEDOR}.pdf"
            logging.info(f"Renombrando el PDF debido a retenciones_que_declara=1 => {nuevo_nombre_pdf}")
        else:
            # Mantener el nombre original
            nuevo_nombre_pdf = archivo_pdf_nombre
            logging.info(f"Manteniendo el nombre original => {nuevo_nombre_pdf}")

        # Construir ruta final en el directorio de facturas
        nueva_ruta_pdf = os.path.join(EMISION_CONSTANCIAS_DIRECTORIO_FACTURAS, nuevo_nombre_pdf)

        # Mover (y renombrar si aplica)
        shutil.move(ruta_descargas_pdf, nueva_ruta_pdf)
        logging.info(f"Archivo movido a: {nueva_ruta_pdf}")

        return nuevo_nombre_pdf  # Regresar el nombre final (con .pdf)

    except Exception as e:
        logging.error(f"Error al cambiar el nombre y mover el archivo PDF: {e}", exc_info=True)
        return None


# SIN TERMINAR: Funcion para abrir el pdf en una nueva pestaña para imprimir, faltan algunos botones por si se quiere implementar más adelante.
def sat_pdf_imprimir_factura(driver, EMISION_CONSTANCIAS_NO_DE_CONSTANCIA_PDF, EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS):
    try:
        # Ruta completa del archivo PDF
        ruta_pdf = os.path.join(EMISION_CONSTANCIAS_DIRECTORIO_DESCARGAS, f"{EMISION_CONSTANCIAS_NO_DE_CONSTANCIA_PDF}.pdf")
        if not os.path.exists(ruta_pdf):
            logging.error(f"El archivo PDF '{ruta_pdf}' no se encontró.")
            return

        # Crear la URL local para abrir el PDF
        url_pdf = f"file://{ruta_pdf}"
        logging.info(f"Ruta del PDF generada: {url_pdf}")
        
        # Abrir una nueva pestaña y cargar el PDF
        driver.switch_to.new_window('tab')  # Abre nueva pestaña
        driver.get(url_pdf)  # Cargar el PDF
        logging.info(f"Archivo PDF '{ruta_pdf}' abierto correctamente en una nueva pestaña.")
        time.sleep(3)

        # Verificar la URL actual
        current_url = driver.current_url
        logging.info(f"URL actual en el navegador: {current_url}")

        # Intentar leer el texto del span con el id 'title'
        try:
            title_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='title']"))
            )
            title_text = title_element.text
            logging.info(f"Texto del título del PDF: {title_text}")
        except Exception as e:
            logging.error(f"Error al intentar leer el texto del título: {e}")
        
        # Intentar presionar el primer botón de la barra de herramientas
        try:
            first_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/pdf-viewer//viewer-toolbar//div/div[3]/cr-icon-button[1]"))
            )
            first_button.click()
            logging.info("Primer botón de la barra de herramientas presionado.")
        except Exception as e:
            logging.error(f"Error al intentar presionar el primer botón: {e}")
        
    except Exception as e:
        logging.error(f"Error al abrir el archivo PDF: {e}")