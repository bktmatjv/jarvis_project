import json
import os

'''
    SCRIPT PARA MANEJAR UNA MEMORIA DE COMANDOS PERSONALIZADOS QUE EL USUARIO PUEDE ENSEÑARLE A JARVIS. LA IDEA ES QUE PUEDAS DECIRLE A JARVIS "RECUÉRDAME QUE CUANDO DIGA 'BUENOS DÍAS' ME RESPONDAS '¡BUENOS DÍAS, JARVIS!'", O "RECUÉRDAME QUE CUANDO DIGA '¿QUÉ HORA ES?' ME RESPONDAS CON LA HORA ACTUAL", Y ESTA HERRAMIENTA SE ENCARGUE DE GUARDAR ESAS ASOCIACIONES EN UN ARCHIVO JSON PARA QUE JARVIS PUEDA CONSULTAR ESA MEMORIA CADA VEZ QUE RECIBA UNA ORDEN DEL USUARIO, Y RESPONDER DE ACUERDO A LO QUE LE HAYAS ENSEÑADO. AUN EN DESARROLLO, NO TODAS LAS FUNCIONES ESTÁN OPTIMIZADAS O TERMINADAS, PERO LA IDEA ES QUE SEA UNA HERRAMIENTA COMPLETA PARA RECORDAR COMANDOS PERSONALIZADOS DESDE EL CEREBRO DE JARVIS.


'''

MEMORY_PATH = os.path.join(os.path.dirname(__file__), "commands.json")


def load_memory():

    if not os.path.exists(MEMORY_PATH):
        return {}

    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(data):

    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_command(user_input):

    memory = load_memory()

    return memory.get(user_input.lower())


def remember_command(user_input, action):

    memory = load_memory()

    memory[user_input.lower()] = action

    save_memory(memory)

    print("Learned new command:", user_input)