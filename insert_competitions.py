import pandas as pd
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=FILIP-PAVILION;'
                      'Database=HurtownieProjekt;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

FILEPATH = './csv/competitions.csv'

print(f'Reading file {FILEPATH}')

df = pd.read_csv(FILEPATH, dtype={'competition_id': str, 'name': str, 'type': str, 'sub_type': str,
                                  'country_name': str})

print('File loaded')

for row in df.itertuples():
    cursor.execute('''
        INSERT INTO DIM_Competition (competition_id, name, type, sub_type, country_name) values
        (?, ?, ?, ?, ?)
        ''',
                   row.competition_id,
                   row.name,
                   row.type,
                   row.sub_type,
                   row.country_name if type(row.country_name) is not float else None
                   )

conn.commit()
