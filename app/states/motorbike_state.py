import reflex as rx
from typing import (
    TypedDict,
    List,
    cast,
    Optional as PyOptional,
)
import datetime
import uuid
from app.models import MotorbikeDB, PartDB
from sqlmodel import select


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
    parts: List[Part]
    total_parts_cost: float
    total_motorbike_cost: float
    is_sold: bool
    sold_value: float | None
    ignore_from_calculations: bool


class MotorbikeState(rx.State):
    motorbikes: List[Motorbike] = []
    buyers: List[str] = ["Tanya", "Gerald"]
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
    edit_motorbike_form_is_sold: bool = False
    edit_motorbike_form_sold_value: str = ""
    edit_motorbike_form_ignore_from_calculations: bool = (
        False
    )
    show_edit_part_dialog: bool = False
    editing_part_motorbike_id: str | None = None
    editing_part_id: str | None = None
    edit_part_form_name: str = ""
    edit_part_form_source: str = ""
    edit_part_form_buyer: str = "Tanya"
    edit_part_form_cost: str = ""

    def _convert_part_db_to_dict(
        self, part_db: PartDB
    ) -> Part:
        return {
            "id": part_db.id,
            "name": part_db.name,
            "source": part_db.source,
            "buyer": part_db.buyer,
            "cost": part_db.cost,
        }

    def _convert_motorbike_db_to_dict(
        self, bike_db: MotorbikeDB
    ) -> Motorbike:
        parts_list = [
            self._convert_part_db_to_dict(p)
            for p in bike_db.parts
        ]
        total_parts_cost = sum(
            (p["cost"] for p in parts_list)
        )
        motorbike_dict: Motorbike = {
            "id": bike_db.id,
            "name": bike_db.name,
            "initial_cost": bike_db.initial_cost,
            "parts": parts_list,
            "total_parts_cost": total_parts_cost,
            "total_motorbike_cost": bike_db.initial_cost
            + total_parts_cost,
            "is_sold": bike_db.is_sold,
            "sold_value": bike_db.sold_value,
            "ignore_from_calculations": bike_db.ignore_from_calculations,
        }
        return motorbike_dict

    @rx.var
    def total_cost(self) -> float:
        return sum(
            (
                bike["total_motorbike_cost"]
                for bike in self.motorbikes
                if not bike["ignore_from_calculations"]
            )
        )

    @rx.var
    def projected_sale(self) -> float:
        cost_of_unsold_bikes = sum(
            (
                bike["total_motorbike_cost"]
                for bike in self.motorbikes
                if not bike["is_sold"]
                and (not bike["ignore_from_calculations"])
            )
        )
        return cost_of_unsold_bikes * 2

    @rx.var
    def actual_profit(self) -> float:
        profit = 0.0
        for bike in self.motorbikes:
            if (
                bike["is_sold"]
                and bike["sold_value"] is not None
                and (not bike["ignore_from_calculations"])
            ):
                profit += (
                    bike["sold_value"]
                    - bike["total_motorbike_cost"]
                )
        return profit

    @rx.var
    def has_motorbikes(self) -> bool:
        return len(self.motorbikes) > 0

    @rx.var
    def selected_motorbike_for_detail(
        self,
    ) -> Motorbike | None:
        motorbike_id_from_url = self.router.page.params.get(
            "route_arg_motorbike_id", ""
        )
        if not motorbike_id_from_url:
            return None
        for bike in self.motorbikes:
            if bike["id"] == motorbike_id_from_url:
                return bike
        return None

    @rx.var
    def sorted_motorbikes_for_display(
        self,
    ) -> List[Motorbike]:
        return sorted(
            self.motorbikes,
            key=lambda bike: (
                bike["is_sold"],
                bike["name"].lower(),
            ),
        )

    @rx.var
    def unsold_motorbikes(self) -> List[Motorbike]:
        return [
            bike
            for bike in self.motorbikes
            if not bike["is_sold"]
        ]

    def _recalculate_motorbike_costs(
        self, motorbike: Motorbike
    ) -> Motorbike:
        motorbike["total_parts_cost"] = sum(
            (p["cost"] for p in motorbike["parts"])
        )
        motorbike["total_motorbike_cost"] = (
            motorbike["initial_cost"]
            + motorbike["total_parts_cost"]
        )
        return motorbike

    @rx.event
    def load_all_data(self):
        temp_motorbikes = []
        with rx.session() as session:
            db_motorbikes = session.exec(
                select(MotorbikeDB)
            ).all()
            for bike_db in db_motorbikes:
                temp_motorbikes.append(
                    self._convert_motorbike_db_to_dict(
                        bike_db
                    )
                )
        self.motorbikes = temp_motorbikes
        if self.unsold_motorbikes and (
            not self.part_form_selected_motorbike_id
        ):
            self.part_form_selected_motorbike_id = (
                self.unsold_motorbikes[0]["id"]
            )
        elif not self.unsold_motorbikes:
            self.part_form_selected_motorbike_id = ""

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
        new_id = str(uuid.uuid4())
        motorbike_db = MotorbikeDB(
            id=new_id,
            name=name,
            initial_cost=initial_cost,
            is_sold=False,
            sold_value=None,
            ignore_from_calculations=False,
        )
        try:
            with rx.session() as session:
                session.add(motorbike_db)
                session.commit()
                session.refresh(motorbike_db)
            new_motorbike_dict = (
                self._convert_motorbike_db_to_dict(
                    motorbike_db
                )
            )
            self.motorbikes.append(new_motorbike_dict)
            self.motorbikes = list(self.motorbikes)
            self.new_motorbike_name = ""
            self.new_motorbike_initial_cost = ""
            if len(self.motorbikes) == 1 and (
                not self.part_form_selected_motorbike_id
            ):
                self.part_form_selected_motorbike_id = (
                    new_id
                )
            return rx.toast(
                f"Motorbike '{name}' added.", duration=3000
            )
        except Exception as e:
            print(
                f"Error processing motorbike '{name}' (ID: {new_id}) after DB commit: {type(e).__name__}: {e}"
            )
            return rx.toast(
                f"Motorbike '{name}' saved to DB, but a post-processing error occurred: {str(e)[:100]}. App state might be inconsistent.",
                duration=5000,
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
            bike_db = session.get(
                MotorbikeDB, motorbike_id_to_use
            )
            if not bike_db:
                return rx.toast(
                    f"Motorbike with ID {motorbike_id_to_use} not found.",
                    duration=3000,
                )
            if bike_db.is_sold:
                return rx.toast(
                    f"Cannot add parts to '{bike_db.name}' as it is already sold.",
                    duration=4000,
                )
            new_part_id = str(uuid.uuid4())
            part_db = PartDB(
                id=new_part_id,
                name=part_name,
                source=form_data.get("source", ""),
                buyer=form_data.get(
                    "buyer",
                    self.buyers[0] if self.buyers else "",
                ),
                cost=cost,
                motorbike_id=bike_db.id,
            )
            session.add(part_db)
            session.commit()
            session.refresh(bike_db)
            for i, bike_in_list in enumerate(
                self.motorbikes
            ):
                if (
                    bike_in_list["id"]
                    == motorbike_id_to_use
                ):
                    self.motorbikes[i] = (
                        self._convert_motorbike_db_to_dict(
                            bike_db
                        )
                    )
                    break
            self.motorbikes = list(self.motorbikes)
        self.new_part_name = ""
        self.new_part_source = ""
        self.new_part_buyer = (
            self.buyers[0] if self.buyers else ""
        )
        self.new_part_cost = ""
        return rx.toast(
            f"Part '{part_name}' added to {bike_db.name}.",
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
    def set_edit_motorbike_form_name(self, value: str):
        self.edit_motorbike_form_name = value

    @rx.event
    def set_edit_motorbike_form_initial_cost(
        self, value: str
    ):
        self.edit_motorbike_form_initial_cost = value

    @rx.event
    def set_edit_motorbike_form_sold_value(
        self, value: str | int | float
    ):
        self.edit_motorbike_form_sold_value = str(value)

    @rx.event
    def set_edit_motorbike_form_ignore_from_calculations(
        self, value: bool
    ):
        self.edit_motorbike_form_ignore_from_calculations = (
            value
        )

    @rx.event
    def open_edit_motorbike_dialog(self, motorbike_id: str):
        for bike in self.motorbikes:
            if bike["id"] == motorbike_id:
                self.editing_motorbike_id = bike["id"]
                self.edit_motorbike_form_name = bike["name"]
                self.edit_motorbike_form_initial_cost = str(
                    bike["initial_cost"]
                )
                self.edit_motorbike_form_is_sold = bike[
                    "is_sold"
                ]
                self.edit_motorbike_form_sold_value = (
                    str(bike["sold_value"])
                    if bike["sold_value"] is not None
                    else ""
                )
                self.edit_motorbike_form_ignore_from_calculations = bike[
                    "ignore_from_calculations"
                ]
                self.show_edit_motorbike_dialog = True
                return
        return rx.toast(
            "Motorbike not found for editing.",
            duration=3000,
        )

    @rx.event
    def set_edit_motorbike_form_is_sold(self, value: bool):
        self.edit_motorbike_form_is_sold = value
        if not value:
            self.edit_motorbike_form_sold_value = ""

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
        is_sold_val = self.edit_motorbike_form_is_sold
        sold_value_val: float | None = None
        if is_sold_val:
            sold_value_input_str = str(
                self.edit_motorbike_form_sold_value
            )
            if sold_value_input_str.strip():
                try:
                    sold_value_val = float(
                        sold_value_input_str.strip()
                    )
                    if sold_value_val < 0:
                        return rx.toast(
                            "Sold value cannot be negative.",
                            duration=3000,
                        )
                except ValueError:
                    return rx.toast(
                        "Invalid sold value format.",
                        duration=3000,
                    )
        with rx.session() as session:
            bike_db = session.get(
                MotorbikeDB, self.editing_motorbike_id
            )
            if not bike_db:
                yield MotorbikeState.close_edit_motorbike_dialog
                return rx.toast(
                    "Motorbike not found in database for update.",
                    duration=3000,
                )
            bike_db.name = name
            bike_db.initial_cost = initial_cost
            bike_db.is_sold = is_sold_val
            bike_db.sold_value = sold_value_val
            bike_db.ignore_from_calculations = (
                self.edit_motorbike_form_ignore_from_calculations
            )
            session.add(bike_db)
            session.commit()
            session.refresh(bike_db)
            for i, bike_in_list in enumerate(
                self.motorbikes
            ):
                if (
                    bike_in_list["id"]
                    == self.editing_motorbike_id
                ):
                    self.motorbikes[i] = (
                        self._convert_motorbike_db_to_dict(
                            bike_db
                        )
                    )
                    break
            self.motorbikes = list(self.motorbikes)
        yield MotorbikeState.close_edit_motorbike_dialog
        return rx.toast(
            "Motorbike details updated.", duration=3000
        )

    @rx.event
    def close_edit_motorbike_dialog(self):
        self.show_edit_motorbike_dialog = False
        self.editing_motorbike_id = None
        self.edit_motorbike_form_name = ""
        self.edit_motorbike_form_initial_cost = ""
        self.edit_motorbike_form_is_sold = False
        self.edit_motorbike_form_sold_value = ""
        self.edit_motorbike_form_ignore_from_calculations = (
            False
        )

    @rx.event
    def delete_motorbike(self, motorbike_id: str):
        with rx.session() as session:
            bike_db = session.get(MotorbikeDB, motorbike_id)
            if bike_db:
                session.delete(bike_db)
                session.commit()
            else:
                return rx.toast(
                    "Motorbike not found in database for deletion.",
                    duration=3000,
                )
        original_length = len(self.motorbikes)
        self.motorbikes = [
            bike
            for bike in self.motorbikes
            if bike["id"] != motorbike_id
        ]
        if len(self.motorbikes) < original_length:
            if (
                self.part_form_selected_motorbike_id
                == motorbike_id
            ):
                if self.unsold_motorbikes:
                    self.part_form_selected_motorbike_id = (
                        self.unsold_motorbikes[0]["id"]
                    )
                else:
                    self.part_form_selected_motorbike_id = (
                        ""
                    )
            return rx.toast(
                "Motorbike deleted.", duration=3000
            )
        return rx.toast(
            "Motorbike not found for deletion (post-DB).",
            duration=3000,
        )

    @rx.event
    def open_edit_part_dialog(
        self, motorbike_id: str, part_id: str
    ):
        for bike in self.motorbikes:
            if bike["id"] == motorbike_id:
                if bike["is_sold"]:
                    return rx.toast(
                        f"Cannot edit parts of '{bike['name']}' as it is sold.",
                        duration=4000,
                    )
                for part_item in bike["parts"]:
                    if part_item["id"] == part_id:
                        self.editing_part_motorbike_id = (
                            motorbike_id
                        )
                        self.editing_part_id = part_id
                        self.edit_part_form_name = (
                            part_item["name"]
                        )
                        self.edit_part_form_source = (
                            part_item["source"]
                        )
                        self.edit_part_form_buyer = (
                            part_item["buyer"]
                        )
                        self.edit_part_form_cost = str(
                            part_item["cost"]
                        )
                        self.show_edit_part_dialog = True
                        return
        return rx.toast(
            "Part or motorbike not found for editing.",
            duration=3000,
        )

    @rx.event
    def save_edited_part(self):
        if (
            not self.editing_part_motorbike_id
            or not self.editing_part_id
        ):
            return rx.toast(
                "No part selected for editing.",
                duration=3000,
            )
        name = self.edit_part_form_name.strip()
        cost_str = self.edit_part_form_cost
        if not name:
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
            part_db = session.get(
                PartDB, self.editing_part_id
            )
            if (
                not part_db
                or part_db.motorbike_id
                != self.editing_part_motorbike_id
            ):
                yield MotorbikeState.close_edit_part_dialog
                return rx.toast(
                    "Part not found in database for update.",
                    duration=3000,
                )
            motorbike_db = session.get(
                MotorbikeDB, self.editing_part_motorbike_id
            )
            if not motorbike_db or motorbike_db.is_sold:
                yield MotorbikeState.close_edit_part_dialog
                return rx.toast(
                    "Cannot edit parts of a sold motorbike or motorbike not found.",
                    duration=4000,
                )
            part_db.name = name
            part_db.source = self.edit_part_form_source
            part_db.buyer = self.edit_part_form_buyer
            part_db.cost = cost
            session.add(part_db)
            session.commit()
            session.refresh(motorbike_db)
            for i, bike_in_list in enumerate(
                self.motorbikes
            ):
                if (
                    bike_in_list["id"]
                    == self.editing_part_motorbike_id
                ):
                    self.motorbikes[i] = (
                        self._convert_motorbike_db_to_dict(
                            motorbike_db
                        )
                    )
                    break
            self.motorbikes = list(self.motorbikes)
        yield MotorbikeState.close_edit_part_dialog
        return rx.toast(
            "Part details updated.", duration=3000
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
        toast_message = (
            "Part or motorbike not found for deletion."
        )
        part_deleted_from_db = False
        with rx.session() as session:
            motorbike_db_check = session.get(
                MotorbikeDB, motorbike_id
            )
            if (
                motorbike_db_check
                and motorbike_db_check.is_sold
            ):
                return rx.toast(
                    f"Cannot delete parts from '{motorbike_db_check.name}' as it is already sold.",
                    duration=4000,
                )
            part_db = session.get(PartDB, part_id)
            if (
                part_db
                and part_db.motorbike_id == motorbike_id
            ):
                session.delete(part_db)
                session.commit()
                part_deleted_from_db = True
                toast_message = "Part deleted."
                motorbike_db_to_refresh = session.get(
                    MotorbikeDB, motorbike_id
                )
                if motorbike_db_to_refresh:
                    session.refresh(motorbike_db_to_refresh)
                    for i, bike_in_list in enumerate(
                        self.motorbikes
                    ):
                        if (
                            bike_in_list["id"]
                            == motorbike_id
                        ):
                            self.motorbikes[i] = (
                                self._convert_motorbike_db_to_dict(
                                    motorbike_db_to_refresh
                                )
                            )
                            break
                    self.motorbikes = list(self.motorbikes)
            elif not part_db:
                toast_message = (
                    "Part not found in database."
                )
            else:
                toast_message = "Part does not belong to the specified motorbike."
        return rx.toast(toast_message, duration=3000)

    @rx.event
    def set_new_motorbike_name(self, value: str):
        self.new_motorbike_name = value

    @rx.event
    def set_new_motorbike_initial_cost(self, value: str):
        self.new_motorbike_initial_cost = value

    @rx.event
    def set_new_part_name(self, value: str):
        self.new_part_name = value

    @rx.event
    def set_new_part_source(self, value: str):
        self.new_part_source = value

    @rx.event
    def set_new_part_cost(self, value: str):
        self.new_part_cost = value

    @rx.event
    def set_edit_part_form_name(self, value: str):
        self.edit_part_form_name = value

    @rx.event
    def set_edit_part_form_source(self, value: str):
        self.edit_part_form_source = value

    @rx.event
    def set_edit_part_form_buyer(self, value: str):
        self.edit_part_form_buyer = value

    @rx.event
    def set_edit_part_form_cost(
        self, value: str | int | float
    ):
        self.edit_part_form_cost = str(value)

    @rx.event
    def set_show_edit_motorbike_dialog(self, value: bool):
        self.show_edit_motorbike_dialog = value
        if not value:
            yield MotorbikeState.close_edit_motorbike_dialog

    @rx.event
    def set_show_edit_part_dialog(self, value: bool):
        self.show_edit_part_dialog = value
        if not value:
            yield MotorbikeState.close_edit_part_dialog