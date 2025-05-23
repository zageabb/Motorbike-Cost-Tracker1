import reflex as rx
from app.states.motorbike_state import Motorbike


def motorbikes_list_item(
    motorbike: Motorbike,
) -> rx.Component:
    return rx.el.div(
        rx.link(
            rx.el.div(
                rx.el.h3(
                    motorbike["name"],
                    class_name="text-lg font-semibold text-indigo-700 hover:text-indigo-900",
                ),
                rx.el.p(
                    f"Initial Cost: ${motorbike['initial_cost']:.2f}",
                    class_name="text-sm text-gray-600",
                ),
                rx.el.p(
                    f"Total Cost: ${motorbike['total_motorbike_cost']:.2f}",
                    class_name="text-sm text-gray-700 font-medium",
                ),
                rx.el.p(
                    f"{motorbike['parts'].length()} parts",
                    class_name="text-xs text-gray-500 mt-1",
                ),
                class_name="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow",
            ),
            href=f"/motorbikes/{motorbike['id']}",
        ),
        class_name="mb-4",
    )