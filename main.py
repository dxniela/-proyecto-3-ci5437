from translator import translator_JSON
import json

def open_and_translate_file(filename):
    """ Dado el nombre de un archivo json, lo abre y
        traduce los datos a variables.

    Args:
        filename (string): Nombre del archivo

    Returns:
        diccionario: Diccionarios de fechas, horarios y participantes.
        Tienen variables como claves y los datos asociados como valores
    """
    # Abre el archivo json
    with open(filename, 'r') as f:
        data = json.load(f)
    return translator_JSON(data)

def main():
    filename = input("Ingrese el nombre del archivo JSON: ")
    dates, hours, participants = open_and_translate_file(filename)
    print("Diccionario de fechas")
    print(dates)
    print("-----------------------------------------------")
    print("Diccionario de horas")
    print(hours)
    print("-----------------------------------------------")
    print("Diccionario de participantes")
    print(participants)
    print("-----------------------------------------------")

main()