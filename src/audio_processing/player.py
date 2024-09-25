import soundfile as sf
import sounddevice as sd
import wave

from src.constants import AUDIO_PATH

def play_audio():
    print("Playing back...")
    # Read the audio file
    data, samplerate = sf.read(AUDIO_PATH)

    # Play the audio without blocking
    sd.play(data, samplerate)

    # Optionally, you can check the playback status
    while sd.get_stream().active:
        print("Audio is playing...")

    print("Finished playback.")


if __name__ == '__main__':
    play_audio()