# Needs splash screen 
# Needs to Update one player into the database via application
import dearpygui.dearpygui as dpg

tableWidth = 450
tableHeight = 410
buttonWidth = 100
buttonHeight = 100
spacerGap = 20

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
def resize_team_window(*_):
    view_width = dpg.get_viewport_client_width()
    view_height = dpg.get_viewport_client_height()

    # Resize main window to fit viewport
    dpg.set_item_width("team_window", view_width )
    dpg.set_item_height("team_window", view_height)

    # Center the tables
    total_table_width = tableWidth * 2 + 20
    left_table_spacer = max((view_width - total_table_width) // 2, 0)
    dpg.set_item_pos("tables_group", (left_table_spacer, 50))

    # Center the buttons under the tables
    total_buttons_width = buttonWidth * 2 + spacerGap
    buttons_x = max((view_width - total_buttons_width) // 2, 0)
    buttons_y = tableHeight + 70  
    dpg.set_item_pos("buttons_group", (buttons_x, buttons_y))

def show_player_entry():
    with dpg.window(tag="team_window", label="Teams",no_title_bar=True, no_move=True, no_resize=True, no_scrollbar=True) as team_window:
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
                            dpg.add_input_int(tag=f"red_id_{i}", width=80, step=0, step_fast=0)
                            dpg.add_input_text(tag=f"red_code_{i}", width=120)
                            dpg.add_input_int(tag=f"red_equip_{i}", width=100, step=0, step_fast=0)
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
                            dpg.add_input_int(tag=f"green_id_{i}", width=80, step=0, step_fast=0)
                            dpg.add_input_text(tag=f"green_code_{i}", width=120)
                            dpg.add_input_int(tag=f"green_equip_{i}", width=100, step=0, step_fast=0)
                
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
            dpg.add_button(label="F5 Start", tag="startButton", width=buttonWidth, height=buttonHeight) #add callback for start
            dpg.add_spacer(width=spacerGap)   # small gap between buttons
            dpg.add_button(label="F12 Clear", tag="clearButton", width=buttonWidth, height=buttonHeight, callback=clear_entries)
        with dpg.handler_registry():
            dpg.add_key_press_handler(dpg.mvKey_F5) #add callback for start
            dpg.add_key_press_handler(dpg.mvKey_F12, callback=clear_entries)

# Initialize DearPyGui, create the UI, and start the render loop.
def main():
    dpg.create_context()
    dpg.create_viewport(title="Laser Tag", width=1000, height=640)
    dpg.set_viewport_small_icon("logo.ico")
    dpg.setup_dearpygui()

    show_player_entry()
    resize_team_window()

    dpg.show_viewport()

    # Manual render loop for dynamic resizing
    while dpg.is_dearpygui_running():
        resize_team_window() 
        dpg.render_dearpygui_frame()

    dpg.destroy_context()

if __name__ == "__main__":
    main()
