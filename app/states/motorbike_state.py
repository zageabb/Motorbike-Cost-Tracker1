import reflex as rx
from typing import TypedDict, List, cast
import datetime
import uuid


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
    show_edit_part_dialog: bool = False
    editing_part_motorbike_id: str | None = None
    editing_part_id: str | None = None
    edit_part_form_name: str = ""
    edit_part_form_source: str = ""
    edit_part_form_buyer: str = "Tanya"
    edit_part_form_cost: str = ""

    @rx.var
    def total_cost(self) -> float:
        total = 0.0
        for bike in self.motorbikes:
            total += bike["total_motorbike_cost"]
        return total

    @rx.var
    def projected_sale(self) -> float:
        cost_of_unsold_bikes = sum(
            (
                bike["total_motorbike_cost"]
                for bike in self.motorbikes
                if not bike["is_sold"]
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
            key=lambda bike: bike["is_sold"],
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
        new_motorbike: Motorbike = {
            "id": new_id,
            "name": name,
            "initial_cost": initial_cost,
            "parts": [],
            "total_parts_cost": 0.0,
            "total_motorbike_cost": initial_cost,
            "is_sold": False,
            "sold_value": None,
        }
        self.motorbikes.append(new_motorbike)
        self.new_motorbike_name = ""
        self.new_motorbike_initial_cost = ""
        if len(self.motorbikes) == 1 and (
            not self.part_form_selected_motorbike_id
        ):
            self.part_form_selected_motorbike_id = new_id
        return rx.toast(
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
        target_motorbike_index: int | None = None
        for i, bike_item in enumerate(self.motorbikes):
            if bike_item["id"] == motorbike_id_to_use:
                if bike_item["is_sold"]:
                    return rx.toast(
                        f"Cannot add parts to '{bike_item['name']}' as it is already sold.",
                        duration=4000,
                    )
                target_motorbike_index = i
                break
        if target_motorbike_index is None:
            return rx.toast(
                f"Motorbike with ID {motorbike_id_to_use} not found.",
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
        bike_to_update = self.motorbikes[
            target_motorbike_index
        ].copy()
        new_part_entry: Part = {
            "id": str(uuid.uuid4()),
            "name": part_name,
            "source": form_data.get("source", ""),
            "buyer": form_data.get(
                "buyer",
                self.buyers[0] if self.buyers else "",
            ),
            "cost": cost,
        }
        if not isinstance(bike_to_update["parts"], list):
            bike_to_update["parts"] = []
        bike_to_update["parts"] = bike_to_update[
            "parts"
        ] + [new_part_entry]
        bike_to_update = self._recalculate_motorbike_costs(
            bike_to_update
        )
        self.motorbikes[target_motorbike_index] = (
            bike_to_update
        )
        self.motorbikes = list(self.motorbikes)
        self.new_part_name = ""
        self.new_part_source = ""
        self.new_part_buyer = (
            self.buyers[0] if self.buyers else ""
        )
        self.new_part_cost = ""
        return rx.toast(
            f"Part '{part_name}' added to {bike_to_update['name']}.",
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
        self, value: str
    ):
        self.edit_motorbike_form_sold_value = value

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
            if self.edit_motorbike_form_sold_value.strip():
                try:
                    sold_value_val = float(
                        self.edit_motorbike_form_sold_value
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
        updated_motorbikes = []
        found = False
        for bike in self.motorbikes:
            if bike["id"] == self.editing_motorbike_id:
                updated_bike = bike.copy()
                updated_bike["name"] = name
                updated_bike["initial_cost"] = initial_cost
                updated_bike["is_sold"] = is_sold_val
                updated_bike["sold_value"] = sold_value_val
                updated_bike = (
                    self._recalculate_motorbike_costs(
                        updated_bike
                    )
                )
                updated_motorbikes.append(updated_bike)
                found = True
            else:
                updated_motorbikes.append(bike)
        if found:
            self.motorbikes = updated_motorbikes
            self.close_edit_motorbike_dialog()
            return rx.toast(
                "Motorbike updated successfully.",
                duration=3000,
            )
        else:
            return rx.toast(
                "Failed to find motorbike to update.",
                duration=3000,
            )

    @rx.event
    def close_edit_motorbike_dialog(self):
        self.show_edit_motorbike_dialog = False
        self.editing_motorbike_id = None
        self.edit_motorbike_form_name = ""
        self.edit_motorbike_form_initial_cost = ""
        self.edit_motorbike_form_is_sold = False
        self.edit_motorbike_form_sold_value = ""

    @rx.event
    def delete_motorbike(self, motorbike_id: str):
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
                self.part_form_selected_motorbike_id = (
                    self.motorbikes[0]["id"]
                    if self.motorbikes
                    else ""
                )
            return rx.toast(
                "Motorbike deleted.", duration=3000
            )
        return rx.toast(
            "Motorbike not found for deletion.",
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
                        f"Cannot edit parts for '{bike['name']}' as it is already sold.",
                        duration=4000,
                    )
                for p in bike["parts"]:
                    if p["id"] == part_id:
                        self.editing_part_motorbike_id = (
                            motorbike_id
                        )
                        self.editing_part_id = part_id
                        self.edit_part_form_name = p["name"]
                        self.edit_part_form_source = p[
                            "source"
                        ]
                        self.edit_part_form_buyer = p[
                            "buyer"
                        ]
                        self.edit_part_form_cost = str(
                            p["cost"]
                        )
                        self.show_edit_part_dialog = True
                        return
        return rx.toast(
            "Part not found for editing.", duration=3000
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
        for bike_check in self.motorbikes:
            if (
                bike_check["id"]
                == self.editing_part_motorbike_id
                and bike_check["is_sold"]
            ):
                self.close_edit_part_dialog()
                return rx.toast(
                    f"Cannot save part for '{bike_check['name']}' as it is already sold.",
                    duration=4000,
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
        updated_motorbikes_list = []
        bike_found_and_updated = False
        for bike_data in self.motorbikes:
            if (
                bike_data["id"]
                == self.editing_part_motorbike_id
            ):
                current_bike_updated = bike_data.copy()
                updated_parts_list = []
                part_found_and_updated = False
                for p_data in current_bike_updated["parts"]:
                    if p_data["id"] == self.editing_part_id:
                        updated_p = p_data.copy()
                        updated_p["name"] = part_name
                        updated_p["source"] = (
                            self.edit_part_form_source
                        )
                        updated_p["buyer"] = (
                            self.edit_part_form_buyer
                        )
                        updated_p["cost"] = cost
                        updated_parts_list.append(updated_p)
                        part_found_and_updated = True
                    else:
                        updated_parts_list.append(p_data)
                if part_found_and_updated:
                    current_bike_updated["parts"] = (
                        updated_parts_list
                    )
                    current_bike_updated = (
                        self._recalculate_motorbike_costs(
                            current_bike_updated
                        )
                    )
                    bike_found_and_updated = True
                updated_motorbikes_list.append(
                    current_bike_updated
                )
            else:
                updated_motorbikes_list.append(bike_data)
        if bike_found_and_updated:
            self.motorbikes = updated_motorbikes_list
            self.close_edit_part_dialog()
            return rx.toast(
                "Part updated successfully.", duration=3000
            )
        else:
            return rx.toast(
                "Failed to find part or motorbike to update.",
                duration=3000,
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
        updated_motorbikes_list = []
        bike_found_and_updated = False
        toast_message = (
            "Part or motorbike not found for deletion."
        )
        for bike_data in self.motorbikes:
            if bike_data["id"] == motorbike_id:
                if bike_data["is_sold"]:
                    toast_message = f"Cannot delete parts from '{bike_data['name']}' as it is already sold."
                    updated_motorbikes_list.append(
                        bike_data
                    )
                    return rx.toast(
                        toast_message, duration=4000
                    )
                current_bike_updated = bike_data.copy()
                original_parts_count = len(
                    current_bike_updated["parts"]
                )
                current_bike_updated["parts"] = [
                    p
                    for p in current_bike_updated["parts"]
                    if p["id"] != part_id
                ]
                if (
                    len(current_bike_updated["parts"])
                    < original_parts_count
                ):
                    current_bike_updated = (
                        self._recalculate_motorbike_costs(
                            current_bike_updated
                        )
                    )
                    bike_found_and_updated = True
                    toast_message = "Part deleted."
                updated_motorbikes_list.append(
                    current_bike_updated
                )
            else:
                updated_motorbikes_list.append(bike_data)
        if bike_found_and_updated:
            self.motorbikes = updated_motorbikes_list
        return rx.toast(toast_message, duration=3000)

    @rx.event
    def do_nothing(self):
        """A placeholder event handler that does nothing."""
        pass