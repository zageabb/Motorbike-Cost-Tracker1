import reflex as rx
from app.states.motorbike_state import MotorbikeState
from app.components.motorbikes_list_item import motorbikes_list_item
from app.components.edit_motorbike_dialog import edit_motorbike_dialog
from app.components.edit_part_dialog import edit_part_dialog
from app.components.layout import page_layout


def motorbikes_page() -> rx.Component:
    content = rx.fragment(
        edit_motorbike_dialog(),
        edit_part_dialog(),
        rx.cond(
            MotorbikeState.sorted_motorbikes_for_display.length() == 0,
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
    )
    return page_layout(
        "All Motorbikes",
        content,
        on_mount=[MotorbikeState.load_all_data],
    )