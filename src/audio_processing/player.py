import pyaudio
import wave

from src.constants import CHUNK, WAVE_OUTPUT_FILENAME

def play_audio(audio_filename):
    # To play back the recorded audio
    print("Playing back...")
    wf = wave.open(audio_filename, 'rb')
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
    play_audio(WAVE_OUTPUT_FILENAME)