import pandas as pd
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=FILIP-PAVILION;'
                      'Database=HurtownieProjekt;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

FILEPATH = './csv/players.csv'

print(f'Reading file {FILEPATH}')

df = pd.read_csv(FILEPATH)

print('File loaded')

for row in df.itertuples():
    cursor.execute('''
        INSERT INTO DIM_Player (player_id, name, current_club_name, country_of_birth, date_of_birth, position,
        sub_position, foot, height_in_cm, market_value_in_eur) values
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
                   row.player_id,
                   row.name,
                   row.current_club_name,
                   row.country_of_birth if type(row.country_of_birth) is str else None,
                   row.date_of_birth if type(row.date_of_birth) is str else None,
                   row.position,
                   row.sub_position if type(row.sub_position) is str else None,
                   row.foot if type(row.foot) is str else None,
                   row.height_in_cm,
                   row.market_value_in_eur if type(row.market_value_in_eur) is str else None
                   )

conn.commit()
