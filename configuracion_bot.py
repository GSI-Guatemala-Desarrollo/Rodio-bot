import logging
import time
import sys
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from constantes import (
    CHROMEDRIVER_PATH,
    BRAVE_BINARY_PATH,
)


# -x-x-x- INICIO CONFIGURACIÓN -x-x-x-

class CriticalHandler(logging.Handler):
    """Detiene la ejecución al detectar un log CRITICAL para que el bot no pueda continuar (p. e. cuando la factura no existe o no logró iniciar sesión)."""

    def __init__(self, driver=None):
        super().__init__()
        self.driver = driver

    def emit(self, record):
        if record.levelno == logging.CRITICAL:
            print("Se detectó un error crítico. Cerrando el navegador...")
            if self.driver:
                try:
                    self.driver.close()
                    self.driver.quit()
                    print("Navegador cerrado correctamente.")
                except Exception as e:
                    print(f"Error al cerrar el navegador: {e}")
            else:
                print("Driver no disponible. Intenta verificar el flujo.")
            sys.exit(1)

def configurar_logging(driver=None):
    """
    Configura el logging para registrar mensajes en terminal y archivo.
    Crea un archivo de log único por ejecución con un nombre basado en la fecha y hora.
    Los logs se guardan en la carpeta 'logs' en la raíz del proyecto.
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Formato del log
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Crear la carpeta 'logs' si no existe
    logs_directory = "logs"
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    # Generar nombre único para el archivo de log basado en fecha y hora
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    log_filename = os.path.join(logs_directory, f"log_RPA_{timestamp}.log")

    # Manejador para archivo
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Manejador para terminal
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    # Limpiar manejadores existentes (evitar duplicados)
    if logger.hasHandlers():
        logger.handlers.clear()

    # Agregar manejadores
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # Agregar manejador personalizado para errores críticos
    if driver is not None:
        critical_handler = CriticalHandler(driver)
        logger.addHandler(critical_handler)
def configurar_driver():
    """
    Configura el driver de Selenium para Brave y lo inicializa sin cargar una URL.
    Retorna:
        driver: WebDriver configurado.
    """
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-gpu")

    # Evitar problemas de sandbox en contenedores
    options.add_argument("--no-sandbox")

    # Limitar logs
    options.add_argument("--log-level=3")

    # Aumentar memoria compartida en Docker u otras VMs
    options.add_argument("--disable-dev-shm-usage")

    # Ubicación del binario de Brave
    options.binary_location = BRAVE_BINARY_PATH

    # Abrir el navegador maximizado
    options.add_argument("--start-maximized")

    # Configurar preferencias de descargas
    prefs = {
        "download.default_directory": r"C:\Users\ads_edgar.menendez\Downloads",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)

    service = Service(CHROMEDRIVER_PATH)

    try:
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("Navegador Brave inicializado correctamente con configuración de descargas.")
        time.sleep(2)
        return driver
    except Exception as e:
        logging.error(f"Error al inicializar el navegador: {e}", exc_info=True)
        raise


def finalizar_automatizacion(driver):
    # -x-x-x- FIN AUTOMATIZACIÓN -x-x-x-

    # Eliminar la instancia
    try:
        time.sleep(10)
        driver.close()
        driver.quit()
        logging.info("Automatización finalizada y navegador cerrado.")
    except Exception as e:
        logging.error(f"Error al cerrar el navegador: {e}")

