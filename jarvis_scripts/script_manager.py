import json
import os

'''
    script para manejar los scripts personalizados que el usuario puede crear para que Jarvis ejecute. La idea es que puedas decirle a Jarvis "crea un script llamado 'buenos días' que abra el bloc de notas y escriba '¡Buenos días, JARVIS!'", o "crea un script llamado 'hora' que me diga la hora actual", y esta función se encargue de guardar esos scripts en un archivo JSON, para que luego puedas decirle a Jarvis "ejecuta el script 'buenos días'", y esta función se encargue de cargar ese script desde el JSON y ejecutarlo paso a paso. AUN EN DESARROLLO, NO TODAS LAS FUNCIONES ESTÁN OPTIMIZADAS O TERMINADAS, PERO LA IDEA ES QUE SEA UNA HERRAMIENTA COMPLETA PARA MANEJAR SCRIPTS PERSONALIZADOS DESDE EL CEREBRO DE JARVIS.
'''

SCRIPTS_PATH = os.path.join(os.path.dirname(__file__), "scripts.json")


def load_scripts():

    if not os.path.exists(SCRIPTS_PATH):
        return {}

    try:
        with open(SCRIPTS_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                return {}

            return json.loads(content)

    except:
        return {}


def save_scripts(data):

    with open(SCRIPTS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def create_script(name, actions):

    scripts = load_scripts()

    scripts[name] = actions

    save_scripts(scripts)

    print(f"Script '{name}' saved.")


def get_script(name):

    scripts = load_scripts()

    return scripts.get(name)