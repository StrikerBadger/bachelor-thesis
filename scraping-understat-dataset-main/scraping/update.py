import match_scraper as ms
import season_scraper as ss


# # Once a season, update sets of teams and matches_id to be scraped
# ms.patch_empty_url_list()
# ss.generate_set_of_teams(2014, 2023)

# Updates the shots datasets
for y in range(2014, 2024):
    ms.update_shots_dataset(y)