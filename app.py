import flet as ft
import json

def main(page: ft.Page):
    # Setando as propriedades da view
    page.title = "The Game"
    page.window_width = 300
    page.window_height = 360
    page.window_frameless = True
    page.window_center()

    player_red = []
    player_blue = []
    fields_left = [13, 15, 17, 19, 21, 23, 25, 27, 29]

    # Criando uma lista de linhas possíveis para vitória
    horizontal_lines = [[13, 15, 17], [19, 21, 23], [25, 27, 29]]
    vertical_lines = [[13, 19, 25], [15, 21, 27], [17, 23, 29]]
    diagonal_lines = [[13, 21, 29], [17, 21, 25]]
    lines = horizontal_lines + vertical_lines + diagonal_lines

    def close(e):
        page.window_close()

    def win(player):
        c = "blue" if player == "Blue" else "red"
        page.window_frameless = False
        page.controls.clear()
        page.add(
            ft.Column(
                [
                    ft.Container(
                        ft.Text(f"Player {player} won!", size=25, color=c),
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        ft.IconButton(
                            icon=ft.icons.CLOSE, icon_size=100, on_click=close
                        ),
                        alignment=ft.alignment.center
                    ),
                ]
            )
        )
        page.update()

    def drag_accept(e):
        src = page.get_control(e.src_id)
        field = int(e.target[1:])  # Certifique-se que 'target' tem o formato correto

        # A cor da célula é alterada
        e.control.content.bgcolor = src.content.bgcolor
        e.control.content.border = None

        try:
            id_player = int(json.loads(e.data)['src_id'][1:])  # Pega o id do jogador
        except (KeyError, ValueError):
            return

        if field in fields_left:
            if id_player == 10:  # Red player
                player_red.append(field)
            elif id_player == 6:  # Blue player
                player_blue.append(field)

            player_red.sort()
            player_blue.sort()
            fields_left.remove(field)

            # Verificando condições de vitória
            for line in lines:
                if all(num in player_red for num in line):
                    win("Red")
                    return
                if all(num in player_blue for num in line):
                    win("Blue")
                    return

            e.control.update()  # Atualiza a visualização da célula no tabuleiro

    page.add(
        ft.Row(
            [
                ft.Draggable(
                    group="color",
                    content=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.colors.BLUE,
                        border_radius=5
                    ),
                    data=json.dumps({"src_id": "draggable_blue"})
                ),
                ft.Container(
                    ft.IconButton(
                        icon=ft.icons.CLOSE, on_click=close
                    ),
                    margin=ft.margin.only(left=60)
                ),
                ft.Draggable(
                    group="color",
                    content=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.colors.RED,
                        border_radius=5
                    ),
                    data=json.dumps({"src_id": "draggable_red"})
                )
            ]
        )
    )

    grid = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=100,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5
    )

    page.add(grid)

    for _ in range(9):
        grid.controls.append(
            ft.DragTarget(
                group="color",
                content=ft.Container(
                    width=50,
                    height=50,
                    bgcolor=ft.colors.BLUE_GREY_100,
                    border_radius=5
                ),
                on_accept=drag_accept
            )
        )
    
    page.update()

ft.app(target=main)
