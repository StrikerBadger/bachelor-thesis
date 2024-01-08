import pandas as pd
import os

# Get all the relevant matches
matches = []
for file in os.listdir(os.fsencode('dataset/intersection/statsbomb_matches_shots/')):
    filename = os.fsdecode(file)
    if 'shots' in filename and 'La Liga' not in filename and filename.endswith('.csv'):
        matches.append(pd.read_csv('dataset/intersection/statsbomb_matches_shots/' + filename))
all_shots = pd.concat(matches)

# Build new dataframe with relevant columns
shots_per_match = {'match_id': [], 'team': [], 'shot_amnt': [], 'shot_xgs': []}
for match_id in all_shots['match_id'].unique():
    matchshots_df_view = all_shots[(all_shots['match_id'] == match_id) & (~all_shots['shot_statsbomb_xg'].isna())]
    for team in all_shots[all_shots['match_id'] == match_id]['team'].unique():
        shots_per_match['match_id'].append(match_id)
        shots_per_match['team'].append(team)
        shots_per_match['shot_amnt'].append(len(matchshots_df_view[matchshots_df_view['team'] == team]))
        shots_per_match['shot_xgs'].append(list(matchshots_df_view[matchshots_df_view['team'] == team]['shot_statsbomb_xg']))
pd.DataFrame(shots_per_match).to_pickle('dataset/intersection/statsbomb_matches_shots/shots_per_match.pkl')