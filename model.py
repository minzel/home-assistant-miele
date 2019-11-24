from typing import List, Optional, Any

class TypeClass:
    __slots__ = "key_localized", "value_raw", "value_localized", "unit"

    def __init__(self, key_localized: str, value_raw: Optional[int], value_localized: str, unit: Optional[str], **kwargs: Any):
        self.key_localized = key_localized
        self.value_raw = value_raw
        self.value_localized = value_localized
        self.unit = unit

class Temperature:
    __slots__ = "value_raw", "value_localized", "unit"

    def __init__(self, value_raw: int, value_localized: Optional[int], unit: str, **kwargs: Any):
        self.value_raw = value_raw
        self.value_localized = value_localized
        self.unit = unit

class RemoteEnable:
    __slots__ = "full_remote_control", "smart_grid"

    def __init__(self, full_remote_control: bool, smart_grid: bool, **kwargs: Any):
        self.full_remote_control = full_remote_control
        self.smart_grid = smart_grid

class State:
    __slots__ = "program_id", "status", "program_type", "program_phase", "remaining_time", "start_time", "target_temperature", "temperature", "signal_info", "signal_failure", "signal_door", "remote_enable", "light", "elapsed_time", "spinning_speed", "drying_step", "ventilation_step", "plate_step"

    def __init__(self, program_id: TypeClass, status: TypeClass, program_type: TypeClass, program_phase: TypeClass, remaining_time: List[int], start_time: List[int], target_temperature: List[Temperature], temperature: List[Temperature], signal_info: bool, signal_failure: bool, signal_door: bool, remote_enable: RemoteEnable, light: int, elapsed_time: List[int], spinning_speed: TypeClass, drying_step: TypeClass, ventilation_step: TypeClass, plate_step: List[Any], **kwargs: Any):
        self.program_id = program_id
        self.status = status
        self.program_type = program_type
        self.program_phase = program_phase
        self.remaining_time = remaining_time
        self.start_time = start_time
        self.target_temperature = target_temperature
        self.temperature = temperature
        self.signal_info = signal_info
        self.signal_failure = signal_failure
        self.signal_door = signal_door
        self.remote_enable = remote_enable
        self.light = light
        self.elapsed_time = elapsed_time
        self.spinning_speed = spinning_speed
        self.drying_step = drying_step
        self.ventilation_step = ventilation_step
        self.plate_step = plate_step

class XkmIdentLabel:
    __slots__ = "tech_type", "release_version"

    def __init__(self, tech_type: str, release_version: str, **kwargs: Any):
        self.tech_type = tech_type
        self.release_version = release_version

class DeviceIdentLabel:
    __slots__ = "fab_number", "fab_index", "tech_type", "mat_number", "swids"

    def __init__(self, fab_number: str, fab_index: int, tech_type: str, mat_number: int, swids: List[int], **kwargs: Any):
        self.fab_number = fab_number
        self.fab_index = fab_index
        self.tech_type = tech_type
        self.mat_number = mat_number
        self.swids = swids

class Ident:
    __slots__ = "type", "device_name", "device_ident_label", "xkm_ident_label"

    def __init__(self, type: TypeClass, device_name: str, device_ident_label: DeviceIdentLabel, xkm_ident_label: XkmIdentLabel, **kwargs: Any):
        self.type = type
        self.device_name = device_name
        self.device_ident_label = device_ident_label
        self.xkm_ident_label = xkm_ident_label

class Device:
    __slots__ = "ident", "state"

    def __init__(self, *, ident: str, state: str, **kwargs: Any):

        self.ident = ident
        self.state = state
