import json
import logging
import os
from urllib.parse import urlparse
import requests
from datetime import datetime, timedelta
from configuracion_bot import configurar_driver, configurar_logging
from constantes import DIRECTORIO_COMPROBANTE, DIRECTORIO_FACTURA

# ID del flujo recepción de facturas
ID_FLUJO_PROVEEDORES="677707350fae253008de917c"

# ID de la etapa para datos del bot
TARGET_STAGE_ID = "67a4f4f597d02bd450ba5f66"

# Cargar variables de entorno
CAMI_USER = os.getenv("CAMI_USER")
CAMI_PASSWORD = os.getenv("CAMI_PASSWORD")
ID_EMPRESA = os.getenv("ID_EMPRESA")

# API URLs
LOGIN_URL = f"https://apitest.camiapp.net/auth/login/bycredentials"
FLOW_ASSIGNED_URL = f"https://apitest.camiapp.net/flow/v2/flow/assigned/{ID_EMPRESA}"
FLOW_LIST_URL = f"https://apitest.camiapp.net//flow/v2/flow/list/{ID_EMPRESA}/{ID_FLUJO_PROVEEDORES}"
CURRENT_FLOW_URL = f"https://apitest.camiapp.net/flow/v2/flow/current/{ID_EMPRESA}"

# Rutas de archivos json
JSON_ASSIGNED_PATH = r"C:\Users\ads_kevin.gonzalez\Desktop\RPA\auto-SAT\conexion_y_manejo_datos\archivos_flujo_en_ejecucion\lista_de_flujos.json"
JSON_CURRENT_PATH = r"C:\Users\ads_kevin.gonzalez\Desktop\RPA\auto-SAT\conexion_y_manejo_datos\archivos_flujo_en_ejecucion\current_flow_data.json"
# JSON_ASSIGNED_PATH = r"C:\Users\ads_edgar.menendez\Desktop\RPA\auto-SAT\conexion_y_manejo_datos\archivos_flujo_en_ejecucion\lista_de_flujos.json"
# JSON_CURRENT_PATH = r"C:\Users\ads_edgar.menendez\Desktop\RPA\auto-SAT\conexion_y_manejo_datos\archivos_flujo_en_ejecucion\current_flow_data.json"

"""
token = None
expiration_time = None
"""

# Token de prueba (no se obtiene de la API)
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwic3ViIjoieVZ5UEJ5cTl3OUlxWGJxczBpNzMiLCJhcHBfYWNjZXNzX2tleSI6bnVsbCwiZXhwIjoxNzQ1OTY3MTg5fQ.Gq8NRulRtKD2STqwDuyLdnu7MFfEIGXQZOfNYErwd7c"
expiration_time = datetime.strptime("2025-04-29T22:53:09.883998+00:00", "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=None)

GUATEMALA_OFFSET = timedelta(hours=-6)  # GMT-6

def get_token():
    """Devuelve el token actual si es válido, de lo contrario, obtiene uno nuevo."""
    global token, expiration_time

    if not token or not expiration_time:
        print("🔄 Token expirado o inexistente. Obteniendo nuevo token...")
        return authenticate()

    # Convertir expiration_time a UTC sumando 6 horas
    expiration_time_utc = expiration_time + GUATEMALA_OFFSET

    if (expiration_time_utc - datetime.utcnow()) <= timedelta(hours=1):
        print("🔄 Token expirado o por expirar pronto. Obteniendo nuevo token...")
        return authenticate()

    print(f"🔐 Token actual válido: {token[:20]}...")  # Solo imprime los primeros caracteres
    return token

def authenticate():
    """Obtiene un nuevo token de autenticación y actualiza la expiración."""
    global token, expiration_time
    response = requests.post(LOGIN_URL, json={"email": CAMI_USER, "password": CAMI_PASSWORD}, verify=False)


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

# API con el listado de los flujos asignados.
def get_assigned_flows():
    """Obtiene la lista de flujos asignados desde CamiAPI y la guarda en un archivo JSON."""
    
    print("\n🔍 Verificando flujos asignados y actuales.")
    token = get_token()

    if not token:
        print("❌ Error: No se pudo obtener el token de acceso.")
        return None

    headers = {"X-Access-Token": token}
    response = requests.get(FLOW_ASSIGNED_URL, headers=headers, verify=False)


    print(f"\n📡 Respuesta de la API (status {response.status_code})")

    if response.status_code == 200:
        try:
            data = response.json()
            
            with open(JSON_ASSIGNED_PATH, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            
            print(f"✅ Lista de flujos asignados guardada en: {JSON_ASSIGNED_PATH}")
            return data  # Devuelve los datos para su uso inmediato si es necesario

        except json.JSONDecodeError:
            print("❌ Error: La API devolvió datos en un formato incorrecto.")
            return None
    else:
        print(f"❌ Error en la petición a CamiAPI: {response.status_code}")
        return None


# Busca en el listado de flujos asignados, el primero que se encuentre en la etapa "resumen bot".
def get_relevant_flow():
    data = load_json(JSON_ASSIGNED_PATH)  # Cargar JSON
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

# Funcion generica para cargar el json.
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

# Usa el API de current para extraer los datos del flujo exacto de la etapa "resumen bot" que se encontró anteriormente.
def get_current_flow_data(flow_id):
    """Obtiene los datos completos de un flujo específico desde la API de `current`."""
    url = f"{CURRENT_FLOW_URL}/{flow_id}"
    
    print(f"\n🔍 Obteniendo datos del flujo actual: {flow_id}")
    
    token = get_token()
    headers = {"X-Access-Token": token}
    
    response = requests.get(url, headers=headers, verify=False)
    print(f"📡 Respuesta de la API `current` (status {response.status_code})")

    if response.status_code == 200:
        try:
            data = response.json()
            
            with open(JSON_CURRENT_PATH, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            
            print(f"✅ Datos del flujo guardados en: {JSON_CURRENT_PATH}")
            return data

        except json.JSONDecodeError:
            print("❌ Error: La API devolvió datos en un formato incorrecto.")
    else:
        print(f"❌ Error en la petición a la API `current`: {response.status_code}")

    return None

# Extrae los datos necesarios para el funcionamiento del bot del flujo seleccionado.

def extract_data(flow):
    """Extrae los datos relevantes de un flujo, incluyendo enlaces de descarga y numeración automática.
       También extrae y guarda los nombres de los archivos PDF descargados.
    """

    if not isinstance(flow, dict):
        print(f"❌ Error: `flow` no es un diccionario. Tipo recibido: {type(flow)}")
        return None

    extracted_data = {}

    # Extraer "Numeración Automática" desde "finishedStages"
    finished_stages = flow.get("data", {}).get("finishedStages", [])
 
    # Lista de claves a extraer en orden
    required_keys = [
        "numeracion_automatica",
        "declara_isr",
        "  flujo_contribuyente",
        "tipo_retencion",
        "s_emision_constancias_nit_retenido",
        "s_emision_constancias_serie_de_factura",
        " s_emision_constancias_no_de_factura",
        "s_emision_constancias_nombre_proveedor",
        "s_emision_constancias_fecha_factura",
        "categoria_de_rentas_opcion_categoria_de_renta",
        "categoria_de_rentas_opcion_regimen",
        "h_introd_comprobantes_id_proveedor",
        "h_introd_comprobantes_no_pedido",
        "h_introd_comprobantes_iva",
        "h_introd_comprobantes_comentario",
        "h_introd_comprobantes_lista_descripciones",
    ]

    # Extraer datos de "sections"
    sections = flow.get("data", {}).get("data", {}).get("sections", [])
    
    for key in required_keys:
        found = False
        for section in sections:
            for field in section.get("fields", []):
                if field.get("name") == key:
                    extracted_data[key] = field.get("defaultValue", "")
                    found = True
                    break
            if found:
                break
        if not found:
            extracted_data[key] = ""  # Si no se encuentra, se deja vacío

    # Buscar enlaces de descarga en "Comprobante de Entrega" y "Factura"
    comprobante_link = ""
    factura_link = ""
    nombre_comprobante_entrega = ""
    nombre_factura = ""

    for stage in finished_stages:  
        for data_entry in stage.get("data", []):
            if not isinstance(data_entry, dict):  # Nueva validación
                print(f"⚠️ Advertencia: `data_entry` no es un diccionario, se encontró {type(data_entry)}")
                continue

            if data_entry.get("name") in ["Comprobante de Entrega", "Factura"]:
                for row in data_entry.get("rows", [[]]):
                    for item in row:
                        if isinstance(item, dict) and item.get("name") == "Cargar Documento":
                            values = item.get("values", [[None]])
                            if isinstance(values, list) and values and isinstance(values[0], list):
                                link = values[0][0]
                            else:
                                link = ""

                            if data_entry["name"] == "Comprobante de Entrega":
                                comprobante_link = link
                                nombre_comprobante_entrega = os.path.basename(link) if link else ""
                            elif data_entry["name"] == "Factura":
                                factura_link = link
                                nombre_factura = os.path.basename(link) if link else ""

    # Agregar los links y nombres de archivos al diccionario
    extracted_data["comprobante_entrega"] = comprobante_link
    extracted_data["nombre_comprobante_entrega"] = nombre_comprobante_entrega
    extracted_data["factura"] = factura_link
    extracted_data["nombre_factura"] = nombre_factura

    return extracted_data


def download_documents(flow):
    """Descarga los documentos de las URLs 'factura' y 'comprobante_entrega' y los guarda en los directorios correspondientes."""
    
    if not isinstance(flow, dict):
        print(f"❌ Error: `flow` no es un diccionario. Tipo recibido: {type(flow)}")
        return None

    # Crear los directorios si no existen
    os.makedirs(DIRECTORIO_COMPROBANTE, exist_ok=True)
    os.makedirs(DIRECTORIO_FACTURA, exist_ok=True)

    # Obtener las URLs de los documentos
    factura_url = flow.get("factura")
    comprobante_url = flow.get("comprobante_entrega")

    # Verificar si ambos URLs están presentes
    if factura_url:
        file_name = os.path.basename(urlparse(factura_url).path)
        if not file_name.lower().endswith(".pdf"):
            file_name += ".pdf"
        save_path = os.path.join(DIRECTORIO_FACTURA, file_name)
        download_file(factura_url, save_path)
    
    if comprobante_url:
        file_name = os.path.basename(urlparse(comprobante_url).path)
        if not file_name.lower().endswith(".pdf"):
            file_name += ".pdf"
        save_path = os.path.join(DIRECTORIO_COMPROBANTE, file_name)
        download_file(comprobante_url, save_path)

    logging.info("Ambos documentos descargados, finalizando función.")

def download_file(url, save_path):
    """Descarga un archivo desde una URL y lo guarda en la ubicación especificada."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        logging.info(f"Archivo descargado: {save_path}")
    else:
        logging.error(f"Error al descargar {url}")

    """
def download_documents(flow):
    #Descarga documentos desde URLs obtenidas en el flujo y los guarda en los directorios correspondientes.

    if not isinstance(flow, dict):
        print(f"❌ Error: `flow` no es un diccionario. Tipo recibido: {type(flow)}")
        return None

    os.makedirs(DIRECTORIO_COMPROBANTE, exist_ok=True)
    os.makedirs(DIRECTORIO_FACTURA, exist_ok=True)

    extracted_names = {"nombre_comprobante_entrega": "", "nombre_factura": ""}
    comprobante_descargado = False
    factura_descargada = False

    for stage in flow.get("data", {}).get("finishedStages", []):
        for data_entry in stage.get("data", []):
            if data_entry.get("name") in ["Comprobante de Entrega", "Factura"]:
                for row in data_entry.get("rows", [[]]):
                    for item in row:
                        if item.get("name") == "Cargar Documento":
                            doc_url = item.get("values", [[None]])[0][0]
                            if doc_url:
                                # Extraer el nombre original del archivo desde la URL
                                file_name = os.path.basename(urlparse(doc_url).path)

                                # Asegurar que el archivo tenga la extensión .pdf
                                if not file_name.lower().endswith(".pdf"):
                                    file_name += ".pdf"

                                # Elegir el directorio correcto
                                if data_entry.get("name") == "Comprobante de Entrega" and not comprobante_descargado:
                                    save_path = os.path.join(DIRECTORIO_COMPROBANTE, file_name)
                                    extracted_names["nombre_comprobante_entrega"] = file_name
                                    comprobante_descargado = True
                                elif data_entry.get("name") == "Factura" and not factura_descargada:
                                    save_path = os.path.join(DIRECTORIO_FACTURA, file_name)
                                    extracted_names["nombre_factura"] = file_name
                                    factura_descargada = True

                                # Descargar el archivo
                                download_file(doc_url, save_path)

                                # Si ya descargamos ambos, terminamos la función
                                if comprobante_descargado and factura_descargada:
                                    print("✅ Se han descargado ambos documentos, finalizando función.")
                                    return extracted_names

    return extracted_names  # Devuelve los nombres de los archivos descargados

def download_file(url, save_path):
    #Descarga un archivo desde una URL y lo guarda en la ubicación especificada.
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"✅ Archivo descargado: {save_path}")
    else:
        print(f"❌ Error al descargar {url}")


def get_flow_list():
 
    global JSON_ASSIGNED_PATH
    
    print("\n Verificando flujos asignados.")
    token = get_token()

    headers = {"X-Access-Token": token}
    response = requests.get(FLOW_LIST_URL, headers=headers)

    print(f"\n Respuesta de la API (status {response.status_code})")

    if response.status_code == 200:
        try:
            data = response.json()
            
            with open(JSON_ASSIGNED_PATH, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            
            print(f"✅ Lista de flujos guardada en: {JSON_ASSIGNED_PATH}")
        except json.JSONDecodeError:
            print("❌ Error: La API devolvió datos en un formato incorrecto.")
    else:
        print(f"❌ Error en la petición a CamiAPI: {response.status_code}")

    """