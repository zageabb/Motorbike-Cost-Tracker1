import reflex as rx
from app.states.motorbike_state import (
    MotorbikeState,
    Part,
    Motorbike,
)
from app.components.edit_motorbike_dialog import (
    edit_motorbike_dialog,
)
from app.components.edit_part_dialog import edit_part_dialog


def render_part_row(
    motorbike_id: rx.Var[str],
    part: rx.Var[Part],
    is_motorbike_sold: rx.Var[bool],
) -> rx.Component:
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
            rx.el.strong(f"${part['cost']:.2f}"),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-right",
        ),
        rx.el.td(
            rx.el.button(
                "Edit",
                on_click=lambda: MotorbikeState.open_edit_part_dialog(
                    motorbike_id, part["id"]
                ),
                class_name="text-indigo-600 hover:text-indigo-900 text-xs px-2 py-1 border border-indigo-300 rounded",
                disabled=is_motorbike_sold,
            ),
            rx.el.button(
                "Delete",
                on_click=lambda: MotorbikeState.delete_part(
                    motorbike_id, part["id"]
                ),
                class_name="text-red-600 hover:text-red-900 ml-2 text-xs px-2 py-1 border border-red-300 rounded",
                disabled=is_motorbike_sold,
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="bg-white even:bg-gray-50",
    )


def motorbike_item_display(
    motorbike: Motorbike,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    motorbike["name"],
                    class_name="text-xl font-semibold text-gray-800",
                ),
                rx.cond(
                    motorbike["is_sold"],
                    rx.el.span(
                        "SOLD",
                        class_name="ml-3 px-2 py-0.5 bg-red-100 text-red-700 text-xs font-semibold rounded-full",
                    ),
                    rx.fragment(),
                ),
            ),
            rx.el.div(
                rx.el.button(
                    "Edit Motorbike",
                    on_click=lambda: MotorbikeState.open_edit_motorbike_dialog(
                        motorbike["id"]
                    ),
                    class_name="text-indigo-600 hover:text-indigo-900 text-sm px-3 py-1 border border-indigo-400 rounded mr-2",
                ),
                rx.el.button(
                    "Delete Motorbike",
                    on_click=lambda: MotorbikeState.delete_motorbike(
                        motorbike["id"]
                    ),
                    class_name="text-red-600 hover:text-red-900 text-sm px-3 py-1 border border-red-400 rounded",
                ),
            ),
            class_name="flex justify-between items-center",
        ),
        rx.el.p(
            f"Initial Cost: ${motorbike['initial_cost']:.2f}",
            class_name="text-sm text-gray-600 my-1",
        ),
        rx.cond(
            motorbike["is_sold"],
            rx.el.p(
                f"Sold Value: ${motorbike['sold_value']:.2f}",
                class_name="text-sm text-green-600 font-semibold my-1",
            ),
            rx.fragment(),
        ),
        rx.cond(
            motorbike["is_sold"],
            rx.el.p(
                f"Profit: ${(motorbike['sold_value'] if motorbike['sold_value'] is not None else 0) - motorbike['total_motorbike_cost']:.2f}",
                class_name="text-sm text-blue-600 font-semibold my-1",
            ),
            rx.fragment(),
        ),
        rx.el.div(
            rx.el.h4(
                "Parts",
                class_name="text-md font-medium text-gray-700 mt-3 mb-2",
            ),
            rx.cond(
                motorbike["is_sold"],
                rx.el.p(
                    "Parts list is final as this motorbike has been sold.",
                    class_name="text-xs text-orange-600 bg-orange-100 p-1 rounded-md mb-2",
                ),
                rx.fragment(),
            ),
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Part Name",
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
                        rx.el.th(
                            "Actions",
                            scope="col",
                            class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        motorbike["parts"],
                        lambda part: render_part_row(
                            motorbike["id"],
                            part,
                            motorbike["is_sold"],
                        ),
                    ),
                    rx.cond(
                        motorbike["parts"].length() == 0,
                        rx.el.tr(
                            rx.el.td(
                                "No parts added for this motorbike yet.",
                                col_span=5,
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center",
                            )
                        ),
                        None,
                    ),
                    class_name="bg-white divide-y divide-gray-200",
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="shadow overflow-hidden border-b border-gray-200 sm:rounded-lg mt-2",
        ),
        rx.el.div(
            rx.el.p(
                "Total Parts Cost: ",
                rx.el.span(
                    f"${motorbike['total_parts_cost']:.2f}",
                    class_name="font-semibold",
                ),
                class_name="text-sm font-medium text-gray-700 mt-2 text-right",
            ),
            rx.el.p(
                "Total Motorbike Cost (Initial + Parts): ",
                rx.el.span(
                    f"${motorbike['total_motorbike_cost']:.2f}",
                    class_name="font-semibold",
                ),
                class_name="text-md font-bold text-gray-800 mt-1 text-right",
            ),
            class_name="mt-4",
        ),
        class_name="mb-8 p-4 bg-white rounded-lg shadow-md",
    )