import reflex as rx
import uuid
from typing import List as PyList, TYPE_CHECKING
from sqlmodel import Field, Relationship


def generate_uuid_str() -> str:
    return str(uuid.uuid4())


class PartDB(rx.Model, table=True):
    __tablename__ = "partdb"
    id: str = Field(
        default_factory=generate_uuid_str,
        primary_key=True,
        index=True,
    )
    name: str
    source: str
    buyer: str
    cost: float
    motorbike_id: str = Field(foreign_key="motorbikedb.id")
    motorbike: "MotorbikeDB" = Relationship(
        back_populates="parts"
    )


class MotorbikeDB(rx.Model, table=True):
    __tablename__ = "motorbikedb"
    id: str = Field(
        default_factory=generate_uuid_str,
        primary_key=True,
        index=True,
    )
    name: str
    initial_cost: float
    parts: PyList["PartDB"] = Relationship(
        back_populates="motorbike",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan"
        },
    )