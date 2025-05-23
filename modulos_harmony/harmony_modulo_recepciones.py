import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def harmony_recepciones_agregar_valor_y_busqueda_oc(driver, h_recepciones_uni_po, h_recepciones_id_oc):
    """
    1. Cambia al iframe principal 'ptifrmtgtframe'.
    2. Ingresa el UNI PO en 'RECV_PO_ADD_BUSINESS_UNIT'.
    3. Presiona el botón 'Añadir' (#ICSearch) y espera 2s.
    4. (Con bucle 30s): Ingresa el ID de la OC en 'PO_PICK_ORD_WRK_ORDER_ID'.
    5. Presiona el botón 'Buscar' (PO_PICK_ORD_WRK_PB_FETCH_PO) y espera 2s.
    6. Realiza scroll y hace clic en 'Selec Todo' (PO_PICK_ORD_WRK_SELECT_ALL_BTN).
    7. Espera 1s y luego presiona el botón 'Aceptar' (#ICSave).
    """

    logging.info("\n\n\n-x-x-x- (OC) harmony_recepciones_agregar_valor_y_busqueda_oc -x-x-x-\n")

    try:
        # 1) Cambiar al iframe principal
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "ptifrmtgtframe"))
        )
        logging.info("Cambiado al iframe principal 'ptifrmtgtframe'.")

        # 2) Ingresar el UNI PO en 'RECV_PO_ADD_BUSINESS_UNIT'
        logging.info(f"Ingresando UNI PO: {h_recepciones_uni_po}")
        uni_po_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "RECV_PO_ADD_BUSINESS_UNIT"))
        )
        uni_po_input.clear()
        uni_po_input.send_keys(h_recepciones_uni_po)

        # 3) Presionar el botón 'Añadir' (#ICSearch)
        logging.info("Haciendo clic en el botón 'Añadir' (#ICSearch).")
        btn_anadir = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "#ICSearch"))
        )
        btn_anadir.click()
        logging.info("Botón 'Añadir' presionado. Esperando 2s...")
        time.sleep(2)

        # 4) Intentar localizar 'PO_PICK_ORD_WRK_ORDER_ID' con bucle hasta 30s
        logging.info(f"Ingresando ID de la OC: {h_recepciones_id_oc}")
        start_time = time.time()
        found_input = False
        while True:
            if time.time() - start_time > 30:
                logging.critical("HARMONY - No se encontró el campo 'PO_PICK_ORD_WRK_ORDER_ID' antes de 30s. Abortando flujo."
                )
                return

            try:
                id_oc_input = driver.find_element(By.ID, "PO_PICK_ORD_WRK_ORDER_ID")
                if id_oc_input.is_enabled() and id_oc_input.is_displayed():
                    id_oc_input.clear()
                    id_oc_input.send_keys(h_recepciones_id_oc)
                    found_input = True
                    logging.info("Campo 'PO_PICK_ORD_WRK_ORDER_ID' localizado y llenado correctamente.")
                    break
            except Exception:
                pass

            time.sleep(1)

        # Continúa solo si se encontró el input
        if not found_input:
            logging.critical("HARMONY - No se pudo llenar el campo 'PO_PICK_ORD_WRK_ORDER_ID'. Se detiene la ejecución."
            )
            return

        # 5) Presionar el botón 'Buscar' (PO_PICK_ORD_WRK_PB_FETCH_PO)
        logging.info("Haciendo clic en el botón 'Buscar' (PO_PICK_ORD_WRK_PB_FETCH_PO).")
        btn_buscar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "PO_PICK_ORD_WRK_PB_FETCH_PO"))
        )
        btn_buscar.click()
        logging.info("Botón 'Buscar' presionado. Esperando 2s mientras se cargan las líneas...")
        time.sleep(2)

        # 6) Realizar scroll y clic en 'Selec Todo' (PO_PICK_ORD_WRK_SELECT_ALL_BTN)
        logging.info("Haciendo scroll y clic en 'Selec Todo'.")
        selec_todo_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "PO_PICK_ORD_WRK_SELECT_ALL_BTN"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", selec_todo_link)
        selec_todo_link.click()
        time.sleep(1)

        # 7) Presionar el botón 'Aceptar' (#ICSave)
        logging.info("Haciendo clic en el botón 'Aceptar' (#ICSave).")
        btn_aceptar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "#ICSave"))
        )
        btn_aceptar.click()
        logging.info("Recepciones agregadas y búsqueda de OC completada correctamente.")

    except Exception as e:
        logging.error(f"Error en 'harmony_recepciones_agregar_valor_y_busqueda_oc': {e}", exc_info=True)


def harmony_recepciones_guardar(driver):
    """
    1) Localiza el botón 'Guardar' (#ICSave).
    2) Hace clic en el botón para confirmar y guardar la información.
    """
    
    logging.info("\n\n\n-x-x-x- (OC) harmony_recepciones_guardar -x-x-x-\n")
    time.sleep(2)
    try:
        guardar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "#ICSave"))
        )
        guardar_btn.click()
        logging.info("Botón 'Guardar' presionado con éxito. Recepciones guardadas.")
        time.sleep(7) # Espera a que se guarden los cambios
    except Exception as e:
        logging.error(f"Error en 'harmony_recepciones_guardar': {e}", exc_info=True)