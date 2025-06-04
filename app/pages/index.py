import reflex as rx
from app.states.motorbike_state import MotorbikeState
from app.states.auth_state import AuthState
from app.components.motorbike_form import motorbike_form
from app.components.part_form import part_form
from app.components.motorbikes_display import (
    motorbikes_display,
)
from app.components.summary_display import summary_display


def index() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Motorbike Cost Tracker",
                    class_name="text-4xl font-bold text-center text-gray-800 mb-2",
                ),
                rx.el.button(
                    "Sign Out",
                    on_click=AuthState.sign_out,
                    class_name="absolute top-4 right-4 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500",
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.link(
                    "View All Motorbikes",
                    href="/motorbikes",
                    class_name="text-center block text-indigo-600 hover:text-indigo-800 mb-2",
                ),
                rx.link(
                    "View Analytics",
                    href="/analytics",
                    class_name="text-center block text-green-600 hover:text-green-800 mb-8",
                ),
            ),
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
        ),
        class_name="min-h-screen bg-gray-100 py-8 font-sans",
        on_mount=[
            MotorbikeState.load_all_data,
            AuthState.check_session,
        ],
    )