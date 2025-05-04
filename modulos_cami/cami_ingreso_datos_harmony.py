import logging
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constantes import H_INTROD_COMPROBANTES_PDF_PATH

def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.2)

# Elige la opción de retención según el mensaje crítico, si o no funcionó SAT
def cami_eleccion_funciono_harmony(driver, critical_error_msg):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "form-select"))
        )

        select_element = driver.find_element(By.CLASS_NAME, "form-select")
        scroll_into_view(driver, select_element)

        seleccion = "No" if critical_error_msg and "Critical Harmony" in critical_error_msg else "Sí"

        try:
            Select(select_element).select_by_visible_text(seleccion)
        except Exception as e:
            logging.warning(f"Fallo al seleccionar opción. Reintentando.")
            driver.execute_script("arguments[0].selectedIndex = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
                                  select_element, 1 if seleccion == "No" else 0)

        logging.info(f"Opción seleccionada (funcionó en Harmony): {seleccion}")

        boton_siguiente = driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div[1]/main/div/div/div[2]/div/div/div/div/div[1]/div/form/div[1]/div[2]/button[2]'
        )
        scroll_into_view(driver, boton_siguiente)
        boton_siguiente.click()
        logging.info("Clic en 'Siguiente Etapa' (Harmony) realizado.")

        time.sleep(5)

    except Exception as e:
        logging.error(f"❌ Error en cami_eleccion_funciono_harmony", exc_info=True)

def cami_cargar_logs(driver, numeracion_automatica, ruta_archivo_log, fecha):
    try:
        time.sleep(5)
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
        scroll_into_view(driver, input_numeracion)
        input_numeracion.clear()
        input_numeracion.send_keys(numeracion_automatica)
        logging.info("Numeración automática ingresada.")

        input_archivo = driver.find_element(By.ID, ":r64:-file")
        scroll_into_view(driver, input_archivo)
        try:
            input_archivo.send_keys(ruta_archivo_log)
        except Exception as e:
            logging.warning(f"Fallo al cargar archivo log, reintentando")
            driver.execute_script("arguments[0].click();", input_archivo)
            input_archivo.send_keys(ruta_archivo_log)
        logging.info("Archivo .log cargado.")

        input_fecha = driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div[1]/main/div/div/div[2]/div/div/div/div/div[1]/div/form/div[2]/div[2]/div[2]/div/div[3]/input'
        )
        scroll_into_view(driver, input_fecha)
        input_fecha.send_keys(fecha)
        logging.info("Fecha ingresada.")

        boton_siguiente = driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div[1]/main/div/div/div[2]/div/div/div/div/div[1]/div/form/div[1]/div[2]/button[2]'
        )
        scroll_into_view(driver, boton_siguiente)
        boton_siguiente.click()
        logging.info("Clic en 'Siguiente Etapa' (Logs) realizado.")

        time.sleep(5)

    except Exception as e:
        logging.error(f"❌ Error en cami_cargar_logs", exc_info=True)
