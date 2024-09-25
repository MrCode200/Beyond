# Audio libraries
import speech_recognition as sr

from src.constants import KEYWORD_THRESHOLD, RECORDER_THRESHOLD, WAKE_WORD

def listen_for_wake_word(wake_word = WAKE_WORD, keyword_threshold=KEYWORD_THRESHOLD, recorder_threshold=RECORDER_THRESHOLD):
    """
    Listens continuously for a wake word and records audio until silence is detected.

    Args:
    :keyword wake_word: The word that will trigger the recording.
    :keyword keyword_threshold: Maximum length of silence in seconds to start recording.
    :keyword recorder_threshold: Maximum length of silence in seconds to stop recording.
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise... Please wait")
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = keyword_threshold
        recognizer.non_speaking_duration = keyword_threshold if recognizer.pause_threshold < recognizer.non_speaking_duration else 0.5
        recognizer.energy_threshold = 500
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


def record_audio(pause_threshold) -> str:
    """
    Records audio until silence is detected.

    :param pause_threshold: The amount of silence it waits to detect in seconds
    :retur: the transcription of what you said
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Adjusting for ambient noise... Please wait")
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = pause_threshold
        recognizer.non_speaking_duration = pause_threshold if recognizer.pause_threshold < recognizer.non_speaking_duration else 0.5

        recognizer.energy_threshold = 500

        print("Recording... (talk and I'll stop recording when you're done)")
        """audio_data = []"""

        try:
            audio = recognizer.listen(source)
            """audio_data.append(audio_chunk)"""

        except sr.WaitTimeoutError:
            print("Silence detected. Stopping recording.")

        print("Finished recording.")
        try:
            print("Transcribing")
            transcription = recognizer.recognize_google(audio)
            print(f"You said: {transcription}")
            return transcription
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")


if __name__ == '__main__':
    listen_for_wake_word(WAKE_WORD)
