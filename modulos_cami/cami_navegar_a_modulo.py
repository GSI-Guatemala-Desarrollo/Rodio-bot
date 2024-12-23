# navegar_modulos.py

import time
import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from constantes import CAMI_URL

def cami_navegar_a_modulo(driver, nombre_seccion):
    """
    Navega a la sección especificada por nombre.
    
    Args:
        driver: WebDriver activo.
        BASE_URL: URL base de la aplicación.
        nombre_seccion: Nombre de la sección a la que se desea navegar.
    """
    try:
        logging.info(f"\n\n\n-x-x-x- cami_navegar_a_modulo TRABAJO - {nombre_seccion.upper()} -x-x-x-\n")
        wait = WebDriverWait(driver, 10)

        # Navegar a la URL base de trabajo
        trabajo_url = f"{CAMI_URL}/trabajo"
        driver.get(trabajo_url)
        logging.info(f"Navegando a {trabajo_url}")

        # Esperar y hacer clic en el botón de la sección correspondiente
        time.sleep(0.5)
        boton = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//h3[text()='{nombre_seccion}']")
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton)
        time.sleep(0.5)
        boton.click()
        logging.info(f"Accedido a '{nombre_seccion}' exitosamente.")
        
    except Exception as e:
        logging.warning(f"Error al navegar a '{nombre_seccion}': {e}")
