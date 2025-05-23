import reflex as rx
from app.states.motorbike_state import MotorbikeState
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
            rx.el.h1(
                "All Motorbikes",
                class_name="text-3xl font-bold text-gray-800 mb-6",
            ),
            rx.link(
                "Back to Dashboard",
                href="/",
                class_name="text-indigo-600 hover:text-indigo-800 mb-6 block",
            ),
            rx.cond(
                MotorbikeState.motorbikes_list.length()
                == 0,
                rx.el.p(
                    "No motorbikes added yet. Go to the dashboard to add one.",
                    class_name="text-gray-600",
                ),
                rx.el.div(
                    rx.foreach(
                        MotorbikeState.motorbikes_list,
                        motorbikes_list_item,
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
            ),
        ),
        class_name="max-w-6xl mx-auto p-4 sm:p-6 lg:p-8 min-h-screen bg-gray-100 py-8",
        on_mount=MotorbikeState.load_motorbikes_from_db,
    )