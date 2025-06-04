import reflex as rx
from app.states.motorbike_state import MotorbikeState
from app.states.auth_state import AuthState
from app.components.motorbikes_list_item import (
    motorbikes_list_item,
)
from app.components.edit_motorbike_dialog import (
    edit_motorbike_dialog,
)
from app.components.edit_part_dialog import edit_part_dialog


def motorbikes_page() -> rx.Component:
    return rx.el.div(
        edit_motorbike_dialog(),
        edit_part_dialog(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "All Motorbikes",
                    class_name="text-3xl font-bold text-gray-800 mb-6",
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
                    "Back to Landing Page",
                    href="/",
                    class_name="text-blue-600 hover:text-blue-800 mr-4",
                ),
                rx.link(
                    "Back to Dashboard",
                    href="/dashboard",
                    class_name="text-indigo-600 hover:text-indigo-800",
                ),
                class_name="mb-6",
            ),
            rx.cond(
                MotorbikeState.sorted_motorbikes_for_display.length()
                == 0,
                rx.el.p(
                    "No motorbikes have been added yet. Go to the dashboard to add one.",
                    class_name="text-gray-600 text-center py-10",
                ),
                rx.el.div(
                    rx.foreach(
                        MotorbikeState.sorted_motorbikes_for_display,
                        motorbikes_list_item,
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
            ),
        ),
        class_name="max-w-6xl mx-auto p-4 sm:p-6 lg:p-8 min-h-screen bg-gray-100 py-8 font-sans",
        on_mount=[
            MotorbikeState.load_all_data,
            AuthState.check_session,
        ],
    )