import reflex as rx
from app.states.motorbike_state import MotorbikeState


def part_form(
    fixed_motorbike_id: rx.Var[str] | None = None,
    motorbike_name: rx.Var[str] | None = None,
) -> rx.Component:
    is_specific_mode_active = fixed_motorbike_id != None
    specific_header_content = rx.fragment(
        "Add Part to: ",
        rx.el.span(
            rx.cond(
                motorbike_name != None,
                motorbike_name,
                "Selected Motorbike",
            ),
            class_name="font-bold",
        ),
    )
    show_dropdown_cond = rx.cond(
        is_specific_mode_active, False, True
    )
    button_disabled_cond = rx.cond(
        show_dropdown_cond,
        MotorbikeState.part_form_selected_motorbike_id
        == "",
        False,
    )
    return rx.el.form(
        rx.el.div(
            rx.el.h3(
                rx.cond(
                    is_specific_mode_active,
                    specific_header_content,
                    "Add New Part (General)",
                ),
                class_name="text-lg font-medium leading-6 text-gray-900 mb-4",
            ),
            rx.cond(
                show_dropdown_cond,
                rx.el.div(
                    rx.el.label(
                        "Select Motorbike:",
                        html_for="part_motorbike_id",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.select(
                        rx.el.option(
                            "Select a motorbike...",
                            value="",
                            disabled=True,
                        ),
                        rx.foreach(
                            MotorbikeState.motorbikes_list,
                            lambda motorbike: rx.el.option(
                                motorbike["name"],
                                value=motorbike["id"],
                            ),
                        ),
                        name="motorbike_id",
                        id="part_motorbike_id",
                        value=MotorbikeState.part_form_selected_motorbike_id,
                        on_change=MotorbikeState.set_part_form_selected_motorbike_id,
                        class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                        disabled=MotorbikeState.motorbikes_list.length()
                        == 0,
                    ),
                    class_name="mb-4",
                ),
                None,
            ),
            rx.el.div(
                rx.el.label(
                    "Part Name:",
                    html_for="part_name",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    name="name",
                    id="part_name",
                    placeholder="Enter part name",
                    default_value=MotorbikeState.new_part_name,
                    key=MotorbikeState.new_part_name,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Part Source:",
                    html_for="part_source",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    name="source",
                    id="part_source",
                    placeholder="Enter part source",
                    default_value=MotorbikeState.new_part_source,
                    key=MotorbikeState.new_part_source,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Buyer:",
                    html_for="part_buyer",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.select(
                    rx.foreach(
                        MotorbikeState.buyers,
                        lambda buyer: rx.el.option(
                            buyer, value=buyer
                        ),
                    ),
                    name="buyer",
                    id="part_buyer",
                    value=MotorbikeState.new_part_buyer,
                    on_change=MotorbikeState.set_new_part_buyer,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Cost:",
                    html_for="part_cost",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    name="cost",
                    id="part_cost",
                    type="number",
                    placeholder="Enter cost (e.g., 25.99)",
                    step="0.01",
                    default_value=MotorbikeState.new_part_cost,
                    key=MotorbikeState.new_part_cost,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.button(
                "Add Part",
                type="submit",
                class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",
                disabled=button_disabled_cond,
            ),
            class_name="p-6 bg-gray-50 rounded-lg shadow",
        ),
        on_submit=lambda form_data: MotorbikeState.add_part(
            form_data, fixed_motorbike_id
        ),
        reset_on_submit=True,
    )