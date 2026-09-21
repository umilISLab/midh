import matplotlib.pyplot as plt
import numpy as np

CONTINUOUS_RATE = 200000


def tone(frequency: float, duration: float, rate: int, harmonics: int = 1) -> np.ndarray:
    t = np.arange(int(rate * duration)) / rate
    signal = sum(np.sin(2 * np.pi * frequency * k * t) / k for k in range(1, harmonics + 1))
    return signal / np.max(np.abs(signal))


def quantize_audio(signal: np.ndarray, bits: int) -> np.ndarray:
    levels = 2 ** bits
    return np.clip(np.floor((signal + 1) / 2 * levels), 0, levels - 1).astype(int)


def dequantize_audio(codes: np.ndarray, bits: int) -> np.ndarray:
    levels = 2 ** bits
    return (codes + 0.5) / levels * 2 - 1


def show_sampling(frequency: float, rates: list, duration: float = 0.005) -> None:
    _, axes = plt.subplots(len(rates), 1, figsize=(10, 2.6 * len(rates)), sharex=True)
    smooth = tone(frequency, duration, CONTINUOUS_RATE)
    smooth_time = np.arange(len(smooth)) / CONTINUOUS_RATE * 1000

    for ax, rate in zip(axes, rates):
        samples = tone(frequency, duration, rate)
        sample_time = np.arange(len(samples)) / rate * 1000
        ax.plot(smooth_time, smooth, color="lightgray", label="onda originale")
        ax.stem(sample_time, samples, basefmt=" ")
        ax.set_title(f"{rate:,} campioni al secondo: {len(samples)} numeri in {duration * 1000:.0f} ms")
        ax.set_ylabel("ampiezza")
    axes[-1].set_xlabel("tempo (ms)")
    plt.tight_layout()
    plt.show()


def show_bit_depth(frequency: float, bits_list: list, rate: int = 44100, duration: float = 0.005) -> None:
    _, axes = plt.subplots(len(bits_list), 1, figsize=(10, 2.6 * len(bits_list)), sharex=True)
    signal = tone(frequency, duration, rate)
    time = np.arange(len(signal)) / rate * 1000

    for ax, bits in zip(axes, bits_list):
        codes = quantize_audio(signal, bits)
        ax.plot(time, signal, color="lightgray", label="onda originale")
        ax.step(time, dequantize_audio(codes, bits), where="mid")
        ax.set_title(f"{bits} bit per campione: {2 ** bits} livelli possibili")
        ax.set_ylabel("ampiezza")
    axes[-1].set_xlabel("tempo (ms)")
    plt.tight_layout()
    plt.show()


def print_audio_sizes(seconds: int = 180) -> None:
    formats = [
        ("Telefono (8 kHz, 8 bit, mono)", 8000, 8, 1),
        ("CD (44,1 kHz, 16 bit, stereo)", 44100, 16, 2),
        ("Studio (96 kHz, 24 bit, stereo)", 96000, 24, 2),
    ]
    print(f"{'formato':<36}{'byte al secondo':>18}{f'{seconds // 60} minuti (MB)':>18}")
    for name, rate, bits, channels in formats:
        per_second = rate * bits // 8 * channels
        print(f"{name:<36}{per_second:>18,}{per_second * seconds / 1e6:>18,.1f}")

    mp3_per_second = 128000 // 8
    cd_per_second = 44100 * 16 // 8 * 2
    print(f"\nUn MP3 a 128 kbit/s: {mp3_per_second:,} byte al secondo, {mp3_per_second * seconds / 1e6:,.1f} MB "
          f"(circa {cd_per_second / mp3_per_second:.0f} volte meno del CD)")


def note(rate: int, bits: int, frequency: float = 440, duration: float = 1.5, harmonics: int = 10) -> np.ndarray:
    signal = tone(frequency, duration, rate, harmonics)
    return dequantize_audio(quantize_audio(signal, bits), bits)
