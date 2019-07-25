from enum import Enum


class AgSyncRateUnits(Enum):
    """
    The Flow Units sent by existing AgSync.
    """
    KILOGRAMS_PER_HA = 5
    POUNDS_PER_ACRE = 10
    FLUID_OZ_PER_ACRE = 18
    GALLONS_PER_ACRE = 19
    QUARTS_PER_ACRE = 21
    PINTS_PER_ACRE = 22
    DRY_OZ_PER_ACRE = 23
    LITERS_PER_HA = 48
    ML_PER_HA = 49
    PINTS_PER_100 = 53
    QUARTS_PER_100 = 54
    GALLONS_PER_100 = 55
    POUNDS_PER_100 = 56


    def ConvertToQDRate(self):
        if self == AgSyncRateUnits.KILOGRAMS_PER_HA:
            return 13
        elif self == AgSyncRateUnits.POUNDS_PER_ACRE:
            return 4
        elif self == AgSyncRateUnits.FLUID_OZ_PER_ACRE:
            return 1
        elif self == AgSyncRateUnits.GALLONS_PER_ACRE:
            return 0
        elif self == AgSyncRateUnits.QUARTS_PER_ACRE:
            return 3
        elif self == AgSyncRateUnits.PINTS_PER_ACRE:
            return 2
        elif self == AgSyncRateUnits.DRY_OZ_PER_ACRE:
            return 11
        elif self == AgSyncRateUnits.LITERS_PER_HA:
            return 5
        elif self == AgSyncRateUnits.ML_PER_HA:
            return 6
        elif self == AgSyncRateUnits.PINTS_PER_100:
            return 8
        elif self == AgSyncRateUnits.QUARTS_PER_100:
            return 9
        elif self == AgSyncRateUnits.GALLONS_PER_100:
            return 10
        elif self == AgSyncRateUnits.POUNDS_PER_100:
            return 7
        else:
            return -2

    def ConvertRateUnitsToQDTotalUnits(self):
        if self == AgSyncRateUnits.KILOGRAMS_PER_HA:
            return 8
        elif self == AgSyncRateUnits.POUNDS_PER_ACRE:
            return 4
        elif self == AgSyncRateUnits.FLUID_OZ_PER_ACRE:
            return 1
        elif self == AgSyncRateUnits.GALLONS_PER_ACRE:
            return 0
        elif self == AgSyncRateUnits.QUARTS_PER_ACRE:
            return 3
        elif self == AgSyncRateUnits.PINTS_PER_ACRE:
            return 2
        elif self == AgSyncRateUnits.DRY_OZ_PER_ACRE:
            return 4
        elif self == AgSyncRateUnits.LITERS_PER_HA:
            return 5
        elif self == AgSyncRateUnits.ML_PER_HA:
            return 6
        elif self == AgSyncRateUnits.PINTS_PER_100:
            return 8
        elif self == AgSyncRateUnits.QUARTS_PER_100:
            return 3
        elif self == AgSyncRateUnits.GALLONS_PER_100:
            return 0
        elif self == AgSyncRateUnits.POUNDS_PER_100:
            return 4
        else:
            return -3
