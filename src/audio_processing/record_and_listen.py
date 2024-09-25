import os
# Audio libraries
import pyaudio
import wave
import speech_recognition as sr

from src.constants import AUDIO_PATH, KEYWORD_THRESHOLD, RECORDER_THRESHOLD, WAKE_WORD, ENERGY_THRESHOLD

# must be later set from config.ini

FORMAT = pyaudio.paInt16

def listen_for_wake_word(wake_word = WAKE_WORD, keyword_threshold=KEYWORD_THRESHOLD, recorder_threshold=RECORDER_THRESHOLD, energy_threshold=ENERGY_THRESHOLD):
    """
    Listens continuously for a wake word and records audio until silence is detected.

    Args:
    :keyword wake_word: The word that will trigger the recording.
    :keyword keyword_threshold: Maximum length of silence in seconds to start recording.
    :keyword recorder_threshold: Maximum length of silence in seconds to stop recording.
    :keyword energy_threshold: Sadly couldnt find anything about it, It starts recording from that energythreshold up
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise... Please wait")
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = keyword_threshold
        recognizer.non_speaking_duration = keyword_threshold if recognizer.pause_threshold < recognizer.non_speaking_duration else 0.5
        recognizer.energy_threshold = energy_threshold
        print("Listening for wake word")

        while True:
            audio = recognizer.listen(source)

            try:
                transcription = recognizer.recognize_google(audio)
                print(f"You said: {transcription}")

                if wake_word.lower() in transcription.lower():
                    print("Wake word detected! Starting recording...")
                    record_audio(recorder_threshold)
                    print("Listening again for wake word")

            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")


def record_audio(pause_threshold):
    """
    Records audio until silence is detected.

    :param pause_threshold: The amount of silence it waits to detect in seconds
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise... Please wait")
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = pause_threshold
        recognizer.non_speaking_duration = pause_threshold if recognizer.pause_threshold < recognizer.non_speaking_duration else 0.5
        recognizer.energy_threshold = ENERGY_THRESHOLD

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
        audio_file_path = os.path.join(os.path.dirname(__file__), AUDIO_PATH)

        with wave.open(audio_file_path, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(combined_audio.sample_width)
            wf.setframerate(combined_audio.sample_rate)
            wf.writeframes(combined_audio.get_raw_data())


if __name__ == '__main__':
    listen_for_wake_word(WAKE_WORD)
