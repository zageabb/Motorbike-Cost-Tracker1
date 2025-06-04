import reflex as rx
from app.states.analytics_state import (
    AnalyticsState,
    BikeAnalytics,
)
from app.states.auth_state import AuthState
from app.states.motorbike_state import MotorbikeState


def render_analytics_row(
    bike_data: BikeAnalytics,
) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            bike_data["name"],
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-900",
        ),
        rx.el.td(
            f"${bike_data['total_cost']:.2f}",
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-right",
        ),
        rx.el.td(
            f"${bike_data['tanya_cost']:.2f}",
            class_name="px-6 py-4 whitespace-nowrap text-sm text-blue-500 text-right",
        ),
        rx.el.td(
            f"${bike_data['gerald_cost']:.2f}",
            class_name="px-6 py-4 whitespace-nowrap text-sm text-green-500 text-right",
        ),
        rx.el.td(
            rx.cond(
                bike_data["profit"] != None,
                f"${bike_data['profit']:.2f}",
                "N/A",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-right",
        ),
        rx.el.td(
            rx.cond(
                bike_data["tanya_profit_share"] != None,
                f"${bike_data['tanya_profit_share']:.2f}",
                "N/A",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-blue-500 text-right",
        ),
        rx.el.td(
            rx.cond(
                bike_data["gerald_profit_share"] != None,
                f"${bike_data['gerald_profit_share']:.2f}",
                "N/A",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-green-500 text-right",
        ),
        rx.el.td(
            rx.cond(
                bike_data["is_sold"],
                rx.el.span(
                    "Yes",
                    class_name="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800",
                ),
                rx.el.span(
                    "No",
                    class_name="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800",
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center",
        ),
        class_name="bg-white even:bg-gray-50 hover:bg-gray-100",
    )


def analytics_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Business Analytics",
                    class_name="text-3xl font-bold text-gray-800 mb-6",
                ),
                rx.el.button(
                    "Sign Out",
                    on_click=AuthState.sign_out,
                    class_name="absolute top-4 right-4 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500",
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.link(
                    "Back to Landing Page",
                    href="/",
                    class_name="text-blue-600 hover:text-blue-800 mr-4",
                ),
                rx.link(
                    "Back to Dashboard",
                    href="/dashboard",
                    class_name="text-indigo-600 hover:text-indigo-800 mr-4",
                ),
                rx.link(
                    "View All Motorbikes",
                    href="/motorbikes",
                    class_name="text-indigo-600 hover:text-indigo-800",
                ),
                class_name="mb-6",
            ),
            rx.el.h2(
                "Overall Summary",
                class_name="text-2xl font-semibold text-gray-700 mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Filter by Sold Status:",
                    class_name="mr-2 font-medium text-gray-700",
                ),
                rx.el.select(
                    rx.el.option(
                        "Show All Bikes", value="all"
                    ),
                    rx.el.option(
                        "Show Sold Bikes Only", value="sold"
                    ),
                    rx.el.option(
                        "Show Unsold Bikes Only",
                        value="unsold",
                    ),
                    value=AnalyticsState.filter_sold_status,
                    on_change=AnalyticsState.set_filter_sold_status,
                    class_name="mb-6 p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500",
                ),
                class_name="mb-6 flex items-center",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Total Tanya's Investment:",
                        class_name="text-sm font-medium text-gray-500",
                    ),
                    rx.el.p(
                        f"${AnalyticsState.overall_summary['total_tanya_investment']:.2f}",
                        class_name="mt-1 text-xl font-semibold text-blue-600",
                    ),
                    class_name="bg-white shadow rounded-lg p-4",
                ),
                rx.el.div(
                    rx.el.p(
                        "Total Gerald's Investment:",
                        class_name="text-sm font-medium text-gray-500",
                    ),
                    rx.el.p(
                        f"${AnalyticsState.overall_summary['total_gerald_investment']:.2f}",
                        class_name="mt-1 text-xl font-semibold text-green-600",
                    ),
                    class_name="bg-white shadow rounded-lg p-4",
                ),
                rx.el.div(
                    rx.el.p(
                        "Total Tanya's Profit Share:",
                        class_name="text-sm font-medium text-gray-500",
                    ),
                    rx.el.p(
                        f"${AnalyticsState.overall_summary['total_tanya_profit_share']:.2f}",
                        class_name="mt-1 text-xl font-semibold text-blue-600",
                    ),
                    class_name="bg-white shadow rounded-lg p-4",
                ),
                rx.el.div(
                    rx.el.p(
                        "Total Gerald's Profit Share:",
                        class_name="text-sm font-medium text-gray-500",
                    ),
                    rx.el.p(
                        f"${AnalyticsState.overall_summary['total_gerald_profit_share']:.2f}",
                        class_name="mt-1 text-xl font-semibold text-green-600",
                    ),
                    class_name="bg-white shadow rounded-lg p-4",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8",
            ),
            rx.el.h2(
                "Bike Breakdown",
                class_name="text-2xl font-semibold text-gray-700 mb-4",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Bike Name",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Total Cost",
                                class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Tanya's Cost (Parts)",
                                class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Gerald's Cost (Parts)",
                                class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Profit",
                                class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Tanya's Share",
                                class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Gerald's Share",
                                class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Sold",
                                class_name="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            AnalyticsState.bike_analytics_data,
                            render_analytics_row,
                        ),
                        rx.cond(
                            AnalyticsState.bike_analytics_data.length()
                            == 0,
                            rx.el.tr(
                                rx.el.td(
                                    "No motorbike data available for the selected filter.",
                                    col_span=8,
                                    class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center",
                                )
                            ),
                            rx.fragment(),
                        ),
                    ),
                    class_name="min-w-full divide-y divide-gray-200 shadow border-b border-gray-200 sm:rounded-lg",
                ),
                class_name="overflow-x-auto",
            ),
        ),
        class_name="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8 min-h-screen bg-gray-100 py-8 font-sans",
        on_mount=[
            MotorbikeState.load_all_data,
            AnalyticsState.set_filter_sold_status("all"),
            AuthState.check_session,
        ],
    )