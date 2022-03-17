# March-Madness-Contrarian-Bracket-Picker
Makes picks for the March Madness :basketball: 2022 Men's Basketball Tournament based on the best value according to contrarian strategy.

Contrarian strategy is a popular strategy used that is based on "going against the grain" and finding teams that the public is undervaluing. To determine the most undervalued teams, statistics on each team's simulated chances to advance for each round from Sporting News' Simulator were compared to ESPN's statistics describing the percentage of the public choosing teams to advance in each round.

Sporting News Simulated Chances: https://www.sportingnews.com/us/ncaa-basketball/news/march-madness-odds-2022-projections/wkmgsmhrbp6xifahweslv1iw  
ESPN Who Picked Whom: https://fantasy.espn.com/tournament-challenge-bracket/2022/en/whopickedwhom  

More information on Contrarian Strategy can be found here (Note: This is for the 2017 Tournament):
https://www.usatoday.com/story/sports/ncaab/tourney/2017/03/15/contrarian-ncaa-tournament-bracket-tips-march-madness-picks-betting/99214700/  

Run the file in 3 steps :grinning: after cloning project to desired destination:  
    1. Open a terminal in folder where project is cloned  
    2. Run `pip install -r March-Madness-Contrarian-Bracket-Picker/requirements.txt`  
    3. Run `venv\Scripts\python bracket_picker.py`  
Note: For Windows use '\' instead of '/'

To change the number of value picks being shown for each round, open the `bracket_picker.py` file in a text editor and change the value of `NUMBER_OF_RANKINGS` to display the desired number of teams per round.  
    Ex. `NUMBER_OF_RANKINGS = 5` displays the top 5 value picks to advance for each respective round.

