import reflex as rx
from app.states.motorbike_state import Motorbike


def motorbikes_list_item(
    motorbike: Motorbike,
) -> rx.Component:
    base_classes = "p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
    sold_classes = "bg-red-50 text-red-700 border-red-300 hover:shadow-lg"
    unsold_classes = "bg-white"
    return rx.el.div(
        rx.link(
            rx.el.div(
                rx.el.h3(
                    motorbike["name"],
                    class_name=rx.cond(
                        motorbike["is_sold"],
                        "text-lg font-semibold text-red-700 hover:text-red-900",
                        "text-lg font-semibold text-indigo-700 hover:text-indigo-900",
                    ),
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
                rx.cond(
                    motorbike["is_sold"],
                    rx.el.div(
                        rx.el.p(
                            "SOLD",
                            class_name="text-sm font-bold text-red-600 mt-1",
                        ),
                        rx.cond(
                            motorbike["sold_value"] != None,
                            rx.el.p(
                                f"Sold Value: ${motorbike['sold_value']:.2f}",
                                class_name="text-xs text-red-500",
                            ),
                            rx.el.p(
                                "Sold Value: N/A",
                                class_name="text-xs text-red-400",
                            ),
                        ),
                    ),
                    rx.fragment(),
                ),
            ),
            href=f"/motorbikes/{motorbike['id']}",
        ),
        class_name=rx.cond(
            motorbike["is_sold"],
            f"{base_classes} {sold_classes}",
            f"{base_classes} {unsold_classes}",
        ),
    )