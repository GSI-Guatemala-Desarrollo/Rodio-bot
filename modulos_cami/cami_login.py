import logging
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constantes import (
    CAMI_URL,
    CAMI_USER_EMAIL,
    CAMI_USER_PASSWORD,
)

def cami_dirigir_a_pagina_y_verificar_estado_login(driver, nombre_empresa):
    """
    Gestiona el estado actual de la aplicación CAMI y ejecuta acciones necesarias según el estado:
    - Si no hay sesión, inicia sesión automáticamente.
    - Si no se ha seleccionado empresa, selecciona la empresa proporcionada.
    - Si ya hay sesión y empresa seleccionada, no realiza ninguna acción adicional.

    Args:
        driver: WebDriver activo.
        nombre_empresa: Nombre de la empresa a seleccionar si es necesario.
    """
    logging.info("\n\n\n-x-x-x- cami_dirigir_a_pagina_y_verificar_estado_login -x-x-x-\n")
    logging.info("Verificando el estado de la sesión en CAMI")

    try:
        # Establecer un tiempo máximo de espera para la carga de la página
        driver.set_page_load_timeout(5)

        logging.info("Cargando la página de CAMI...")
        driver.get(CAMI_URL)
        logging.info(f"Página de CAMI cargada: {driver.current_url}")

    except TimeoutException:
        logging.critical("La página de CAMI no cargó dentro del tiempo esperado, revise su conexión y vuelva a intentarlo.")

    # Restaurar el tiempo de espera original después de la carga
    driver.set_page_load_timeout(10)

    try:
        # Verificar si la URL es igual a la base (sin sesión iniciada)
        current_url = driver.current_url
        logging.info(f"URL actual: {current_url}")

        if current_url.rstrip("/") == CAMI_URL.rstrip("/"):  # URL sin nada adicional
            logging.info("No se ha iniciado sesión. Iniciando sesión...")
            cami_login(driver)  # Llama a la función de login
            cami_seleccionar_empresa(driver, nombre_empresa)  # Seleccionar empresa después del login
            return

        # Verificar si aparece el texto "Selecciona una empresa a continuación"
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[text()='Selecciona una empresa a continuación']")
            )
        )
        logging.info("Sesión iniciada, pero no se ha seleccionado una empresa.")
        cami_seleccionar_empresa(driver, nombre_empresa)  # Seleccionar empresa
        return

    except TimeoutException:
        logging.info("Sesión iniciada y empresa seleccionada.")
        return


def cami_login(driver, email=CAMI_USER_EMAIL, password=CAMI_USER_PASSWORD):
    """
    Realiza el inicio de sesión en la aplicación CAMI.

    Args:
        driver: WebDriver activo.
        email: Correo electrónico del usuario (por defecto usa CAMI_USER_EMAIL).
        password: Contraseña del usuario (por defecto usa CAMI_USER_PASSWORD).
    """
    try:
        logging.info(f"\n\n-x-x-x- cami_login -x-x-x-\n\n")
        wait = WebDriverWait(driver, 10)  # Esperar hasta 10 segundos

        # Esperar a que el campo de email sea interactuable
        email_field = wait.until(EC.element_to_be_clickable((By.NAME, "user_email")))
        email_field.click()
        email_field.send_keys(email)
        logging.info("Usuario ingresado.")

        # Esperar a que el campo de contraseña sea interactuable
        password_field = wait.until(
            EC.element_to_be_clickable((By.NAME, "user_password"))
        )
        password_field.click()
        password_field.send_keys(password)
        logging.info("Contraseña ingresada.")

        # Esperar a que el botón de login sea interactuable
        login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        login_button.click()
        logging.info("Formulario de login enviado correctamente.")
    except TimeoutException as te:
        logging.warning(f"Error: Elementos del formulario no encontrados a tiempo. {te}")
    except Exception as e:
        logging.critical(f"Error durante el inicio de sesión: {e}")


def cami_seleccionar_empresa(driver, nombre_empresa):
    try:
        logging.info(f"\n\n\n-x-x-x- cami_seleccionar_empresa -x-x-x-\n")
        wait = WebDriverWait(driver, 7)

        # Esperar hasta que el botón esté presente en el DOM, si pasa de 7s no encontró la empresa.
        boton = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    f"//button[@type='button' and contains(text(), '{nombre_empresa}')]",
                )
            )
        )

        # En este caso se utiliza JS para forzar el click porque aparece "Visible: False".
        # Primero intenta hacer click normal.
        try:
            boton.click()
            logging.info(f"Empresa '{nombre_empresa}' seleccionada correctamente.")
        except Exception:
            logging.info("Forzando click con JS")
            driver.execute_script("arguments[0].click();", boton)
            logging.info(f"Empresa '{nombre_empresa}' seleccionada correctamente.")

    except Exception as e:
        logging.critical(f"Error al seleccionar la empresa: {e}")