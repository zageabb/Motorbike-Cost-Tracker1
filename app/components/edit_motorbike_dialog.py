import reflex as rx
from app.states.motorbike_state import MotorbikeState


def edit_motorbike_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Edit Motorbike"),
            rx.dialog.description(
                "Modify the details of the motorbike.",
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Motorbike Name:",
                    html_for="edit_motorbike_name",
                ),
                rx.el.input(
                    id="edit_motorbike_name",
                    default_value=MotorbikeState.edit_motorbike_form_name,
                    on_change=MotorbikeState.set_edit_motorbike_form_name,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Initial Cost:",
                    html_for="edit_motorbike_initial_cost",
                ),
                rx.el.input(
                    id="edit_motorbike_initial_cost",
                    type="number",
                    step="0.01",
                    default_value=MotorbikeState.edit_motorbike_form_initial_cost,
                    on_change=MotorbikeState.set_edit_motorbike_form_initial_cost,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Tanya's Share:",
                    html_for="edit_motorbike_tanya_initial_cost",
                ),
                rx.el.input(
                    id="edit_motorbike_tanya_initial_cost",
                    type="number",
                    step="0.01",
                    default_value=MotorbikeState.edit_motorbike_form_tanya_initial_cost,
                    on_change=MotorbikeState.set_edit_motorbike_form_tanya_initial_cost,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Gerald's Share:",
                    html_for="edit_motorbike_gerald_initial_cost",
                ),
                rx.el.input(
                    id="edit_motorbike_gerald_initial_cost",
                    type="number",
                    step="0.01",
                    default_value=MotorbikeState.edit_motorbike_form_gerald_initial_cost,
                    on_change=MotorbikeState.set_edit_motorbike_form_gerald_initial_cost,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Bought By:",
                    html_for="edit_motorbike_buyer",
                ),
                rx.el.select(
                    rx.foreach(
                        MotorbikeState.buyers,
                        lambda buyer: rx.el.option(
                            buyer, value=buyer
                        ),
                    ),
                    id="edit_motorbike_buyer",
                    value=MotorbikeState.edit_motorbike_form_buyer,
                    on_change=MotorbikeState.set_edit_motorbike_form_buyer,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    rx.el.input(
                        type="checkbox",
                        checked=MotorbikeState.edit_motorbike_form_is_sold,
                        on_change=MotorbikeState.set_edit_motorbike_form_is_sold,
                        class_name="mr-2 leading-tight",
                    ),
                    rx.el.span("Mark as Sold"),
                    class_name="flex items-center text-sm font-medium text-gray-700",
                ),
                class_name="mb-4",
            ),
            rx.cond(
                MotorbikeState.edit_motorbike_form_is_sold,
                rx.el.div(
                    rx.el.label(
                        "Sold Value:",
                        html_for="edit_motorbike_sold_value",
                    ),
                    rx.el.input(
                        id="edit_motorbike_sold_value",
                        type="number",
                        step="0.01",
                        placeholder="Enter sold value (optional)",
                        default_value=MotorbikeState.edit_motorbike_form_sold_value,
                        on_change=MotorbikeState.set_edit_motorbike_form_sold_value,
                        class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                    ),
                    class_name="mb-4",
                ),
                rx.fragment(),
            ),
            rx.el.div(
                rx.el.label(
                    rx.el.input(
                        type="checkbox",
                        checked=MotorbikeState.edit_motorbike_form_ignore_from_calculations,
                        on_change=MotorbikeState.set_edit_motorbike_form_ignore_from_calculations,
                        class_name="mr-2 leading-tight",
                    ),
                    rx.el.span(
                        "Ignore from Dashboard Calculations"
                    ),
                    class_name="flex items-center text-sm font-medium text-gray-700",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=MotorbikeState.close_edit_motorbike_dialog,
                    class_name="mr-2 py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",
                ),
                rx.el.button(
                    "Save Changes",
                    on_click=MotorbikeState.save_edited_motorbike,
                    class_name="py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",
                ),
                class_name="flex justify-end mt-4",
            ),
        ),
        open=MotorbikeState.show_edit_motorbike_dialog,
        on_open_change=MotorbikeState.set_show_edit_motorbike_dialog,
    )