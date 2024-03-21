from translator import translator_JSON
import json

def open_and_translate_file(filename):
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