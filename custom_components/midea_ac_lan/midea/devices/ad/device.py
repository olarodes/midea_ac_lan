import logging
import json
from .message import (
    MessageADResponse,
    Message21Query,
    Message31Query
)
try:
    from enum import StrEnum
except ImportError:
    from ...backports.enum import StrEnum
from ...core.device import MiedaDevice

_LOGGER = logging.getLogger(__name__)

class DeviceAttributes(StrEnum):
    temperature = "temperature"
    humidity = "humidity"
    tvoc = "tvoc"
    co2 = "co2"
    pm25 = "pm25"
    hcho = "hcho"
    presets_function = "presets_function"
    fall_asleep_status = "fall_asleep_status"
    portable_sense = "portable_sense"
    night_mode = "night_mode"
    screen_extinction_timeout = "screen_extinction_timeout"
    screen_status = "screen_status"
    led_status = "led_status"
    arofene_link = "arofene_link"
    header_exist = "header_exist"
    radar_exist = "radar_exist"
    header_led_status = "header_led_status"
    temperature_raw = "temperature_raw"
    humidity_raw = "humidity_raw"
    temperature_compensate = "temperature_compensate"
    humidity_compensate = "humidity_compensate"

class MideaADDevice(MiedaDevice):

    def __init__(
            self,
            name: str,
            device_id: int,
            ip_address: str,
            port: int,
            token: str,
            key: str,
            protocol: int,
            model: str,
            subtype: int,
            customize: str
    ):
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=0xAD,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            protocol=protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.temperature: None,
                DeviceAttributes.humidity: None,
                DeviceAttributes.tvoc: None,
                DeviceAttributes.co2: None,
                DeviceAttributes.pm25: None,
                DeviceAttributes.hcho: None,
                DeviceAttributes.presets_function: None,
                DeviceAttributes.fall_asleep_status: None,
                DeviceAttributes.portable_sense: None,
                DeviceAttributes.night_mode: None,
                DeviceAttributes.screen_extinction_timeout: None,
                DeviceAttributes.screen_status: None,
                DeviceAttributes.led_status: None,
                DeviceAttributes.arofene_link: None,
                DeviceAttributes.header_exist: None,
                DeviceAttributes.radar_exist: None,
                DeviceAttributes.header_led_status: None,
                DeviceAttributes.temperature_raw: None,
                DeviceAttributes.humidity_raw: None,
                DeviceAttributes.temperature_compensate: None,
                DeviceAttributes.humidity_compensate: None,                        
            })

    def build_query(self):
        return [
            Message21Query(self._protocol_version),
            Message31Query(self._protocol_version)
        ]
    
    def process_message(self, msg):
        message = MessageADResponse(msg)
        _LOGGER.debug(f"[{self.device_id}] Received: {message}")
        new_status = {}
        for status in self._attributes.keys():
            if hasattr(message, str(status)):
                value = getattr(message, str(status))
                self._attributes[status] = value
                new_status[str(status)] = self._attributes[status]
        return new_status

    def set_attribute(self, attr, value):
        pass

class MideaAppliance(MideaADDevice):
    pass
