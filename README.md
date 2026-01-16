# A "Connect 5" Tournament, similar to connnect 4 but with some special rules to counter plagiatism. The main.java shows my engine, that was able to get the 2. place overall in the tournament. The rest ist a python setup to make engine play against each other. I have not done all of them, credits to Yannick Fischer.

# groups.txt
This file you be in the same folder as the application. The file contains the groups participating in the tournament.
The groups are listed line by line and consist of a name and program call separated by ';'.
An example configuration for the file could look like this:
team 01;python /home/team01/FiveWins.py
team 02;javac /home/team02/FiveWins.java
team 03;/home/team03/FiveWins

The team name is arbitrary but will be used for display. You can follow any naming scheme you like as long as it does not contain ';'

# Starting the GUI
```sh
python main.py
```

# Selecting a battle
The list on the right side of the GUI contains the currently active groups. You can select groups which should battle by using drag and drop. Simply drag a group from the list to left side into the boxes beside the "vs." text and drop them. The corresponding player A and B fields will be filled with this group. You can also use drag and drop from within these boxes if you want to undo a selection.
Its also possible to select a group by double clicking an item inside the selection on the right side. This way first empty slot will be filled.

# Simulating the battles
Once two teams are selected you can simulate the battles. Simply use the 'Start battle' button to start the game.
==NOTE:== The moment you click the 'Start battle' button two games will be simulated and no selection is possible. You will need to wait for the games to finish.
The current game state will be drawn in the screen and updates live during the game.

# Results
After the two games are simulated the labels below the game will update showing which player won and how many moves were played.
Also a GIF containing the sequence of moves is created. This GIF will have the name '5GewinntState_[TEAM LEFT]_[TEAM RIGHT].gif' and is
contained in the GIF folder.

# Reseting the state
If the games have finished and the results are interpreted you can use the 'Reset' button to clear the current selection to create a new one.

# Removing/Adding teams
Its possible to remove and add teams to the selection. Selection is done by left clicking a team in the list on the right. Then you can use the 'Remove' button to remove this team from the selection. This reduces the number of teams to select from and should help keeping track of who is still in the tournament. Once a team was removed its possible to re-add it to the game by using the 'Add group button'. 
Only the teams in groups.txt will be available at any time.

# Workflow
1. Select two teams to battle
2. Simulate the battles
3. Reset the state
4. Update the teams

Repeat this process until there is a winner
