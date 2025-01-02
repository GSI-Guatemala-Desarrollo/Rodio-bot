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

def harmony_dirigir_a_pagina_y_verificar_estado_login(driver, max_retries=3):
    """
    Verifica si ya hay sesión iniciada en la página de Harmony.
    Si no hay sesión activa, carga la página y hace login.
    Usa reintentos si la carga excede los 6s.
    """
    logging.info("\n\n\n-x-x-x- (PASO 1) harmony_dirigir_a_pagina_y_verificar_estado_login -x-x-x-\n")
    logging.info("Verificando el estado de la sesión en Harmony")

    reintento = 0
    while reintento < max_retries:
        try:
            # Establecer el tiempo máximo de carga a 6s (si tarda más, capturamos TimeoutException)
            driver.set_page_load_timeout(10)

            logging.info(f"Intento #{reintento+1}: Cargando la página de Harmony...")
            driver.get(HARMONY_URL)
            logging.info(f"Página de Harmony cargada: {driver.current_url}")

            # Si llegamos aquí sin excepción, rompemos el ciclo
            break

        except TimeoutException:
            reintento += 1
            logging.error(f"La página no cargó dentro de 6s. Reintento {reintento}/{max_retries}...")

            if reintento == max_retries:
                logging.critical("La página no cargó tras múltiples reintentos. Abortando proceso.")
                return  # o lanzar una excepción, dependiendo de tu flujo

    # (Opcional) restaurar un page_load_timeout más largo para pasos posteriores
    driver.set_page_load_timeout(10)

    # Verificar si requiere inicio de sesión
    if "login" in driver.current_url.lower():
        logging.info("No hay sesión activa. Es necesario iniciar sesión.")
        harmony_login(driver, HARMONY_USER_EMAIL, HARMONY_USER_PASSWORD)
    else:
        logging.info("Sesión activa detectada.")


def harmony_login(driver, username, password):
    """
    Realiza el inicio de sesión en la página de Harmony.
    Usa un WebDriverWait para esperar que la URL deje de contener 'login'.
    """
    try:
        logging.info("\n\n\n-x-x-x- (PASOS 2-3) harmony_login -x-x-x-\n")
        logging.info("Realizando inicio de sesión en Harmony...")
        wait = WebDriverWait(driver, 10)

        # 1. Esperar a que aparezcan los campos de usuario/contraseña
        username_input = wait.until(
            EC.presence_of_element_located((By.ID, "userid"))
        )
        password_input = driver.find_element(By.ID, "pwd")
        login_button = driver.find_element(By.XPATH, '//*[@id="login"]/div/div[1]/div[8]/input')

        # 2. Ingresar credenciales y hacer clic
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

        # 3. Esperar a que la URL deje de contener 'login'
        #    Usamos una lambda que evalúa el driver.current_url
        try:
            wait.until(
                lambda d: "login" not in d.current_url.lower()
            )
            logging.info("Inicio de sesión exitoso.")
        except TimeoutException:
            logging.critical(
                "Error de inicio de sesión: La página tardó demasiado en redirigir. "
                "Revise la conexión o las credenciales."
            )

    except Exception as e:
        logging.critical(
            f"Error inesperado durante el inicio de sesión: {e}", 
            exc_info=True
        )