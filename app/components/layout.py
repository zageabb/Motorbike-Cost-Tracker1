import reflex as rx
from app.states.auth_state import AuthState


def page_layout(page_title: str, content: rx.Component, **props) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                page_title,
                class_name="text-3xl font-bold",
            ),
            rx.el.div(
                rx.el.button(
                    "Sign Out",
                    on_click=AuthState.sign_out,
                    class_name="mr-4 py-1 px-3 rounded-md text-sm text-white bg-red-600 hover:bg-red-700",
                ),
                rx.image(
                    src="/favicon.ico",
                    alt="Company Logo",
                    class_name="h-10 w-10",
                ),
                class_name="flex items-center ml-auto",
            ),
            class_name="flex items-center justify-between px-4 py-2 bg-gray-200",
        ),
        rx.el.nav(
            rx.hstack(
                rx.link(
                    "All Motorbikes",
                    href="/",
                    class_name="px-3 py-2 text-blue-600 hover:text-blue-800",
                ),
                rx.link(
                    "Dashboard",
                    href="/dashboard",
                    class_name="px-3 py-2 text-indigo-600 hover:text-indigo-800",
                ),
                rx.link(
                    "Analytics",
                    href="/analytics",
                    class_name="px-3 py-2 text-purple-600 hover:text-purple-800",
                ),
                class_name="space-x-4",
            ),
            class_name="bg-gray-300 px-4 py-2",
        ),
        rx.el.div(
            content,
            class_name="p-4",
        ),
        class_name="min-h-screen bg-gray-100 font-sans",
        **props,
    )
