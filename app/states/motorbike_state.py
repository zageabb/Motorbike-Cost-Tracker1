import reflex as rx
from typing import TypedDict, List as PyList, cast
import uuid
from sqlmodel import select
from app.models import MotorbikeDB, PartDB


class Part(TypedDict):
    id: str
    name: str
    source: str
    buyer: str
    cost: float


class Motorbike(TypedDict):
    id: str
    name: str
    initial_cost: float
    parts: PyList[Part]
    total_parts_cost: float
    total_motorbike_cost: float


class MotorbikeState(rx.State):
    motorbikes_list: PyList[Motorbike] = []
    buyers: PyList[str] = ["Tanya", "Gerald"]
    new_motorbike_name: str = ""
    new_motorbike_initial_cost: str = ""
    part_form_selected_motorbike_id: str = ""
    new_part_name: str = ""
    new_part_source: str = ""
    new_part_buyer: str = "Tanya"
    new_part_cost: str = ""
    show_edit_motorbike_dialog: bool = False
    editing_motorbike_id: str | None = None
    edit_motorbike_form_name: str = ""
    edit_motorbike_form_initial_cost: str = ""
    show_edit_part_dialog: bool = False
    editing_part_motorbike_id: str | None = None
    editing_part_id: str | None = None
    edit_part_form_name: str = ""
    edit_part_form_source: str = ""
    edit_part_form_buyer: str = "User1"
    edit_part_form_cost: str = ""

    @rx.event
    def load_motorbikes_from_db(self):
        loaded_motorbikes: PyList[Motorbike] = []
        with rx.session() as session:
            db_motorbikes = session.exec(
                select(MotorbikeDB)
            ).all()
            for db_bike in db_motorbikes:
                parts_list: PyList[Part] = []
                total_parts_cost = 0.0
                bike_parts = session.exec(
                    select(PartDB).where(
                        PartDB.motorbike_id == db_bike.id
                    )
                ).all()
                for db_part in bike_parts:
                    part_typed_dict: Part = {
                        "id": db_part.id,
                        "name": db_part.name,
                        "source": db_part.source,
                        "buyer": db_part.buyer,
                        "cost": db_part.cost,
                    }
                    parts_list.append(part_typed_dict)
                    total_parts_cost += db_part.cost
                total_motorbike_cost = (
                    db_bike.initial_cost + total_parts_cost
                )
                motorbike_typed_dict: Motorbike = {
                    "id": db_bike.id,
                    "name": db_bike.name,
                    "initial_cost": db_bike.initial_cost,
                    "parts": parts_list,
                    "total_parts_cost": total_parts_cost,
                    "total_motorbike_cost": total_motorbike_cost,
                }
                loaded_motorbikes.append(
                    motorbike_typed_dict
                )
        self.motorbikes_list = loaded_motorbikes

    @rx.var
    def total_cost(self) -> float:
        return sum(
            (
                bike["total_motorbike_cost"]
                for bike in self.motorbikes_list
            )
        )

    @rx.var
    def projected_sale(self) -> float:
        return self.total_cost * 2

    @rx.var
    def has_motorbikes(self) -> bool:
        return len(self.motorbikes_list) > 0

    @rx.var
    def selected_motorbike_for_detail(
        self,
    ) -> Motorbike | None:
        motorbike_id_from_url = self.router.page.params.get(
            "route_arg_motorbike_id", ""
        )
        if not motorbike_id_from_url:
            return None
        for bike in self.motorbikes_list:
            if bike["id"] == motorbike_id_from_url:
                return bike
        return None

    @rx.event
    def add_motorbike(self, form_data: dict):
        name = form_data.get("name", "").strip()
        initial_cost_str = form_data.get("initial_cost", "")
        if not name:
            return rx.toast(
                "Motorbike name cannot be empty.",
                duration=3000,
            )
        if not initial_cost_str:
            return rx.toast(
                "Initial cost cannot be empty.",
                duration=3000,
            )
        try:
            initial_cost = float(initial_cost_str)
            if initial_cost < 0:
                return rx.toast(
                    "Initial cost cannot be negative.",
                    duration=3000,
                )
        except ValueError:
            return rx.toast(
                "Invalid initial cost format.",
                duration=3000,
            )
        with rx.session() as session:
            new_db_motorbike = MotorbikeDB(
                name=name, initial_cost=initial_cost
            )
            session.add(new_db_motorbike)
            session.commit()
            new_id = new_db_motorbike.id
        self.new_motorbike_name = ""
        self.new_motorbike_initial_cost = ""
        if (
            len(self.motorbikes_list) == 0
            and new_id
            and (not self.part_form_selected_motorbike_id)
        ):
            self.part_form_selected_motorbike_id = new_id
        yield MotorbikeState.load_motorbikes_from_db
        yield rx.toast(
            f"Motorbike '{name}' added.", duration=3000
        )

    @rx.event
    def add_part(
        self,
        form_data: dict,
        specific_motorbike_id: str | None = None,
    ):
        motorbike_id_to_use = (
            specific_motorbike_id
            if specific_motorbike_id
            else form_data.get("motorbike_id")
        )
        if not motorbike_id_to_use:
            return rx.toast(
                "Please select or specify a motorbike.",
                duration=3000,
            )
        part_name = form_data.get("name", "").strip()
        cost_str = form_data.get("cost", "")
        if not part_name:
            return rx.toast(
                "Part name cannot be empty.", duration=3000
            )
        if not cost_str:
            return rx.toast(
                "Part cost cannot be empty.", duration=3000
            )
        try:
            cost = float(cost_str)
            if cost < 0:
                return rx.toast(
                    "Part cost cannot be negative.",
                    duration=3000,
                )
        except ValueError:
            return rx.toast(
                "Invalid part cost format.", duration=3000
            )
        with rx.session() as session:
            db_motorbike = session.exec(
                select(MotorbikeDB).where(
                    MotorbikeDB.id == motorbike_id_to_use
                )
            ).first()
            if not db_motorbike:
                return rx.toast(
                    f"Motorbike with ID {motorbike_id_to_use} not found.",
                    duration=3000,
                )
            new_db_part = PartDB(
                name=part_name,
                source=form_data.get("source", ""),
                buyer=form_data.get(
                    "buyer",
                    self.buyers[0] if self.buyers else "",
                ),
                cost=cost,
                motorbike_id=db_motorbike.id,
            )
            session.add(new_db_part)
            session.commit()
            motorbike_name_for_toast = db_motorbike.name
        self.new_part_name = ""
        self.new_part_source = ""
        self.new_part_buyer = (
            self.buyers[0] if self.buyers else ""
        )
        self.new_part_cost = ""
        yield MotorbikeState.load_motorbikes_from_db
        yield rx.toast(
            f"Part '{part_name}' added to {motorbike_name_for_toast}.",
            duration=3000,
        )

    @rx.event
    def set_part_form_selected_motorbike_id(
        self, motorbike_id: str
    ):
        self.part_form_selected_motorbike_id = motorbike_id

    @rx.event
    def set_new_part_buyer(self, buyer: str):
        self.new_part_buyer = buyer

    @rx.event
    def open_edit_motorbike_dialog(self, motorbike_id: str):
        bike_to_edit = next(
            (
                bike
                for bike in self.motorbikes_list
                if bike["id"] == motorbike_id
            ),
            None,
        )
        if bike_to_edit:
            self.editing_motorbike_id = bike_to_edit["id"]
            self.edit_motorbike_form_name = bike_to_edit[
                "name"
            ]
            self.edit_motorbike_form_initial_cost = str(
                bike_to_edit["initial_cost"]
            )
            self.show_edit_motorbike_dialog = True
        else:
            return rx.toast(
                "Motorbike not found for editing.",
                duration=3000,
            )

    @rx.event
    def save_edited_motorbike(self):
        if self.editing_motorbike_id is None:
            return rx.toast(
                "No motorbike selected for editing.",
                duration=3000,
            )
        name = self.edit_motorbike_form_name.strip()
        initial_cost_str = (
            self.edit_motorbike_form_initial_cost
        )
        if not name:
            return rx.toast(
                "Motorbike name cannot be empty.",
                duration=3000,
            )
        if not initial_cost_str:
            return rx.toast(
                "Initial cost cannot be empty.",
                duration=3000,
            )
        try:
            initial_cost = float(initial_cost_str)
            if initial_cost < 0:
                return rx.toast(
                    "Initial cost cannot be negative.",
                    duration=3000,
                )
        except ValueError:
            return rx.toast(
                "Invalid initial cost format.",
                duration=3000,
            )
        with rx.session() as session:
            db_motorbike = session.get(
                MotorbikeDB, self.editing_motorbike_id
            )
            if db_motorbike:
                db_motorbike.name = name
                db_motorbike.initial_cost = initial_cost
                session.add(db_motorbike)
                session.commit()
            else:
                return rx.toast(
                    "Failed to find motorbike to update.",
                    duration=3000,
                )
        self.close_edit_motorbike_dialog()
        yield MotorbikeState.load_motorbikes_from_db
        yield rx.toast(
            "Motorbike updated successfully.", duration=3000
        )

    @rx.event
    def close_edit_motorbike_dialog(self):
        self.show_edit_motorbike_dialog = False
        self.editing_motorbike_id = None
        self.edit_motorbike_form_name = ""
        self.edit_motorbike_form_initial_cost = ""

    @rx.event
    def delete_motorbike(self, motorbike_id: str):
        with rx.session() as session:
            db_motorbike = session.get(
                MotorbikeDB, motorbike_id
            )
            if db_motorbike:
                session.delete(db_motorbike)
                session.commit()
                if (
                    self.part_form_selected_motorbike_id
                    == motorbike_id
                ):
                    self.part_form_selected_motorbike_id = (
                        ""
                    )
            else:
                return rx.toast(
                    "Motorbike not found for deletion.",
                    duration=3000,
                )
        yield MotorbikeState.load_motorbikes_from_db
        yield rx.toast("Motorbike deleted.", duration=3000)

    @rx.event
    def open_edit_part_dialog(
        self, motorbike_id: str, part_id: str
    ):
        current_motorbike = next(
            (
                bike
                for bike in self.motorbikes_list
                if bike["id"] == motorbike_id
            ),
            None,
        )
        if current_motorbike:
            part_to_edit = next(
                (
                    p
                    for p in current_motorbike["parts"]
                    if p["id"] == part_id
                ),
                None,
            )
            if part_to_edit:
                self.editing_part_motorbike_id = (
                    motorbike_id
                )
                self.editing_part_id = part_id
                self.edit_part_form_name = part_to_edit[
                    "name"
                ]
                self.edit_part_form_source = part_to_edit[
                    "source"
                ]
                self.edit_part_form_buyer = part_to_edit[
                    "buyer"
                ]
                self.edit_part_form_cost = str(
                    part_to_edit["cost"]
                )
                self.show_edit_part_dialog = True
                return
        return rx.toast(
            "Part not found for editing.", duration=3000
        )

    @rx.event
    def save_edited_part(self):
        if not self.editing_part_id:
            return rx.toast(
                "No part selected for editing.",
                duration=3000,
            )
        part_name = self.edit_part_form_name.strip()
        cost_str = self.edit_part_form_cost
        if not part_name:
            return rx.toast(
                "Part name cannot be empty.", duration=3000
            )
        if not cost_str:
            return rx.toast(
                "Part cost cannot be empty.", duration=3000
            )
        try:
            cost = float(cost_str)
            if cost < 0:
                return rx.toast(
                    "Part cost cannot be negative.",
                    duration=3000,
                )
        except ValueError:
            return rx.toast(
                "Invalid part cost format.", duration=3000
            )
        with rx.session() as session:
            db_part = session.get(
                PartDB, self.editing_part_id
            )
            if db_part:
                db_part.name = part_name
                db_part.source = self.edit_part_form_source
                db_part.buyer = self.edit_part_form_buyer
                db_part.cost = cost
                session.add(db_part)
                session.commit()
            else:
                return rx.toast(
                    "Failed to find part to update.",
                    duration=3000,
                )
        self.close_edit_part_dialog()
        yield MotorbikeState.load_motorbikes_from_db
        yield rx.toast(
            "Part updated successfully.", duration=3000
        )

    @rx.event
    def close_edit_part_dialog(self):
        self.show_edit_part_dialog = False
        self.editing_part_motorbike_id = None
        self.editing_part_id = None
        self.edit_part_form_name = ""
        self.edit_part_form_source = ""
        self.edit_part_form_buyer = (
            self.buyers[0] if self.buyers else ""
        )
        self.edit_part_form_cost = ""

    @rx.event
    def delete_part(self, motorbike_id: str, part_id: str):
        with rx.session() as session:
            db_part = session.get(PartDB, part_id)
            if db_part:
                session.delete(db_part)
                session.commit()
            else:
                return rx.toast(
                    "Part not found for deletion.",
                    duration=3000,
                )
        yield MotorbikeState.load_motorbikes_from_db
        yield rx.toast("Part deleted.", duration=3000)
