import numpy as np
import math
import ctypes

from datetime import datetime
from pathlib import Path

from dataclasses import dataclass

@dataclass
class SignalBase:
    samples: int
    sampleRate: int
    amplitude: int
    # data: np.ndarray = None

    def generate(self, filename: Path = None):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def getSignalType(self):
        return self.__class__.__name__

@dataclass
class SignalGeneratorBase:
    file: Path
    # samples: int
    # sampleRate: int
    version: str = "1.1"
    date: datetime = datetime.now()
    description: str = ""
    segmentId: int = 1
    markerBits: int = 8
    signal: SignalBase = None

    def write(self):
        if not self.signal:
            raise ValueError("Signal is not set.")

        self.signal.generate(self.file.with_suffix(".qid"))

        with open(self.file, "w") as f:
            f.write(f"version = {self.version}\n")
            f.write(f"dataFile = {self.file.stem}.qid\n")
            f.write(f"dateCreated = {self.date.strftime('%Y-%m-%d-%H:%M:%S')}\n")
            f.write(f"description = {self.description}\n")
            f.write(f"segmentID = {self.segmentId}\n")
            f.write(f"numberOfSamples = {self.signal.samples}\n")
            f.write(f"samplingRate = {self.signal.sampleRate}\n")
            f.write(f"markerBits = {self.markerBits}\n")
            f.write(f"signalType = {self.signal.getSignalType()}\n")