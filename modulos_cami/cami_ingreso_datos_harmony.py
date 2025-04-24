import logging
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constantes import H_INTROD_COMPROBANTES_PDF_PATH

# Elige la opción de retención según el mensaje crítico, si o no funcionó SAT
def cami_eleccion_funciono_harmony(driver, critical_error_msg):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "form-select"))
        )

        select_element = driver.find_element(By.CLASS_NAME, "form-select")
        select = Select(select_element)

        if critical_error_msg and "Critical Harmony" in critical_error_msg:
            seleccion = "No"
        else:
            seleccion = "Sí"

        select.select_by_visible_text(seleccion)
        logging.info(f"Opción seleccionada (funcionó en Harmony): {seleccion}")

        # Clic en "Siguiente Etapa"
        boton_siguiente = driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div[1]/main/div/div/div[2]/div/div/div/div/div[1]/div/form/div[1]/div[2]/button[2]'
        )
        boton_siguiente.click()
        logging.info("Clic en 'Siguiente Etapa' (Harmony) realizado.")

        time.sleep(5)

    except Exception as e:
        logging.error(f"❌ Error en cami_eleccion_funciono_harmony: {e}", exc_info=True)

def cami_cargar_logs(driver, numeracion_automatica, ruta_archivo_log, fecha):
    try:
        # Esperar a que aparezca el input de numeración automática
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="root"]/div[1]/main/div/div/div[2]/div/div/div/div/div[1]/div/form/div[2]/div[2]/div[2]/div/div[1]/input'
            ))
        )

        input_numeracion = driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div[1]/main/div/div/div[2]/div/div/div/div/div[1]/div/form/div[2]/div[2]/div[2]/div/div[1]/input'
        )
        input_numeracion.clear()
        input_numeracion.send_keys(numeracion_automatica)
        logging.info("Numeración automática ingresada.")

        # Subir archivo .log
        input_archivo = driver.find_element(By.ID, ":r64:-file")
        input_archivo.send_keys(ruta_archivo_log)
        logging.info("Archivo .log cargado.")

        # Ingresar fecha
        input_fecha = driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div[1]/main/div/div/div[2]/div/div/div/div/div[1]/div/form/div[2]/div[2]/div[2]/div/div[3]/input'
        )
        input_fecha.send_keys(fecha)
        logging.info("Fecha ingresada.")

        # Click en Siguiente Etapa
        boton_siguiente = driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div[1]/main/div/div/div[2]/div/div/div/div/div[1]/div/form/div[1]/div[2]/button[2]'
        )
        boton_siguiente.click()
        logging.info("Clic en 'Siguiente Etapa' (Logs) realizado.")

        time.sleep(5)

    except Exception as e:
        logging.error(f"❌ Error en cami_cargar_logs: {e}", exc_info=True)
