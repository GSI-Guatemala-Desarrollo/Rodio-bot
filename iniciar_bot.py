import logging
import time
from conexion_y_manejo_datos.ejecucion_casos import eleccion_caso_bot, estandarizacion_de_datos
from conexion_y_manejo_datos.cami_api import download_documents, extract_data, get_assigned_flows, get_current_flow_data, get_relevant_flow
from configuracion_bot import CriticalFlowError, configurar_driver, configurar_logging
from modulos_cami.cami_flujos import notificar_y_subir_archivos_cami
import configuracion_bot

def run_bot():
    """Ejecuta el bot en un bucle infinito, verificando los flujos periódicamente."""
    try:
        print("🚀 Iniciando bot")

        while True:
            try:
                
                time.sleep(5)
                print("get_assigned_flows")
                get_assigned_flows()
                
                time.sleep(5)
                print("get_relevant_flow")
                flow = get_relevant_flow()
                creationDate = flow.get('creationDate')
                print(f"Fecha de creación del flujo: {creationDate}")

                if flow:
                    flow_id = flow.get("_id")  # Asegurar que se extrae el ID del flujo
                    if flow_id:
                        
                        print("get_current_flow_data")
                        flow_data = get_current_flow_data(flow_id)

                        if flow_data:
                            
                            print("extract_data")
                            extracted_data = extract_data(flow_data)
                            
                            # Configurar el driver y logging primero
                            numeracion_automatica = extracted_data.get("numeracion_automatica", "N/A")
                            driver = configurar_driver()
                            configurar_logging(driver, numeracion_automatica)  # Manejo de logs críticos con el driver actual
                            
                            # Mostrar datos extraídos para depuración
                            logging.info("\n Datos extraídos:")
                            for key, value in extracted_data.items():
                                logging.info(f"{key}: {value}")
                            
                            
                            print("\ndownload_documents")
                            download_documents(extracted_data)
                            
                            
                            print("estandarizacion_de_datos")
                            modified_data = estandarizacion_de_datos(extracted_data)
                            
                            
                            print("eleccion_caso_bot")
                            eleccion_caso_bot(modified_data, driver)
                            
                            
                            print("notificar_y_subir_archivos_cami")
                            notificar_y_subir_archivos_cami(configuracion_bot.ultimo_mensaje_critico, creationDate, modified_data)
                            
                        else:
                            print("❌ No se pudieron obtener los datos del flujo actual.")
                    else:
                        print("❌ No se encontró un ID de flujo válido.")
                else:
                    print("❌ No se encontró un flujo válido.")
                # Llamar a la función con el mensaje crítico (si hay)
    
            #except CriticalFlowError as cfe:
            #    print(f"🚨 Error crítico en el flujo: {cfe}. Cerrando navegador y pasando al siguiente flujo.")
                # Aquí ya se cerró el navegador dentro del CriticalHandler, así que solo dejamos de ejecutar el caso actual.
            except Exception as e:
                print(f"🚨 Error en la verificación de flujos: {e}")

            print("\n\nSiguiente flujo.")
            time.sleep(10)  # Espera 1h antes de la siguiente iteración

    except KeyboardInterrupt:
        print("\n🛑 Bot detenido manualmente.")

if __name__ == "__main__":
    run_bot()
