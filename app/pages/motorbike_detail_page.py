import reflex as rx
from app.states.motorbike_state import MotorbikeState, Part
from app.components.part_form import part_form
from app.components.edit_motorbike_dialog import (
    edit_motorbike_dialog,
)
from app.components.edit_part_dialog import edit_part_dialog


def render_detail_part_row(
    motorbike_id: rx.Var[str], part: rx.Var[Part]
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
            ),
            rx.el.button(
                "Delete",
                on_click=lambda: MotorbikeState.delete_part(
                    motorbike_id, part["id"]
                ),
                class_name="text-red-600 hover:text-red-900 ml-2 text-xs px-2 py-1 border border-red-300 rounded",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        class_name="bg-white even:bg-gray-50",
    )


def motorbike_detail_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    MotorbikeState.selected_motorbike_for_detail[
                        "name"
                    ],
                    class_name="text-2xl font-bold text-gray-800",
                ),
                rx.el.button(
                    "Edit Motorbike Details",
                    on_click=lambda: MotorbikeState.open_edit_motorbike_dialog(
                        MotorbikeState.selected_motorbike_for_detail[
                            "id"
                        ]
                    ),
                    class_name="ml-4 text-sm text-indigo-600 hover:text-indigo-800 px-3 py-1 border border-indigo-300 rounded",
                ),
            ),
            class_name="flex items-center justify-between mb-2",
        ),
        rx.el.p(
            f"Initial Cost: ${MotorbikeState.selected_motorbike_for_detail['initial_cost']:.2f}",
            class_name="text-gray-600 mb-4",
        ),
        rx.el.h3(
            "Parts",
            class_name="text-xl font-semibold text-gray-700 mt-6 mb-3",
        ),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Part Name",
                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Source",
                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Buyer",
                        class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Cost",
                        class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                    ),
                    rx.el.th(
                        "Actions",
                        class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                    ),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    MotorbikeState.selected_motorbike_for_detail[
                        "parts"
                    ],
                    lambda part: render_detail_part_row(
                        MotorbikeState.selected_motorbike_for_detail[
                            "id"
                        ],
                        part,
                    ),
                ),
                rx.cond(
                    MotorbikeState.selected_motorbike_for_detail[
                        "parts"
                    ].length()
                    == 0,
                    rx.el.tr(
                        rx.el.td(
                            "No parts added yet.",
                            col_span=5,
                            class_name="text-center py-4 text-gray-500",
                        )
                    ),
                    None,
                ),
                class_name="bg-white divide-y divide-gray-200",
            ),
            class_name="min-w-full divide-y divide-gray-200 shadow overflow-hidden border-b border-gray-200 sm:rounded-lg",
        ),
        rx.el.div(
            rx.el.p(
                "Total Parts Cost: ",
                rx.el.span(
                    f"${MotorbikeState.selected_motorbike_for_detail['total_parts_cost']:.2f}",
                    class_name="font-semibold",
                ),
                class_name="text-md font-medium text-gray-700 mt-4 text-right",
            ),
            rx.el.p(
                "Total Motorbike Cost: ",
                rx.el.span(
                    f"${MotorbikeState.selected_motorbike_for_detail['total_motorbike_cost']:.2f}",
                    class_name="font-bold text-lg",
                ),
                class_name="text-lg font-bold text-gray-800 mt-1 text-right",
            ),
            class_name="mt-4",
        ),
        rx.el.div(
            part_form(
                fixed_motorbike_id=MotorbikeState.selected_motorbike_for_detail[
                    "id"
                ],
                motorbike_name=MotorbikeState.selected_motorbike_for_detail[
                    "name"
                ],
            ),
            class_name="mt-8",
        ),
    )


def motorbike_detail_page() -> rx.Component:
    return rx.el.div(
        edit_motorbike_dialog(),
        edit_part_dialog(),
        rx.el.div(
            rx.el.h1(
                "Motorbike Details",
                class_name="text-3xl font-bold text-gray-800 mb-6",
            ),
            rx.el.div(
                rx.link(
                    "Back to All Motorbikes",
                    href="/motorbikes",
                    class_name="text-indigo-600 hover:text-indigo-800 mr-4",
                ),
                rx.link(
                    "Back to Dashboard",
                    href="/",
                    class_name="text-indigo-600 hover:text-indigo-800",
                ),
                class_name="mb-6",
            ),
            rx.cond(
                MotorbikeState.selected_motorbike_for_detail
                != None,
                motorbike_detail_content(),
                rx.el.p(
                    "Motorbike not found or ID not specified. Refreshing data...",
                    class_name="text-red-500",
                ),
            ),
        ),
        class_name="max-w-4xl mx-auto p-4 sm:p-6 lg:p-8 min-h-screen bg-gray-100 py-8",
        on_mount=MotorbikeState.load_motorbikes_from_db,
    )