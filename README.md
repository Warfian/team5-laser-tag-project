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
- Broadcasts equipment ID through UDP when ENTER is pressed in text box
- Ability to change broadcast network address

**How to Run:**
1. Download contents of main github folder into local directory.
2. In a terminal that's in the local directory, type "chmod +x install.sh" to make the install script executable.
3. Execute install script by typing "./install.sh" (NOTE: The DearPyGUI install in the script will take a while (5ish minutes)).
4. The program will start automatically once everything is installed. If you need to run it again after install, type either "make" to run the makefile or type "python3 main.py" to run directly.