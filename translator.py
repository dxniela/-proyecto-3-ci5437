from datetime import datetime, timedelta

def translator_JSON(data):
    """ Funcion que dado el diccionario de un JSON, retorna
        traduce los datos a variables.

    Args:
        data (diccionario): Diccionario con los datos de entrada

    Returns:
        diccionarios: Diccionarios de fechas, horarios y participantes.
        Tienen variables como claves y los datos asociados como valores
    """
    # Fechas en formato ISO 8601
    start_date = data["start_date"]
    end_date = data["end_date"]

    # Convertir las cadenas de texto a objetos de fecha
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Horas en formato ISO 8601
    start_time = data["start_time"]
    end_time = data["end_time"]

    # Convertir las cadenas de texto a objetos de fecha
    start_time = datetime.strptime(start_time, "%H:%M:%S.%f")
    end_time = datetime.strptime(end_time, "%H:%M:%S.%f")

    # Comprobar si las horas son horas en punto
    if start_time.minute != 0 or start_time.second != 0 or start_time.microsecond != 0:
        raise ValueError("start_time debe ser una hora en punto")
    if end_time.minute != 0 or end_time.second != 0 or end_time.microsecond != 0:
        raise ValueError("end_time debe ser una hora en punto")

    # Crear un diccionario para almacenar las fechas y otro para las horas
    dates = {}
    hours = {}

    # Generar las fechas intermedias
    curr_date = start_date
    i = 0
    while curr_date <= end_date:
        # Agregar la fecha al diccionario con una clave variable
        dates[f"d{i}"] = curr_date.strftime("%Y-%m-%d")
        curr_date += timedelta(days=1)
        i += 1

    # Generar las horas intermedias
    curr_time = start_time
    i = 0
    while curr_time <= end_time - timedelta(hours=2):
        # Agregar la hora al diccionario con una clave variable
        hours[f"h{i}"] = curr_time.strftime("%H:%M:%S.%f")
        curr_time += timedelta(hours=2)
        i += 1

    # Genera los participantes
    participants = {}
    i = 0
    for p in data["participants"]:
        participants[f"p{i}"] = p
        i += 1

    variables = {}
    counter = 1
    for i in participants:
        for j in participants:
            if i != j:
                for d in dates:
                    for h in hours:
                        variables[(i, j, d, h)] = counter
                        counter += 1

    return dates, hours, participants, variables

def translator_CNF(dates, hours, participants, variables, model):

    # Genera las claves del diccionario de variables de juegos
    keys = list(variables.keys())
    games = []
    for i in model:
        games += [{
            "participant1": participants[keys[i - 1][0]],
            "participant2": participants[keys[i - 1][1]],
            "date": dates[keys[i - 1][2]],
            "time": hours[keys[i - 1][3]]
        }]

    return games