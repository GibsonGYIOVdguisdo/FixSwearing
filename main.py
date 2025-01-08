from typing import List
import socket
import speech_recognition as sr
import os
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

class BluetoothDevice:
    def __init__(self, mac_address: str):
        self.client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.client.connect(mac_address)
    
    def send(self, data: bytes):
        self.client.send(data)

def main():
    banned_words = BannedWords()
    r = sr.Recognizer() # Create recogniser instance
    mic = sr.Microphone() # Create microphone instance
    
    client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    client.connect(os.environ["MAX_ADDRESS"])

    while True: # Main loop
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
        except:
            text = ""

        if text != "" and banned_words.contains_banned_word(text):
            client.send(b"1")
        else:
            print(text)
    # r.recognize_sphinx(audio) works offline but is less accurate
    # r.recognize_google(audio) only works online but is very accurate

if __name__ == "__main__":
    main()