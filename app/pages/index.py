import reflex as rx


def index() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            "This page is deprecated. Please use the new landing page."
        ),
        rx.link("Go to Landing Page", href="/"),
    )