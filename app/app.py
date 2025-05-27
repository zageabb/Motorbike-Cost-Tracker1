import reflex as rx
from app.pages.index import index
from app.pages.motorbikes_page import motorbikes_page
from app.pages.motorbike_detail_page import (
    motorbike_detail_page,
)
from app.pages.sign_in import sign_in
from app.pages.sign_up import sign_up
from app.states.motorbike_state import MotorbikeState
from app.states.auth_state import AuthState
from app.db_setup import (
    create_db_and_tables,
    populate_example_data,
)


def app_with_theme():
    return rx.App(theme=rx.theme(appearance="light"))


app = app_with_theme()
create_db_and_tables()
populate_example_data()
app.add_page(
    index, route="/", on_load=AuthState.check_session
)
app.add_page(
    motorbikes_page,
    route="/motorbikes",
    on_load=AuthState.check_session,
)
app.add_page(
    motorbike_detail_page,
    route="/motorbikes/[route_arg_motorbike_id]",
    on_load=AuthState.check_session,
)
app.add_page(sign_in, route="/sign-in")
app.add_page(sign_up, route="/sign-up")