

import json

from constants import DATOS_INICIALES, SAVE_FILE
#Cargar datos de guardado, si no existe o se ha borrado el archivo se crea con los datos iniciales
def cargar_datos():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):

        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(DATOS_INICIALES, f, indent=4)

        return DATOS_INICIALES.copy()
#Guardar datos de guardado, se sobreescribe el archivo con los nuevos datos 
def guardar_datos(datos):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)