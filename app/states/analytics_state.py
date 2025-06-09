import reflex as rx
from typing import List, TypedDict, Dict, Any
from app.states.motorbike_state import (
    MotorbikeState,
    Motorbike,
    Part,
)


class BikeAnalytics(TypedDict):
    id: str
    name: str
    initial_cost: float
    bike_buyer: str | None
    total_cost: float
    tanya_investment_on_bike: float
    gerald_investment_on_bike: float
    profit: float | None
    tanya_profit_share: float | None
    gerald_profit_share: float | None
    is_sold: bool


class AnalyticsState(rx.State):
    filter_sold_status: str = "all"

    @rx.event
    def set_filter_sold_status(self, status: str):
        self.filter_sold_status = status

    @rx.var
    async def bike_analytics_data(
        self,
    ) -> List[BikeAnalytics]:
        motorbike_s = await self.get_state(MotorbikeState)
        analytics: List[BikeAnalytics] = []
        filtered_bikes: List[Motorbike] = []
        for bike_data in motorbike_s.motorbikes:
            if self.filter_sold_status == "all":
                filtered_bikes.append(bike_data)
            elif (
                self.filter_sold_status == "sold"
                and bike_data["is_sold"]
            ):
                filtered_bikes.append(bike_data)
            elif self.filter_sold_status == "unsold" and (
                not bike_data["is_sold"]
            ):
                filtered_bikes.append(bike_data)
        for bike in filtered_bikes:
            if bike["ignore_from_calculations"]:
                continue
            tanya_total_investment_on_bike = (
                bike["tanya_parts_cost"] + bike["tanya_initial_cost"]
            )
            gerald_total_investment_on_bike = (
                bike["gerald_parts_cost"] + bike["gerald_initial_cost"]
            )
            profit = None
            tanya_profit_share = None
            gerald_profit_share = None
            if (
                bike["is_sold"]
                and bike["sold_value"] is not None
            ):
                profit = (
                    bike["sold_value"]
                    - bike["total_motorbike_cost"]
                )
                tanya_profit_share = profit / 2
                gerald_profit_share = profit / 2
            analytics.append(
                {
                    "id": bike["id"],
                    "name": bike["name"],
                    "initial_cost": bike["initial_cost"],
                    "bike_buyer": bike["bike_buyer"],
                    "total_cost": bike[
                        "total_motorbike_cost"
                    ],
                    "tanya_investment_on_bike": tanya_total_investment_on_bike,
                    "gerald_investment_on_bike": gerald_total_investment_on_bike,
                    "profit": profit,
                    "tanya_profit_share": tanya_profit_share,
                    "gerald_profit_share": gerald_profit_share,
                    "is_sold": bike["is_sold"],
                }
            )
        return analytics

    @rx.var
    async def overall_summary(self) -> Dict[str, float]:
        data = await self.bike_analytics_data
        total_tanya_inv = sum(
            (b["tanya_investment_on_bike"] for b in data)
        )
        total_gerald_inv = sum(
            (b["gerald_investment_on_bike"] for b in data)
        )
        total_tanya_profit = sum(
            (
                b["tanya_profit_share"]
                for b in data
                if b["tanya_profit_share"] is not None
            )
        )
        total_gerald_profit = sum(
            (
                b["gerald_profit_share"]
                for b in data
                if b["gerald_profit_share"] is not None
            )
        )
        return {
            "total_tanya_investment": total_tanya_inv,
            "total_gerald_investment": total_gerald_inv,
            "total_tanya_profit_share": total_tanya_profit,
            "total_gerald_profit_share": total_gerald_profit,
        }