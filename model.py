from typing import List, Any
from enum import Enum, unique
import sys

@unique
class Type(Enum):
    washing_machine = 1
    tumble_dryer = 2
    dishwasher = 7
    dishwasher_semi_prof = 8
    oven = 12
    oven_microwave = 13
    hob_highlight = 14
    steam_oven = 15
    microwave = 16
    coffee_system = 17
    hood = 18
    fridge = 19
    freezer = 20
    fridge_freezer_combination = 21
    vacuum_cleaner = 23
    washer_dryer = 24
    dish_warmer = 25
    hob_induction = 27
    hob_gas = 28
    steam_oven_combination = 31
    wine_cabinet = 32
    wine_conditioning_unit = 33
    wine_storage_conditioning_unit = 34
    double_oven = 39
    double_steam_oven = 40
    double_steam_oven_combination = 41
    double_microwave = 42
    double_microwave_oven = 43
    steam_oven_microwave_combination = 45
    vacuum_drawer = 48
    dialogoven = 67
    wine_cabinet_freezer_combination = 68

@unique
class Status(Enum):
    off = 1
    on = 2
    programmed = 3
    programmed_waiting_to_start = 4
    running = 5
    pause = 6
    end_programmed = 7
    failure = 8
    programme_interrupted = 9
    idle = 10
    rinse_hold = 11
    service = 12
    superfreezing = 13
    supercooling = 14
    superheating = 15
    supercooling_superfreezing = 146
    not_connected = 255

@unique
class ProgramType(Enum):
    normal_operation_mode = 0
    own_program = 1
    automatic_program = 2
    cleaning_care_program = 3

programPhase = {
    # washing machine
    256: "not_running",
    257: "pre_wash",
    258: "soak",
    259: "pre_wash",
    260: "main_wash",
    261: "rinse",
    262: "rinse_hold",
    263: "main_wash",
    264: "cooling_down",
    265: "drain",
    266: "spin",
    267: "anti_crease",
    268: "finished",
    269: "venting",
    270: "starch_stop",
    271: "freshen_up_moisten",
    272: "steam_smoothing",
    279: "hygiene",
    280: "drying",
    285: "disinfection",
    295: "steam_smoothing"
}

class TypeClass:
    __slots__ = "key_localized", "value_raw", "value_localized", "value"

    def __init__(self, key_localized, value_raw, value_localized, **kwargs: Any):
        self.key_localized = key_localized
        self.value_raw = value_raw
        self.value_localized = value_localized

        self.value = str_to_class(programPhase).get(value_raw, "unknown")

    def str_to_class(classname):
        return getattr(sys.modules[__name__], classname)

class Temperature:
    __slots__ = "value_raw", "value_localized", "unit"

    def __init__(self, value_raw, value_localized, unit, **kwargs: Any):
        self.value_raw = value_raw
        self.value_localized = value_localized
        self.unit = unit

class RemoteEnable:
    __slots__ = "fullRemoteControl", "smartGrid"

    def __init__(self, fullRemoteControl: bool, smartGrid: bool, **kwargs: Any):
        self.fullRemoteControl = fullRemoteControl
        self.smartGrid = smartGrid

class State:
    __slots__ = "programId", "status", "programType", "programPhase", "remainingTime", "startTime", "targetTemperature", "temperature", "signalInfo", "signalFailure", "signalDoor", "remoteEnable", "light", "elapsedTime", "spinningSpeed", "dryingStep", "ventilationStep", "plateStep"

    def __init__(self, ProgramID, status, programType, programPhase, remainingTime, startTime, targetTemperature, temperature, signalInfo, signalFailure, signalDoor, remoteEnable, light, elapsedTime, spinningSpeed, dryingStep, ventilationStep, plateStep, **kwargs: Any):
        self.programId = TypeClass(**ProgramID)
        self.status = TypeClass(**status)
        self.programType = TypeClass(**programType)
        self.programPhase = TypeClass(**programPhase)
        self.remainingTime = remainingTime
        self.startTime = startTime
        self.targetTemperature = [Temperature(**t) for t in targetTemperature]
        self.temperature = [Temperature(**t) for t in temperature]
        self.signalInfo = signalInfo
        self.signalFailure = signalFailure
        self.signalDoor = signalDoor
        self.remoteEnable = RemoteEnable(**remoteEnable)
        self.light = light
        self.elapsedTime = elapsedTime
        self.spinningSpeed = TypeClass(**spinningSpeed)
        self.dryingStep = TypeClass(**dryingStep)
        self.ventilationStep = TypeClass(**ventilationStep)
        self.plateStep = plateStep

    def __iter__(self):
        for prop in dir(self):
            if(prop[:2] != "__"):
                value = getattr(self, prop)
                if(isinstance(value,TypeClass)):
                    yield prop, value.value

class XkmIdentLabel:
    __slots__ = "techType", "releaseVersion"

    def __init__(self, techType, releaseVersion, **kwargs: Any):
        self.techType = techType
        self.releaseVersion = releaseVersion

class DeviceIdentLabel:
    __slots__ = "fabNumber", "fabIndex", "techType", "matNumber", "swids"

    def __init__(self, fabNumber, fabIndex, techType, matNumber, swids: List[int], **kwargs: Any):
        self.fabNumber = fabNumber
        self.fabIndex = fabIndex
        self.techType = techType
        self.matNumber = matNumber
        self.swids = swids

class Ident:
    __slots__ = "type", "deviceName", "deviceIdentLabel", "xkmIdentLabel"

    def __init__(self, type, deviceName, deviceIdentLabel, xkmIdentLabel, **kwargs: Any):
        self.type = TypeClass(**type)
        self.deviceName = deviceName
        self.deviceIdentLabel = DeviceIdentLabel(**deviceIdentLabel)
        self.xkmIdentLabel = XkmIdentLabel(**xkmIdentLabel)

class Device:
    __slots__ = "ident", "state"

    def __init__(self, *, ident, state, **kwargs: Any):
        self.ident = Ident(**ident)
        self.state = State(**state)

    def getId(self):
        return self.ident.deviceIdentLabel.fabNumber

    def getName(self):
        return "{} [{}]".format(self.ident.type.value_localized, self.getId())

    def getType(self):
        return Type(self.ident.type.value_raw).name

    def getState(self):
        return Status(self.state.status.value_raw).name
