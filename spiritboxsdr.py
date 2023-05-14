import numpy as np
from rtlsdr import RtlSdr
import sounddevice as sd

# Get available RTL-SDR devices
devices = RtlSdr.get_device_info()

if len(devices) == 0:
    print("No RTL-SDR devices found. Please make sure your device is connected.")
else:
    # Print device index and name
    print("Available RTL-SDR devices:")
    for i, device in enumerate(devices):
        print(f"Device Index {i}: {device['name']}")

    # Prompt user for RTL-SDR device index
    device_index = int(input("Enter RTL-SDR device index: "))

    # RTL-SDR settings
    sdr = RtlSdr(device_index=device_index)
    sdr.sample_rate = 2.4e6  # Adjust according to your needs

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
        samples = sdr.read_samples(1024)  # Read samples from RTL-SDR device

        # Demodulate the received samples
        audio_signal = np.real(samples)  # Use real component as audio signal

        # Modulate the audio signal with the carrier signal
        modulated_audio = np.sin(2 * np.pi * carrier_freq * t + audio_signal)

        # Add modulation to the audio samples
        output_audio = np.interleave(modulated_audio, modulation_signal)

        # Play the audio
        sd.play(output_audio, sample_rate)
        sd.wait()
