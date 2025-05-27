import reflex as rx
import bcrypt
from sqlmodel import select
from app.models import UserDB


class AuthState(rx.State):
    in_session: bool = True
    current_user_email: str | None = None

    @rx.event
    def sign_up(self, form_data: dict):
        email = form_data.get("email", "").strip().lower()
        password = form_data.get("password", "")
        if not email or not password:
            yield rx.toast(
                "Email and password cannot be empty.",
                duration=3000,
            )
            return
        with rx.session() as session:
            existing_user = session.exec(
                select(UserDB).where(UserDB.email == email)
            ).first()
            if existing_user:
                yield rx.toast(
                    "Email already in use.", duration=3000
                )
                return
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            new_user = UserDB(
                email=email, password_hash=hashed_password
            )
            session.add(new_user)
            session.commit()
            self.in_session = True
            self.current_user_email = email
            return rx.redirect("/")

    @rx.event
    def sign_in(self, form_data: dict):
        email = form_data.get("email", "").strip().lower()
        password = form_data.get("password", "")
        if not email or not password:
            yield rx.toast(
                "Email and password cannot be empty.",
                duration=3000,
            )
            return
        with rx.session() as session:
            user = session.exec(
                select(UserDB).where(UserDB.email == email)
            ).first()
            if user and bcrypt.checkpw(
                password.encode("utf-8"),
                user.password_hash.encode("utf-8"),
            ):
                self.in_session = True
                self.current_user_email = user.email
                return rx.redirect("/")
            else:
                self.in_session = False
                self.current_user_email = None
                yield rx.toast(
                    "Invalid email or password.",
                    duration=3000,
                )

    @rx.event
    def sign_out(self):
        self.in_session = False
        self.current_user_email = None
        return rx.redirect("/sign-in")

    @rx.event
    def check_session(self):
        if not self.in_session:
            return rx.redirect("/sign-in")