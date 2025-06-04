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
    total_cost: float
    tanya_cost: float
    gerald_cost: float
    profit: float | None
    tanya_profit_share: float | None
    gerald_profit_share: float | None
    is_sold: bool


class AnalyticsState(rx.State):

    @rx.var
    async def bike_analytics_data(
        self,
    ) -> List[BikeAnalytics]:
        motorbike_s = await self.get_state(MotorbikeState)
        analytics: List[BikeAnalytics] = []
        for bike in motorbike_s.motorbikes:
            tanya_cost = 0.0
            gerald_cost = 0.0
            for part in bike["parts"]:
                if part["buyer"].lower() == "tanya":
                    tanya_cost += part["cost"]
                elif part["buyer"].lower() == "gerald":
                    gerald_cost += part["cost"]
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
                    "total_cost": bike[
                        "total_motorbike_cost"
                    ],
                    "tanya_cost": tanya_cost,
                    "gerald_cost": gerald_cost,
                    "profit": profit,
                    "tanya_profit_share": tanya_profit_share,
                    "gerald_profit_share": gerald_profit_share,
                    "is_sold": bike["is_sold"],
                }
            )
        return analytics

    @rx.var
    def total_tanya_investment(self) -> float:
        total = 0.0
        return 0.0

    @rx.var
    def total_gerald_investment(self) -> float:
        return 0.0

    @rx.var
    def total_tanya_profit_share(self) -> float:
        return 0.0

    @rx.var
    def total_gerald_profit_share(self) -> float:
        return 0.0

    @rx.var
    async def overall_summary(self) -> Dict[str, float]:
        data = await self.bike_analytics_data
        total_tanya_inv = sum(
            (b["tanya_cost"] for b in data)
        )
        total_gerald_inv = sum(
            (b["gerald_cost"] for b in data)
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