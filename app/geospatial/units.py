def convert_length(value: float) -> tuple[float, str]:
    if value >= 1000:
        return value / 1000, "km"

    return value, "m"


def convert_area(value: float) -> tuple[float, str]:
    if value >= 1_000_000:
        return value / 1_000_000, "km2"

    if value >= 10_000:
        return value / 10_000, "ha"

    return value, "m2"