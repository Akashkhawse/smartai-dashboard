import speech_recognition as sr
import pyttsx3

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)  # background noise adjust
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print("You said:", command)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError:
            speak("Network error.")
            return ""

if __name__ == "__main__":
    speak("Hello Akash, I am your SmartAI Assistant. How can I help you?")
    while True:
        command = listen()

        if "hello" in command:
            speak("Hello! How are you?")
        elif "time" in command:
            import datetime
            speak(f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}")
        elif "stop" in command or "exit" in command:
            speak("Goodbye Akash!")
            break

