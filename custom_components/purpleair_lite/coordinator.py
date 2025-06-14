"""Define a PurpleAirLite DataUpdateCoordinator."""

from __future__ import annotations

from datetime import timedelta

from aiopurpleair import API
from aiopurpleair.errors import InvalidApiKeyError, PurpleAirError
from aiopurpleair.models.sensors import GetSensorsResponse

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_SENSOR_INDICES, LOGGER

#ToDo: Config integration to change list dynamicly bases on enables HA sensors
SENSOR_FIELDS_TO_RETRIEVE = [
    "humidity",
    "temperature",
    "voc",
    "name", #Needed for setup
]

# This is not used yet, 
# ToDo: seperate out the initial config data fetch from the ongoing data refresh fetchs
SENSOR_FIELDS_FOR_INITIAL_SETUP = [
    "firmware_version",
    "hardware",
    "latitude",
    "location_type",
    "longitude",
    "model",
    "name",
    "uptime",
]

# This is not used and is here for reference, 
# These are all the PurpleAir Sensor Feilds that this integration is configured to handle
FULL_LIST_OF_SENSOR_FIELDS_CONFIGURED = [
    "0.3_um_count",
    "0.5_um_count",
    "1.0_um_count",
    "10.0_um_count",
    "2.5_um_count",
    "5.0_um_count",
    "altitude",
    "firmware_version",
    "hardware",
    "humidity",
    "latitude",
    "location_type",
    "longitude",
    "model",
    "name",
    "pm1.0",
    "pm10.0",
    "pm2.5",
    "pressure",
    "rssi",
    "temperature",
    "uptime",
    "voc",
]

UPDATE_INTERVAL = timedelta(minutes=5)


type PurpleAirConfigEntry = ConfigEntry[PurpleAirDataUpdateCoordinator]


class PurpleAirDataUpdateCoordinator(DataUpdateCoordinator[GetSensorsResponse]):
    """Define a PurpleAir-specific coordinator."""

    config_entry: PurpleAirConfigEntry

    def __init__(self, hass: HomeAssistant, entry: PurpleAirConfigEntry) -> None:
        """Initialize."""
        self._api = API(
            entry.data[CONF_API_KEY],
            session=aiohttp_client.async_get_clientsession(hass),
        )

        super().__init__(
            hass,
            LOGGER,
            config_entry=entry,
            name=entry.title,
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self) -> GetSensorsResponse:
        """Get the latest sensor information."""
        try:
            return await self._api.sensors.async_get_sensors(
                SENSOR_FIELDS_TO_RETRIEVE,
                sensor_indices=self.config_entry.options[CONF_SENSOR_INDICES],
            )
        except InvalidApiKeyError as err:
            raise ConfigEntryAuthFailed("Invalid API key") from err
        except PurpleAirError as err:
            raise UpdateFailed(f"Error while fetching data: {err}") from err

    @callback
    def async_get_map_url(self, sensor_index: int) -> str:
        """Get the map URL for a sensor index."""
        return self._api.get_map_url(sensor_index)
