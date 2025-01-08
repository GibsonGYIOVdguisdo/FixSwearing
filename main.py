from typing import List
import socket
import speech_recognition as sr
import os
import threading
class BannedWords:

    BANNED_WORD_FILE = "word_list.txt"

    def __init__(self):
        """Initialise banned words"""
        self._banned_words = self._get_banned_words_from_file()

    @classmethod
    def _get_banned_words_from_file(cls) -> List[str]:
        """Return list of banned words from file"""
        banned_words = []
        with open(cls.BANNED_WORD_FILE) as fh:
            return [
                word.strip()
                for word in fh.readlines()
            ]
        return banned_words

    def contains_banned_word(self, text: str) -> bool:
        """Check if text contains a bad word"""
        words = text.split()
        for word in words:
            for banned_word in self._banned_words:
                if word.lower().startswith(banned_word.lower()):
                    return True
        return False
    
def processAudio(r, audio, client, banned_words):
    try:
        text = r.recognize_google(audio)
    except:
        text = ""

    if text != "" and banned_words.contains_banned_word(text):
        client.send(b"1")
    print(text)

def main():
    banned_words = BannedWords()
    r = sr.Recognizer() # Create recogniser instance
    mic = sr.Microphone() # Create microphone instance
    
    client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    client.connect(os.environ["MAC_ADDRESS"])
    client = None
    while True: # Main loop
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(mic, duration=5)
        threading.Thread(target=processAudio, args=[r, audio, client, banned_words]).start()
    # r.recognize_sphinx(audio) works offline but is less accurate
    # r.recognize_google(audio) only works online but is very accurate

if __name__ == "__main__":
    main()