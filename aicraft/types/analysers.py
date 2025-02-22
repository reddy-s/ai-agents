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


class State(Enum):
    UT = "Utah"
    DE = "Delaware"
    MO = "Missouri"
    RI = "Rhode Island"
    CA = "California"
    ND = "North Dakota"
    IN = "Indiana"
    TN = "Tennessee"
    KY = "Kentucky"
    NJ = "New Jersey"
    NV = "Nevada"
    HI = "Hawaii"
    MI = "Michigan"
    CO = "Colorado"
    AR = "Arkansas"
    IL = "Illinois"
    VA = "Virginia"
    WY = "Wyoming"
    NH = "New Hampshire"
    AL = "Alabama"
    AZ = "Arizona"
    ID = "Idaho"
    KS = "Kansas"
    TX = "Texas"
    CT = "Connecticut"
    MS = "Mississippi"
    OH = "Ohio"
    ME = "Maine"
    WA = "Washington"
    LA = "Louisiana"
    WI = "Wisconsin"
    FL = "Florida"
    PA = "Pennsylvania"
    MN = "Minnesota"
    SC = "South Carolina"
    SD = "South Dakota"
    GA = "Georgia"
    AK = "Alaska"
    MT = "Montana"
    NC = "North Carolina"
    IA = "Iowa"
    WV = "West Virginia"
    NE = "Nebraska"
    OK = "Oklahoma"
    OR = "Oregon"
    VT = "Vermont"
    DC = "District of Columbia"
    MA = "Massachusetts"
    MD = "Maryland"
    NY = "New York"
    NM = "New Mexico"
    XX = "Unknown"


class HobuCustomerConversationPreference(BaseModel):
    desired_state_in_us: list[State] = []
    counties_interested_in: list[str] = []
    metros_interested_in: list[str] = []
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

    def analyse_education_preferences(self) -> bool:
        if len(self.desired_school_districts) > 0:
            return True
        return False

    def analyse_location_preferences(self) -> bool:
        if len(self.counties_interested_in) > 0 or len(self.metros_interested_in) > 0:
            return True
        return False

    def analyse_property_preferences(self) -> bool:
        if (
            len(self.interested_in_property_types) > 0
            and len(self.metros_interested_in) > 0
        ):
            return True
        return False

    class Config:
        arbitrary_types_allowed = True
