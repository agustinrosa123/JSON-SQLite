import json

# Cargar el archivo JSON
with open('roster_data.json') as f:
    roster_data = json.load(f)

# Imprimir el contenido para verificar la estructura
print(roster_data)
