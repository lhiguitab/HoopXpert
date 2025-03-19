import pandas as pd
import json

# Lee el archivo CSV
df = pd.read_csv('exercise_database.csv')

#Guardar el DataFrame en un archivo JSON
df.to_json('exercise_db.json', orient='records')

with open('exercise_db.json') as file:
    exercise_db = json.load(file)