
import reflex as rx


class AuthState(rx.State):
    users: dict = {"admin@reflex.com": "password123"}
    in_session: bool = True

    @rx.event
    def sign_up(self, form_data: dict):
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "")
        if not email or not password:
            yield rx.toast(
                "Email and password cannot be empty.",
                duration=3000,
            )
            return
        if email in self.users:
            yield rx.toast(
                "Email already in use.", duration=3000
            )
        else:
            self.users[email] = password
            self.in_session = True
            return rx.redirect("/")

    @rx.event
    def sign_in(self, form_data: dict):
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "")
        if not email or not password:
            yield rx.toast(
                "Email and password cannot be empty.",
                duration=3000,
            )
            return
        if (
            email in self.users
            and self.users[email] == password
        ):
            self.in_session = True
            return rx.redirect("/")
        else:
            self.in_session = False
            yield rx.toast(
                "Invalid email or password.", duration=3000
            )

    @rx.event
    def sign_out(self):
        self.in_session = False
        return rx.redirect("/sign-in")

    @rx.event
    def check_session(self):
        if not self.in_session:
            return rx.redirect("/sign-in")