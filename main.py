import dearpygui.dearpygui as dpg
import python_pg as db
import pygame
import network
import time
import sys

from gamescreen import game_screen
from gamescreen import resize_game_window 
from gamescreen import runTimer

tableWidth = 450
tableHeight = 410
buttonWidth = 100
buttonHeight = 100
spacerGap = 20
entry_book = {}

# Callback function to add to db
# Since ID must be paired, with codename, we need to store IDs to be paired with the codename
def add_to_db(sender, app_data, user_data):
    # Extract the user input from the input field and prep SQL input fields
    data = dpg.get_value(sender)
    id = 0
    name = 0

    # Add an arbitrary value to the green table listing to prevent overlap with Entry Book keys
    if "green" in sender:
        user_data += 20

    # If the table does not have an ID-name pair, store the given data in a dictionary for later.
    if user_data not in entry_book.keys():
        # Assign the entry to its number on the entry screen
        entry_book[user_data] = data

        # Make sure everything looks good
        print(entry_book)
        return
    
    # If caller has a matching value and is a name, grab the ID from the dictionary
    elif "code" in sender:
        id = entry_book[user_data]
        name = data
    # Repeat the same process for a callback from an ID field
    else:
        id = data
        name = entry_book[user_data]

    # Send both inputs to the database
    db.add(id, name)

    # Remove the Entry from the Entry Book
    entry_book.pop(user_data)

def splash_screen():
    pygame.init()

    # Match your planned DPG size
    width, height = 1000, 640
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Laser Tag")  # match title

    try:
        icon = pygame.image.load("table_logo.ico")  
        pygame.display.set_icon(icon)
    except pygame.error:
        print("Warning: Could not load icon for title bar")

    try:
        logo = pygame.image.load("logo.jpg")
    except pygame.error:
        print("Error: Could not load image.")
        pygame.quit()
        sys.exit()

    logo = pygame.transform.smoothscale(logo, (940, 600))
    logorect = logo.get_rect()

    screen.fill((0, 0, 0))  # black background
    logorect.center = (width // 2, height // 2 - 20)
    screen.blit(logo, logorect)
    pygame.display.flip()

    start_time = time.time()
    while time.time() - start_time < 3:  # show for 3 seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    pygame.quit()

# Reset all Red/Green team input fields back to default values.
# Triggered by the 'Clear' button or F12 key. 
def clear_entries():
    for i in range(15):
        # Red Team Inputs
        dpg.set_value(f"red_id_{i}", 0)
        dpg.set_value(f"red_code_{i}", "")
        dpg.set_value(f"red_equip_{i}", 0)
    
        # Green Team Inputs
        dpg.set_value(f"green_id_{i}", 0)
        dpg.set_value(f"green_code_{i}", "")
        dpg.set_value(f"green_equip_{i}", 0)

# Adjust size and position of the team window, tables, and buttons whenever the viewport is resized.
def resize_window(*_):
    view_width = dpg.get_viewport_client_width()
    view_height = dpg.get_viewport_client_height()

    # Resize team_window
    if dpg.does_item_exist("team_window"):
        dpg.set_item_width("team_window", view_width)
        dpg.set_item_height("team_window", view_height)

        if dpg.does_item_exist("tables_group") and dpg.does_item_exist("buttons_group"):
            total_table_width = tableWidth * 2 + 20
            left_table_spacer = max((view_width - total_table_width) // 2, 0)
            dpg.set_item_pos("tables_group", (left_table_spacer, 50))

            total_buttons_width = buttonWidth * 2 + spacerGap
            buttons_x = max((view_width - total_buttons_width) // 2, 0)
            buttons_y = tableHeight + 70
            dpg.set_item_pos("buttons_group", (buttons_x, buttons_y))

def start_game_callback():
    # Capture values from entry screen
    red_players = {}
    green_players = {}
    for i in range(15):
        if dpg.does_item_exist(f"red_code_{i}") and dpg.does_item_exist(f"red_equip_{i}"):
            code = dpg.get_value(f"red_code_{i}")
            equip = dpg.get_value(f"red_equip_{i}")
            if code and code.strip():
                red_players[equip] = {"name": code.strip(), "score": 0}

        if dpg.does_item_exist(f"green_code_{i}") and dpg.does_item_exist(f"green_equip_{i}"):
            code = dpg.get_value(f"green_code_{i}")
            equip = dpg.get_value(f"green_equip_{i}")
            if code and code.strip():
                green_players[equip] = {"name": code.strip(), "score": 0}

    # print("DEBUG BEFORE GAME SCREEN:")
    # print("RED PLAYERS:", red_players)
    # print("GREEN PLAYERS:", green_players)

    #Call the screen and pass players
    game_screen(red_players, green_players)

def validate_equip_id(sender, app_data):
    tag = sender
    team = "red" if "red" in tag else "green"

    is_valid = (
        (team == "red" and app_data % 2 != 0) or
        (team == "green" and app_data % 2 == 0)
    )

    if not is_valid:
        dpg.set_value(sender, 0)
        print(f" Invalid ID {app_data} for {team.title()} Team")
        return

    # now call 
    equipment_added_callback(sender, app_data)

def show_player_entry():
    with dpg.window(tag="team_window", label="Teams",no_title_bar=True, no_move=True, no_resize=True, no_scrollbar=True) as teamWindow:
        with dpg.group(tag= "tables_group", horizontal=True):  # Side-by-side layout
            # Red Team table
            with dpg.child_window(tag="redTeam", width=tableWidth, height=tableHeight) as redTeam:
                dpg.add_text("Red Team")
                with dpg.table(header_row=True): # Table column headers
                    dpg.add_table_column(label="Player Number", width_fixed=True, width=110)
                    dpg.add_table_column(label="Player ID", width_fixed=True,width=80)
                    dpg.add_table_column(label="Player Codename", width_fixed=True,width=120)
                    dpg.add_table_column(label="Equipment ID", width_fixed=True,width=100)

                    # Create 15 rows
                    for i in range(15):
                        with dpg.table_row():
                            dpg.add_text(f"Player {i + 1}")

                            # Add callback, user_data, and on_enter to red_id and red_code to add to db
                            # Add callback, user_data, and on_enter to red_equip to broadcast equipment id
                            dpg.add_input_int(tag=f"red_id_{i}", width=80, step=0, step_fast=0, callback=add_to_db, user_data=i, on_enter=True)
                            dpg.add_input_text(tag=f"red_code_{i}", width=120, callback=add_to_db, user_data=i, on_enter=True)
                            dpg.add_input_int(tag=f"red_equip_{i}", width=100, step=0, step_fast=0, on_enter=True, callback=validate_equip_id)
                # Red Team Theme
                with dpg.theme() as redTheme:
                    with dpg.theme_component(dpg.mvAll):
                        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (225, 49, 55))          # Background of child
                        dpg.add_theme_color(dpg.mvThemeCol_Header, (240, 105, 105))         # Table header
                        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (225, 49, 55))    # Header Hover OFF
                        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (240, 105, 105))        # Frame/backgrounds
                        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
                        dpg.add_theme_color(dpg.mvThemeCol_Border, (225, 49, 55))           # Border color
                        dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 10)               # Rounded corners
                        dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 2)              # Border size
                    with dpg.theme_component(dpg.mvTable):
                        dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, (225, 49, 55))    #Table Label Background
                dpg.bind_item_theme(redTeam, redTheme)
            # Spacer between tables
            dpg.add_spacer(width=spacerGap)

            # Green Team table
            with dpg.child_window(tag="greenTeam", width=tableWidth, height=tableHeight) as greenTeam:
                dpg.add_text("Green Team")
                with dpg.table(header_row=True, ): # Table column headers
                    dpg.add_table_column(label="Player Number", width_fixed=True,width=110)
                    dpg.add_table_column(label="Player ID", width_fixed=True,width=80)
                    dpg.add_table_column(label="Player Codename", width_fixed=True,width=120)
                    dpg.add_table_column(label="Equipment ID", width_fixed=True,width=100)

                    # Create 15 rows
                    for i in range(15):
                        with dpg.table_row():
                            dpg.add_text(f"Player {i + 1}")

                            # Add callback, user_data, and on_enter to green_id and green_code to add to db
                            # Add callback, user_data, and on_enter to green_equip to broadcast equipment id
                            dpg.add_input_int(tag=f"green_id_{i}", width=80, step=0, step_fast=0, callback=add_to_db, user_data=i, on_enter=True)
                            dpg.add_input_text(tag=f"green_code_{i}", width=120, callback=add_to_db, user_data=i, on_enter=True)
                            dpg.add_input_int(tag=f"green_equip_{i}", width=100, step=0, step_fast=0, on_enter=True, callback=validate_equip_id)
                
                # Green Team Theme
                with dpg.theme() as greenTheme:
                    with dpg.theme_component(dpg.mvAll):
                        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (49, 225, 55))          # Background of child
                        dpg.add_theme_color(dpg.mvThemeCol_Header, (105, 240, 105))         # Table header
                        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (49, 225, 55))    # Header Hover OFF
                        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (105, 240, 105))        # Frame/backgrounds
                        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
                        dpg.add_theme_color(dpg.mvThemeCol_Border, (49, 225, 55))           # Border color
                        dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 10)               # Rounded corners
                        dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 2)  
                    with dpg.theme_component(dpg.mvTable):
                        dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, (49, 225, 55))    
                dpg.bind_item_theme(greenTeam, greenTheme)
        # Buttons and Shortcuts
        with dpg.group(tag="buttons_group", horizontal=True):
            dpg.add_button(label="  F5\nStart\nGame", tag="startButton", width=buttonWidth, height=buttonHeight, callback=start_game_callback) #add callback for start
            dpg.add_spacer(width=spacerGap)   # small gap between buttons
            dpg.add_button(label=" F12\nClear", tag="clearButton", width=buttonWidth, height=buttonHeight, callback=clear_entries)
            # adds text box and utilizes callback to edit netword addr on enter;
            # can be altered to project needs/group consensus
            dpg.add_spacer(width=spacerGap)
            with dpg.child_window(tag="network_box", width=150, height=buttonHeight, border=True):
                dpg.add_text("Network Address")
                dpg.add_input_text(tag="network_address", default_value="127.0.0.1", callback=network_change_callback, on_enter=True, width=120)
            with dpg.theme() as networkTheme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0, 0))   # dark gray background
                    dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0, 0)) # light gray border
            dpg.bind_item_theme("network_box", networkTheme)
        with dpg.handler_registry():
            dpg.add_key_press_handler(dpg.mvKey_F5) #add callback for start
            dpg.add_key_press_handler(dpg.mvKey_F12, callback=clear_entries)
    with dpg.theme() as windowTheme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0))
    dpg.bind_item_theme(teamWindow, windowTheme)
    
# network callbacks to broadcast equip id 
# && change network addr
def equipment_added_callback (sender, new_val):
    equip_id_str = str(new_val)

    # broadcast player added event
    # (sendto() is a method in socket, imported in network)
    # print(f"Sending code {equip_id_str} to {network.broadcast_addr_port}") <-- test print statement
    network.broadcast_sock.sendto(str.encode(equip_id_str), network.broadcast_addr_port)

def network_change_callback (sender, new_addr):
    network.change_broadcast_ip (new_addr)
    network.broadcast_sock, network.broadcast_addr_port = network.setup_broadcast_socket(network.broadcast_addr, network.BROADCAST_PORT)

# Initialize DearPyGui, create the UI, and start the render loop.
def main():
    #splash_screen()

    dpg.create_context()
    dpg.create_viewport(title="Laser Tag", width=1000, height=640)
    dpg.set_viewport_small_icon("table_logo.ico")
    dpg.setup_dearpygui()

    show_player_entry()
    #game_screen() 
    resize_window()
    resize_game_window()
    runTimer()
    dpg.show_viewport()


    network.start_listening(network.recv_sock, network.incoming_q)

    # Manual render loop for dynamic resizing
    while dpg.is_dearpygui_running():
        resize_window()
        resize_game_window() 
        runTimer()
        dpg.render_dearpygui_frame()

    dpg.destroy_context()

if __name__ == "__main__":
    main()