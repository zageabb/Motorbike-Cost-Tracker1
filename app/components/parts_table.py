import reflex as rx
from app.states.motorbike_state import MotorbikeState, Part


def render_part_row(part: Part) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            part["name"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-900",
        ),
        rx.el.td(
            part["source"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            part["buyer"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
        rx.el.td(
            f"${part['cost']:.2f}",
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-right",
        ),
        class_name="bg-white even:bg-gray-50",
    )


def parts_table() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "All Parts (Legacy View - Not Grouped)",
            class_name="text-lg font-medium leading-6 text-gray-900 mb-4",
        ),
        rx.el.p(
            "This view shows all parts across all motorbikes. The main display now groups parts by motorbike.",
            class_name="text-sm text-gray-600 mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Name",
                            scope="col",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Source",
                            scope="col",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Buyer",
                            scope="col",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Cost",
                            scope="col",
                            class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                    )
                ),
                rx.el.tbody(
                    rx.el.tr(
                        rx.el.td(
                            "Legacy view needs update to show all parts.",
                            col_span=4,
                            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center",
                        )
                    ),
                    class_name="bg-white divide-y divide-gray-200",
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg",
        ),
        class_name="mt-8",
    )