import speech_recognition as sr

def get_banned_words():
    banned_words = []
    with open("word_list.txt") as word_list:
        for word in word_list.readlines():
            banned_words.append(word.strip())
    return banned_words

def contains_bad_words(text):
    banned_words = get_banned_words()
    words = text.split()
    for word in words:
        for banned_word in banned_words:
            if word.lower() == banned_word.lower():
                return True
    return False

def bad_word_found():
    print("run stuff")

def main():
    r = sr.Recognizer() # Create recogniser instance
    mic = sr.Microphone() # Create microphone instance
    print("began listening")
    while True: # Main loo
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
        except:
            text = ""
        if text != "" and contains_bad_words(text):
            bad_word_found()
        else:
            print(text)
    # r.recognize_sphinx(audio) works offline but is less accurate
    # r.recognize_google(audio) only works online but is very accurate

if __name__ == "__main__":
    main()