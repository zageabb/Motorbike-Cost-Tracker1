import reflex as rx
from app.states.motorbike_state import MotorbikeState, Part
from app.components.part_form import part_form
from app.components.edit_motorbike_dialog import edit_motorbike_dialog
from app.components.edit_part_dialog import edit_part_dialog
from app.components.layout import page_layout


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
                disabled=MotorbikeState.selected_motorbike_for_detail[
                    "is_sold"
                ],
            ),
            rx.el.button(
                "Delete",
                on_click=lambda: MotorbikeState.delete_part(
                    motorbike_id, part["id"]
                ),
                class_name="text-red-600 hover:text-red-900 ml-2 text-xs px-2 py-1 border border-red-300 rounded",
                disabled=MotorbikeState.selected_motorbike_for_detail[
                    "is_sold"
                ],
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
                rx.cond(
                    MotorbikeState.selected_motorbike_for_detail[
                        "is_sold"
                    ],
                    rx.el.span(
                        "SOLD",
                        class_name="ml-4 px-3 py-1 bg-green-100 text-green-700 text-sm font-semibold rounded-full",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    MotorbikeState.selected_motorbike_for_detail[
                        "ignore_from_calculations"
                    ],
                    rx.el.span(
                        "IGNORED IN CALCS",
                        class_name="ml-4 px-3 py-1 bg-yellow-100 text-yellow-700 text-sm font-semibold rounded-full",
                    ),
                    rx.fragment(),
                ),
                class_name="flex items-center",
            ),
            rx.el.button(
                "Edit Motorbike Details",
                on_click=lambda: MotorbikeState.open_edit_motorbike_dialog(
                    MotorbikeState.selected_motorbike_for_detail[
                        "id"
                    ]
                ),
                class_name="ml-auto text-sm text-indigo-600 hover:text-indigo-800 px-3 py-1 border border-indigo-300 rounded",
            ),
            class_name="flex items-center justify-between mb-2",
        ),
        rx.el.p(
            f"Initial Cost: ${MotorbikeState.selected_motorbike_for_detail['initial_cost']:.2f}",
            class_name="text-gray-600 mb-1",
        ),
        rx.cond(
            MotorbikeState.selected_motorbike_for_detail[
                "bike_buyer"
            ]
            != None,
            rx.el.p(
                "Bought by: ",
                rx.el.span(
                    MotorbikeState.selected_motorbike_for_detail[
                        "bike_buyer"
                    ],
                    class_name="font-semibold",
                ),
                class_name="text-gray-600 mb-1",
            ),
            rx.fragment(),
        ),
        rx.cond(
            MotorbikeState.selected_motorbike_for_detail[
                "is_sold"
            ],
            rx.el.p(
                f"Sold Value: ${MotorbikeState.selected_motorbike_for_detail['sold_value']:.2f}",
                class_name="text-green-600 font-semibold mb-1",
            ),
            rx.fragment(),
        ),
        rx.cond(
            MotorbikeState.selected_motorbike_for_detail[
                "is_sold"
            ],
            rx.el.p(
                f"Profit: ${rx.cond(MotorbikeState.selected_motorbike_for_detail['sold_value'] != None, MotorbikeState.selected_motorbike_for_detail['sold_value'], 0) - MotorbikeState.selected_motorbike_for_detail['total_motorbike_cost']:.2f}",
                class_name="text-blue-600 font-semibold mb-4",
            ),
            rx.fragment(),
        ),
        rx.el.h3(
            "Parts",
            class_name="text-xl font-semibold text-gray-700 mt-6 mb-3",
        ),
        rx.cond(
            MotorbikeState.selected_motorbike_for_detail[
                "is_sold"
            ],
            rx.el.p(
                "Parts list is final as this motorbike has been sold.",
                class_name="text-sm text-orange-600 bg-orange-100 p-2 rounded-md mb-3",
            ),
            rx.fragment(),
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
                "Tanya's Parts Cost: ",
                rx.el.span(
                    f"${MotorbikeState.selected_motorbike_for_detail['tanya_parts_cost']:.2f}",
                    class_name="font-semibold text-blue-600",
                ),
                class_name="text-sm font-medium text-gray-700 mt-1 text-right",
            ),
            rx.el.p(
                "Gerald's Parts Cost: ",
                rx.el.span(
                    f"${MotorbikeState.selected_motorbike_for_detail['gerald_parts_cost']:.2f}",
                    class_name="font-semibold text-green-600",
                ),
                class_name="text-sm font-medium text-gray-700 mt-1 text-right",
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
        rx.cond(
            MotorbikeState.selected_motorbike_for_detail[
                "is_sold"
            ],
            rx.fragment(),
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
        ),
    )


def motorbike_detail_page() -> rx.Component:
    content = rx.fragment(
        edit_motorbike_dialog(),
        edit_part_dialog(),
        rx.cond(
            MotorbikeState.selected_motorbike_for_detail != None,
            motorbike_detail_content(),
            rx.el.p(
                "Loading motorbike details or motorbike not found...",
                class_name="text-gray-500",
            ),
        ),
        class_name="max-w-4xl mx-auto p-4 sm:p-6 lg:p-8",
    )
    return page_layout(
        "Motorbike Details",
        content,
        on_mount=[MotorbikeState.load_all_data],
    )