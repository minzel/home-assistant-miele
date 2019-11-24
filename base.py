from typing import Union

from .miele_api import MieleApi
from .model import Device

class MieleDevice:
    __slots__ = "device", "api"

    def __init__(self, device: Device, api: MieleApi):
        self.device = device
        self.api = api