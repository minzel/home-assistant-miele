from typing import List, Any
from datetime import time
from enum import Enum, unique
from inflection import underscore

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

Status = {
    1: "off",
    2: "on",
    3: "programmed",
    4: "programmed_waiting_to_start",
    5: "running",
    6: "pause",
    7: "end_programmed",
    8: "failure",
    9: "programme_interrupted",
    10: "idle",
    11: "rinse_hold",
    12: "service",
    13: "superfreezing",
    14: "supercooling",
    15: "superheating",
    146: "supercooling_superfreezing",
    255: "not_connected"
}

ProgramType = {
    0: "normal_operation_mode",
    1: "own_program",
    2: "automatic_program",
    3: "cleaning_care_program"
}

ProgramPhase = {
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
    295: "steam_smoothing",
    # clothes dryer
    512: "not_running",
    513: "program_running",
    514: "drying",
    515: "machine_iron",
    516: "hand_iron",
    517: "normal",
    518: "normal_plus",
    519: "cooling_down",
    520: "hand_iron",
    521: "anti_crease",
    522: "finished",
    523: "extra_dry",
    524: "hand_iron",
    526: "moisten",
    528: "timed_drying",
    529: "warm_air",
    530: "steam_smoothing",
    531: "comfort_cooling",
    532: "rinse_out_lint",
    533: "rinses",
    534: "smoothing",
    538: "slightly_dry",
    539: "safety_cooling",
    # dishwasher
    1792: "not_running",
    1793: "reactivating",
    1794: "pre_wash",
    1795: "main wash",
    1796: "rinse",
    1797: "interim_rinse",
    1798: "final_rinse",
    1799: "drying",
    1800: "finished",
    1801: "pre_wash",
}

DryingStep = {
    0: "extra_dry",
    1: "normal_plus",
    2: "normal",
    3: "slightly_dry",
    4: "hand_iron_level_1",
    5: "hand_iron_level_2",
    6: "machine_iron"
}

VentilationStep = {
    0: "off",
    1: "step_1",
    2: "step_2",
    3: "step_3",
    4: "step_4"
}

class BaseType:
    __slots__ = "key_localized", "value_raw", "value_localized", "value"

    def __init__(self, type, *, key_localized, value_raw, value_localized, **kwargs: Any):
        self.key_localized = key_localized
        self.value_raw = value_raw
        self.value_localized = value_localized
  
        if(type == "Type"):
          self.value = globals()[type](self.value_raw).name
        else:
          self.value = globals()[type].get(self.value_raw, "unknown")

class Temperature:
    __slots__ = "value_raw", "value_localized", "unit"

    def __init__(self, value_raw, value_localized, unit, **kwargs: Any):
        self.value_raw = value_raw
        self.value_localized = value_localized
        self.unit = unit

class Time:
    __slots__ = "hour", "minute"

    def __init__(self, hour, minute):
      self.hour = hour
      self.minute = minute
    
    def __str__(self):
      return time(self.hour, self.minute).strftime('%H:%M')

class RemoteEnable:
    __slots__ = "fullRemoteControl", "smartGrid"

    def __init__(self, fullRemoteControl: bool, smartGrid: bool, **kwargs: Any):
        self.fullRemoteControl = fullRemoteControl
        self.smartGrid = smartGrid

    def __iter__(self):
      for prop in dir(self):
        if(prop[:2] != "__"):
          yield underscore(prop), getattr(self, prop)

class State():
    __slots__ = "programId", "status", "programType", "programPhase", "remainingTime", "startTime", "targetTemperature", "temperature", "signalInfo", "signalFailure", "signalDoor", "remoteEnable", "light", "elapsedTime", "spinningSpeed", "dryingStep", "ventilationStep", "plateStep"

    def __init__(self, deviceType, *, ProgramID, status, programType, programPhase, remainingTime, startTime, targetTemperature, temperature, signalInfo, signalFailure, signalDoor, remoteEnable, light, elapsedTime, spinningSpeed, dryingStep, ventilationStep, plateStep, **kwargs: Any):

        self.programId = BaseType("Status",**ProgramID)
        self.status = BaseType("Status",**status)
        self.programType = BaseType("ProgramType",**programType)
        self.programPhase = BaseType("ProgramPhase",**programPhase)
        self.remainingTime = Time(*remainingTime)
        self.startTime = Time(*startTime)
        
        self.targetTemperature = []
        targetTemperatures = [Temperature(**t) for t in targetTemperature]
        for i in range(len(targetTemperatures)):
          # if a temperature is not used/existing, its corresponding value is set to -32768.
          if(targetTemperatures[i].value_raw != -32768):
            self.targetTemperature.append(targetTemperatures[i])
        
        self.temperature = []
        for temperatureObj in [Temperature(**t) for t in temperature]:
          if(temperatureObj.value_raw != -32768):
            self.temperature.append(temperatureObj)
        
        self.signalInfo = signalInfo
        self.signalFailure = signalFailure
        self.signalDoor = signalDoor
        self.remoteEnable = RemoteEnable(**remoteEnable)
        self.light = light
        self.elapsedTime = Time(*elapsedTime)
        self.plateStep = plateStep
        self.spinningSpeed = BaseType("Status", **spinningSpeed)
        # this field is only valid for tumble dryers (2) and washer-dryer (24) combinations
        self.dryingStep = BaseType("DryingStep", **dryingStep) if deviceType in [2, 24] else None
        # this field is only valid for hoods (18)
        self.ventilationStep = BaseType("VentilationStep", **ventilationStep) if deviceType in [18] else None

    def __str__(self):
        return self.status.value

    def __iter__(self):
      for prop in dir(self):
        if(prop[:2] != "__"):
          value = getattr(self, prop)
          prop = underscore(prop)
          if(any([isinstance(value, bool), isinstance(value, int)])):
            yield prop, value
          elif(isinstance(value, BaseType)):
            yield prop, value.value_localized
          elif(isinstance(value, Time)):
            yield prop, str(value)
          elif(isinstance(value, RemoteEnable)):
            for v in value:
              yield v
          elif (isinstance(value, list)):
            for i in range(len(value)):
                key = "{0}_{1}".format(prop, (i+1)) if len(value) > 1 else prop
                if(isinstance(value[i], Temperature)):
                    yield key, value[i].value_localized


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
        self.type = BaseType("Type", **type)
        self.deviceName = deviceName
        self.deviceIdentLabel = DeviceIdentLabel(**deviceIdentLabel)
        self.xkmIdentLabel = XkmIdentLabel(**xkmIdentLabel)

class Device:
    __slots__ = "id", "ident", "state", "type"

    def __init__(self, id, *, ident, state, **kwargs: Any):
        self.id = id;
        self.ident = Ident(**ident)
        self.state = State(self.ident.type.value_raw, **state)
        self.type = self.ident.type.value
