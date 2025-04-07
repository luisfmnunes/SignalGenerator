import math
import numpy as np
from .IQSignal import IQSignal, MarkedIQSignal
from .SignalBase import SignalGeneratorBase

from dataclasses import dataclass
from scipy.signal import resample_poly

@dataclass
class IQTextSignal(IQSignal):

    text: str = "Hallo"
    mod: str = "QPSK"
    samples_per_symbol: int = 10

    def __post_init__(self):
        self.byte_data = self.text.encode('utf-8')
        self.bit_array = np.unpackbits(np.frombuffer(self.byte_data, dtype=np.uint8))

        def qpsk_mod(bits):

            self.iValues = np.zeros(len(bits) // 2)
            self.qValues = np.zeros(len(bits) // 2)

            symbols = []
            for i in range(0, len(bits), 2):
                b1 = bits[i] if i < len(bits) else 0
                b2 = bits[i + 1] if i + 1 < len(bits) else 0
                self.iValues[i//2] = (1 if b1 == 0 else -1)
                self.qValues[i//2] = (1 if b2 == 0 else -1)
                
                symbols.append((self.iValues[i//2], self.qValues[i//2]))

            return np.array(symbols)
        
        def resample(signal):
            signal = resample_poly(signal, self.samples_per_symbol, 1)
            return np.int16(np.clip(signal * self.amplitude, -32768, 32767))

        self.symbols = qpsk_mod(self.bit_array) if self.mod == "QPSK" else None
        
        self.iValues = resample(self.iValues)
        self.qValues = resample(self.qValues)
        self.samples = len(self.iValues)

@dataclass
class MarkedIQTextSignal(MarkedIQSignal, IQTextSignal):
    
    def __post_init__(self):
        IQTextSignal.__post_init__(self)
        self.markers = np.zeros(self.samples, dtype=np.uint8)
        self.markers[0] = self.markerBit

# @dataclass
# class TextGenerator(SignalGeneratorBase):
