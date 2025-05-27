import reflex as rx
from app.states.motorbike_state import Motorbike


def motorbikes_list_item(
    motorbike: Motorbike,
) -> rx.Component:
    base_classes = "p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
    sold_classes = "bg-green-50 text-green-700 border-green-300 hover:shadow-lg"
    unsold_classes = "bg-white"
    return rx.el.div(
        rx.link(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        motorbike["name"],
                        class_name=rx.cond(
                            motorbike["is_sold"],
                            "text-lg font-semibold text-green-700 hover:text-green-900",
                            "text-lg font-semibold text-indigo-700 hover:text-indigo-900",
                        ),
                    ),
                    rx.cond(
                        motorbike["is_sold"],
                        rx.el.span(
                            "SOLD",
                            class_name="ml-2 px-2 py-0.5 bg-green-100 text-green-600 text-xs font-semibold rounded-full",
                        ),
                        rx.fragment(),
                    ),
                    rx.cond(
                        motorbike[
                            "ignore_from_calculations"
                        ],
                        rx.el.span(
                            "IGNORED",
                            class_name="ml-2 px-2 py-0.5 bg-yellow-100 text-yellow-600 text-xs font-semibold rounded-full",
                        ),
                        rx.fragment(),
                    ),
                    class_name="flex items-center mb-1",
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
                        rx.cond(
                            motorbike["sold_value"] != None,
                            rx.el.p(
                                f"Sold Value: ${motorbike['sold_value']:.2f}",
                                class_name="text-xs text-green-500 mt-1",
                            ),
                            rx.el.p(
                                "Sold Value: N/A",
                                class_name="text-xs text-green-400 mt-1",
                            ),
                        )
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