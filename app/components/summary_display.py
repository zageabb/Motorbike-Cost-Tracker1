import reflex as rx
from app.states.motorbike_state import MotorbikeState


def summary_display() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Financial Summary",
            class_name="text-lg font-medium leading-6 text-gray-900 mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Total Costs (All Bikes):",
                    class_name="text-sm font-medium text-gray-500",
                ),
                rx.el.p(
                    f"${MotorbikeState.total_cost:.2f}",
                    class_name="mt-1 text-2xl font-semibold text-gray-900",
                ),
                class_name="bg-white shadow rounded-lg p-4",
            ),
            rx.el.div(
                rx.el.p(
                    "Projected Sale (Unsold Bikes x2):",
                    class_name="text-sm font-medium text-gray-500",
                ),
                rx.el.p(
                    f"${MotorbikeState.projected_sale:.2f}",
                    class_name="mt-1 text-2xl font-semibold text-orange-600",
                ),
                class_name="bg-white shadow rounded-lg p-4",
            ),
            rx.el.div(
                rx.el.p(
                    "Actual Profit (Sold Bikes):",
                    class_name="text-sm font-medium text-gray-500",
                ),
                rx.el.p(
                    f"${MotorbikeState.actual_profit:.2f}",
                    class_name=rx.cond(
                        MotorbikeState.actual_profit >= 0,
                        "mt-1 text-2xl font-semibold text-green-600",
                        "mt-1 text-2xl font-semibold text-red-600",
                    ),
                ),
                class_name="bg-white shadow rounded-lg p-4",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-4",
        ),
        class_name="mt-8 p-6 bg-gray-50 rounded-lg shadow",
    )