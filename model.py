from typing import List, Any
from enum import Enum, unique

@unique
class Type(Enum):
    WASHING_MACHINE = 1
    TUMBLE_DRYER = 2
    DISHWASHER = 7
    DISHWASHER_SEMI_PROF = 8
    OVEN = 12
    OVEN_MICROWAVE = 13
    HOB_HIGHLIGHT = 14
    STEAM_OVEN = 15
    MICROWAVE = 16
    COFFEE_SYSTEM = 17
    HOOD = 18
    FRIDGE = 19
    FREEZER = 20
    FRIDGE_FREEZER_COMBINATION = 21
    VACUUM_CLEANER = 23
    WASHER_DRYER = 24
    DISH_WARMER = 25
    HOB_INDUCTION = 27
    HOB_GAS = 28
    STEAM_OVEN_COMBINATION = 31
    WINE_CABINET = 32
    WINE_CONDITIONING_UNIT = 33
    WINE_STORAGE_CONDITIONING_UNIT = 34
    DOUBLE_OVEN = 39
    DOUBLE_STEAM_OVEN = 40
    DOUBLE_STEAM_OVEN_COMBINATION = 41
    DOUBLE_MICROWAVE = 42
    DOUBLE_MICROWAVE_OVEN = 43
    STEAM_OVEN_MICROWAVE_COMBINATION = 45
    VACUUM_DRAWER = 48
    DIALOGOVEN = 67
    WINE_CABINET_FREEZER_COMBINATION = 68

@unique
class Status(Enum):
    OFF = 1
    ON = 2
    PROGRAMMED = 3
    PROGRAMMED_WAITING_TO_START = 4
    RUNNING = 5
    PAUSE = 6
    END_PROGRAMMED = 7
    FAILURE = 8
    PROGRAMME_INTERRUPTED = 9
    IDLE = 10
    RINSE_HOLD = 11
    SERVICE = 12
    SUPERFREEZING = 13
    SUPERCOOLING = 14
    SUPERHEATING = 15
    SUPERCOOLING_SUPERFREEZING = 146
    NOT_CONNECTED = 255

class TypeClass:
    __slots__ = "key_localized", "value_raw", "value_localized"

    def __init__(self, key_localized, value_raw, value_localized, **kwargs: Any):
        self.key_localized = key_localized
        self.value_raw = value_raw
        self.value_localized = value_localized

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
    
    def getState():
        return Status(self.state.status.value_raw).name

