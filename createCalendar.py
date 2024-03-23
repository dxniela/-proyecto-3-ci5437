from ics import Calendar, Event
from datetime import datetime, timedelta

def create_ics_file(games, filename):
    # Crea un nuevo calendario
    c = Calendar()

    # Itera sobre todos los juegos obtenidos
    for game in games:

        # Crea un nuevo evento
        e = Event()

        # Establece el nombre del evento como el juego
        e.name = f"local {game['participant1']} vs visitante {game['participant2']}"

        # Establece la fecha y hora de inicio del evento
        e.begin = datetime.strptime(game['date'] + " " + game['time'], "%Y-%m-%d %H:%M:%S.%f")

        # Establece la duración del evento como 2 horas
        e.duration = timedelta(hours=2)

        # Añade el evento al calendario
        c.events.add(e)
    
    # Escribe el calendario a un archivo .ics
    with open(f"{filename}.ics", "w") as f:
        f.write(str(c))

