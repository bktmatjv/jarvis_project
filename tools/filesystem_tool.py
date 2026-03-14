import os
import shutil
from pathlib import Path

# funciones para manejar archivos y carpetas, como crear, escribir, leer, eliminar y listar. La idea es que puedas enviar órdenes al cerebro como "crea una carpeta en el escritorio llamada 'proyecto'", o "escribe 'hola mundo' en un archivo llamado 'nota.txt' dentro de la carpeta 'proyecto'", o "léeme el contenido de esa nota", o "bórrame la carpeta completa". Y esta herramienta se encarga de traducir esas órdenes a comandos del sistema operativo para manipular el sistema de archivos de Windows.
# AUN EN DESARROLLO, NO TODAS LAS FUNCIONES ESTÁN IMPLEMENTADAS O OPTIMIZADAS, PERO LA IDEA ES QUE SEA UNA HERRAMIENTA MUY VERSÁTIL PARA CONTROLAR ARCHIVOS Y CARPETAS DESDE EL CEREBRO DE JARVIS.

# Diccionario de rutas estándar de Windows detectadas dinámicamente
BASE_DIRECTORIES = {
    "desktop": Path.home() / "Desktop",
    "documents": Path.home() / "Documents",
    "downloads": Path.home() / "Downloads",
    "music": Path.home() / "Music",
    "pictures": Path.home() / "Pictures",
    "videos": Path.home() / "Videos",
    "root": Path.home()  # C:/Users/TuUsuario
}

def _resolve_path(path_string):
    """
    Traduce rutas amigables (ej: 'desktop/nota.txt') a rutas reales de Windows.
    """
    if not path_string:
        return None
        
    # Normalizamos separadores y limpiamos espacios
    path_string = path_string.replace("\\", "/").strip()
    parts = path_string.split("/")
    first_folder = parts[0].lower()

    if first_folder in BASE_DIRECTORIES:
        base_path = BASE_DIRECTORIES[first_folder]
        # Unimos la base con el resto de la ruta (si existe)
        full_path = base_path.joinpath(*parts[1:])
        return str(full_path)
    
    # Si no es una ruta especial, devolvemos la ruta absoluta desde el proyecto
    return os.path.abspath(path_string)

def create_folder(params):
    """Crea una carpeta en una ruta base o relativa."""
    path_raw = params.get("name")
    full_path = _resolve_path(path_raw)
    
    try:
        os.makedirs(full_path, exist_ok=True)
        print(f"📁 Jarvis: Carpeta asegurada en '{full_path}'")
    except Exception as e:
        print(f"❌ Error al crear carpeta: {e}")

def create_file(params):
    """Crea un archivo vacío."""
    path_raw = params.get("path")
    full_path = _resolve_path(path_raw)
    
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            pass
        print(f"📄 Jarvis: Archivo creado en '{full_path}'")
    except Exception as e:
        print(f"❌ Error al crear archivo: {e}")

def write_file(params):
    """Escribe contenido en un archivo (sobrescribe)."""
    path_raw = params.get("path")
    content = params.get("content", "")
    full_path = _resolve_path(path_raw)
    
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✍️ Jarvis: Contenido escrito en '{full_path}'")
    except Exception as e:
        print(f"❌ Error al escribir: {e}")

def read_file(params):
    """Lee y retorna el contenido de un archivo."""
    path_raw = params.get("path")
    full_path = _resolve_path(path_raw)
    
    try:
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                data = f.read()
            print(f"📖 Jarvis: Archivo '{full_path}' leído.")
            return data
        else:
            print(f"⚠️ El archivo '{full_path}' no existe.")
            return None
    except Exception as e:
        print(f"❌ Error al leer: {e}")
        return None

def delete_path(params):
    """Elimina archivos o carpetas recursivamente."""
    path_raw = params.get("path")
    full_path = _resolve_path(path_raw)
    
    try:
        if os.path.isfile(full_path):
            os.remove(full_path)
            print(f"🗑️ Jarvis: Archivo '{full_path}' eliminado.")
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)
            print(f"🗑️ Jarvis: Carpeta '{full_path}' eliminada.")
        else:
            print(f"⚠️ No se encontró nada para borrar en '{full_path}'.")
    except Exception as e:
        print(f"❌ Error al eliminar: {e}")

def list_directory(params):
    """Lista el contenido de una ruta."""
    path_raw = params.get("path", "root") # Por defecto carpeta de usuario
    full_path = _resolve_path(path_raw)
    
    try:
        if os.path.exists(full_path):
            items = os.listdir(full_path)
            print(f"📂 Jarvis: Contenido de '{full_path}':")
            for item in items:
                tipo = "📁" if os.path.isdir(os.path.join(full_path, item)) else "📄"
                print(f" {tipo} {item}")
            return items
        else:
            print(f"⚠️ La ruta '{full_path}' no existe.")
            return []
    except Exception as e:
        print(f"❌ Error al listar: {e}")
        return []