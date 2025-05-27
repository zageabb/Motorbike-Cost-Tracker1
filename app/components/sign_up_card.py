import reflex as rx
from app.states.auth_state import AuthState


def sign_up_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Create an account",
                class_name="font-semibold tracking-tight text-xl",
            ),
            rx.el.p(
                "Enter your email below to create your account",
                class_name="text-sm text-gray-500 font-medium",
            ),
            class_name="flex flex-col",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Email",
                    class_name="text-sm font-medium leading-none",
                ),
                rx.el.input(
                    type="email",
                    placeholder="user@example.com",
                    name="email",
                    id="email",
                    required=True,
                    class_name="flex h-9 w-full rounded-md border bg-transparent px-3 py-1 text-base shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 md:text-sm font-medium",
                ),
                class_name="flex flex-col gap-1.5",
            ),
            rx.el.div(
                rx.el.label(
                    "Password",
                    class_name="text-sm font-medium leading-none",
                ),
                rx.el.input(
                    type="password",
                    name="password",
                    id="password",
                    required=True,
                    class_name="flex h-9 w-full rounded-md border bg-transparent px-3 py-1 text-base shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1 md:text-sm font-medium",
                ),
                class_name="flex flex-col gap-1.5",
            ),
            rx.el.button(
                "Create account",
                type="submit",
                class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors text-white shadow bg-blue-500 hover:bg-blue-600 h-9 px-4 py-2 w-full",
            ),
            rx.el.div(
                rx.el.span(
                    "Already have an account?",
                    class_name="text-sm text-gray-500 font-medium",
                ),
                rx.el.a(
                    "Sign in",
                    href="/sign-in",
                    class_name="text-sm text-blue-500 font-medium underline hover:text-blue-600 transition-colors",
                ),
                class_name="flex flex-row gap-2",
            ),
            class_name="flex flex-col gap-4",
            on_submit=AuthState.sign_up,
        ),
        class_name="font-sans p-6 rounded-xl bg-white flex flex-col gap-4 shadow-lg border border-gray-200 text-black min-w-[27rem]",
    )