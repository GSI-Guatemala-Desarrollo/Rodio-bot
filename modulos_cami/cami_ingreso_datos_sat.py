import logging
import os
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configuracion_bot import ULTIMO_LOG_FILE, ULTIMO_LOG_TIMESTAMP
from constantes import DIRECTORIO_LOGS, H_INTROD_COMPROBANTES_PDF_PATH
from modulos_cami.cami_ingreso_datos_harmony import cami_cargar_logs, cami_eleccion_funciono_harmony
# Elige el flujo
def cami_elegir_flujo(driver, target_fecha):
    """
    Navega a la página de flujos de CamiApp, despliega la sección de "Recepción de Facturas" y
    busca en la tabla la fila en la que la fecha (columna 3) coincide exactamente con target_fecha.
    Para cada fila, se registra la fecha encontrada mediante logging.info.
    Si se encuentra la coincidencia, se hace clic en el botón "Trabajar" de esa fila y luego en
    "Siguiente Etapa" para continuar en el flujo.
    
    Args:
        driver: WebDriver activo.
        target_fecha (str): Fecha objetivo (por ejemplo, "21/3/2025, 9:36:52 a. m.").
    """
    logging.info("Navegando a la página de flujos de CamiApp...")
    driver.get("https://next.camiapp.net/v2/flujos")
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]'))
        )
    except Exception as e:
        logging.error(f"Error al cargar la página de flujos")
        return

    # Desplegar la sección "Recepción de Facturas"
    accordion_xpath = '//*[@id="root"]/div[1]/main/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div/h2/button'
    try:
        logging.info("Esperando que el botón 'Recepción de Facturas' esté presente...")
        recepcion_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, accordion_xpath))
        )
        recepcion_button.click()
        logging.info("Clic en 'Recepción de Facturas' realizado.")
    except Exception as e:
        logging.error(f"Error al desplegar la sección 'Recepción de Facturas'")
        return

    # Dar un tiempo adicional para que la tabla se cargue
    time.sleep(3)
    
    # Esperar a que se cargue la tabla de flujos
    table_rows_xpath = '//*[@id="root"]/div[1]/main/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div[1]/div/div/div/div/table/tbody/tr'
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, table_rows_xpath))
        )
    except Exception as e:
        logging.error(f"Error al esperar que la tabla de flujos cargue")
        return

    rows = driver.find_elements(By.XPATH, table_rows_xpath)
    logging.info(f"Se encontraron {len(rows)} filas en la tabla de flujos.")

    row_found = None
    for idx, row in enumerate(rows, start=1):
        try:
            fecha_cell = row.find_element(By.XPATH, "./td[3]")
            fecha_text = fecha_cell.text.strip()
            logging.info(f"Fila {idx}: Fecha encontrada: {fecha_text}")
            if fecha_text == target_fecha:
                logging.info(f"✅ Coincidencia encontrada en la fila {idx} con fecha: {fecha_text}.")
                row_found = row
                break
            else:
                logging.info(f"Fila {idx}: Fecha no coincide (target: {target_fecha}).")
        except Exception as e:
            logging.warning(f"Error al leer la fecha en la fila {idx}")

    if row_found is None:
        logging.error(f"❌ No se encontró ninguna fila con la fecha: {target_fecha}")
        return

    # Intentar hacer clic en el botón "Trabajar" en la fila encontrada
    try:
        trabajar_button = row_found.find_element(By.XPATH, "./td[6]/a")
        driver.execute_script("arguments[0].scrollIntoView(true);", trabajar_button)
        time.sleep(1)
        try:
            trabajar_button.click()
        except Exception as e:
            logging.warning(f"Clic normal falló, intentando clic con JavaScript")
            driver.execute_script("arguments[0].click();", trabajar_button)
        logging.info("Clic en el botón 'Trabajar' realizado exitosamente.")
    except Exception as e:
        logging.error(f"Error al hacer clic en el botón 'Trabajar'")
        return

    # Esperar a que se cargue la página del flujo y hacer clic en "Siguiente Etapa"
    siguiente_etapa_xpath = '//*[@id="root"]/div[1]/main/div/div/div[2]/div/div/div/div/div[1]/div/form/div[1]/div[2]/button[2]'
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, siguiente_etapa_xpath))
        )
        siguiente_etapa_button = driver.find_element(By.XPATH, siguiente_etapa_xpath)
        driver.execute_script("arguments[0].scrollIntoView(true);", siguiente_etapa_button)
        time.sleep(1)
        siguiente_etapa_button.click()
        logging.info("Clic en 'Siguiente Etapa' realizado exitosamente.")
    except Exception as e:
        logging.error(f"Error al hacer clic en 'Siguiente Etapa'")
        return

# Elige la opción de retención según el mensaje crítico, si o no funcionó SAT

def cami_eleccion_funciono_sat(driver, mensaje_critico, modified_data):
    try:
        logging.info("Ejecutando: cami_eleccion_funciono_sat")

        
        # Esperar botón de siguiente etapa
        boton_siguiente = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and contains(@class, "btn-primary")]'))
        )

        # Scroll hacia el botón
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_siguiente)
        time.sleep(0.3)

        # Clic en siguiente
        boton_siguiente.click()
        logging.info("Clic en 'Siguiente Etapa' realizado.")

        # Espera a que aparezca el <select>
        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "form-select"))
        )

        # Scroll hacia el <select>
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", select_element)
        time.sleep(0.3)

        # Seleccionar opción según mensaje
        seleccion = "No" if mensaje_critico and "SAT" in mensaje_critico else "Sí"
        logging.info(f"Seleccionando opción: {seleccion}")
        Select(select_element).select_by_visible_text(seleccion)
        time.sleep(0.5)

        # Esperar botón de siguiente etapa
        boton_siguiente = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and contains(@class, "btn-primary")]'))
        )

        # Scroll hacia el botón
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_siguiente)
        time.sleep(0.3)

        # Clic en siguiente
        boton_siguiente.click()
        logging.info("Clic en 'Siguiente Etapa' realizado.")

        # Si se seleccionó "Sí", ejecutar funciones extra
        if seleccion == "Sí":
            cami_funciono_sat_iva(driver, modified_data)

            if modified_data.get("tipo_retencion") == "RETENISR ROSSI":
                cami_funciono_sat_isr(driver, modified_data)

            cami_eleccion_funciono_harmony(driver, mensaje_critico, modified_data)

        # Cargar logs
        logging.info("Se procederá con la carga de logs.")
        numeracion_automatica = modified_data.get("numeracion_automatica")

        ruta_archivo_log = ULTIMO_LOG_FILE
        if not ruta_archivo_log or not os.path.exists(ruta_archivo_log):
            for fn in os.listdir(DIRECTORIO_LOGS):
                if numeracion_automatica in fn and fn.endswith(".log"):
                    ruta_archivo_log = os.path.join(DIRECTORIO_LOGS, fn)
                    break

        fecha = ""
        if ULTIMO_LOG_TIMESTAMP:
            fecha = ULTIMO_LOG_TIMESTAMP.split("_")[0]

        cami_cargar_logs(driver, numeracion_automatica, ruta_archivo_log, fecha)

    except Exception as e:
        logging.error(f"Error en cami_eleccion_funciono_sat")

def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.2)


def cami_funciono_sat_iva(driver, modified_data):
    try:
        logging.info("Ejecutando cami_funciono_sat_iva...")

        id_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="ID proveedor"]'))
        )
        scroll_into_view(driver, id_input)
        id_input.send_keys(modified_data["h_introd_comprobantes_id_proveedor"])

        fecha_input = driver.find_element(By.XPATH, '//input[@placeholder="Fecha"]')
        scroll_into_view(driver, fecha_input)
        fecha_input.send_keys(modified_data["h_introd_comprobantes_fecha_factura"])

        factura_input = driver.find_element(By.XPATH, '//input[@placeholder="No Factura"]')
        scroll_into_view(driver, factura_input)
        factura_input.send_keys(modified_data["s_emision_constancias_no_de_factura"])

        # Subir archivo de retención IVA
        archivo_path = os.path.join(
            H_INTROD_COMPROBANTES_PDF_PATH[3],
            modified_data["h_introd_comprobantes_nombre_pdf"][3]
        )
        input_file = driver.find_element(By.XPATH, '//*[@id=":r2q:-file"]')
        scroll_into_view(driver, input_file)
        try:
            input_file.send_keys(archivo_path)
        except Exception as e:
            logging.warning(f"Primer intento fallido al subir archivo IVA")
            driver.execute_script("arguments[0].click();", input_file)
            input_file.send_keys(archivo_path)

        boton_siguiente = driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div[1]/main/div/div/div[2]/div/div/div/div/div[1]/div/form/div[1]/div[2]/button[2]'
        )
        scroll_into_view(driver, boton_siguiente)
        boton_siguiente.click()

        logging.info("✔️ Se completó cami_funciono_sat_iva correctamente.")

    except Exception as e:
        logging.error(f"❌ Error en cami_funciono_sat_iva", exc_info=True)


def cami_funciono_sat_isr(driver, modified_data):
    try:
        logging.info("Ejecutando cami_funciono_sat_isr...")

        try:
            id_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//input[@placeholder="ID proveedor"]'))
            )
        except Exception:
            logging.info("ID proveedor no visible, haciendo clic en botón de reordenar campos...")
            boton_ordenar = driver.find_element(By.XPATH, '//button[@type="button" and contains(@class, "btn-sm")]')
            scroll_into_view(driver, boton_ordenar)
            boton_ordenar.click()
            id_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//input[@placeholder="ID proveedor"]'))
            )

        scroll_into_view(driver, id_input)
        id_input.send_keys(modified_data["h_introd_comprobantes_id_proveedor"])

        constancia_input = driver.find_element(By.XPATH, '//input[@placeholder="Número de constancia"]')
        scroll_into_view(driver, constancia_input)
        constancia_input.send_keys(modified_data["numeracion_automatica"].replace("GT", ""))

        fecha_input = driver.find_element(By.XPATH, '//input[@placeholder="Fecha"]')
        scroll_into_view(driver, fecha_input)
        fecha_input.send_keys(modified_data["h_introd_comprobantes_fecha_factura"])

        archivo_path = os.path.join(
            H_INTROD_COMPROBANTES_PDF_PATH[4],
            modified_data["h_introd_comprobantes_nombre_pdf"][4]
        )
        input_file = driver.find_element(By.XPATH, '//*[@id=":r5d:-file"]')
        scroll_into_view(driver, input_file)
        try:
            input_file.send_keys(archivo_path)
        except Exception as e:
            logging.warning(f"Primer intento fallido al subir archivo ISR")
            driver.execute_script("arguments[0].click();", input_file)
            input_file.send_keys(archivo_path)

        boton_siguiente = driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div[1]/main/div/div/div[2]/div/div/div/div/div[1]/div/form/div[1]/div[2]/button[2]'
        )
        scroll_into_view(driver, boton_siguiente)
        boton_siguiente.click()

        logging.info("✔️ Se completó cami_funciono_sat_isr correctamente.")

    except Exception as e:
        logging.error(f"❌ Error en cami_funciono_sat_isr", exc_info=True)
