import pyaudio
import wave

from src.constants import CHUNK, AUDIO_PATH

def play_audio():
    """
    plays_the_audio from the audio dir as written in AUDIO_PATH in constants.py
    """

    # To play back the recorded audio
    print("Playing back...")
    wf = wave.open(AUDIO_PATH, 'rb')
    play_audio = pyaudio.PyAudio()

    stream = play_audio.open(format=play_audio.get_format_from_width(wf.getsampwidth()),
                              channels=wf.getnchannels(),
                              rate=wf.getframerate(),
                              output=True)

    data = wf.readframes(CHUNK)

    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    play_audio.terminate()


if __name__ == '__main__':
    play_audio()