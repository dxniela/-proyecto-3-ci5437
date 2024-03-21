from translator import translator_JSON
import json

# Abre el archivo json
with open('./test0.json', 'r') as f:
    data = json.load(f)

dates, hours, participants = translator_JSON(data)

print("Diccionario de fechas")
print(dates)
print("-----------------------------------------------")
print("Diccionario de horas")
print(hours)
print("-----------------------------------------------")
print("Diccionario de participantes")
print(participants)
print("-----------------------------------------------")