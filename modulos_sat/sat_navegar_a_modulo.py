import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from constantes import SAT_URL

def sat_navegar_por_busqueda(driver, texto_busqueda):
    """
    Navega a una sección de la página usando la barra de búsqueda.

    :param driver: Instancia de WebDriver de Selenium.
    :param texto_busqueda: Texto a buscar en la barra de búsqueda.
    """
    try:
        logging.info(f"\n\n\n-x-x-x- ('{texto_busqueda}') sat_navegar_por_busqueda -x-x-x-\n")
        # Intentar interactuar con la barra de búsqueda
        barra_busqueda = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "itBuscar"))
        )
        logging.info("Barra de búsqueda localizada correctamente.")

    except Exception:
        # Si no se puede interactuar con la barra, recargar la página
        logging.warning("No se pudo interactuar con la barra de búsqueda. Recargando página...")
        driver.get(SAT_URL)
        time.sleep(4)

    try:
        # Localizar nuevamente la barra después de recargar
        barra_busqueda = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "itBuscar"))
        )
        # Escribir el texto en la barra de búsqueda
        barra_busqueda.clear()
        barra_busqueda.send_keys(texto_busqueda)
        logging.info(f"Texto '{texto_busqueda}' escrito en la barra de búsqueda.")

        # Esperar a que aparezca la lista de resultados
        lista_resultados = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='ui-id-2']"))
        )
        logging.info("Lista de resultados visible.")
        time.sleep(1)

        # Seleccionar la primera opción de la lista
        primera_opcion = WebDriverWait(lista_resultados, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='ui-id-2']/li[1]/div"))
        )
        logging.info("Primera opción de la lista localizada.")

        # Intentar hacer clic con ActionChains
        action = ActionChains(driver)
        action.move_to_element(primera_opcion).click().perform()
        logging.info(f"Sección '{texto_busqueda}' seleccionada exitosamente.")

        # Esperar un momento para asegurar que la página cargue
        time.sleep(4)

    except Exception as e:
        logging.error(f"Error navegando a la sección '{texto_busqueda}': {e}")
