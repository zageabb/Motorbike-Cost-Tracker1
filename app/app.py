import reflex as rx
from app.pages.index import index
from app.pages.motorbikes_page import motorbikes_page
from app.pages.motorbike_detail_page import (
    motorbike_detail_page,
)
from app.states.motorbike_state import MotorbikeState


def app_with_theme():
    return rx.App(theme=rx.theme(appearance="light"))


app = app_with_theme()
app.add_page(index, route="/")
app.add_page(motorbikes_page, route="/motorbikes")
app.add_page(
    motorbike_detail_page,
    route="/motorbikes/[route_arg_motorbike_id]",
)