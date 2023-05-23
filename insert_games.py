import pandas as pd
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=FILIP-PAVILION;'
                      'Database=HurtownieProjekt;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

FILEPATH = './csv/games.csv'

print(f'Reading file {FILEPATH}')

df = pd.read_csv(FILEPATH)

print('File loaded')

for row in df.itertuples():
    cursor.execute('''
        INSERT INTO DIM_Game (game_id, competition_type, season, round, date, home_club_goals, away_club_goals,
        home_club_position, away_club_position, home_club_manager_name, away_club_manager_name, stadium, attendance
        ) values
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
                   row.game_id,
                   row.competition_type,
                   row.season,
                   row.round,
                   row.date.replace('-', '') if type(row.date) is str else None,
                   row.home_club_goals,
                   row.away_club_goals,
                   row.home_club_position,
                   row.away_club_position,
                   row.home_club_manager_name if type(row.home_club_manager_name) is str else None,
                   row.away_club_manager_name if type(row.away_club_manager_name) is str else None,
                   row.stadium if type(row.stadium) is str else None,
                   row.attendance
                   )

conn.commit()
