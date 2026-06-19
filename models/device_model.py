from dataclasses import dataclass

@dataclass
class DeviceModel:
    ip_address: str = ""
    power_state: bool = False
    online: bool = False