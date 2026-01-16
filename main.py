import flet as ft
import random

# --- 1. EXPANDED WORD LISTS ---
CATEGORIES = {
    "Everyday Objects": [
        "Chair", "Table", "Laptop", "Bottle", "Spoon", 
        "Umbrella", "Clock", "Key", "Wallet", "Backpack",
        "Toothbrush", "Mirror", "Pillow", "Shoe", "Glasses"
    ],
    "Animals": [
        "Lion", "Tiger", "Elephant", "Dog", "Cat",
        "Giraffe", "Penguin", "Dolphin", "Eagle", "Shark",
        "Kangaroo", "Panda", "Wolf", "Zebra", "Owl"
    ],
    "Foods & Drinks": [
        "Pizza", "Burger", "Sushi", "Pasta", "Salad",
        "Ice Cream", "Coffee", "Tea", "Chocolate", "Sandwich",
        "Tacos", "Pancakes", "Steak", "Fries", "Soup"
    ],
    "Science & Tech": [
        "Robot", "Rocket", "Microscope", "Satellite", "Computer",
        "Telescope", "Drone", "Laser", "Battery", "Magnet",
        "Circuit", "Laboratary", "Atom", "Gravity", "Internet"
    ],
    "Places": [
        "Beach", "Mountain", "Forest", "Desert", "City",
        "School", "Hospital", "Airport", "Library", "Stadium",
        "Museum", "Park", "Cinema", "Restaurant", "Hotel"
    ]
}

def main(page: ft.Page):
    page.title = "Imposter Who? - Mr. White Mode"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 800
    page.bgcolor = "grey100"
    
    # COLORS
    COLOR_PRIMARY = "yellow400"
    COLOR_WHITE_MODE = "bluegrey900" # Special Dark Theme for Mr. White
    COLOR_TEXT = "black"

    # --- GAME STATE ---
    game_state = {
        "players": 4,
        "imposters": 1, 
        "imposter_indices": [], 
        "word": "",
        "current_player": 0,
        "names": [],
        "category": "Everyday Objects",
        "mr_white_mode": False # The Twist Toggle
    }

    # --- UI COMPONENT: NAVIGATION ---
    def go_to_main_menu(e=None):
        page.clean()
        
        # LABELS & SLIDERS
        player_label = ft.Text(f"Players: {game_state['players']}", size=16, weight="bold")
        imposter_label = ft.Text(f"Imposters: {game_state['imposters']}", size=16, weight="bold")

        imposter_slider = ft.Slider(min=1, max=3, divisions=2, value=game_state["imposters"], active_color="red400", label="{value}")
        player_slider = ft.Slider(min=3, max=12, divisions=9, value=game_state["players"], active_color=COLOR_TEXT, label="{value}")

        def on_player_change(e):
            count = int(e.control.value)
            game_state["players"] = count
            player_label.value = f"Players: {count}"
            # Smart Logic: Max imposters cannot be >= players
            max_safe = max(1, count - 2)
            if imposter_slider.value > max_safe:
                imposter_slider.value = max_safe
                game_state["imposters"] = max_safe
                imposter_label.value = f"Imposters: {int(imposter_slider.value)}"
            page.update()

        def on_imposter_change(e):
            count = int(e.control.value)
            max_safe = max(1, int(player_slider.value) - 2)
            if count > max_safe:
                e.control.value = max_safe
                count = max_safe
            game_state["imposters"] = count
            imposter_label.value = f"Imposters: {count}"
            page.update()

        player_slider.on_change = on_player_change
        imposter_slider.on_change = on_imposter_change

        category_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(k) for k in CATEGORIES.keys()],
            value=game_state["category"],
            width=250, bgcolor="white", border_color="black"
        )

        # --- THE TWIST: MR WHITE TOGGLE ---
        mr_white_switch = ft.Switch(
            label="Mr. White Mode (Guess to Win)",
            value=game_state["mr_white_mode"],
            active_color=COLOR_WHITE_MODE
        )

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("IMPOSTER\nWHO?", size=50, weight="bold", text_align="center", color=COLOR_TEXT),
                    
                    # Settings Card
                    ft.Container(
                        content=ft.Column([
                            ft.Text("GAME SETTINGS", size=12, weight="bold", color="grey"),
                            ft.Divider(),
                            player_label, player_slider,
                            ft.Container(height=10),
                            imposter_label, imposter_slider,
                            ft.Divider(),
                            ft.Text("CATEGORY", size=12, weight="bold", color="grey"),
                            category_dropdown,
                            ft.Divider(),
                            
                            # MR WHITE UI
                            ft.Container(
                                content=mr_white_switch,
                                bgcolor="white", padding=10, border_radius=10
                            )
                        ]),
                        padding=20, bgcolor="white", border_radius=15,
                        shadow=ft.BoxShadow(blur_radius=10, color="grey300")
                    ),

                    ft.Container(height=20),
                    
                    ft.FilledButton(
                        content=ft.Text("START GAME", size=18, weight="bold", color="black"),
                        on_click=lambda e: start_game(category_dropdown.value, mr_white_switch.value),
                        style=ft.ButtonStyle(bgcolor=COLOR_PRIMARY, shape=ft.RoundedRectangleBorder(radius=10)),
                        height=60, width=250
                    )
                ], horizontal_alignment="center", alignment="center"),
                alignment=ft.Alignment(0, 0), padding=20, expand=True
            )
        )
        page.update()

    def start_game(category, is_mr_white):
        game_state["category"] = category
        game_state["mr_white_mode"] = is_mr_white
        game_state["names"] = [f"Player {i+1}" for i in range(game_state["players"])]
        game_state["word"] = random.choice(CATEGORIES[category])
        
        num_imposters = game_state["imposters"]
        game_state["imposter_indices"] = random.sample(range(game_state["players"]), num_imposters)
        game_state["current_player"] = 0
        go_to_handover()

    def go_to_handover():
        if game_state["current_player"] >= game_state["players"]:
            go_to_discussion()
            return

        current_name = game_state["names"][game_state["current_player"]]
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.PHONE_ANDROID, size=80, color=COLOR_TEXT),
                    ft.Text(f"Pass phone to\n{current_name}", size=30, weight="bold", text_align="center"),
                    ft.Container(height=20),
                    ft.FilledButton(
                        content=ft.Text("I AM READY", color="black"), 
                        on_click=lambda e: go_to_reveal(current_name),
                        style=ft.ButtonStyle(bgcolor=COLOR_PRIMARY),
                        height=50, width=200
                    )
                ], alignment="center", horizontal_alignment="center"),
                alignment=ft.Alignment(0, 0), expand=True
            )
        )
        page.update()

    def go_to_reveal(player_name):
        is_imposter = game_state["current_player"] in game_state["imposter_indices"]
        
        # --- LOGIC: If Mr White Mode, change the text ---
        if is_imposter:
            if game_state["mr_white_mode"]:
                role_text = "YOU ARE\nMR. WHITE!"
                sub_text = "You have no word.\nBlend in, or guess the word at the end!"
                bg_color = COLOR_WHITE_MODE
            else:
                role_text = "YOU ARE THE\nIMPOSTER!"
                sub_text = "Blend in and don't get caught!"
                bg_color = "red400"
        else:
            role_text = f"WORD:\n{game_state['word']}"
            sub_text = f"Category: {game_state['category']}"
            bg_color = COLOR_PRIMARY
        
        # Secret Content
        secret_content = ft.Container(
            content=ft.Column([
                ft.Text(role_text, size=30, weight="bold", color="white", text_align="center"),
                ft.Text(sub_text, size=16, color="white70", text_align="center")
            ], alignment="center", horizontal_alignment="center"),
            alignment=ft.Alignment(0, 0), opacity=0, animate_opacity=200
        )

        instruction_text = ft.Column([
            ft.Icon(ft.Icons.TOUCH_APP, size=50, color="black"),
            ft.Text("HOLD TO REVEAL", size=20, weight="bold", color="black")
        ], alignment="center", horizontal_alignment="center")

        def show_secret(e):
            secret_content.opacity = 1
            instruction_container.opacity = 0
            page.update()

        def hide_secret(e):
            secret_content.opacity = 0
            instruction_container.opacity = 1
            page.update()
        
        def finish_turn(e):
            game_state["current_player"] += 1
            go_to_handover()

        instruction_container = ft.Container(content=instruction_text, opacity=1, animate_opacity=200)

        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text(player_name, size=40, weight="bold"),
                    ft.Text("Don't show anyone!", color="grey"),
                    
                    ft.GestureDetector(
                        on_tap_down=show_secret, on_tap_up=hide_secret,
                        content=ft.Container(
                            content=ft.Stack([
                                ft.Container(content=instruction_container, alignment=ft.Alignment(0, 0)),
                                secret_content
                            ]),
                            width=300, height=400,
                            bgcolor=bg_color,
                            border_radius=20, alignment=ft.Alignment(0, 0),
                            shadow=ft.BoxShadow(blur_radius=15, color="grey")
                        )
                    ),
                    ft.FilledButton("NEXT PLAYER", on_click=finish_turn, width=200, height=50)
                ], horizontal_alignment="center", spacing=20),
                alignment=ft.Alignment(0, 0), expand=True, padding=20
            )
        )
        page.update()

    def go_to_discussion():
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("TIME TO DISCUSS!", size=30, weight="bold"),
                    ft.Text("Who is the Imposter?", size=20, color="grey"),
                    ft.Icon(ft.Icons.PEOPLE_OUTLINE, size=100, color=COLOR_TEXT),
                    ft.Container(height=50),
                    ft.FilledButton(
                        content=ft.Text("REVEAL IMPOSTER", color="white"),
                        style=ft.ButtonStyle(bgcolor="black"),
                        height=60, width=250,
                        on_click=lambda e: go_to_confirmation() 
                    )
                ], alignment="center", horizontal_alignment="center"),
                alignment=ft.Alignment(0, 0), expand=True
            )
        )
        page.update()

    def go_to_confirmation():
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=80, color="orange"),
                    ft.Text("End the Game?", size=30, weight="bold"),
                    ft.Text("Are you sure you want to reveal the winner?", text_align="center", color="grey"),
                    ft.Container(height=30),
                    ft.Row([
                        ft.OutlinedButton("NO", on_click=lambda e: go_to_discussion(), width=100),
                        ft.FilledButton("YES", on_click=lambda e: check_mr_white_trigger(), width=100, style=ft.ButtonStyle(bgcolor="red"))
                    ], alignment="center", spacing=20)
                ], alignment="center", horizontal_alignment="center"),
                alignment=ft.Alignment(0, 0), expand=True
            )
        )
        page.update()

    def check_mr_white_trigger():
        # If Mr White Mode is ON, we don't end the game yet. We go to "The Guess" phase.
        if game_state["mr_white_mode"]:
            go_to_mr_white_guess()
        else:
            go_to_results(mr_white_win=False)

    def go_to_mr_white_guess():
        # --- THE TWIST SCREEN ---
        guess_input = ft.TextField(label="Enter Secret Word", width=250)
        
        def submit_guess(e):
            # Check if guess matches (Case insensitive)
            if guess_input.value.strip().lower() == game_state["word"].lower():
                go_to_results(mr_white_win=True)
            else:
                go_to_results(mr_white_win=False)

        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.SEARCH, size=80, color=COLOR_WHITE_MODE),
                    ft.Text("MR. WHITE FOUND!", size=30, weight="bold", color=COLOR_WHITE_MODE),
                    ft.Text("But wait... you have one chance.", size=16),
                    ft.Container(height=20),
                    ft.Text("Guess the word to steal the win!", weight="bold"),
                    guess_input,
                    ft.Container(height=20),
                    ft.FilledButton("SUBMIT GUESS", on_click=submit_guess, width=200, style=ft.ButtonStyle(bgcolor=COLOR_WHITE_MODE))
                ], alignment="center", horizontal_alignment="center"),
                alignment=ft.Alignment(0, 0), expand=True
            )
        )
        page.update()

    def go_to_results(mr_white_win=False):
        imposter_names = [game_state["names"][i] for i in game_state["imposter_indices"]]
        imposter_str = ", ".join(imposter_names)
        
        # Dynamic Result Text
        if game_state["mr_white_mode"]:
            if mr_white_win:
                title = "MR. WHITE WINS!"
                color = "green"
                msg = "He guessed the word correctly!"
            else:
                title = "CIVILIANS WIN!"
                color = "blue"
                msg = "Mr. White was caught and failed to guess."
        else:
            title = "GAME OVER"
            color = "black"
            msg = "Here are the results:"

        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text(title, size=40, weight="bold", color=color),
                    ft.Text(msg, size=16, color="grey"),
                    ft.Divider(),
                    ft.Text("The Word Was:", size=15),
                    ft.Text(game_state["word"], size=35, weight="bold", color="blue"),
                    ft.Container(height=20),
                    ft.Text("The Imposters Were:", size=15),
                    ft.Text(imposter_str, size=30, weight="bold", color="red"),
                    
                    ft.Container(height=50),
                    ft.FilledButton(
                        "NEW GAME", 
                        on_click=go_to_main_menu, 
                        height=60, width=200,
                        style=ft.ButtonStyle(bgcolor=COLOR_PRIMARY, color="black")
                    )
                ], alignment="center", horizontal_alignment="center"),
                alignment=ft.Alignment(0, 0), expand=True
            )
        )
        page.update()

    go_to_main_menu()

ft.run(main)
