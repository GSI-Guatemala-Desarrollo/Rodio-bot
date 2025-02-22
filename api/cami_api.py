import json
import os
import requests
from datetime import datetime, timedelta
ID_FLUJO_PROVEEDORES="677707350fae253008de917c"
ID_FLUJO_TEST="6786cda90fae253008de9212"
# Cargar variables de entorno
CAMI_USER = os.getenv("CAMI_USER")
CAMI_PASSWORD = os.getenv("CAMI_PASSWORD")
ID_EMPRESA = os.getenv("ID_EMPRESA")
LOGIN_URL = f"https://apitest.camiapp.net/auth/login/bycredentials"
FLOW_LIST_URL = f"https://apitest.camiapp.net//flow/v2/flow/list/{ID_EMPRESA}/{ID_FLUJO_PROVEEDORES}"

# Rutas de archivos
JSON_PATH = r"C:\Users\ads_edgar.menendez\Desktop\RPA\auto-SAT\api\temp_files\lista_de_flujos.json"


# ID de la etapa para datos del bot
TARGET_STAGE_ID = "67a4f4f597d02bd450ba5f66"



"""
token = None
expiration_time = None

"""
# Token de prueba (no se obtiene de la API)
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwic3ViIjoieVZ5UEJ5cTl3OUlxWGJxczBpNzMiLCJhcHBfYWNjZXNzX2tleSI6bnVsbCwiZXhwIjoxNzQwMzQ0ODU5fQ.eG2ITQInLkRI-JUaMkjHVJ868op37n7IpFAykbR5pbM"
expiration_time = datetime.strptime("2025-02-23T21:07:39.904303+00:00", "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=None)

def get_token():
    """Devuelve el token actual si es válido, de lo contrario, obtiene uno nuevo."""
    global token, expiration_time
    if not token or not expiration_time or (expiration_time - datetime.utcnow()) <= timedelta(hours=1):
        print("🔄 Token expirado o inexistente. Obteniendo nuevo token...")
        return authenticate()

    print(f"🔐 Token actual válido: {token[:20]}...")  # Solo imprime los primeros caracteres
    return token

def authenticate():
    """Obtiene un nuevo token de autenticación y actualiza la expiración."""
    global token, expiration_time
    response = requests.post(LOGIN_URL, json={"email": CAMI_USER, "password": CAMI_PASSWORD})

    print(f"🔍 Respuesta de autenticación (status {response.status_code})")  # <-- Ver qué devuelve la API

    if response.status_code == 200:
        try:
            data = response.json()
            print(f"🔑 Datos de autenticación recibidos: {data}")  # <-- Imprimir datos completos
            
            if data["code"] == 0:
                token = data["data"]["access_token"]
                expiration_str = data["data"]["expiration"]
                expiration_time = datetime.strptime(expiration_str, "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=None)
                print(f"✅ Nuevo token obtenido, expira en: {expiration_time}")
                return token
            else:
                print(f"❌ Error en autenticación: {data}")
        except Exception as e:
            print(f"❌ Error procesando respuesta de autenticación: {e}")
    
    raise Exception("❌ Error al autenticar con CamiAPI")

def get_flow_list():
    """Obtiene la lista de flujos desde CamiAPI y la guarda en un archivo JSON."""
    global JSON_PATH
    
    print("\n Verificando flujos asignados.")
    token = get_token()

    headers = {"X-Access-Token": token}
    response = requests.get(FLOW_LIST_URL, headers=headers)

    print(f"\n Respuesta de la API (status {response.status_code})")

    if response.status_code == 200:
        try:
            data = response.json()
            
            with open(JSON_PATH, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            
            print(f"✅ Lista de flujos guardada en: {JSON_PATH}")
        except json.JSONDecodeError:
            print("❌ Error: La API devolvió datos en un formato incorrecto.")
    else:
        print(f"❌ Error en la petición a CamiAPI: {response.status_code}")


def load_json(filepath):
    """Carga un archivo JSON desde la ruta especificada."""
    with open(filepath, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)  # Cargar JSON
            print(f"🔍 Tipo de data cargada desde {filepath}: {type(data)}")  # <-- Ver qué tipo de dato es
            return data
        except json.JSONDecodeError:
            print(f"❌ Error: El archivo JSON en {filepath} no tiene un formato válido.")
            return {}  # Retorna un diccionario vacío en caso de error

def get_relevant_flow():
    data = load_json(JSON_PATH)  # Cargar JSON
    print(f"🔍 Tipo de datos en `get_relevant_flow()`: {type(data)}")

    if not isinstance(data, dict):
        print("❌ Error: `data` no es un diccionario.")
        return None

    for flow in data.get("data", []):  
        print(f"⏩ Revisando flujo con ID: {flow.get('_id')} y currentStageId: {flow.get('currentStageId')}")

        if flow.get("currentStageId") == "67a4f4f597d02bd450ba5f66":
            print("✅ Flujo correcto encontrado:")
            print(f"ID: {flow.get('_id')}, Fecha: {flow.get('creationDate')}")
            return flow  

    print("❌ No se encontró un flujo con el currentStageId esperado.")
    return None

def extract_data(flow):
    """Extrae los datos relevantes de un flujo."""
    
    if not isinstance(flow, dict):
        print(f"❌ Error: `flow` no es un diccionario. Tipo recibido: {type(flow)}")
        print(f"📝 Contenido de flow (primeros 500 caracteres): {repr(flow)[:500]}")
        return None

    extracted_data = {}
    required_keys = {
        "Numeración Automática", "ID Proveedor", "Nombre Proveedor", "NIT",
        "Tipo de Contribuyente", "% Retención IVA", "Aplica Retención ISR",
        "Número de Orden de compra", "Número Factura", "Serie Factura",
        "Fecha de Factura", "Comentario", "Cargar Documento"
    }

    print("🔍 Iniciando extracción de datos...")
    
    finished_stages = flow.get("finishedStages", [])

    if not isinstance(finished_stages, list):
        print(f"❌ Error: `finishedStages` no es una lista. Tipo recibido: {type(finished_stages)}")
        return None
    
    for stage in finished_stages:
        if not isinstance(stage, dict):
            print(f"⚠️ Advertencia: `stage` no es un diccionario. Tipo recibido: {type(stage)}")
            continue

        print(f"📌 Revisando stage: {repr(stage)[:200]}")  # Muestra parte del stage para debug
        
        for data_entry in stage.get("data", []):
            if not isinstance(data_entry, dict):
                print(f"⚠️ Advertencia: `data_entry` no es un diccionario. Tipo recibido: {type(data_entry)}")
                continue

            for row in data_entry.get("rows", []):
                if not isinstance(row, list):
                    print(f"⚠️ Advertencia: `row` no es una lista. Tipo recibido: {type(row)}")
                    continue

                for item in row:
                    if isinstance(item, dict):
                        key = item.get("name")
                        value = item.get("values", [None])[0]

                        if key in required_keys:
                            extracted_data[key] = value

    print("\n✅ **Datos extraídos:**")
    for key, value in extracted_data.items():
        print(f"{key}: {value}")

    return extracted_data


def download_documents(flow, save_dir):
    """Descarga documentos desde URLs obtenidas en el flujo."""
    os.makedirs(save_dir, exist_ok=True)

    doc_map = {
        "Factura": "factura_bot.pdf",
        "Orden de Compra": "orden_compra_bot.pdf",
        "Comprobante de Entrega": "comprobante_bot.pdf"
    }

    for stage in flow.get("finishedStages", []):
        for data_entry in stage.get("data", []):
            if data_entry.get("name") in doc_map:
                for row in data_entry.get("rows", [[]]):
                    for item in row:
                        if item.get("name") == "Cargar Documento":
                            doc_url = item.get("values", [[None]])[0][0]
                            if doc_url:
                                download_file(doc_url, os.path.join(save_dir, doc_map[data_entry.get("name")]))


def download_file(url, save_path):
    """Descarga un archivo desde una URL y lo guarda en la ubicación especificada."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"✅ Archivo descargado: {save_path}")
    else:
        print(f"❌ Error al descargar {url}")