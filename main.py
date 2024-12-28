import speech_recognition as sr
r = sr.Recognizer() # Create recogniser instance
mic = sr.Microphone() # Create microphone instance

banned_words = []
with open("word_list.txt") as word_list:
    for word in word_list.readlines():
      banned_words.append(word.strip())

print(banned_words)
while True: # Main loo
  with mic as source:
    audio = r.listen(source)
  try:
    print(r.recognize_google(audio))
  except:
    print("Could not recognise")
# r.recognize_sphinx(audio) works offline but is less accurate
# r.recognize_google(audio) only works online but is very accurate