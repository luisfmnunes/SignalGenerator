import math
import numpy as np
from .SignalBase import SignalBase

from dataclasses import dataclass

@dataclass
class IQSignal(SignalBase):

    frequency: int
    iValues: np.ndarray = None
    qValues: np.ndarray = None

    def __post_init__(self):

        self.iValues = np.ones(self.samples)
        self.qValues = np.ones(self.samples)

        for i in range(self.samples):
            self.iValues[i] = self.amplitude * math.sin(2 * math.pi * self.frequency / self.samples)
            self.qValues[i] = self.amplitude * math.cos(2 * math.pi * self.frequency / self.samples)

    def generate(self, filename = None):
        
        with open(filename, "wb") as f:
            for i in range(self.samples):
                f.write((int)(self.iValues[i]).to_bytes(2, byteorder='little', signed=True))
                f.write((int)(self.qValues[i]).to_bytes(2, byteorder='little', signed=True))



@dataclass
class MarkedIQSignal(SignalBase):

    frequency: int
    iValues: np.ndarray = None
    qValues: np.ndarray = None

    def __post_init__(self):

        self.iValues = np.ones(self.samples)
        self.qValues = np.ones(self.samples)
        self.markerBit = 0x00000001

        for i in range(self.samples):
            self.iValues[i] = self.amplitude * math.sin(2 * math.pi * self.frequency / self.samples)
            self.qValues[i] = self.amplitude * math.cos(2 * math.pi * self.frequency / self.samples)

    def generate(self, filename = None):
        
        with open(filename, "wb") as f:
            for i in range(self.samples):
                f.write((int)(self.markerBit).to_bytes(1, byteorder='little', signed=False))
                f.write((int)(self.iValues[i]).to_bytes(2, byteorder='little', signed=True))
                f.write((int)(self.qValues[i]).to_bytes(2, byteorder='little', signed=True))