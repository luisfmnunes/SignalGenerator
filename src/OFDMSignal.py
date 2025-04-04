from .SignalBase import SignalBase
import numpy as np
import math

from dataclasses import dataclass

@dataclass
class OFDMSignal(SignalBase):

    frequency: int                     # Carrier frequency
    mod_order: int = 64                # Modulation order
    subcarriers: int = 64              # Number of subcarriers
    cp_len: int = 1                    # Length of cyclic prefix 
    duration_seconds: float = 1.0      # Duration of the signal in seconds
    num_streams: int = 4               # MIMO 4x4

    def __post_init__(self):
        self.samples_per_symbol = self.subcarriers + self.cp_len
        self.total_samples = int(self.sampleRate * self.duration_seconds)
        self.num_symbols = self.total_samples // self.samples_per_symbol

    def generate(self, filename = None):
        
        def generate_qam_symbols(n):
            M = int(np.sqrt(self.mod_order))
            real = 2 * (np.random.randint(0, M, n) - (M - 1)/2)
            imag = 2 * (np.random.randint(0, M, n) - (M - 1)/2)
            return (real + 1j * imag) / np.sqrt(10) # Power Normalization
        
        def generate_ofdm_signal():
            signal = []
            for _ in range(self.num_symbols):
                qam = generate_qam_symbols(self.subcarriers)
                ofdm_symbol = np.fft.ifft(qam)
                with_cp = np.concatenate([ofdm_symbol[-self.cp_len:], ofdm_symbol])
                signal.append(with_cp)
            return np.concatenate(signal)

        for ch in range(self.num_streams):
            iq_signal = generate_ofdm_signal()
            iq_signal /= np.max(np.abs(iq_signal)) #Normalization [-1, 1]
            
            i_data = np.int16(np.real(iq_signal) * 32767)
            q_data = np.int16(np.imag(iq_signal) * 32767)

            output = filename.parent / f"Channel_{ch+1}"

            with open(output / filename.with_suffix(".qid").name, "wb") as f:
                for i in range(q_data.size[0]):
                    f.write((int)(i_data[i]).to_bytes(2, byteorder='little', signed=True))
                    f.write((int)(q_data[i]).to_bytes(2, byteorder='little', signed=True))
                    
@dataclass
class MarkedOFDMSignal(SignalBase):

    frequency: int                     # Carrier frequency
    mod_order: int = 64                # Modulation order
    subcarriers: int = 64              # Number of subcarriers
    cp_len: int = 1                    # Length of cyclic prefix 
    duration_seconds: float = 1.0      # Duration of the signal in seconds
    num_streams: int = 4               # MIMO 4x4

    def __post_init__(self):
        self.samples_per_symbol = self.subcarriers + self.cp_len
        self.total_samples = int(self.sampleRate * self.duration_seconds)
        self.num_symbols = self.total_samples // self.samples_per_symbol

    def generate(self, filename = None):
        
        def generate_qam_symbols(n):
            M = int(np.sqrt(self.mod_order))
            real = 2 * (np.random.randint(0, M, n) - (M - 1)/2)
            imag = 2 * (np.random.randint(0, M, n) - (M - 1)/2)
            return (real + 1j * imag) / np.sqrt(10) # Power Normalization
        
        def generate_ofdm_signal():
            signal = []
            for _ in range(self.num_symbols):
                qam = generate_qam_symbols(self.subcarriers)
                ofdm_symbol = np.fft.ifft(qam)
                with_cp = np.concatenate([ofdm_symbol[-self.cp_len:], ofdm_symbol])
                signal.append(with_cp)
            return np.concatenate(signal)

        for ch in range(self.num_streams):
            iq_signal = generate_ofdm_signal()
            iq_signal /= np.max(np.abs(iq_signal)) #Normalization [-1, 1]
            
            i_data = np.int16(np.real(iq_signal) * 32767)
            q_data = np.int16(np.imag(iq_signal) * 32767)

            marker = np.zeros(len(iq_signal), dtype=np.uint8)
            for s in range(self.num_symbols):
                idx = s * (self.subcarriers + self.cp_len) + self.cp_len
                if idx < len(marker):
                    marker[idx] = 1

            output = filename.parent / f"Channel_{ch+1}"

            with open(output / filename.with_suffix(".qid").name, "wb") as f:
                for i in range(q_data.size[0]):
                    f.write((int)(i_data[i]).to_bytes(2, byteorder='little', signed=True))
                    f.write((int)(q_data[i]).to_bytes(2, byteorder='little', signed=True))