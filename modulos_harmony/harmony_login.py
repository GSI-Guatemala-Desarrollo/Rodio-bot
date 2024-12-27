import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from constantes import (
    HARMONY_URL,
    HARMONY_USER_EMAIL,
    HARMONY_USER_PASSWORD,
)

def harmony_dirigir_a_pagina_y_verificar_estado_login(driver):
    """
    Verifica si ya hay sesión iniciada en la página de Harmony.
    Si no hay sesión activa, carga la página de Harmony e inicia sesión.

    Args:
        driver: WebDriver activo.
    """
    logging.info("\n\n\n-x-x-x- (PASO 1) harmony_dirigir_a_pagina_y_verificar_estado_login -x-x-x-\n")
    logging.info("Verificando el estado de la sesión en Harmony")

    try:
        # Establecer el tiempo máximo de espera para la carga de la página
        driver.set_page_load_timeout(5)

        logging.info("Cargando la página de Harmony...")
        driver.get(HARMONY_URL)
        logging.info(f"Página de Harmony cargada: {driver.current_url}")

    except TimeoutException:
        logging.critical("La página no cargó dentro del tiempo esperado, revise su conexión y vuelva a intentarlo.")

    # Restaurar el tiempo de espera original después de la carga
    driver.set_page_load_timeout(10)

    # Verificar si requiere inicio de sesión
    if "login" in driver.current_url:
        logging.info("No hay sesión activa. Es necesario iniciar sesión.")
        harmony_login(driver, HARMONY_USER_EMAIL, HARMONY_USER_PASSWORD)
    else:
        logging.info("Sesión activa detectada.")


def harmony_login(driver, username, password):
    """
    Realiza el inicio de sesión en la página de Harmony.

    Args:
        driver: WebDriver activo.
        username (str): Usuario para el inicio de sesión.
        password (str): Contraseña para el inicio de sesión.
    """
    try:
        logging.info("\n\n\n-x-x-x- (PASOS 2-3) harmony_login -x-x-x-\n")
        logging.info("Realizando inicio de sesión en Harmony...")
        wait = WebDriverWait(driver, 10)

        # Esperar y encontrar los elementos de usuario, contraseña y botón
        username_input = wait.until(
            EC.presence_of_element_located((By.ID, "userid"))
        )
        password_input = driver.find_element(By.ID, "pwd")
        login_button = driver.find_element(By.XPATH, '//*[@id="login"]/div/div[1]/div[8]/input')

        # Ingresar credenciales
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

        # Verificar si el login fue exitoso al redirigir fuera de "login"
        time.sleep(7)  # Breve espera para redirigir
        if "login" in driver.current_url:
            logging.critical("Error de inicio de sesión: verifique la conexión o las credenciales y vuelva a intentarlo.")

        logging.info("Inicio de sesión exitoso.")
    except Exception as e:
        logging.critical(f"Error durante el inicio de sesión: {e}")
