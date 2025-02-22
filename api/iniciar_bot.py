import time
from cami_api import download_documents, extract_data, get_relevant_flow, get_flow_list, get_token

SAVE_DIRECTORY = r"C:\Users\ads_edgar.menendez\Desktop\RPA\auto-SAT\api\temp_files"

def run_bot():
    """Ejecuta el bot en un bucle infinito, verificando los flujos periódicamente."""
    try:
        print("🚀 Iniciando bot")

        while True:
            try:
                time.sleep(5)
                get_flow_list()
                time.sleep(5)
                print("get_relevant_flow")
                flow = get_relevant_flow()

                if flow:
                
                    print("extract_data")
                    extracted_data = extract_data(flow)
                    print("download_documents")
                    download_documents(flow, SAVE_DIRECTORY)
                else:
                    print("❌ No se encontró un flujo válido.")

            except Exception as e:
                print(f"🚨 Error en la verificación de flujos: {e}")

            time.sleep(600)  # Espera 10 minutos antes de la siguiente iteración

    except KeyboardInterrupt:
        print("\n🛑 Bot detenido manualmente.")

if __name__ == "__main__":
    run_bot()
