from dataclasses import dataclass


@dataclass
class Device:
    name: str = ""
    dp: float = 0.0

    def get_dp(self):
        raise NotImplementedError


@dataclass
class Pipe25(Device):
    name: str = "Pipe DN25"
    dp: float = 0.5

    def get_dp(self):
        return self.dp
