import speech_recognition as sr
import webbrowser
import pyttsx3
import music_Library
import requests


recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "2996705e68164cb9a86f35556a22e597"

def speak(text):
    print("[JARVIS REPLY]:", text)   # Jarvis ka reply kya aya show karta hai.
    engine = pyttsx3.init("sapi5")   # fresh engine each time
    engine.say(text)
    engine.runAndWait()

def simple_ai_reply(ai_cmd):

    ai_cmd = ai_cmd.lower()

    if "how r u" in ai_cmd:
        return "I am fine, how are you?"
    
    elif "your name" in ai_cmd:
        return "I am Jarvis, your assistant."
    
    elif "climate check" in ai_cmd:
        return "I cannot check live weather without API, but I can search on Google for you."

    else:
        return "Sorry, I cannot answer that right now, but I will learn soon."


# Web Sites Ko Open Karne ka Fucntion
def processCommand(c):
    print("[DEBUG] type of c:", type(c))
    print("[DEBUG] has lower:", hasattr(c, "lower"))
    c = str(c).casefold() 

    if "open google" in c:
        webbrowser.open("https://google.com")

    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")

    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")

    elif c.lower().startswith("play"):          # Songs Library
        song = "".join (c.lower().split(" ")[1:])
        if song in music_Library.music:
            links = music_Library.music[song]
            webbrowser.open(links)
        else:
            speak("Sorry, song not found in library")


    elif "news" in c.lower():
        # r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apikey={newsapi}")
        r = requests.get(f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apikey={newsapi}")
        print("API Response Code:", r.status_code)


        if r.status_code == 200:
            # pasre the JSON response
            data = r.json()
            print("Sample JSON:", r.json())

            # Extract the articles
            articles = data.get("articles", [])

            # Prints the Headlines
            for article in articles[:3]:
                speak(article['title'])

    else:
        reply = simple_ai_reply(c)
        speak(reply)


if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
    # Listen for the wake word "Jarvis"
    # Obtain audio from the Microphone
        r = sr.Recognizer()

        print("Recognizing...")

        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = r.listen(source, timeout=3, phrase_time_limit=3)

            word = r.recognize_google(audio)
            print(f"[DEBUG] Recognizer heard: {word}")    # ye apun kya bol rahe hai wo show karega

            if "jarvis" in word.lower():
                speak("Ya")

                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source)
                    print("Jarvis Active")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    print(f"[DEBUG] Recognizer heard: {command}")
                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))
