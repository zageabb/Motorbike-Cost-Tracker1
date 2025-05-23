import reflex as rx
from app.states.motorbike_state import MotorbikeState


def motorbike_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.h3(
                "Add New Motorbike",
                class_name="text-lg font-medium leading-6 text-gray-900 mb-4",
            ),
            rx.el.label(
                "Motorbike Name:",
                html_for="motorbike_name",
                class_name="block text-sm font-medium text-gray-700",
            ),
            rx.el.input(
                name="name",
                id="motorbike_name",
                placeholder="Enter motorbike name (e.g., Honda CB500)",
                default_value=MotorbikeState.new_motorbike_name,
                key=MotorbikeState.new_motorbike_name,
                class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Initial Cost:",
                html_for="motorbike_initial_cost",
                class_name="block text-sm font-medium text-gray-700",
            ),
            rx.el.input(
                name="initial_cost",
                id="motorbike_initial_cost",
                type="number",
                placeholder="Enter initial cost (e.g., 1500.00)",
                step="0.01",
                default_value=MotorbikeState.new_motorbike_initial_cost,
                key=MotorbikeState.new_motorbike_initial_cost,
                class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            ),
            class_name="mb-4",
        ),
        rx.el.button(
            "Add Motorbike",
            type="submit",
            class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500",
        ),
        on_submit=MotorbikeState.add_motorbike,
        reset_on_submit=True,
        class_name="p-6 bg-gray-50 rounded-lg shadow",
    )