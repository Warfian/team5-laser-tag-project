**Team 5 Laser Tag Project**

**Github User    --> Real Name**
Warfian        -->  Daniel Eyraud
Cole-C25       -->  Cole Cooper
crystalgooding -->  Crystal Gooding
kylerj15       -->  Kyler Jones
FortyFathom    -->  Jordan Wood

**Current Functionality:**
- Launches splash screen and player entry table upon startup
- Stores player ID and code name into database when ENTER is pressed in text box
- If code name already stored in database, it will be autofilled upon ENTERing the player ID
- Broadcasts equipment ID through UDP when ENTER is pressed in text box
- Ability to change broadcast network address
- Button to clear names in player entry table
- Button to start game, which takes user into play action display
- 30 minute countdown timer before the game begins, which launches in a separate window
- Play action display tracks hits, friendly fire, and base scoring through UDP broadcasts
- Names in play action display will move to have the highest score at the top, team score displayed in the team's column
- 6 minute timer in play action display
- Music plays upon start of game, and separate helmet noises will play upon hits, friendly fire, and base scores

**How to Run:**
1. Download contents of main github folder into local directory.
2. In a terminal that's in the local directory, type "chmod +x install.sh" to make the install script executable.
3. Execute install script by typing "./install.sh".
4. The program will start automatically once everything is installed. If you need to run it again after install, type either "make" to run the makefile or type "python3 main.py" to run directly.