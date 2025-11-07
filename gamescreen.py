import dearpygui.dearpygui as dpg
import time
from PIL import Image
import network

# Layout Constants
spacerGap = 20
scoreHeight = 530
scoreWidth = 300
scoreTopPadding = 10
timerWidth = 100
timerHeight = 40

# Global state
startTime = None
started = False
warned = False
gameDuration = 6 * 60
countDown = 30

# Game Data Stores
red_players = {}
green_players = {}
base_hit_players = set()
base_icon_texture_id = None

# loads base icon
def load_base_icon_texture():
    global base_icon_texture_id

    if base_icon_texture_id is not None:
        return  # Already loaded

    try:
        image = Image.open("baseicon.jpg").convert("RGBA")
        width, height = image.size

        # Flatten image data 
        pixel_data = list(image.getdata())  
        image_data = [channel / 255.0 for pixel in pixel_data for channel in pixel]

        with dpg.texture_registry(show=False):
            base_icon_texture_id = dpg.add_static_texture(width, height, image_data)
    except Exception as e:
        print(f"Failed to load base icon: {e}")

# Handle base being hit
def handle_base_hit(base_color: str, equipment_id: int):
    if base_color == "red" and equipment_id in green_players:
        green_players[equipment_id]["score"] += 100
        base_hit_players.add(equipment_id)
    elif base_color == "green" and equipment_id in red_players:
        red_players[equipment_id]["score"] += 100
        base_hit_players.add(equipment_id)

# Add/Subtrat Points
def add_points(equipment_id: int):
    if equipment_id in red_players:
        red_players[equipment_id]["score"] += 10
    elif equipment_id in green_players:
        green_players[equipment_id]["score"] += 10

def sub_points(equipment_id: int):
    if equipment_id in red_players:
        red_players[equipment_id]["score"] -= 10
    elif equipment_id in green_players:
        green_players[equipment_id]["score"] -= 10

def handle_score_event(equipment_id: int, action: str):
    if action == "add":
        add_points(equipment_id)
    elif action == "sub":
        sub_points(equipment_id)

# Window Resizing
def resize_game_window():
    view_width = dpg.get_viewport_client_width()
    view_height = dpg.get_viewport_client_height()

    if dpg.does_item_exist("game_screen"):
        dpg.set_item_width("game_screen", view_width)
        dpg.set_item_height("game_screen", view_height)

    if dpg.does_item_exist("score_group"):
        total_table_width = scoreWidth * 2
        center_x = max((view_width - total_table_width) // 2, 0)
        dpg.set_item_pos("score_group", (center_x, scoreTopPadding))

    if dpg.does_item_exist("timer_box"):
        dpg.set_item_pos("timer_box", (view_width - timerWidth - 20, scoreTopPadding))

# Game Screen
def game_screen(red_data, green_data):
    global red_players, green_players, startTime, warned, started
    red_players = red_data
    green_players = green_data

    # Set the time variables 
    startTime = time.time()
    warned = False
    started = False

    load_base_icon_texture()
    dpg.delete_item("team_window")

    # Define font locally and apply it only to the game screen
    with dpg.font_registry():game_font = dpg.add_font("consola.ttf", 20)
    # note from j.t. - we can't use absolute paths from our local machines in the VM,
    # but we can put any .ttf we like in the repo and just reference it directly here.
        

    with dpg.window(tag="game_screen", no_title_bar=True, no_move=True, no_resize=True, no_scrollbar=True):
        dpg.set_primary_window("game_screen", True)

        with dpg.group(tag="score_group", horizontal=True):
            # RED TEAM
            with dpg.child_window(tag="red_score", width=scoreWidth, height=scoreHeight, no_scrollbar=True):
                if dpg.does_item_exist("red_score"):
                    dpg.bind_item_font("red_score", game_font)
                red_team_score = sum(player["score"] for player in red_players.values())
                dpg.add_text(f"Red Team: {red_team_score}", tag="red_team_score_text")
                dpg.add_separator()
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=20)                    # icon column
                    dpg.add_text("Name")                        # name column
                    dpg.add_spacer(width=80 - len("Name") * 6) 
                    dpg.add_text("Score")                       # score column

                top_red = sorted(red_players.items(), key=lambda item: item[1]["score"], reverse=True)
                for equip_id, data in top_red:
                    with dpg.group(horizontal=True):
                        if equip_id in base_hit_players and base_icon_texture_id:
                            dpg.add_image(base_icon_texture_id, width=20, height=20)
                        else:
                            dpg.add_spacer(width=20)
                        dpg.add_text(f"{data['name']:<10} {data['score']}")
            
            # Red theme          
            with dpg.theme() as red_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (225, 49, 55))
                    dpg.add_theme_color(dpg.mvThemeCol_Border, (200, 30, 30))
                    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 2)
                    dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 10)
            dpg.bind_item_theme("red_score", red_theme)

            # GREEN TEAM
            with dpg.child_window(tag="green_score", width=scoreWidth, height=scoreHeight, no_scrollbar=True):
                if dpg.does_item_exist("green_score"):
                    dpg.bind_item_font("green_score", game_font)
                green_team_score = sum(player["score"] for player in green_players.values())
                dpg.add_text(f"Green Team:  {green_team_score}", tag="green_team_score_text")

                dpg.add_separator()

                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=20)                    # icon column
                    dpg.add_text("Name")                        # name column
                    dpg.add_spacer(width=80 - len("Name") * 6)  
                    dpg.add_text("Score")                       # score column

                top_green = sorted(green_players.items(), key=lambda item: item[1]["score"], reverse=True)
                for equip_id, data in top_green:
                    with dpg.group(horizontal=True):
                        if equip_id in base_hit_players and base_icon_texture_id:
                            dpg.add_image(base_icon_texture_id, width=20, height=20)
                        else:
                            dpg.add_spacer(width=20)
                        dpg.add_text(f"{data['name']:<10} {data['score']}")
           
            # Green Theme
            with dpg.theme() as green_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (49, 225, 55))
                    dpg.add_theme_color(dpg.mvThemeCol_Border, (30, 200, 30))
                    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 2)
                    dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 10)
            dpg.bind_item_theme("green_score", green_theme)

        # Timer Box
        with dpg.group(horizontal=True):
            with dpg.child_window(tag="timer_box", width=timerWidth, height=timerHeight, no_scrollbar=True):
                if dpg.does_item_exist("timer_box"):
                    dpg.bind_item_font("timer_box", game_font)
                dpg.add_text("00:00", tag="timer_text")

        with dpg.theme() as timer_theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0))
        dpg.bind_item_theme("timer_box", timer_theme)

        # Background Theme
        with dpg.theme() as screen_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0))
        dpg.bind_item_theme("game_screen", screen_theme)

# Update Timer
def runTimer():
    #print("RUNNING TIMER")
    global startTime, warned, started

    if startTime is None or not dpg.does_item_exist("timer_text"):
        #print("AAAAHHH NO TIMER")
        return

    elapsed = time.time() - startTime

    if not warned:
        remaining = int(countDown - elapsed)
        if remaining > 0:
            minutes = remaining // 60
            seconds = remaining % 60
            dpg.set_value("timer_text", f"Starting in: {minutes:02d}:{seconds:02d}")
        else:
            warned = True
            started = True
            network.broadcast_game_start()
            startTime = time.time()  # reset for the 6-minute countdown
            dpg.set_value("timer_text", "06:00")
            
        return

    if started:
        remaining = int(gameDuration - elapsed)
        if remaining <= 0:
            dpg.set_value("timer_text", "TIME UP!")
            network.broadcast_game_end()
            started = False
            return
        minutes = remaining // 60
        seconds = remaining % 60
        dpg.set_value("timer_text", f"{minutes:02d}:{seconds:02d}")

    # Update Team Scores if game is running
    if started:
        if dpg.does_item_exist("red_team_score_text"):
            red_score = sum(player["score"] for player in red_players.values())
            dpg.set_value("red_team_score_text", f"Red Team: {red_score}")

        if dpg.does_item_exist("green_team_score_text"):
            green_score = sum(player["score"] for player in green_players.values())
            dpg.set_value("green_team_score_text", f"Green Team: {green_score}")

