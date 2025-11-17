import time
from PIL import Image
import network
import music
import pygame
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "third_party"))  # so we can import from parent directory
import dearpygui.dearpygui as dpg

# Layout Constants
spacerGap = 20
scoreHeight = 530
scoreWidth = 300
scoreTopPadding = 10
timerWidth = 100
timerHeight = 40
buttonWidth = 100
buttonHeight = 100
winnerWidth = 892
winnerHeight = 410

# Global state
startTime = None
musicStarted = False
started = False
gameDuration = 6 * 60
flashCounter = 0
winner_txt = "none"

# Game Data Stores
red_players = {}
green_players = {}
base_hit_players = set()
base_icon_texture_id = None

# loads base icon
def load_base_icon_texture():
    global base_icon_texture_id

    if base_icon_texture_id is not None:
        return
    try:
        image = Image.open("baseicon.jpg").convert("RGBA")
        width, height = image.size
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

# Add/Subtract Points
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

def handle_event_printing(shooter_id: int, target_id: int, is_green: bool, action: str):
    if action == "unfriendly_fire":
        if is_green:
            shooter_name = green_players[shooter_id]["name"]
            target_name = red_players[target_id]["name"]
            shooter_color = (49, 225, 55)
            target_color = (225, 49, 55)
        else:
            shooter_name = red_players[shooter_id]["name"]
            target_name = green_players[target_id]["name"]
            shooter_color = (225, 49, 55)
            target_color = (49, 225, 55)

        with dpg.group(parent="game_text", horizontal=True):
            dpg.add_text(shooter_name, color=shooter_color)
            dpg.add_text(" hit ")
            dpg.add_text(target_name, color=target_color)
            dpg.add_text("!")
        dpg.add_text("(+10 points)", parent="game_text")

    elif action == "friendly_fire":
        if is_green:
            shooter_name = green_players[shooter_id]["name"]
            target_name = green_players[target_id]["name"]
            team_color = (49, 225, 55)
        else:
            shooter_name = red_players[shooter_id]["name"]
            target_name = red_players[target_id]["name"]
            team_color = (225, 49, 55)

        with dpg.group(parent="game_text", horizontal=True):
            dpg.add_text("Oops! ")
            dpg.add_text(shooter_name, color=team_color)
            dpg.add_text(" hit ")
            dpg.add_text(target_name, color=team_color)
            dpg.add_text("!")
        dpg.add_text("(-10 points each)", parent="game_text")

    elif action == "base_score":
        if is_green:
            shooter_name = green_players[shooter_id]["name"]
            base_name = "green base"
            base_color = (49, 225, 55)
        else:
            shooter_name = red_players[shooter_id]["name"]
            base_name = "red base"
            base_color = (225, 49, 55)

        with dpg.group(parent="game_text", horizontal=True):
            dpg.add_text(shooter_name, color=base_color)
            dpg.add_text(" scored ")
            dpg.add_text(base_name, color=base_color)
            dpg.add_text("!")
        dpg.add_text("(+100 points)", parent="game_text")

    dpg.set_y_scroll("game_text", -1)

def resize_game_window():
    global winner_txt, flashCounter

    view_width = dpg.get_viewport_client_width()
    view_height = dpg.get_viewport_client_height()

    if dpg.does_item_exist("game_screen"):
        dpg.set_item_width("game_screen", view_width)
        dpg.set_item_height("game_screen", view_height)

    if dpg.does_item_exist("score_group"):
        total_table_width = scoreWidth * 2
        center_x = max((view_width - total_table_width) // 2, 0)
        dpg.set_item_pos("score_group", (center_x, scoreTopPadding))

    if dpg.does_item_exist("game_text"):
        total_table_width = scoreWidth * 2
        center_x = max((view_width - total_table_width) // 2, 0)
        table_y = scoreTopPadding + scoreHeight + 10
        dpg.set_item_pos("game_text", (center_x, table_y))

    if dpg.does_item_exist("timer_box"):
        dpg.set_item_pos("timer_box", (view_width - timerWidth - 20, scoreTopPadding))

    # Center the child window showing the winner
    if dpg.does_item_exist("winner_team"):
        winner_x = max((view_width - winnerWidth) // 2, 0)
        winner_y = max((view_height - winnerHeight) // 2 - 40, 0)
        dpg.set_item_pos("winner_team", (winner_x, winner_y))

        # Center the button under the child window
        if dpg.does_item_exist("button_group"):
            button_x = max((view_width - buttonWidth) // 2, 0)
            button_y = winner_y + winnerHeight + 20  
            dpg.set_item_pos("button_group", (button_x, button_y))
        
        # Flash winner text
        if dpg.does_item_exist("winner_txt"):
            flashCounter += 1

            if (flashCounter > 50):
                dpg.set_value("winner_txt", " ")
            else:
                dpg.set_value("winner_txt", winner_txt)

            if (flashCounter > 100):
                flashCounter = 0

# Game Screen
def game_screen(red_data, green_data):
    global red_players, green_players, startTime, warned, started
    red_players = red_data
    green_players = green_data

    startTime = time.time()
    warned = False
    started = False

    load_base_icon_texture()
    dpg.delete_item("team_window")
    
    # Define font only to the game screen
    if not dpg.does_item_exist("game_font"):
        with dpg.font_registry():
            dpg.add_font("CONSOLA.TTF", 20, tag="game_font")
            dpg.add_font("CONSOLA.TTF", 70, tag="winner_font")
     
    with dpg.window(tag="game_screen", no_title_bar=True, no_move=True, no_resize=True, no_scrollbar=True):
        dpg.set_primary_window("game_screen", True)

        with dpg.group(tag="score_group", horizontal=True):
            # RED TEAM
            with dpg.child_window(tag="red_score", width=scoreWidth, height=scoreHeight, no_scrollbar=True):
                dpg.bind_item_font("red_score", "game_font")
                red_team_score = sum(player["score"] for player in red_players.values())
                dpg.add_text(f"Red Team: {red_team_score}", tag="red_team_score_text")
                dpg.add_separator()
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=20)
                    dpg.add_text("Name")
                    dpg.add_spacer(width=80 - len("Name") * 6)
                    dpg.add_text("Score")

                dpg.add_group(tag="red_player_rows")  # rows handled by runTimer()

            with dpg.theme() as red_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (225, 49, 55))
                    dpg.add_theme_color(dpg.mvThemeCol_Border, (200, 30, 30))
                    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 2)
                    dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 10)
            dpg.bind_item_theme("red_score", red_theme)

            with dpg.child_window(tag="green_score", width=scoreWidth, height=scoreHeight, no_scrollbar=True):
                dpg.bind_item_font("green_score", "game_font")
                green_team_score = sum(player["score"] for player in green_players.values())
                dpg.add_text(f"Green Team:  {green_team_score}", tag="green_team_score_text")
                dpg.add_separator()
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width=20)
                    dpg.add_text("Name")
                    dpg.add_spacer(width=80 - len("Name") * 6)
                    dpg.add_text("Score")

                dpg.add_group(tag="green_player_rows")  # rows handled by runTimer()

            with dpg.theme() as green_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (49, 225, 55))
                    dpg.add_theme_color(dpg.mvThemeCol_Border, (30, 200, 30))
                    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 2)
                    dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 10)
            dpg.bind_item_theme("green_score", green_theme)

        # Game play
        with dpg.child_window(tag="game_text", width=((scoreWidth * 2) + 8), height=(scoreHeight // 4), no_scrollbar=True):
            dpg.bind_item_font("game_text", "game_font")

        # Theme for the box where the game text will go 
        with dpg.theme() as game_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_Border, (200, 30, 30))
                dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 2)
                dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 10)
        dpg.bind_item_theme("game_text", game_theme)

        with dpg.group(horizontal=True):
            with dpg.child_window(tag="timer_box", width=timerWidth, height=timerHeight, no_scrollbar=True):
                dpg.bind_item_font("timer_box", "game_font")
                dpg.add_text("00:00", tag="timer_text")

        with dpg.theme() as timer_theme:
            with dpg.theme_component(dpg.mvChildWindow):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0))
        dpg.bind_item_theme("timer_box", timer_theme)

        with dpg.theme() as screen_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0))
                dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0))
        dpg.bind_item_theme("game_screen", screen_theme)

def winner_screen():
    global red_players, green_players, winner_txt, winner_color

    if dpg.does_item_exist("game_screen"):
        dpg.delete_item("game_screen")

    if dpg.does_item_exist("winner_window"):
        dpg.delete_item("winner_window")

    #Calulates the scores so we can see who won
    red_score = sum(p["score"] for p in red_players.values())
    green_score = sum(p["score"] for p in green_players.values())

    if dpg.does_item_exist("game_screen"):
        dpg.delete_item("game_screen")

    if dpg.does_item_exist("winner_window"):
        dpg.delete_item("winner_window")
    
    #Compares who won! 
    if red_score > green_score:
        winner_txt = "RED  TEAM  WINS!"
        winner_color = (225, 49, 55)
    elif green_score > red_score:
        winner_txt = "GREEN TEAM WINS!"
        winner_color = (49, 225, 55)
    else:
        winner_txt = "TEAMS HAVE TIED!"
        winner_color = (255, 192, 203) #IM MAKING SOMETHING PINK IN THIS CODE RAHHHH

    with dpg.window(tag="winner_window", label="Game Over", width=1000, height=640, no_title_bar=True, no_move=True, no_resize=True, no_scrollbar=True) as winner_window:
        dpg.add_spacer(height=200) #center

        with dpg.group(tag="group", horizontal=True):
            with dpg.child_window(tag="winner_team", width=winnerWidth, height=winnerHeight):
                dpg.bind_item_font("winner_team", "winner_font")
                dpg.add_spacer(height=150)
                dpg.add_text(winner_txt, color=winner_color, tag="winner_txt", pos=((winnerWidth // 8) + 35, (winnerHeight // 2)))

        with dpg.theme() as winner_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (0, 0, 0))
        dpg.bind_item_theme("winner_team", winner_theme)    

        with dpg.group(tag="button_group", horizontal=True):
            dpg.add_button(label="New Game", width=buttonWidth, height=buttonHeight, callback=new_game)

    with dpg.theme() as window_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (0, 0, 0))
            dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 0, 0))
    dpg.bind_item_theme("winner_window", window_theme)

def new_game():
    #print("Start New Game button clicked!")
    global red_players, green_players
    red_players.clear()
    green_players.clear()

    if dpg.does_item_exist("winner_window"):
        dpg.delete_item("winner_window", children_only=False)

    from main import show_player_entry
    show_player_entry()
    
def run_pregame_timer(red_players, green_players):
    pygame.init()
    width, height = 1000, 640
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Laser Tag")  # match title

    try:
        icon = pygame.image.load("table_logo.ico")  
        pygame.display.set_icon(icon)
    except pygame.error:
        print("Warning: Could not load icon for title bar")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 74)
    start = pygame.time.get_ticks()

    music_started = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        seconds = 30 - (pygame.time.get_ticks() - start) // 1000
        if seconds < 0:
            seconds = 0
        
        if not music_started and seconds <= 16:
            music.play_music()
            music_started = True

        screen.fill((0, 0, 0))
        text = font.render(f"Game Starts: {seconds:02d}", True, (49, 225, 55))
        textBox = text.get_rect(center=screen.get_rect().center)
        screen.blit(text, textBox)

        pygame.display.flip()

        if seconds == 0:
            screen.fill((0, 0, 0))
            go_text = font.render("GO!", True, (49, 225, 55))
            go_rect = go_text.get_rect(center=screen.get_rect().center)
            screen.blit(go_text, go_rect)
            pygame.display.flip()
            pygame.time.delay(2000)
            break

        clock.tick(60)

    pygame.display.quit()

    game_screen(red_players, green_players)

    time.sleep(0.1)

    network.broadcast_game_start()

def runTimer():
    global startTime, musicStarted, gameDuration, flashCounter

    if startTime is None or not dpg.does_item_exist("timer_text"):
        return
        
    elapsed = time.time() - startTime

    remaining = int(gameDuration - elapsed)
    if remaining <= 0:
        dpg.set_value("timer_text", "TIME UP!")
        network.broadcast_game_end()
        started = False
        winner_screen()

        return
    minutes = remaining // 60
    seconds = remaining % 60
    dpg.set_value("timer_text", f"{minutes:02d}:{seconds:02d}")

    # Updated Team scores
    if dpg.does_item_exist("red_team_score_text") and dpg.does_item_exist("green_team_score_text"):
        flashCounter += 1

        red_score = sum(player["score"] for player in red_players.values())
        green_score = sum(player["score"] for player in green_players.values())

        dpg.set_value("red_team_score_text", f"Red Team: {red_score}")
        dpg.set_value("green_team_score_text", f"Green Team: {green_score}")

        if (flashCounter > 30):
            if (red_score > green_score):
                dpg.set_value("red_team_score_text", f"Red Team: ")
            elif (green_score > red_score):
                dpg.set_value("green_team_score_text", f"Green Team: ")
            else:
                dpg.set_value("red_team_score_text", f"Red Team: ")
                dpg.set_value("green_team_score_text", f"Green Team: ")

        if (flashCounter > 60):
            flashCounter = 0

    # Redraw Red player rows
    if dpg.does_item_exist("red_player_rows"):
        dpg.delete_item("red_player_rows", children_only=True)
        top_red = sorted(red_players.items(), key=lambda item: item[1]["score"], reverse=True)
        for equip_id, data in top_red:
            with dpg.group(horizontal=True, parent="red_player_rows"):
                if equip_id in base_hit_players and base_icon_texture_id:
                    dpg.add_image(base_icon_texture_id, width=20, height=20)
                else:
                    dpg.add_spacer(width=20)
                dpg.add_text(f"{data['name']:<10} {data['score']}", tag=f"red_score_{equip_id}")

    # Redraw Green player rows
    if dpg.does_item_exist("green_player_rows"):
        dpg.delete_item("green_player_rows", children_only=True)
        top_green = sorted(green_players.items(), key=lambda item: item[1]["score"], reverse=True)
        for equip_id, data in top_green:
            with dpg.group(horizontal=True, parent="green_player_rows"):
                if equip_id in base_hit_players and base_icon_texture_id:
                    dpg.add_image(base_icon_texture_id, width=20, height=20)
                else:
                    dpg.add_spacer(width=20)
                dpg.add_text(f"{data['name']:<10} {data['score']}", tag=f"green_score_{equip_id}")