import reflex as rx
from app.components.sign_up_card import sign_up_card


def sign_up() -> rx.Component:
    return rx.el.div(
        sign_up_card(),
        class_name="flex flex-col items-center justify-center h-screen bg-gray-100",
    )