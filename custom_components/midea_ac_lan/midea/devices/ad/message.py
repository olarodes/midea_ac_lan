from enum import IntEnum
from ...core.message import (
    MessageType,
    MessageRequest,
    MessageResponse,
    MessageBody
)
from ...core.crc8 import calculate

class MessageADBase(MessageRequest):
    def __init__(self, protocol_version, message_type, body_type):
        super().__init__(
            protocol_version=protocol_version,
            device_type=0xAD,
            message_type=message_type,
            body_type=body_type
        )

    @property
    def _body(self):
        raise NotImplementedError

class Message21Query(MessageADBase):
    def __init__(self, protocol_version):
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=0x21)

    @property
    def _body(self):
        return bytearray([0x01])
    
class Message31Query(MessageADBase):
    def __init__(self, protocol_version):
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=0x31)

    @property
    def _body(self):
        return bytearray([0x01])

class X31MessageBody(MessageBody):
    def __init__(self, body):
        super().__init__(body)
        self.screen_status = body[2] > 0 if body[2] != 0xFF else None
        self.led_status = body[3] > 0 if body[3] != 0xFF else None
        self.arofene_link = body[4] > 0 if body[4] != 0xFF else None
        self.header_exist = body[5] > 0 if body[5] != 0xFF else None
        self.radar_exist = body[6] > 0 if body[6] != 0xFF else None
        self.header_led_status = body[7] > 0 if body[7] != 0xFF else None
        self.temperature_raw = (body[8] << 8) + body[9] if body[8] !=0xFF else None
        self.humidity_raw = (body[10] << 8) + body[11] if body[10] !=0xFF else None
        self.temperature_compensate = (body[12] << 8) + body[13] if body[1] > 0x0D else None
        self.humidity_compensate = (body[14] << 8) + body[15] if body[1] > 0x0D else None

class X21MessageBody(MessageBody):
    def __init__(self, body):
        super().__init__(body)
        self.portable_sense = (body[2] > 0)
        self.night_mode = (body[3] > 0)
        self.screen_extinction_timeout = body[4] if (body[4] != 0xFF) else None

class X11MessageBody(MessageBody):
    def __init__(self, body):
        super().__init__(body)
        if body[1] == 0x01:
            self.temperature = ((((body[3] << 8) + body[4]) - 65535) - 1) / 100  if body[3] >= 128 else ((body[3] << 8) + body[4]) / 100
            self.humidity =  ((body[5] << 8) + body[6]) / 100 if body[5] !=0xFF else None
            self.tvoc =  ((body[7] << 8) + body[8]) if body[7] !=0xFF else None
            self.pm25 =  ((body[9] << 8) + body[10]) if body[9] !=0xFF else None
            self.co2 =  ((body[11] << 8) + body[12]) if body[11] !=0xFF else None
            self.hcho =  ((body[13] << 8) + body[14]) / 100 if body[13] !=0xFF else None
            self.arofene_link = ((body[16] & 0x01) > 0) if body[16] !=0xFF else None
            self.radar_exist = ((body[16] & 0x02) > 0) if body[16] !=0xFF else None
        elif body[1] == 0x04:
            if body[3] == 0x01:
                self.presets_function = body[4] == 0x01  
            elif body[3] == 0x02:
                self.fall_asleep_status = body[4] == 0x01
                    

class MessageADResponse(MessageResponse):
    def __init__(self, message):
        super().__init__(message)
        body = message[self.HEADER_LENGTH: -1]
        if self._body_type == 0x11:
            self.set_body(X11MessageBody(body))
        elif self._body_type == 0x21:
            self.set_body(X21MessageBody(body))
        elif self._body_type == 0x31:
            self.set_body(X31MessageBody(body))
        self.set_attr()
