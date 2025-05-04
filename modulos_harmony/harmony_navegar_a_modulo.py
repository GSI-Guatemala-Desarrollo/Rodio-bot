import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def harmony_navegar_a_modulo(driver, indices):
    """
    Navega por los módulos utilizando índices y hace clic en el último nivel.
    Si ya se encuentra en la página de inicio, se hace clic en el botón de "Volver a la Página Home".

    Args:
        driver: WebDriver activo.
        indices (tuple): Lista de índices (por nivel) para navegar por las listas.
    """
    try:
        _ = driver.title
    except Exception as e:
        logging.info("El navegador no está disponible. Se detiene la ejecución de la función.")
        return
    logging.info("\n\n\n-x-x-x- harmony_navegar_a_modulo -x-x-x-\n")
    logging.info("Verificando si cargó la página.")

    start_time = time.time()
    found_menu_header = False

    while True:
        if time.time() - start_time > 30:
            logging.critical("HARMONY - No se encontró el h2 'ptpgltlbl_MENU' antes de 30s. Abortando flujo."
            )
            return  # o raise, según tu manejo de errores
        try:
            menu_header = driver.find_element(By.ID, "ptpgltlbl_MENU")
            # Verificamos que el elemento esté visible
            if menu_header.is_displayed():
                found_menu_header = True
                logging.info("h2 'ptpgltlbl_MENU' encontrado. Continuando el flujo.")
                break
        except Exception:
            # No hace nada, reintenta
            pass

        time.sleep(1)

    if not found_menu_header:
        logging.critical("HARMONY - No se encontró el h2 'ptpgltlbl_MENU'. Se detiene la ejecución."
        )
        return

    try:
        # Verificar si estamos en la página de inicio y si es necesario hacer clic en el botón de regreso
        try:
            back_button = driver.find_element(By.ID, "PT_WORK_PT_BUTTON_BACK")
            back_button.click()
            logging.info("Regresando a la página de inicio...")
            time.sleep(3)  # Esperar para asegurarse de que se haya cargado la página
        except:
            logging.info("Ya estamos en la página de inicio.")

        logging.info(f"Navegando por los módulos con índices: {indices}")
        # Ahora que estamos en la página de inicio, empezamos la navegación por los módulos
        ul_xpath = '//*[@id="ptnav2tree"]'
        current_ul = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ul_xpath))
        )

        for i, index in enumerate(indices):
            logging.info(f"Accediendo al nivel {i + 1}, índice {index}...")
            li_xpath = f"./li[{index}]"
            li_element = current_ul.find_element(By.XPATH, li_xpath)

            # Hacer scroll para asegurarse de que sea visible
            driver.execute_script("arguments[0].scrollIntoView(true);", li_element)
            logging.info(f"Desplazado a la vista el elemento en nivel {i + 1}, índice {index}.")
            time.sleep(1)

            # Expandir la sublista si no es el último nivel
            if i < len(indices) - 1:
                toggle_div = li_element.find_element(By.XPATH, './div[@class="ptnav2toggle"]')
                toggle_div.click()
                logging.info(f"Flecha desplegada en nivel {i + 1}, índice {index}.")
                time.sleep(1)  # Espera para cargar la sublista
                current_ul = li_element.find_element(By.XPATH, './ul')
                logging.info(f"Sublista encontrada en nivel {i + 1}.")
            else:
                # Aquí se vuelve a buscar el último enlace en lugar de usar el encontrado previamente
                link_xpath = './a'
                logging.info(f"Buscando el enlace en el nivel {i + 1}, índice {index}.")
                link_element = WebDriverWait(li_element, 10).until(
                    EC.presence_of_element_located((By.XPATH, link_xpath))
                )
                logging.info(f"Enlace encontrado: {link_element.text}")
                
                driver.execute_script("arguments[0].scrollIntoView(true);", link_element)
                logging.info(f"Desplazado a la vista el enlace: {link_element.text}.")
                time.sleep(1)  # Esperar un poco para asegurar que sea visible

                try:
                    # Intentar hacer clic en el enlace con un manejo de excepciones específico
                    logging.info(f"Haciendo clic en el enlace: {link_element.text}.")
                    link_element.click()
                    logging.info(f"Elemento seleccionado: {link_element.text}.")
                    
                    # Esperar explícitamente a que la página cambie o se cargue un nuevo elemento
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 'xpath_del_elemento_cargado')))
                    logging.info("Nuevo contenido cargado correctamente.")
                    
                except Exception as e:
                    # En caso de que el error de 'stale element reference' ocurra, intentar continuar
                    # logging.error(f"Error al hacer clic en el enlace: {e}.")
                    time.sleep(3)
                    return

    except Exception as e:
        logging.critical(f"HARMONY - Error al navegar por los módulos: {e}")
