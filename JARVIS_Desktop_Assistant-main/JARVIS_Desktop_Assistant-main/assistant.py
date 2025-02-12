import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# here [0] represents male voice and [1] represents female's voice in the system
engine.setProperty('voice', voices[0].id)  # getting details of current voice

def open_website_in_chrome(url):
    # Path to your Google Chrome executable
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    webbrowser.get('chrome').open(url)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# WISHME is a function which wishes the user
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("GOOD MORNING SIR")
    elif hour >= 12 and hour < 18:
        speak("GOOD AFTERNOON SIR")
    else:
        speak("GOOD EVENING SIR")
    speak("I am your Personal AI Assistant Jarvis. Please tell me how may I help you")

def takeCommand():
    # it takes microphone input from user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=5)
        print("Listening....")
        r.pause_threshold = 1
        try:
            # Stop listening after 5 seconds of no input
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
            speak("I didn't catch anything. Please try again.")
            return "None"
    try:
        print("Recognising...")
        query = r.recognize_google(audio, language='en-in')  # recognize speech using Google Speech Recognition
        print(f"User said: {query}\n")  # User query will be printed.
    except Exception as e:
        print(e)
        print("Say that again please...")  # Say that again will be printed in case of improper voice
        return "None"
    return query

if __name__ == "__main__":
    wishMe()
    # here we have commented while loop because if we don't the system will continue
    # to listen to the user even if one command is completed so now
    # the system will stop listening after one command is complete
    # while True:
    if 1:
        query = takeCommand().lower()  # Converting user query into lower case
        # logic for executing take based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            # here sentences=2 means that Jarvis will read 1 sentence from wikipedia it can be changed to any desired
            results = wikipedia.summary(query, sentences=5)
            speak("According to Wikipedia")
            print(results)
            speak(results)


        elif 'open youtube' in query:
            open_website_in_chrome("http://youtube.com")
        elif 'open google' in query:
            open_website_in_chrome("http://google.com")
        elif 'the time' in query:
            # (%H:%M:%S) this will give the time in the specified format strtime = string time
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        elif 'open visual studio code' in query:
            codePath = r"C:\Users\nanda\AppData\Local\Programs\Microsoft VS Code\Code.exe"  # Update this path if your Visual Studio version or installation path is different
            os.startfile(codePath)
        elif 'open visual studio' in query:
            vsPath = r"C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.exe"  # Update this path if your Visual Studio version or installation path is different
            os.startfile(vsPath)
        else:
            speak("Sorry, I can't understand what you are saying")
