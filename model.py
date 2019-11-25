from typing import List, Any

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

