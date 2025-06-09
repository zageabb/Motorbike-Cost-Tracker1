import reflex as rx
from sqlmodel import SQLModel, Field, Relationship, select
from app.models import MotorbikeDB, PartDB, UserDB
import bcrypt


def create_db_and_tables():
    """Creates the database and all tables based on the defined models."""
    engine = rx.model.get_engine()
    SQLModel.metadata.create_all(engine)
    print("Database and tables created successfully.")


def populate_example_data():
    """Populates the database with some example entries."""
    with rx.session() as session:
        admin_email = "admin@reflex.com"
        existing_admin_user = session.exec(
            select(UserDB).where(
                UserDB.email == admin_email
            )
        ).first()
        if not existing_admin_user:
            hashed_password = bcrypt.hashpw(
                "password123".encode("utf-8"),
                bcrypt.gensalt(),
            ).decode("utf-8")
            admin_user = UserDB(
                email=admin_email,
                password_hash=hashed_password,
            )
            session.add(admin_user)
            print(f"Example user '{admin_email}' created.")
        else:
            print(
                f"Example user '{admin_email}' already exists. Skipping creation."
            )
        existing_bike_check = (
            session.query(MotorbikeDB)
            .filter(MotorbikeDB.name == "Honda CB750")
            .first()
        )
        if existing_bike_check:
            print(
                "Example motorbike data (Honda CB750) already exists. Skipping population."
            )
        else:
            bike1 = MotorbikeDB(
                name="Honda CB750",
                initial_cost=2500.0,
                tanya_initial_cost=1250.0,
                gerald_initial_cost=1250.0,
            )
            part1_1 = PartDB(
                name="Carburetor Kit",
                source="eBay",
                buyer="User1",
                cost=120.5,
                motorbike=bike1,
            )
            part1_2 = PartDB(
                name="New Tires",
                source="Local Shop",
                buyer="User2",
                cost=250.0,
                motorbike=bike1,
            )
            bike2 = MotorbikeDB(
                name="Yamaha XS650",
                initial_cost=1800.0,
                tanya_initial_cost=900.0,
                gerald_initial_cost=900.0,
            )
            part2_1 = PartDB(
                name="Brake Pads",
                source="Online Store",
                buyer="User1",
                cost=45.75,
                motorbike=bike2,
            )
            part2_2 = PartDB(
                name="Chain and Sprocket Set",
                source="RevZilla",
                buyer="User1",
                cost=150.0,
                motorbike=bike2,
            )
            session.add_all(
                [
                    bike1,
                    bike2,
                    part1_1,
                    part1_2,
                    part2_1,
                    part2_2,
                ]
            )
            print(
                "Example motorbike and part data populated."
            )
        session.commit()
        print("Example data population process finished.")


if __name__ == "__main__":
    print("Starting database setup...")
    create_db_and_tables()
    populate_example_data()
    print(
        "Database setup finished. You can now run your Reflex app."
    )