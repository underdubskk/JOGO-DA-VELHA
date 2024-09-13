# Importando o flet
import flet as ft
from flet import (
    Column,
    Container,
    Draggable,
    DragTarget,
    DragTargetAcceptEvent,
    Page,
    Row,
    GridView,
    colors,
)

def main(page: Page):
    page.title = "Drag and Drop example"

    def drag_accept(e: DragTargetAcceptEvent):
        src = page.get_control(e.src_id)
        e.control.content.bgcolor = src.content.bgcolor
        e.control.content.border = None
        e.control.update()

    grid = GridView(
        expand=1,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
    )

    for _ in range(9):
        grid.controls.append(
            DragTarget(
                group="color",
                content=Container(
                    width=50,
                    height=50,
                    bgcolor=colors.BLUE_GREY_100,
                    border_radius=5,
                ),
                on_accept=drag_accept
            )
        )

    page.add(
        Row(
            [
                Column(
                    [
                        Draggable(
                            group="color",
                            content=Container(
                                width=50,
                                height=50,
                                bgcolor=colors.RED,
                                border_radius=5,
                            ),
                        ),
                        Draggable(
                            group="color",
                            content=Container(
                                width=50,
                                height=50,
                                bgcolor=colors.BLUE,
                                border_radius=5,
                            ),
                        ),
                    ]
                ),
                grid
            ]
        )
    )

ft.app(main)
