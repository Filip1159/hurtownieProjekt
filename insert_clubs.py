import math
import pandas as pd
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=FILIP-PAVILION;'
                      'Database=HurtownieProjekt;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

FILEPATH = './csv/clubs.csv'

print(f'Reading file {FILEPATH}')

df = pd.read_csv(FILEPATH, dtype={'club_id': int, 'name': str, 'squad_size': int, 'average_age': float,
                                  'foreigners_number': int, 'foreigners_percentage': float})
df.fillna(value=0)
print('File loaded')

for row in df.itertuples():
    cursor.execute('''
        INSERT INTO DIM_Club (club_id, name, squad_size, average_age, foreigners_number, foreigners_percentage) values
        (?, ?, ?, ?, ?, ?)
        ''',
                   row.club_id,
                   row.name,
                   row.squad_size,
                   row.average_age if not math.isnan(row.average_age) else None,
                   row.foreigners_number,
                   row.foreigners_percentage if not math.isnan(row.foreigners_percentage) else None
                   )

conn.commit()
