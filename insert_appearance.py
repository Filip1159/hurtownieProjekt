import pandas as pd
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=FILIP-PAVILION;'
                      'Database=HurtownieProjekt;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

FILEPATH = './csv/appearances.csv'
VALUATIONS_FILEPATH = './csv/player_valuations.csv'

print(f'Reading files {FILEPATH} & {VALUATIONS_FILEPATH}')

df = pd.read_csv(FILEPATH)
valuationd_df = pd.read_csv(VALUATIONS_FILEPATH)

print('Files loaded')

player_to_days_and_valuations = {}
for valuation in valuationd_df.itertuples():
    if valuation.player_id not in player_to_days_and_valuations:
        player_to_days_and_valuations[valuation.player_id] = []
    player_to_days_and_valuations[valuation.player_id].append((valuation.date, valuation.market_value_in_eur))

for days_to_valuations in player_to_days_and_valuations.values():
    sorted(days_to_valuations, key=lambda tpl: tpl[0])

print(player_to_days_and_valuations.keys())


def get_player_valuation_for_day(player_id, date):
    if player_id not in player_to_days_and_valuations:
        return None
    player_valuations = player_to_days_and_valuations[player_id]
    if player_valuations[0][0] > date:
        return None
    for i in range(1, len(player_valuations)):
        if player_valuations[i][0] > date:
            return player_valuations[i-1][1]


for row in df.itertuples():
    cursor.execute('''
        INSERT INTO FACT_APPEARANCES (player_id, game_id, player_club_id, player_current_club_id, date, competition_id,
        yellow_cards, red_cards, goals, assists, minutes_played, market_value_in_eur) values
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
                   row.player_id,
                   row.game_id,
                   row.player_club_id,
                   row.player_current_club_id,
                   row.date.replace('-', '') if type(row.date) is str else None,
                   row.competition_id,
                   row.yellow_cards,
                   row.red_cards,
                   row.goals,
                   row.assists,
                   row.minutes_played,
                   get_player_valuation_for_day(row.player_id, row.date) if type(row.date) is str else None
                   )

conn.commit()

