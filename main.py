import os

from src.audio_processing import listen_for_wake_word
from src.ai_interaction import send_to_longchain

def main():
    os.makedirs('audio', exist_ok=True)
    transcript = listen_for_wake_word()
    send_to_longchain(transcript)


if __name__ == '__main__':
    main()
