import pywinauto
from pywinauto import Desktop


'''
    script para controlar las ventanas abiertas en Windows usando pywinauto. La idea es que puedas enviar comandos al cerebro de Jarvis como "minimiza la ventana del navegador", o "maximiza el bloc de notas", o "cierra la ventana de Spotify", y esta herramienta se encargue de traducir esos comandos a acciones reales en el sistema operativo, buscando las ventanas por título, trayéndolas al frente, minimizándolas, maximizándolas o cerrándolas según lo que le pidas. AUN EN DESARROLLO, NO TODAS LAS FUNCIONES ESTÁN OPTIMIZADAS O TERMINADAS, PERO LA IDEA ES QUE SEA UNA HERRAMIENTA COMPLETA PARA CONTROLAR LAS VENTANAS DE TU PC DESDE EL CEREBRO DE JARVIS.
    funciones:
    - list_windows: devuelve una lista de las ventanas visibles actualmente, para que el LLM pueda saber qué ventanas hay abiertas y sus títulos.
    - focus_window: trae una ventana al frente buscando por título.
    - minimize_window: minimiza una ventana específica.
    - maximize_window: maximiza una ventana específica.
    - close_window: cierra una ventana específica.

'''

def _get_window(title_regex):
    """
    Función helper interna: Escanea el escritorio y devuelve la primera 
    ventana visible que coincida con la expresión regular.
    """
    # Hacer el regex "a prueba de LLMs" para que busque en cualquier parte del título
    if not title_regex.startswith(".*"):
        title_regex = ".*" + title_regex
    if not title_regex.endswith(".*"):
        title_regex = title_regex + ".*"
        
    escritorio = Desktop(backend="uia")
    return escritorio.window(title_re=title_regex, visible_only=True, found_index=0)

def list_windows(params=None):
    """Devuelve una lista de las ventanas visibles actualmente."""
    print("👁️ Jarvis está escaneando las ventanas abiertas...")
    try:
        escritorio = Desktop(backend="uia")
        # Obtenemos todas las ventanas visibles
        ventanas = escritorio.windows(visible_only=True)
        
        # Extraemos los títulos descartando las que no tienen nombre
        titulos = [v.window_text() for v in ventanas if v.window_text().strip()]
        
        # Filtramos elementos invisibles del sistema que pywinauto a veces detecta
        lista_ignorados = ["Program Manager", "Task View", "Barra de tareas"]
        titulos_limpios = [t for t in titulos if t not in lista_ignorados]
        
        print(f"✅ Se encontraron {len(titulos_limpios)} ventanas activas.")
        
        print(titulos_limpios)

        # Retornamos la lista (tu executor podría enviarle esto de vuelta al LLM si lo necesita)
        return titulos_limpios
        
    except Exception as e:
        print(f"❌ Error al listar ventanas: {e}")
        return str(e)

def focus_window(params):
    """Trae una ventana al frente."""
    title = params.get("title")
    if not title:
        print("❌ Jarvis necesita el parámetro 'title' para enfocar una ventana.")
        return
        
    print(f"🔍 Jarvis buscando ventana para enfocar: '{title}'...")
    try:
        ventana = _get_window(title)
        ventana.set_focus()
        print(f"✅ Ventana enfocada con éxito.")
    except pywinauto.findwindows.ElementNotFoundError:
        print(f"❌ Jarvis no pudo encontrar ninguna ventana que coincida con '{title}'.")
    except Exception as e:
        print(f"❌ Error al enfocar ventana: {e}")

def minimize_window(params):
    """Minimiza una ventana específica."""
    title = params.get("title")
    if not title: return
    
    print(f"🔽 Jarvis minimizando: '{title}'...")
    try:
        ventana = _get_window(title)
        ventana.minimize()
        print("✅ Ventana minimizada.")
    except pywinauto.findwindows.ElementNotFoundError:
        print(f"❌ No se encontró la ventana '{title}'.")

def maximize_window(params):
    """Maximiza una ventana específica."""
    title = params.get("title")
    if not title: return
    
    print(f"🔼 Jarvis maximizando: '{title}'...")
    try:
        ventana = _get_window(title)
        ventana.maximize()
        print("✅ Ventana maximizada.")
    except pywinauto.findwindows.ElementNotFoundError:
        print(f"❌ No se encontró la ventana '{title}'.")

def close_window(params):
    """Cierra una ventana específica de forma segura."""
    title = params.get("title")
    if not title: return
    
    print(f"❌ Jarvis cerrando ventana: '{title}'...")
    try:
        ventana = _get_window(title)
        ventana.close()
        print("✅ Ventana cerrada.")
    except pywinauto.findwindows.ElementNotFoundError:
        print(f"❌ No se encontró la ventana '{title}'.")