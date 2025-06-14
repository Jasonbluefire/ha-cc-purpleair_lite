"""Constants for the PurpleAirLite integration."""

import logging
from typing import Final

from homeassistant.const import Platform

LOGGER: Final = logging.getLogger(__package__)
PLATFORMS: Final = [Platform.SENSOR]

DOMAIN: Final[str] = "purpleair_lite"

CONF_SENSOR_INDICES: Final[str] = "sensor_indices"
