from translator import translator_JSON
from rules import rule_1, rule_2, rule_3, rule_4
import json
from pysat.solvers import Solver

s = Solver(name="g421")

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
    
    s.append_formula(rule_1(participants, dates, hours))
    s.append_formula(rule_2(participants, dates, hours))
    s.append_formula(rule_3(participants, dates, hours))
    s.append_formula(rule_4(participants, dates, hours))
    
    if s.solve():
        print("Hay solución")
    else:
        print("No hay solución")
    
    print(s.get_model())  

main()