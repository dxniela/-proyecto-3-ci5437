from translator import translator_JSON, translator_CNF
from rules import rule_1, rule_2, rule_3, rule_4
from createCalendar import create_ics_file
from pysat.solvers import Solver
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
    return translator_JSON(data), data["tournament_name"]

def main():
    filename = input("Ingrese el nombre del archivo JSON: ")
    (dates, hours, participants, variables), name_tournament = open_and_translate_file(filename)

    s = Solver(name='g421')
    s.append_formula(rule_1(participants, dates, hours, variables))
    s.append_formula(rule_2(participants, dates, hours, variables))
    s.append_formula(rule_3(participants, dates, hours, variables))
    s.append_formula(rule_4(participants, dates, hours, variables))

    if not s.solve():
        print("No hay solución")
        exit()
    print("Hay solución")
    games = [i for i in s.get_model() if i > 0 ]
    create_ics_file(translator_CNF(dates, hours, participants, variables, games), name_tournament)

main()