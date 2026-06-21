from __future__ import annotations
import asyncio, logging, os
import httpx
from datetime import timedelta
from homeassistant.components.update import UpdateEntity, UpdateEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator, UpdateFailed
from .const import CONF_SPACE_ID, DOMAIN, HA_RELEASES_URL, SCAN_INTERVAL, UPDATER_NAME

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = HASpaceUpdaterCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([HASpaceUpdateEntity(coordinator, entry)])

class HASpaceUpdaterCoordinator(DataUpdateCoordinator):
    def __init__(self, hass):
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=timedelta(seconds=SCAN_INTERVAL))

    async def _async_update_data(self):
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                response = await client.get(HA_RELEASES_URL, headers={"Accept": "application/vnd.github.v3+json"}, follow_redirects=True)
                response.raise_for_status()
                data = response.json()
                latest_version = data.get("tag_name", "").lstrip("v")
                from homeassistant import const as ha_const
                current_version = getattr(ha_const, "__version__", "unknown")
                return {"current_version": current_version, "latest_version": latest_version, "release_url": data.get("html_url", ""), "release_notes": data.get("body", ""), "published_at": data.get("published_at", "")}
            except httpx.HTTPStatusError as err:
                if err.response.status_code == 403:
                    if self.data: return self.data
                raise UpdateFailed(f"GitHub API error: {err.response.status_code}")
            except Exception as err:
                raise UpdateFailed(f"Error: {err}")

class HASpaceUpdateEntity(CoordinatorEntity, UpdateEntity):
    _attr_has_entity_name = True
    _attr_name = "Home Assistant Core"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._entry = entry
        self._space_id = entry.data[CONF_SPACE_ID]
        self._attr_unique_id = f"ha_space_updater_{self._space_id}"
        self._attr_title = UPDATER_NAME
        self._attr_supported_features = UpdateEntityFeature.INSTALL | UpdateEntityFeature.BACKUP | UpdateEntityFeature.PROGRESS

    @property
    def installed_version(self):
        return self.coordinator.data.get("current_version") if self.coordinator.data else None

    @property
    def latest_version(self):
        return self.coordinator.data.get("latest_version") if self.coordinator.data else None

    @property
    def release_url(self):
        return self.coordinator.data.get("release_url") if self.coordinator.data else None

    @property
    def release_summary(self):
        if self.coordinator.data and self.coordinator.data.get("release_notes"):
            return self.coordinator.data["release_notes"][:500]
        return None

    async def async_install(self, version=None, backup=False, **kwargs):
        _LOGGER.info("Starting HA Space rebuild for version %s...", version or "latest")
        hf_token = os.environ.get("HF_TOKEN")
        if not hf_token:
            raise Exception("HF_TOKEN not available. Must run inside a HF Space.")

        self._async_write_ha_entity_state(progress=10)
        await asyncio.sleep(0.5)

        try:
            from huggingface_hub import HfApi
            api = HfApi(token=hf_token)
            _LOGGER.info("Pushing version update to Space repo...")
            self._async_write_ha_entity_state(progress=30)
            version_str = version or self.latest_version or "latest"
            await self.hass.async_add_executor_job(api.upload_file, version_str.encode(), "HA_VERSION", self._space_id, "space")
            _LOGGER.info("Version file updated. Triggering rebuild...")
            self._async_write_ha_entity_state(progress=60)
            await self.hass.async_add_executor_job(api.restart_space, self._space_id)
            self._async_write_ha_entity_state(progress=90)
            _LOGGER.info("Space rebuild triggered. Space will restart in 2-5 min.")
        except Exception as err:
            _LOGGER.error("Failed: %s", err)
            self._async_write_ha_entity_state(progress=0)
            raise Exception(f"Rebuild failed: {err}")

    def _async_write_ha_entity_state(self, progress):
        self._attr_in_progress = 0 < progress < 100
        self._attr_update_percentage = progress
        self.async_write_ha_state()
