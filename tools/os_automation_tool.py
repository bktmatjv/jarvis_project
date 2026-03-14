import subprocess
import time
from pywinauto import Desktop

# script para automatizar la apertura y control de programas en Windows usando pywinauto. La idea es que puedas enviar comandos al cerebro de Jarvis como "abre el bloc de notas y escribe 'Hola mundo'", o "abre el navegador y busca 'Python programming'", y esta herramienta se encargue de traducir esos comandos a acciones reales en el sistema operativo, abriendo programas, buscando ventanas por título, trayéndolas al frente y simulando la escritura de texto dentro de ellas. AUN EN DESARROLLO, NO TODAS LAS FUNCIONES ESTÁN OPTIMIZADAS O TERMINADAS, PERO LA IDEA ES QUE SEA UNA HERRAMIENTA COMPLETA PARA CONTROLAR PROGRAMAS DESDE EL CEREBRO DE JARVIS.

def automate_program(params):
    # Jarvis extraerá estos parámetros de tu orden
    executable = params.get("executable", "notepad.exe")
    window_title = params.get("window_title", ".*Bloc de notas|.*Notepad")
    text_to_type = params.get("text", "")

    print(f"⚙️ Jarvis intentando abrir y controlar: {executable}...")

    try:
        # 1. Abre el programa
        subprocess.Popen(executable)
        time.sleep(2)  # Pausa para que el OS renderice la ventana

        # 2. Busca la ventana en el escritorio
        escritorio = Desktop(backend="uia")
        ventana = escritorio.window(title_re=window_title, visible_only=True, found_index=0)
        
        # 3. Trae la ventana al frente
        ventana.set_focus()

        # 4. Si Jarvis tiene algo que escribir, lo inyecta
        if text_to_type:
            # Formateamos el texto por si tiene espacios (with_spaces=True)
            print("✍️ Jarvis está escribiendo en el sistema...")
            
            # Reemplazamos los espacios normales por la pulsación de tecla {SPACE}
            texto_seguro = text_to_type.replace(" ", "{SPACE}")
            texto_seguro += "{ENTER}"  # Presionamos Enter al final del texto
            print(texto_seguro)

            # Enviamos el texto seguro
            ventana.type_keys(texto_seguro)
        print("✅ Acción de sistema operativo completada.")

    except Exception as e:
        print(f"❌ Error al intentar controlar el sistema: {e}")

# Ejemplo de los parámetros que enviaría el LLM:
# automate_program({"executable": "notepad.exe", "window_title": ".*Bloc de notas|.*Notepad", "text": "Mensaje de prueba."})