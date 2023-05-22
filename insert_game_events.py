import pandas as pd
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=FILIP-PAVILION;'
                      'Database=HurtownieProjekt;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

FILEPATH = './csv/game_events.csv'

print(f'Reading file {FILEPATH}')

df = pd.read_csv(FILEPATH)

print('File loaded')

for row in df.itertuples():
    cursor.execute('''
        INSERT INTO DIM_GameEvent (game_id, minute, type) values
        (?, ?, ?)
        ''',
                   row.game_id,
                   row.minute,
                   row.type
                   )

conn.commit()
