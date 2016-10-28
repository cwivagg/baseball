# baseball
Baseball Statistics Scripts

If the entire repository is cloned, these scripts will function flawlessly. However, they will take a long time to run, because they respect baseball-reference.com's robots.txt by only sending a request for one webpage every 3 s. The following items will be collected:

1) MLB team schedules as specified in teams_by_year.csv <br />
user$ python schedule_retrieval.py

2) MLB box scores for all games in the team schedules pages stored in the schedules directory <br />
user$ python game_list_generator.py

3) Handedness information for every player involved in every game in the parsed_box_scores directory <br />
user$ python hand_retrieval.py
