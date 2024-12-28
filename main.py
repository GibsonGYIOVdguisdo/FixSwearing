import speech_recognition as sr
r = sr.Recognizer() # Create recogniser instance
mic = sr.Microphone() # Create microphone instance

banned_words = []
with open("word_list.txt") as word_list:
    for word in word_list.readlines():
      banned_words.append(word.strip())

def contains_bad_words(string):
  words = string.split()
  for word in words:
    for banned_word in banned_words:
      if word.lower() == banned_word.lower():
        return True
  return False

print(f"banned_words: {banned_words}")

while True: # Main loo
  with mic as source:
    audio = r.listen(source)
  try:
    text = r.recognize_google(audio)
  except:
    text = ""
  print(text)
  print(contains_bad_words(text))

# r.recognize_sphinx(audio) works offline but is less accurate
# r.recognize_google(audio) only works online but is very accurate