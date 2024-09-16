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

    # Criando uma lista de linhas horizontais
    horizontal_lines = [[13, 15, 17], [19, 21, 23], [25, 27, 29]]

    # Criando uma lista de linhas verticais
    vertical_lines = [[13, 19, 25], [15, 21, 27], [17, 23, 29]]

    # Criando uma lista de linhas diagonais
    diagonal_lines = [[13, 21, 29], [17, 21, 25]]

    # Combinando todas as linhas possíveis
    lines = horizontal_lines + vertical_lines + diagonal_lines

    def close(e):
        page.window_close()

    def win(player):
        """
        Função chamada quando um jogador ganha o jogo.
        Define a cor do texto com base no jogador vencedor e atualiza a GUI.
        """
        # Definindo uma cor base para o projeto
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
        """
        Função chamada quando um jogador arrasta e solta uma peça no tabuleiro.
        Atualiza o tabuleiro e verifica se a jogada resultou em vitória.
        """
        src = page.get_control(e.src_id)
        field = int(e.target[1:])
        e.control.content.bgcolor = src.content.bgcolor
        e.control.content.border = None
        id_player = int(json.loads(e.data)['src_id'][1:])

        if field in fields_left:
            e.control.update()

        if id_player == 10 and field in fields_left:
            player_red.append(field)
            player_red.sort()
            fields_left.remove(field)

        if id_player == 6 and field in fields_left:
            player_blue.append(field)
            player_blue.sort()
            fields_left.remove(field)

        for line in lines:
            # Verificando todos os números da linha vermelha
            if all(num in player_red for num in line):
                win("Red")
                return

            # Verificando todos os números da linha azul
            if all(num in player_blue for num in line):
                win("Blue")
                return

    page.add(
        ft.Row(
            [
                ft.Row(
                    [
                        ft.Draggable(
                            group="color",
                            content=ft.Container(
                                width=50,
                                height=50,
                                bgcolor=ft.colors.BLUE,
                                border_radius=5
                            )
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
                                margin=ft.margin.only(left=60),
                                width=50,
                                height=50,
                                bgcolor=ft.colors.RED,
                                border_radius=5
                            )
                        )
                    ]
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
