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

"""
class CriticalHandler(logging.Handler):
    #Detiene la ejecución al detectar un log CRITICAL para que el bot no pueda continuar (p. e. cuando la factura no existe o no logró iniciar sesión).

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
"""

ultimo_mensaje_critico = ""


class CriticalFlowError(Exception):
    """Excepción para indicar que ocurrió un error crítico en el flujo."""
    pass

class CriticalHandler(logging.Handler):
    """Maneja errores críticos, cierra el navegador y almacena el mensaje."""
    def __init__(self, driver=None):
        super().__init__()
        self.driver = driver
        self.closed = False  # Para evitar múltiples cierres

    def emit(self, record):
        global ultimo_mensaje_critico  # Usamos la variable global
        if record.levelno == logging.CRITICAL:
            ultimo_mensaje_critico = record.getMessage()  # Guarda el mensaje crítico
            print(f"Se detectó un error crítico: {ultimo_mensaje_critico}. Cerrando el navegador...")

            if self.driver and not self.closed:
                try:
                    self.driver.close()
                    self.driver.quit()
                    print("Navegador cerrado correctamente.")
                    self.closed = True
                except Exception as e:
                    print(f"Error al cerrar el navegador: {e}")
            
            # raise CriticalFlowError("Error crítico detectado, flujo abortado.")

def configurar_logging(driver=None, numero_caso="N/A"):
    """
    Configura el logging y guarda en ULTIMO_LOG_FILE y ULTIMO_LOG_TIMESTAMP
    la ruta completa y el timestamp (YYYY-MM-DD_HH-MM) del archivo de log.
    """
    global ULTIMO_LOG_FILE, ULTIMO_LOG_TIMESTAMP

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Carpeta de logs
    logs_directory = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_directory, exist_ok=True)

    # Timestamp único
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    ULTIMO_LOG_TIMESTAMP = timestamp  # Guardamos

    # Nombre del log
    log_filename = os.path.join(
        logs_directory,
        f"log_RPA_{numero_caso}_{timestamp}.log"
    )
    ULTIMO_LOG_FILE = log_filename  # Guardamos

    # File handler
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    # Limpiamos handlers previos
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # Critical handler, si corresponde
    if driver is not None:
        from configuracion_bot import CriticalHandler
        logger.addHandler(CriticalHandler(driver))

    logging.info(f"Logging configurado para caso: {numero_caso}. Log file: {log_filename}")

    return log_filename  # Opcional, pero a veces útil
    
        
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
        "download.default_directory": r"C:\Users\Kev\Downloads",
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
        time.sleep(5)
        driver.close()
        driver.quit()
        logging.info("Navegador cerrado.")
    except Exception as e:
        logging.error(f"Error al cerrar el navegador: {e}")

