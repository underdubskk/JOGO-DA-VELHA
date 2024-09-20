import flet as ft
import json

def main(page: ft.Page):
    page.title = "The Game"
    page.window.width = 300
    page.window.height = 390
    page.window.frameless = True
    page.window.center()

    player_red = []
    player_blue = []
    fields_left = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    current_turn = "Red"

    horizontal_lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    vertical_lines = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
    diagonal_lines = [[0, 4, 8], [2, 4, 6]]
    lines = horizontal_lines + vertical_lines + diagonal_lines

    def close(e):
        page.window_close()

    def restart(e):
        # Resetando o estado do jogo
        nonlocal player_red, player_blue, fields_left, current_turn
        player_red = []
        player_blue = []
        fields_left = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        current_turn = "Red"
        
        # Limpar os controles atuais
        page.controls.clear()
        
        # Configurar o tabuleiro novamente
        setup_game_board()
        
        # Atualizar a página
        page.update()

    def win(player):
        c = "blue" if player == "Blue" else "red"
        page.window.frameless = False
        page.controls.clear()
        page.add(
            ft.Container(
                bgcolor=ft.colors.WHITE,
                padding=20,
                content=ft.Column(
                    [
                        ft.Container(
                            ft.Text(f"Player {player} won!", size=31, weight="bold", color=c),
                            alignment=ft.alignment.center
                        ),
                        ft.Container(
                            ft.Text("Congratulations", size=25, weight="normal", color=ft.colors.BLACK),
                            alignment=ft.alignment.center
                        ),
                        ft.Row(
                            [
                                ft.Container(
                                    ft.IconButton(
                                        icon=ft.icons.CLOSE, icon_size=60, on_click=close
                                    ),
                                    margin=10
                                ),
                                ft.Container(
                                    ft.IconButton(
                                        icon=ft.icons.REPLAY, icon_size=60, on_click=restart
                                    ),
                                    margin=10
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                alignment=ft.alignment.center  # Removeu a duplicação
            )
        )
        page.update()

    def drag_accept(e):
        nonlocal current_turn

        src = page.get_control(e.src_id)
        index = int(e.control.data)

        if index not in fields_left:
            return

        if (current_turn == "Red" and src.data == json.dumps({"src_id": "draggable_red"})) or \
           (current_turn == "Blue" and src.data == json.dumps({"src_id": "draggable_blue"})):
            e.control.content.bgcolor = src.content.bgcolor
            e.control.content.border = None

            if current_turn == "Red":
                player_red.append(index)
            else:
                player_blue.append(index)

            player_red.sort()
            player_blue.sort()
            fields_left.remove(index)

            for line in lines:
                if all(num in player_red for num in line):
                    win("Red")
                    return
                if all(num in player_blue for num in line):
                    win("Blue")
                    return

            current_turn = "Blue" if current_turn == "Red" else "Red"

        e.control.update()

    def setup_game_board():
        # Configura o tabuleiro do jogo
        page.add(
            ft.Row(
                [
                    ft.Draggable(
                        group="color",
                        content=ft.Container(
                            width=55,
                            height=55,
                            bgcolor=ft.colors.BLUE,
                            border_radius=30
                        ),
                        data=json.dumps({"src_id": "draggable_blue"})
                    ),
                    ft.Container(
                        ft.IconButton(
                            icon=ft.icons.CLOSE, icon_size=60, on_click=close
                        ),
                        margin=ft.margin.only(left=35, right=40)
                    ),
                    ft.Draggable(
                        group="color",
                        content=ft.Container(
                            width=55,
                            height=55,
                            bgcolor=ft.colors.RED,
                            border_radius=30
                        ),
                        data=json.dumps({"src_id": "draggable_red"})
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

        grid = ft.GridView(
            expand=1,
            runs_count=3,
            max_extent=100,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5
        )

        page.add(grid)

        for i in range(9):
            grid.controls.append(
                ft.DragTarget(
                    group="color",
                    content=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.colors.BLUE_GREY_100,
                        border_radius=5
                    ),
                    on_accept=drag_accept,
                    data=str(i)
                )
            )

    setup_game_board()
    page.update()

ft.app(target=main)
