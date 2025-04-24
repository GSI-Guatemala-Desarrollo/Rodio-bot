import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from constantes import (
    SAT_URL,
    SAT_USER_EMAIL,
    SAT_USER_PASSWORD,
)

def sat_dirigir_a_pagina_y_verificar_estado_login(driver):
    """
    Verifica si ya hay sesión iniciada en la página de la SAT.
    Si no hay sesión activa, carga la página de la SAT e inicia sesión.

    Args:
        driver: WebDriver activo.
    """
    logging.info("\n\n\n-x-x-x- (PASO 1) sat_dirigir_a_pagina_y_verificar_estado_login -x-x-x-\n")
    logging.info("Verificando el estado de la sesión en SAT")

    try:
        # Establecer el tiempo máximo de espera para la carga de la página
        driver.set_page_load_timeout(5)  # Espera máxima de 5 segundos para cargar la página

        logging.info("Cargando la página de la SAT...")
        driver.get(SAT_URL)
        logging.info(f"Página de la SAT cargada: {driver.current_url}")

    except TimeoutException:
        raise TimeoutException

    # Restaurar el tiempo de espera original después de la carga
    finally:
        driver.set_page_load_timeout(10)

    # Verificar si requiere inicio de sesión
    if "login" in driver.current_url:
        logging.info("No hay sesión activa. Es necesario iniciar sesión.")
        sat_login(driver, SAT_USER_EMAIL, SAT_USER_PASSWORD)
    else:
        logging.info("Sesión activa detectada.")


def sat_login(driver, username, password):
    """
    Realiza el inicio de sesión en la página de la SAT.

    Args:
        driver: WebDriver activo.
        username (str): Usuario para el inicio de sesión.
        password (str): Contraseña para el inicio de sesión.
    """
    try:
        logging.info("\n\n\n-x-x-x- (PASOS 2-3) sat_login -x-x-x-\n")
        logging.info("Realizando inicio de sesión en la SAT...")
        wait = WebDriverWait(driver, 10)

        # Esperar y encontrar los elementos de usuario, contraseña y botón
        username_input = wait.until(
            EC.presence_of_element_located((By.ID, "formContent:username"))
        )
        password_input = driver.find_element(By.ID, "formContent:password")
        login_button = driver.find_element(By.ID, "formContent:cmdbtnIngresar")

        # Ingresar credenciales
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

        # Verificar si el login fue exitoso al redirigir fuera de "login"
        time.sleep(7)  # Breve espera para redirigir
        if "login" in driver.current_url:
            logging.critical("SAT -Error de inicio de sesión: verifique la conexión o las credenciales y vuelva a intentarlo.")

        logging.info("Inicio de sesión exitoso.")
    except Exception as e:
        logging.critical(f"SAT - Error durante el inicio de sesión: {e}")
