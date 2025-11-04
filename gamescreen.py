import dearpygui.dearpygui as dpg
import time
import music

spacerGap = 20
scoreHeight = 175
scoreWidth = 150
scoreTopPadding = 10
timerWidth = 150
timerHeight = 50

# Global state
startTime = None
started = False
musicStarted = False
warned = False
gameDuration = 60
countDown = 30
 
red_players = {}
green_players = {}

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
        dpg.set_item_pos("timer_box", (view_width - timerWidth - 90, scoreTopPadding))


def game_screen(red_data, green_data):
    global red_players, green_players, startTime, warned, started
    red_players = red_data
    green_players = green_data

    #set the time variables 
    startTime = time.time()
    warned = False
    started = False

    dpg.delete_item("team_window")

    with dpg.window(tag="game_screen", no_title_bar=True, no_move=True, no_resize=True, no_scrollbar=True):
        dpg.set_primary_window("game_screen", True)

        with dpg.group(tag="score_group", horizontal=True):
            # RED TEAM
            with dpg.child_window(tag="red_score", width=scoreWidth, height=scoreHeight, no_scrollbar=True):
                dpg.add_text("Red Team")
                dpg.add_separator()
                dpg.add_text("Name     Score")
                top_red = sorted(red_players.items(), key=lambda item: item[1]["score"], reverse=True)[:5]
                for _, data in top_red:
                    dpg.add_text(f"{data['name']:<10} {data['score']}")

            with dpg.theme() as red_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (225, 49, 55))
                    dpg.add_theme_color(dpg.mvThemeCol_Border, (200, 30, 30))
                    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 2)
                    dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 10)
            dpg.bind_item_theme("red_score", red_theme)

            # GREEN TEAM
            with dpg.child_window(tag="green_score", width=scoreWidth, height=scoreHeight, no_scrollbar=True):
                dpg.add_text("Green Team")
                dpg.add_separator()
                dpg.add_text("Name     Score")
                top_green = sorted(green_players.items(), key=lambda item: item[1]["score"], reverse=True)[:5]
                for _, data in top_green:
                    dpg.add_text(f"{data['name']:<10} {data['score']}")

            with dpg.theme() as green_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (49, 225, 55))
                    dpg.add_theme_color(dpg.mvThemeCol_Border, (30, 200, 30))
                    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 2)
                    dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 10)
            dpg.bind_item_theme("green_score", green_theme)

        # TIMER
        with dpg.child_window(tag="timer_box", width=timerWidth, height=timerHeight, no_scrollbar=True):
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

def runTimer():
    #print("RUNNING TIMER")
    global startTime, warned, started, musicStarted

    if startTime is None or not dpg.does_item_exist("timer_text"):
        #print("AAAAHHH NO TIMER")
        return

    elapsed = time.time() - startTime

    if not warned:
        remaining = int(countDown - elapsed)
        if remaining > 0:
            minutes = remaining // 60
            seconds = remaining % 60
            # DAN ADDITION: Adding call to music function so that it's properly timed
            if (seconds == 17 and not musicStarted):
                music.play_music()
                musicStarted = True
            dpg.set_value("timer_text", f"Starting in: {minutes:02d}:{seconds:02d}")
        else:
            warned = True
            started = True
            startTime = time.time()  # reset for the 6-minute countdown
            dpg.set_value("timer_text", "06:00")
        return

    if started:
        remaining = int(gameDuration - elapsed)
        if remaining <= 0:
            dpg.set_value("timer_text", "TIME UP!")
            started = False
            return
        minutes = remaining // 60
        seconds = remaining % 60
        dpg.set_value("timer_text", f"{minutes:02d}:{seconds:02d}")