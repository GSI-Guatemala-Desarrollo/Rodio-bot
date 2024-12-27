import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

def harmony_introd_comprobantes_agregar_factura(driver, proveedor_id, no_factura, fecha_factura):
    """
    Ingresa al iframe principal (ptifrmtgtframe), llena los 3 campos
    y finaliza dando clic en el botón 'Añadir'.
    """

    try:
        # 1. Cambiar al iframe principal donde están los inputs
        logging.info("Cambiando al iframe principal (ptifrmtgtframe).")
        WebDriverWait(driver, 15).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "ptifrmtgtframe"))
        )
        time.sleep(1)  # Pausa para asegurar que el iframe cargó

        # 2. Ingresar Proveedor ID
        logging.info(f"Ingresando Proveedor ID: {proveedor_id}")
        input_proveedor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="VCHR_ADDSRCH_VW_VENDOR_ID"]'))
        )
        input_proveedor.clear()
        input_proveedor.send_keys(proveedor_id)
        time.sleep(2)  
        # ↑ Damos tiempo a Peoplesoft para que complete cualquier recarga automática tras ingresar el Proveedor

        # 3. Realiza la búsqueda del proveedor al interactuar con otro input
        input_no_factura = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="VCHR_ADDSRCH_VW_INVOICE_ID"]'))
        )
        input_no_factura.clear()
        input_no_factura.send_keys(" ")
        time.sleep(1)
        
        # 4. Ingresar Fecha de la factura
        logging.info(f"Ingresando Fecha de la Factura: {fecha_factura}")
        input_fecha_factura = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="VCHR_ADDSRCH_VW_INVOICE_DT"]'))
        )
        input_fecha_factura.clear()
        input_fecha_factura.send_keys(fecha_factura)
        time.sleep(1)

        # 5. Ingresar Número de factura
        logging.info(f"Ingresando Número de Factura: {no_factura}")
        input_no_factura = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="VCHR_ADDSRCH_VW_INVOICE_ID"]'))
        )
        input_no_factura.clear()
        time.sleep(1)
        input_no_factura.send_keys(no_factura)
        time.sleep(1)

        # 6. Clic en el botón "Añadir"
        logging.info("Dando clic en el botón 'Añadir'.")
        btn_anadir = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="#ICSearch"]'))
        )
        btn_anadir.click()

        logging.info("Factura añadida correctamente.")

    except Exception as e:
        logging.error("Error al agregar la factura: %s", e, exc_info=True)
        # Manejo adicional de errores si fuera necesario

import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

def harmony_introd_comprobantes_copiar_documento(driver, uni_po, no_pedido):
    """
    1. Selecciona 'N Recepción Ped' en el select (VCHR_PANELS_WRK_VCHRWS_CPY_OPT).
    2. Da clic en el link 'Ir'.
    3. Espera 2 segundos para que cargue la página.
    4. Ingresa en el campo UNI PO.
    5. Ingresa el número de pedido.
    6. Da clic en el botón 'Buscar'.
    7. Espera a que se cargue la tabla.
    8. 'Scroll' al botón 'Selec Todo' y clic en él.
    9. Clic en el botón 'Copiar Líneas Seleccionadas'.
    10. Espera a que cargue la página anterior.
    """

    try:
        logging.info("Iniciando 'harmony_introd_comprobantes_copiar_documento'...")

        # Seleccionar la opción 'N Recepción Ped' (value='PORV') en el select
        logging.info("Seleccionando opción 'N Recepción Ped' en el select.")
        select_cpy_opt = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VCHR_PANELS_WRK_VCHRWS_CPY_OPT"))
        )
        Select(select_cpy_opt).select_by_value("PORV")  # <option value="PORV">N Recepción Ped</option>

        # Clic en el link 'Ir'
        logging.info("Haciendo clic en el link 'Ir'.")
        ir_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="VCHR_PANELS_WRK_PB_GO$span"]'))
        )
        ir_link.click()

        # Espera 2s para que cargue la nueva pantalla
        logging.info("Esperando 2 segundos para que la página se recargue...")
        time.sleep(2)

        # Ingresar UNI PO
        logging.info(f"Ingresando UNI PO: {uni_po}")
        input_uni_po = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "VCHR_PANELS_WRK_BUSINESS_UNIT_PO"))
        )
        input_uni_po.clear()
        input_uni_po.send_keys(uni_po)

        # Ingresar número de pedido
        logging.info(f"Ingresando Número de Pedido: {no_pedido}")
        input_no_pedido = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "VCHR_PANELS_WRK_PO_ID"))
        )
        input_no_pedido.clear()
        input_no_pedido.send_keys(no_pedido)

        # Clic en el botón 'Buscar'
        logging.info("Dando clic en el botón 'Buscar'.")
        btn_buscar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VCHR_PANELS_WRK_PB_GET_PO"))
        )
        btn_buscar.click()

        # 7. Esperamos a que la tabla (u otro indicador) se cargue.
        #    Puedes localizar algún elemento de esa tabla para asegurar que ya esté disponible.
        logging.info("Esperando a que la tabla se cargue...")
        # Por ejemplo, podrías esperar la presencia de un elemento en la tabla:
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, '//table[@id="someTableId"]'))
        # )
        time.sleep(2)

        # 8. 'Scroll' al botón 'Selec Todo' y clic
        logging.info("Haciendo scroll hacia el botón 'Selec Todo'.")
        select_todo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VCHR_PANELS_WRK_SELECT_ALL$0"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", select_todo)
        select_todo.click()
        time.sleep(1)

        # 9. Clic en el botón 'Copiar Líneas Seleccionadas'
        logging.info("Haciendo clic en el botón 'Copiar Líneas Seleccionadas'.")
        btn_copiar_lineas = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "VCHR_PANELS_WRK_VCHR_COPY_HDR"))
        )
        btn_copiar_lineas.click()

        # 10. Esperar a que cargue la página anterior
        logging.info("Esperando 2 segundos mientras carga la página anterior...")
        time.sleep(2)

        logging.info("Función 'harmony_introd_comprobantes_copiar_documento' finalizada correctamente.")

    except Exception as e:
        logging.error("Error en 'harmony_introd_comprobantes_copiar_documento': %s", e, exc_info=True)
        # Manejo adicional de errores si fuera necesario
