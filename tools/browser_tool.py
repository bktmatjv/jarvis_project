import webbrowser
import urllib.parse

def open_url(params):
    """Abre una URL específica en el navegador predeterminado."""
    url = params.get("url")
    if not url: return
    
    # Aseguramos que la URL tenga el protocolo http
    if not url.startswith("http"):
        url = "https://" + url
        
    print(f"🌐 Jarvis: Abriendo la web '{url}'...")
    try:
        webbrowser.open(url)
        print("✅ Navegador iniciado.")
    except Exception as e:
        print(f"❌ Error al abrir el navegador: {e}")

def open_tab(params):
    """Abre una nueva pestaña (en la práctica funciona igual que open_url)."""
    open_url(params)

def search_google(params):
    """Realiza una búsqueda directa en Google."""
    query = params.get("query")
    if not query: return
    
    # Codificamos el texto para que sea válido en una URL (ej: espacios -> %20)
    query_encoded = urllib.parse.quote(query)
    search_url = f"https://www.google.com/search?q={query_encoded}"
    
    print(f"🔍 Jarvis: Buscando en Google: '{query}'...")
    try:
        webbrowser.open(search_url)
        print("✅ Búsqueda enviada.")
    except Exception as e:
        print(f"❌ Error al realizar la búsqueda: {e}")