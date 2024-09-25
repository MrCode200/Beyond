import pyaudio
import wave
import speech_recognition as sr

# must be later set from config.ini
WAKE_WORD = "hey Beyond"

FORMAT = pyaudio.paInt16

def listen_for_wake_word(wake_word, threshold=0.5, duration=None):
    """
    Listens continuously for a wake word and records audio until silence is detected.

    Args:
    :keyword wake_word: The word that will trigger the recording.
    :keyword threshold: Minimum length of silence in seconds to stop recording.
    :keyword duration: Maximum duration of each audio chunk. If `None`, recording is indefinite.
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise... Please wait")
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 0.5
        recognizer.energy_threshold = 500
        print("Listening for wake word")

        while True:
            audio = recognizer.listen(source)

            try:
                transcription = recognizer.recognize_google(audio)
                print(f"You said: {transcription}")

                if wake_word.lower() in transcription.lower():
                    print("Wake word detected! Starting recording...")
                    record_audio(threshold)

            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")


def record_audio(pause_threshold):
    """
    Records audio until silence is detected.
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise... Please wait")
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 0.6
        recognizer.energy_threshold = 500

        print("Recording... (talk and I'll stop recording when you're done)")
        audio_data = []

        try:
            audio_chunk = recognizer.listen(source)
            audio_data.append(audio_chunk)

        except sr.WaitTimeoutError:
            print("Silence detected. Stopping recording.")

        print("Finished recording.")

        # Combine all audio chunks into a single AudioData object
        combined_audio = sr.AudioData(b''.join([chunk.get_raw_data() for chunk in audio_data]),
                                      sample_rate=audio_data[0].sample_rate,
                                      sample_width=audio_data[0].sample_width)

        # Save the recorded data as a WAV file
        with wave.open("recorded_audio.wav", 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(combined_audio.sample_width)
            wf.setframerate(combined_audio.sample_rate)
            wf.writeframes(combined_audio.get_raw_data())


if __name__ == '__main__':
    listen_for_wake_word(WAKE_WORD)
