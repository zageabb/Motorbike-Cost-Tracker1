import reflex as rx
from app.states.motorbike_state import MotorbikeState
from app.components.motorbike_form import motorbike_form
from app.components.part_form import part_form
from app.components.motorbikes_display import motorbikes_display
from app.components.summary_display import summary_display
from app.components.layout import page_layout


def dashboard_page() -> rx.Component:
    content = rx.fragment(
        rx.el.div(
            rx.el.div(
                motorbike_form(),
                class_name="w-full md:w-1/2 md:pr-4 mb-8 md:mb-0",
            ),
            rx.el.div(
                part_form(),
                class_name="w-full md:w-1/2 md:pl-4",
            ),
            class_name="md:flex md:space-x-4 mb-8",
        ),
        rx.el.div(summary_display(), class_name="my-8"),
        rx.el.div(motorbikes_display()),
        class_name="max-w-5xl mx-auto p-4 sm:p-6 lg:p-8",
    )
    return page_layout(
        "Motorbike Cost Tracker Dashboard",
        content,
        on_mount=[MotorbikeState.load_all_data],
    )