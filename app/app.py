import reflex as rx
from app.pages.index import index
from app.pages.motorbikes_page import motorbikes_page
from app.pages.motorbike_detail_page import (
    motorbike_detail_page,
)
from app.db_setup import (
    create_db_and_tables,
    populate_example_data,
)


def initialize_database_if_needed():
    """
    Ensures that the database tables are created and example data is populated.
    This function is called once when the application starts.
    """
    print("Attempting to initialize database and tables...")
    create_db_and_tables()
    populate_example_data()
    print("Database initialization attempt finished.")


initialize_database_if_needed()


def app_with_theme():
    return rx.App(theme=rx.theme(appearance="light"))


app = app_with_theme()
app.add_page(index, route="/")
app.add_page(motorbikes_page, route="/motorbikes")
app.add_page(
    motorbike_detail_page,
    route="/motorbikes/[route_arg_motorbike_id]",
)