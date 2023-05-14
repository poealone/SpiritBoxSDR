import numpy as np
from pyrtlsdr import RtlSdr
import sounddevice as sd
import asyncio

async def get_device_info():
    sdr = RtlSdr()
    devices = await sdr.get_device_list()
    return devices

async def main():
    while True:
        # Get available RTL-SDR devices
        devices = await sd.asyncio.run(get_device_info)

        if len(devices) == 0:
            print("No RTL-SDR devices found. Please make sure your device is connected.")
            input("Press Enter to try again...")
        else:
            # Print device index and name
            print("Available RTL-SDR devices:")
            for i, device in enumerate(devices):
                print(f"Device Index {i}: {device['name']}")

            # Prompt user for RTL-SDR device index
            device_index = int(input("Enter RTL-SDR device index: "))

            try:
                # RTL-SDR settings
                async with RtlSdr(device_index=device_index) as sdr:
                    # Audio settings
                    sample_rate = 44100  # Adjust according to your needs
                    duration = 1.0  # Duration of audio playback in seconds

                    # Spirit Box settings
                    carrier_freq = 1000  # Frequency of the carrier signal in Hz
                    modulation_freq = 10  # Frequency of the modulation signal in Hz
                    modulation_amp = 0.5  # Modulation amplitude

                    # Generate modulation signal
                    t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
                    modulation_signal = modulation_amp * np.sin(2 * np.pi * modulation_freq * t)

                    # Main loop
                    while True:
                        samples = await sdr.read_samples_async(1024)  # Read samples from RTL-SDR device

                        # Demodulate the received samples
                        audio_signal = np.real(samples)  # Use real component as audio signal

                        # Modulate the audio signal with the carrier signal
                        modulated_audio = np.sin(2 * np.pi * carrier_freq * t + audio_signal)

                        # Add modulation to the audio samples
                        output_audio = np.interleave(modulated_audio, modulation_signal)

                        # Play the audio
                        sd.play(output_audio, sample_rate)
                        sd.wait()

            except KeyboardInterrupt:
                # Stop audio playback and exit on keyboard interrupt
                sd.stop()
                break

asyncio.run(main())
