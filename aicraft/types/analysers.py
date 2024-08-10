from pydantic import BaseModel
from enum import Enum


class PropertyType(Enum):
    SINGLE_FAMILY_HOUSE = "single_family_house"
    TOWNHOUSE = "townhouse"
    CONDO = "condo"
    LAND = "land"
    MULTI_FAMILY_HOUSE = "multi_family_house"
    MOBILE_HOME = "mobile_home"
    APARTMENT = "apartment"
    CO_OP = "co-op"
    OTHER = "other"
    UNKNOWN = "unknown"


class Amenities(Enum):
    LAUNDRY = "laundry"
    HOSPITAL = "hospital"
    GYM = "gym"
    SWIMMING_POOL = "swimming_pool"
    FITNESS_CENTER = "fitness_center"
    SHOPPING_CENTER = "shopping_center"
    RAILWAY_STATION = "railway_station"
    BUS_STATION = "bus_station"
    FUEL_STATION = "fuel_station"
    OTHER = "other"


class PropertyFeatures(Enum):
    PARKING = "parking"
    STORAGE = "storage"
    SWIMMING_POOL = "swimming_pool"
    GARDEN = "garden"
    GARAGE = "garage"
    ZONED_HEATING = "zoned_heating"
    HEAT_PUMP = "heat_pump"
    AIR_CONDITIONING = "air_conditioning"
    FIRE_PIT = "fire_pit"
    FIREPLACE = "fireplace"
    FENCE = "fence"
    OTHER = "other"


class HobuCustomerConversationPreference(BaseModel):
    desired_state_in_us: str = ""
    counties_interested_in: list[str] = []
    townships_interested_in: list[str] = []
    interested_in_property_types: list[PropertyType] = []
    min_price: int = 0
    max_price: int = 0
    min_sqft: int = 0
    max_sqft: int = 0
    min_beds: int = 0
    max_beds: int = 0
    min_baths: int = 0
    max_baths: int = 0
    min_lot_size: int = 0
    max_lot_size: int = 0
    desired_amenities: list[Amenities] = []
    importance_for_schools: int = 0
    desired_school_names: list[str] = []
    desired_school_districts: list[str] = []
    desired_property_features: list[PropertyFeatures] = []

    def get_preference_status(self) -> dict[str, list]:
        unknown_fields = []
        known_fields = []
        for field_name, field_value in self.__fields__.items():
            default_value = field_value.get_default()
            if getattr(self, field_name) == default_value:
                unknown_fields.append(field_name)
            else:
                known_fields.append(
                    {"label": field_name, "value": getattr(self, field_name)}
                )

        return {
            "unknown": unknown_fields,
            "known": known_fields,
        }

    class Config:
        arbitrary_types_allowed = True
