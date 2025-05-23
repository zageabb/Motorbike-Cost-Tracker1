import reflex as rx
from sqlmodel import SQLModel, Field, Relationship
from app.models import MotorbikeDB, PartDB


def create_db_and_tables():
    """Creates the database and all tables based on the defined models."""
    engine = rx.model.get_engine()
    SQLModel.metadata.create_all(engine)
    print("Database and tables created successfully.")


def populate_example_data():
    """Populates the database with some example entries."""
    with rx.session() as session:
        existing_bike_check = (
            session.query(MotorbikeDB)
            .filter(MotorbikeDB.name == "Honda CB750")
            .first()
        )
        if existing_bike_check:
            print(
                "Example data (Honda CB750) already exists. Skipping population."
            )
            return
        bike1 = MotorbikeDB(
            name="Honda CB750", initial_cost=2500.0
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
            name="Yamaha XS650", initial_cost=1800.0
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
        session.commit()
        print("Example data populated successfully.")


if __name__ == "__main__":
    print("Starting database setup...")
    create_db_and_tables()
    populate_example_data()
    print(
        "Database setup finished. You can now run your Reflex app."
    )