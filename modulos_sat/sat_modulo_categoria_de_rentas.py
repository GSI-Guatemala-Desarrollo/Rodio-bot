import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def sat_categoria_de_rentas_busqueda_parametros(driver, CATEGORIA_DE_RENTAS_NIT_RETENIDO, CATEGORIA_DE_RENTAS_PERIODO_DEL, CATEGORIA_DE_RENTAS_PERIODO_AL, CATEGORIA_DE_RENTAS_ESTADO_DE_ASIGNACION):
    """
    Completa los parámetros del formulario en la página de categoría de rentas.
    """

    try:
        try:
            _ = driver.title
        except Exception as e:
            logging.info("El navegador no está disponible. Se detiene la ejecución de la función.")
            return
        
        logging.info(f"\n\n\n-x-x-x- (PASOS 23-24) sat_categoria_de_rentas_busqueda_parametros -x-x-x-\n")
        CATEGORIA_DE_RENTAS_ESTADO_DE_ASIGNACION = CATEGORIA_DE_RENTAS_ESTADO_DE_ASIGNACION - 1
        # Cambiar al iframe donde se encuentran los elementos
        try:
            driver.switch_to.default_content()
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                driver.switch_to.frame(iframe)
                if driver.find_elements(By.XPATH, "//*[@id='formContent:itPer_input']"):
                    logging.info("Elemento encontrado dentro del iframe, cambiando de contexto.")
                    break
                driver.switch_to.default_content()
        except Exception as e:
            logging.warning(f"No se encontró el elemento en ningún iframe. Error: {e}")

        # Seleccionar PERIODO_DEL
        if CATEGORIA_DE_RENTAS_PERIODO_DEL.strip():
            try:
                xpath_periodo_del = "//*[@id='formContent:itPer_input']"
                element_del = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, xpath_periodo_del))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", element_del)
                time.sleep(1)

                # Quitar los slashes de la fecha
                fecha_sin_slash = CATEGORIA_DE_RENTAS_PERIODO_DEL.replace("/", "")

                # Asignar por JavaScript y forzar eventos de cambio
                driver.execute_script("""
                    arguments[0].value = arguments[1];
                    arguments[0].dispatchEvent(new Event('change'));
                    arguments[0].dispatchEvent(new Event('blur'));
                """, element_del, fecha_sin_slash)

                logging.info(f"PERIODO_DEL '{CATEGORIA_DE_RENTAS_PERIODO_DEL}' (sin '/') asignado como '{fecha_sin_slash}'.")
                time.sleep(1)

            except Exception as e:
                logging.error(f"Error al asignar PERIODO_DEL: {e}")
        else:
            logging.info("CATEGORIA_DE_RENTAS_PERIODO_DEL está vacío, se omite la asignación de fecha.")

        # Seleccionar PERIODO_AL
        if CATEGORIA_DE_RENTAS_PERIODO_AL.strip():
            try:
                xpath_periodo_al = "//*[@id='formContent:itAl_input']"
                element_al = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, xpath_periodo_al))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", element_al)
                time.sleep(1)

                fecha_sin_slash = CATEGORIA_DE_RENTAS_PERIODO_AL.replace("/", "")

                driver.execute_script("""
                    arguments[0].value = arguments[1];
                    arguments[0].dispatchEvent(new Event('change'));
                    arguments[0].dispatchEvent(new Event('blur'));
                """, element_al, fecha_sin_slash)

                logging.info(f"PERIODO_AL '{CATEGORIA_DE_RENTAS_PERIODO_AL}' (sin '/') asignado como '{fecha_sin_slash}'.")
                time.sleep(1)

            except Exception as e:
                logging.error(f"Error al asignar PERIODO_AL: {e}")
        else:
            logging.info("CATEGORIA_DE_RENTAS_PERIODO_AL está vacío, se omite la asignación de fecha.")

        # Ingresar NIT_RETENIDO
        try:
            nit_input = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "formContent:itNitISR"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", nit_input)
            nit_input.clear()
            nit_input.send_keys(CATEGORIA_DE_RENTAS_NIT_RETENIDO)
            logging.info(f"NIT retenido {CATEGORIA_DE_RENTAS_NIT_RETENIDO} ingresado correctamente.")
        except Exception as e:
            logging.error(f"Error al ingresar el NIT retenido: {e}")

        # Seleccionar ESTADO_DE_ASIGNACION
        try:
            # Abrir la lista desplegable
            estado_label = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.ID, "formContent:statusAsigna_label"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", estado_label)
            estado_label.click()

            # Seleccionar la opción correspondiente
            estado_opcion_xpath = f"//*[@id='formContent:statusAsigna_items']/li[{CATEGORIA_DE_RENTAS_ESTADO_DE_ASIGNACION+1}]"
            estado_opcion = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, estado_opcion_xpath))
            )
            estado_opcion.click()
            time.sleep(2) # Esperar a que se asigne antes de buscar
            logging.info(f"Estado de asignación seleccionado correctamente: opción {CATEGORIA_DE_RENTAS_ESTADO_DE_ASIGNACION+1}.")
        except Exception as e:
            logging.error(f"Error al seleccionar el estado de asignación: {e}")

        logging.info("Formulario de categoría de rentas completado correctamente.")
    except Exception as e:
        logging.error(f"Error al completar el formulario: {e}")

    # Presionar el botón "BUSCAR"
    try:
        # Presionar el botón de búsqueda
        boton_busqueda = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.ID, "formContent:j_idt90"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", boton_busqueda)
        boton_busqueda.click()
        time.sleep(4) # Esperar a que se genere la tabla de facturas
        logging.info("Botón de búsqueda presionado correctamente.")
    except Exception as e:
        logging.error(f"Error al presionar el botón de búsqueda: {e}")


def seleccionar_fecha(driver, input_xpath, fecha):
    """
    Selecciona una fecha en el calendario desplegable.

    :param input_xpath: XPath del input para abrir el calendario.
    :param fecha: Fecha en formato "DD/MM/YYYY".
    """
    try:
        # Intentar localizar y hacer clic en el input para abrir el calendario
        fecha_input = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, input_xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", fecha_input)
        time.sleep(1)
        fecha_input.click()

        # Dividir la fecha en día, mes y año
        dia, mes, anio = fecha.split("/")

        # Seleccionar el año
        select_anio_xpath = "//*[@id='ui-datepicker-div']/div/div/select[2]"
        select_anio = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, select_anio_xpath))
        )
        Select(select_anio).select_by_visible_text(anio)

        # Seleccionar el mes
        select_mes_xpath = "//*[@id='ui-datepicker-div']/div/div/select[1]"
        select_mes = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, select_mes_xpath))
        )
        Select(select_mes).select_by_index(int(mes) - 1)

        # Seleccionar el día
        calendario_tabla_xpath = "//*[@id='ui-datepicker-div']/table"
        calendario_tabla = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, calendario_tabla_xpath))
        )
        dias = calendario_tabla.find_elements(By.TAG_NAME, "td")
        for dia_elemento in dias:
            if dia_elemento.text == dia and dia_elemento.is_enabled():
                dia_elemento.click()
                logging.info(f"Día {dia} seleccionado correctamente.")
                break
    except Exception as e:
        logging.error(f"Error al seleccionar la fecha {fecha}: {e}")


def sat_categoria_de_rentas_buscar_en_tabla(driver, numero_factura):
    
    """
    Busca un número de factura en la tabla, presiona el checkbox en la primera columna,
    y luego presiona el lápiz en la última columna de la misma fila.

    :param driver: Instancia de WebDriver de Selenium.
    :param numero_factura: Número de factura a buscar en la tabla.
    """
    try:
        try:
            _ = driver.title
        except Exception as e:
            logging.info("El navegador no está disponible. Se detiene la ejecución de la función.")
            return
        logging.info(f"\n\n\n-x-x-x- (PASOS 25-26) sat_categoria_de_rentas_buscar_en_tabla -x-x-x-\n")
        # Localizar la tabla
        tabla_xpath = "//*[@id='formContent:dtIdCatTable_data']"
        tabla = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, tabla_xpath))
        )

        # Localizar las filas de la tabla
        filas = tabla.find_elements(By.TAG_NAME, "tr")
        for index, fila in enumerate(filas, start=1):  # Enumerar filas para obtener el índice
            # Hacer scroll hacia la fila actual para asegurar visibilidad
            driver.execute_script("arguments[0].scrollIntoView(true);", fila)

            # Localizar las celdas de la fila
            celdas = fila.find_elements(By.TAG_NAME, "td")
            if len(celdas) >= 9:  # Asegurar que hay suficientes columnas en la fila
                numero_actual = celdas[8].text.strip()  # Extraer texto y limpiar espacios
                logging.info(f"Factura actual en fila {index}: {repr(numero_actual)}")  # Usar repr para ver el formato exacto
                
                if numero_actual == str(numero_factura):
                    logging.info(f"Número de factura encontrado: {numero_factura} en fila {index}")

                    # Localizar el checkbox en la primera columna de la fila
                    checkbox_xpath = f"//*[@id='formContent:dtIdCatTable_data']/tr[{index}]/td[1]/div/div[1]/input"
                    checkbox = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, checkbox_xpath))
                    )
                    # Usar JS para hacer click en el checkbox
                    driver.execute_script("arguments[0].click();", checkbox)
                    logging.info(f"Checkbox de la fila {index} presionado correctamente.")

                    # Localizar el icono de lápiz en la última columna de la fila
                    lapiz_xpath = f"//*[@id='formContent:dtIdCatTable:{index - 1}:linkCategoria']"
                    lapiz = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, lapiz_xpath))
                    )
                    # Usar JS para hacer click en el icono de lápiz
                    driver.execute_script("arguments[0].click();", lapiz)
                    logging.info(f"Lápiz de la fila {index} presionado correctamente.")
                    return

        logging.info(f"Número de factura no encontrado: {numero_factura}")
    except Exception as e:
        logging.error(f"Error al buscar el número de factura y presionar los botones: {e}")


def sat_categoria_de_rentas_asignar_categoria_y_regimen(driver, CATEGORIA_DE_RENTAS_OPCION_CATEGORIA_DE_RENTA, CATEGORIA_DE_RENTAS_OPCION_REGIMEN):
    """
    Selecciona la opción de categoría y régimen según los valores recibidos, y luego presiona los botones necesarios.

    :param driver: Instancia de WebDriver de Selenium.
    :param CATEGORIA_DE_RENTAS_OPCION_CATEGORIA_DE_RENTA: Constante que representa la opción de categoría de renta a seleccionar.
    :param CATEGORIA_DE_RENTAS_OPCION_REGIMEN: Constante que representa la opción de régimen a seleccionar.
    """
    try:
        try:
            _ = driver.title
        except Exception as e:
            logging.info("El navegador no está disponible. Se detiene la ejecución de la función.")
            return
        logging.info(f"\n\n\n-x-x-x- (PASOS 27-29) sat_categoria_de_rentas_asignar_categoria_y_regimen -x-x-x-\n")
        # Paso 1: Seleccionar categoría de renta
        label_categoria_xpath = "//*[@id='formContent:selTipoConsulta3_label']"
        label_categoria = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, label_categoria_xpath))
        )
        driver.execute_script("arguments[0].click();", label_categoria)
        logging.info("Abriendo lista de categorías de renta.")

        lista_categoria_xpath = "//*[@id='formContent:selTipoConsulta3_items']"
        lista_categoria = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, lista_categoria_xpath))
        )

        opciones_categoria = lista_categoria.find_elements(By.TAG_NAME, "li")
        if 0 < CATEGORIA_DE_RENTAS_OPCION_CATEGORIA_DE_RENTA <= len(opciones_categoria):
            time.sleep(1)
            opciones_categoria[CATEGORIA_DE_RENTAS_OPCION_CATEGORIA_DE_RENTA - 1].click()
            logging.info(f"Opción de categoría {CATEGORIA_DE_RENTAS_OPCION_CATEGORIA_DE_RENTA} seleccionada correctamente.")
            time.sleep(2)
        else:
            logging.warning(f"Opción de categoría {CATEGORIA_DE_RENTAS_OPCION_CATEGORIA_DE_RENTA} fuera de rango. No se seleccionó ninguna opción.")

        # Paso 2: Presionar el primer botón OK
        boton_ok_categoria_xpath = "//*[@id='formContent:j_idt174']"
        boton_ok_categoria = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, boton_ok_categoria_xpath))
        )
        driver.execute_script("arguments[0].click();", boton_ok_categoria)
        logging.info("Botón OK presionado correctamente tras seleccionar la categoría.")
        time.sleep(2)

        # Paso 3: Seleccionar régimen en la segunda lista desplegable
        select_regimen_xpath = "//*[@id='formContent:selTipoConsulta2_input']"
        select_regimen = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, select_regimen_xpath))
        )
        opciones_regimen = select_regimen.find_elements(By.TAG_NAME, "option")
        if 0 < CATEGORIA_DE_RENTAS_OPCION_REGIMEN <= len(opciones_regimen):
            driver.execute_script("arguments[0].selected = true;", opciones_regimen[CATEGORIA_DE_RENTAS_OPCION_REGIMEN - 1])
            opciones_regimen[CATEGORIA_DE_RENTAS_OPCION_REGIMEN - 1].click()
            logging.info(f"Opción de régimen {CATEGORIA_DE_RENTAS_OPCION_REGIMEN} seleccionada correctamente.")
            time.sleep(2)
        else:
            logging.warning(f"Opción de régimen {CATEGORIA_DE_RENTAS_OPCION_REGIMEN} fuera de rango. No se seleccionó ninguna opción.")

        # Paso 4: Presionar el botón para asignar el régimen
        boton_asignar_regimen_xpath = "//*[@id='formContent:j_idt182']"
        boton_asignar_regimen = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, boton_asignar_regimen_xpath))
        )
        driver.execute_script("arguments[0].click();", boton_asignar_regimen)
        time.sleep(2)
        logging.info("Botón para asignar régimen presionado correctamente.")

        # Paso 5: Manejar la ventana emergente según el caso
        try:
            # Caso 1: Confirmación de asignación inicial
            boton_confirmar_xpath = "//*[@id='formContent:j_idt147']"
            boton_confirmar = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, boton_confirmar_xpath))
            )
            driver.execute_script("arguments[0].click();", boton_confirmar)
            logging.info("Confirmación de asignación de régimen realizada correctamente.")
        except Exception as e:
            # Caso 2: Advertencia de cambio de categoría existente
            logging.info("No se encontró confirmación inicial. Verificando ventana de advertencia...")
            boton_cambio_categoria_xpath = "//*[@id='formContent:j_idt166']"
            boton_cambio_categoria = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, boton_cambio_categoria_xpath))
            )
            driver.execute_script("arguments[0].click();", boton_cambio_categoria)
            logging.info("Advertencia de cambio de categoría existente manejada correctamente.")

        # Esperar unos segundos para que se complete el proceso
        time.sleep(2)

    except Exception as e:
        logging.error(f"Error al asignar categoría y régimen: {e}")
