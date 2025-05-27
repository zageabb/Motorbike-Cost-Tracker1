import reflex as rx
from app.components.sign_in_card import sign_in_card


def sign_in() -> rx.Component:
    return rx.el.div(
        sign_in_card(),
        class_name="flex flex-col items-center justify-center h-screen bg-gray-100",
    )