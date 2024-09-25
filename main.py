import os

from src.audio_processing import listen_for_wake_word, play_audio

def main():
    os.makedirs('audio', exist_ok=True)
    listen_for_wake_word()

if __name__ == '__main__':
    main()
