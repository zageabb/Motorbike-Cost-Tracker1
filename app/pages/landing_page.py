import reflex as rx
from app.states.auth_state import AuthState


def landing_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Motorbike Cost Tracker - Welcome!",
                class_name="text-4xl font-bold text-center text-gray-800 mb-8",
            ),
            rx.el.button(
                "Sign Out",
                on_click=AuthState.sign_out,
                class_name="absolute top-4 right-4 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500",
            ),
            class_name="relative",
        ),
        rx.el.div(
            rx.el.h2(
                "Navigation",
                class_name="text-2xl font-semibold text-gray-700 mb-4",
            ),
            rx.el.ul(
                rx.el.li(
                    rx.link(
                        rx.el.div(
                            rx.icon(
                                "layout-dashboard",
                                class_name="mr-2 h-5 w-5",
                            ),
                            "Dashboard",
                            class_name="flex items-center text-lg text-indigo-600 hover:text-indigo-800",
                        ),
                        href="/dashboard",
                        class_name="p-4 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow block",
                    ),
                    class_name="mb-4",
                ),
                rx.el.li(
                    rx.link(
                        rx.el.div(
                            rx.icon(
                                "bike",
                                class_name="mr-2 h-5 w-5",
                            ),
                            "All Motorbikes",
                            class_name="flex items-center text-lg text-green-600 hover:text-green-800",
                        ),
                        href="/motorbikes",
                        class_name="p-4 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow block",
                    ),
                    class_name="mb-4",
                ),
                rx.el.li(
                    rx.link(
                        rx.el.div(
                            rx.icon(
                                "bar-chart-3",
                                class_name="mr-2 h-5 w-5",
                            ),
                            "Analytics",
                            class_name="flex items-center text-lg text-purple-600 hover:text-purple-800",
                        ),
                        href="/analytics",
                        class_name="p-4 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow block",
                    ),
                    class_name="mb-4",
                ),
                class_name="list-none p-0",
            ),
            class_name="max-w-md mx-auto",
        ),
        class_name="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8 font-sans flex flex-col items-center justify-center",
        on_mount=AuthState.check_session,
    )