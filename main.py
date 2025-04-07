import yaml

from src import SignalBase
from src import IQSignal
from src import OFDMSignal
from src import TextSignal

from pathlib import Path
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description="Signal Generator")
    parser.add_argument("config", type=Path, help="Path to the configuration file")
    return parser.parse_args()

def main(args):
    config = yaml.safe_load(args.config.read_text())

    signalGenrator = SignalBase.SignalGeneratorBase(
        file=Path(config["output"]),
        description=config["description"],
        segmentId=config["segmentId"],
    )

    # print(config["frequency"], type(config["frequency"]))

    if config["type"] == "IQ":
        signal = IQSignal.IQSignal(
            samples=config["samples"],
            amplitude=config["amplitude"],
            frequency=config["frequency"],
            sampleRate=int(config["samplingRate"]),
        )
    elif config["type"] == "mIQ":
        signal = IQSignal.MarkedIQSignal(
            samples=config["samples"],
            amplitude=config["amplitude"],
            frequency=config["frequency"],
            sampleRate=int(config["samplingRate"]),
        )
    elif config["type"] == "TIQ":
        signal = TextSignal.IQTextSignal(
            samples=config["samples"],
            amplitude=config["amplitude"],
            frequency=config["frequency"],
            sampleRate=int(config["samplingRate"]),
            text=config["text"],
            # mod=config["modulation"],
        )
    elif config["type"] == "mTIQ":
        signal = TextSignal.MarkedIQTextSignal(
            samples=config["samples"],
            amplitude=config["amplitude"],
            frequency=config["frequency"],
            sampleRate=int(config["samplingRate"]),
            text=config["text"],
            # mod=config["modulation"],
        )
    elif config["type"] == "OFDM":
        signal = OFDMSignal.OFDMSignal(
            samples=config["samples"],
            amplitude=config["amplitude"],
            frequency=config["frequency"],
        )
    else:
        raise ValueError("Invalid signal type")
    
    signalGenrator.signal = signal
    signalGenrator.write()

if __name__ == "__main__":
    main(parse_args())
