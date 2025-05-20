import reflex as rx
from app.states.motorbike_state import MotorbikeState


def edit_part_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Edit Part"),
            rx.dialog.description(
                "Modify the details of the part.",
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Part Name:", html_for="edit_part_name"
                ),
                rx.el.input(
                    id="edit_part_name",
                    default_value=MotorbikeState.edit_part_form_name,
                    on_change=MotorbikeState.set_edit_part_form_name,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Part Source:",
                    html_for="edit_part_source",
                ),
                rx.el.input(
                    id="edit_part_source",
                    default_value=MotorbikeState.edit_part_form_source,
                    on_change=MotorbikeState.set_edit_part_form_source,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Buyer:", html_for="edit_part_buyer"
                ),
                rx.el.select(
                    rx.foreach(
                        MotorbikeState.buyers,
                        lambda buyer: rx.el.option(
                            buyer, value=buyer
                        ),
                    ),
                    id="edit_part_buyer",
                    value=MotorbikeState.edit_part_form_buyer,
                    on_change=MotorbikeState.set_edit_part_form_buyer,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Cost:", html_for="edit_part_cost"
                ),
                rx.el.input(
                    id="edit_part_cost",
                    type="number",
                    step="0.01",
                    default_value=MotorbikeState.edit_part_form_cost,
                    on_change=MotorbikeState.set_edit_part_form_cost,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=MotorbikeState.close_edit_part_dialog,
                    class_name="mr-2 py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",
                ),
                rx.el.button(
                    "Save Changes",
                    on_click=MotorbikeState.save_edited_part,
                    class_name="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",
                ),
                class_name="flex justify-end mt-4",
            ),
        ),
        open=MotorbikeState.show_edit_part_dialog,
        on_open_change=MotorbikeState.set_show_edit_part_dialog,
    )