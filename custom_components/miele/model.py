from typing import List, Any
from datetime import time
from enum import Enum, unique
from inflection import underscore
from datetime import datetime, timedelta

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

status = {
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

programType = {
    0: "normal_operation_mode",
    1: "own_program",
    2: "automatic_program",
    3: "cleaning_care_program"
}

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

dryingStep = {
    0: "extra_dry",
    1: "normal_plus",
    2: "normal",
    3: "slightly_dry",
    4: "hand_iron_level_1",
    5: "hand_iron_level_2",
    6: "machine_iron"
}

ventilationStep = {
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

        # fallback (e.g. spinningSpeed) -- maybe plateStep too
        if(type in ["ProgramID", "spinningSpeed", "plateStep"]):
            self.value = self.value_localized
        elif(type == "Type"):
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

class Sensor():

  __slots__ = "friendly_name", "state", "device_class", "unit_of_measurement", "attributes"

  def __init__(self, friendly_name, state, device_class = None, unit_of_measurement = None):
        self.friendly_name = friendly_name
        self.state = state
        self.device_class = device_class
        self.unit_of_measurement = unit_of_measurement
        self.attributes = {}
        #self.attributes = { 'friendly_name': friendly_name } -- better friendly_name support needed

class State():

    def __init__(self, deviceType, **kwargs: Any):

        for key, value in kwargs.items():

            if(key in ["signalDoor"]):
                setattr(self, key, Sensor(underscore(key), value, "door"))

            elif(key in ["signalFailure", "signalInfo"]):
                setattr(self, key, Sensor(underscore(key), value, "problem"))

            elif(any([isinstance(value, bool), isinstance(value, int)])):
                setattr(self, key, Sensor(underscore(key), value))

            elif(key in ["ProgramID", "status", "programType", "programPhase", "spinningSpeed"]):
                obj = BaseType(key, **value);
                setattr(self, key, Sensor(obj.key_localized, obj.value_localized))
                if(key == "status"):
                        self.state = obj.value

            elif(key == "dryingStep"):
                # this field is only valid for tumble dryers (2) and washer-dryer (24) combinations
                if deviceType in [2, 24]:
                  obj = BaseType(key, **value)
                  setattr(self, key, Sensor(obj.key_localized, obj.value_localized))

            elif(key == "ventilationStep"):
                # this field is only valid for hoods (18)
                if deviceType in [18]:
                  obj = BaseType(key, **value)
                  setattr(self, key, Sensor(obj.key_localized, obj.value_localized)) if deviceType in [18] else None

            elif(key == "remoteEnable"):
                for k, v in RemoteEnable(**value):

                    setattr(self, k, Sensor(k, v)) if v else None

            elif(key in ["remainingTime", "startTime", "elapsedTime"]):
                if value is not None:
                  state = Time(*value)
                  minutes = int(timedelta(hours=state.hour, minutes=state.minute).seconds / 60)

                  friendly_name = underscore(key.replace("Time", "")) # -- no real timestamps
                  setattr(self, friendly_name, Sensor(friendly_name, minutes, None, "min"))

                  if(key == "remainingTime"):
                    setattr(self, "finishTime", Sensor("finish_time", datetime.now() + timedelta(minutes=minutes) if minutes > 0 else "", "timestamp"))

            # -- api unreliable; temperature raw value -32768 not always set, exclude by device type

            elif("targettemperature" in key.lower()):
                if(isinstance(value, list)):
                    targetTemperatures = []
                    for t in [Temperature(**t) for t in value]:
                        
                        targetTemperatures.append(t)

                        if(deviceType in [1]): # washing machine supports only first target temperature
                            break
                    
                    # TODO duplicate code
                    for i in range(len(targetTemperatures)):
                        temperature = (int)(targetTemperatures[i].value_localized)
                        name = "{0}_{1}".format(key, (i+1)) if len(targetTemperatures) > 1 else key
                        setattr(self, name, Sensor(underscore(name), temperature if temperature > 0 else "", "temperature", "°C"))

            elif("temperature" in key.lower()):
                if(isinstance(value, list)):
                    targetTemperatures = []
                    for t in [Temperature(**t) for t in value]:

                        if(deviceType in [1]): # washing machine supports no more temperatures
                            break

                        targetTemperatures.append(t)
                    
                    # TODO duplicate code
                    for i in range(len(targetTemperatures)):
                        temperature = (int)(targetTemperatures[i].value_localized)
                        name = "{0}_{1}".format(key, (i+1)) if len(targetTemperatures) > 1 else key
                        setattr(self, name, Sensor(underscore(name), temperature if temperature > 0 else "", "temperature", "°C"))

                else:
                    setattr(self, key, Sensor(underscore(key), (int)(value["value_localized"]), "temperature", "°C"))

    def __str__(self):
        return self.state

    def __iter__(self):
        for prop in dir(self):
            if(prop[:2] != "__" and prop != "state"):
                yield underscore(prop), getattr(self, prop)

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
        self.id = id
        self.ident = Ident(**ident)
        self.state = State(self.ident.type.value_raw, **state)
        self.type = self.ident.type.value

        self.state.status.attributes.update({
            'serial_number': self.ident.deviceIdentLabel.fabNumber,
            'index': self.ident.deviceIdentLabel.fabIndex,
            'type': self.ident.deviceIdentLabel.techType,
            'material_number': self.ident.deviceIdentLabel.matNumber,
            'gateway_type': self.ident.xkmIdentLabel.techType,
            'gateway_version': self.ident.xkmIdentLabel.releaseVersion
        })

