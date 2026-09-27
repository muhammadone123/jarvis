import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import subprocess

# -----------------------------
# JARVIS SETUP
# -----------------------------

engine = pyttsx3.init()

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")

# Try to use a male voice
if len(voices) > 0:
    engine.setProperty("voice", voices[0].id)


def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

            print("Processing...")

            command = recognizer.recognize_google(
                audio,
                language="en-US"
            )

            print("YOU:", command)
            return command.lower()

        except sr.WaitTimeoutError:
            return ""

        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return ""

        except sr.RequestError:
            speak("I cannot connect to the speech recognition service.")
            return ""


# -----------------------------
# COMMAND HANDLER
# -----------------------------

def execute_command(command):

    if not command:
        return True

    # EXIT
    if "exit" in command or "quit" in command or "shutdown jarvis" in command:
        speak("Goodbye. See you later.")
        return False

    # GREETING
    elif "hello" in command or "hi jarvis" in command:
        speak("Hello. How can I help you?")

    # TIME
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    # DATE
    elif "date" in command:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {today}")

    # GOOGLE
    elif "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    # YOUTUBE
    elif "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    # GITHUB
    elif "open github" in command:
        speak("Opening GitHub.")
        webbrowser.open("https://github.com")

    # CHATGPT
    elif "open chatgpt" in command:
        speak("Opening ChatGPT.")
        webbrowser.open("https://chatgpt.com")

    # GOOGLE SEARCH
    elif command.startswith("search"):
        search_text = command.replace("search", "", 1).strip()

        if search_text:
            speak(f"Searching Google for {search_text}")
            url = "https://www.google.com/search?q=" + search_text.replace(" ", "+")
            webbrowser.open(url)
        else:
            speak("What should I search for?")

    # YOUTUBE SEARCH
    elif command.startswith("play"):
        video = command.replace("play", "", 1).strip()

        if video:
            speak(f"Searching YouTube for {video}")
            url = "https://www.youtube.com/results?search_query=" + video.replace(" ", "+")
            webbrowser.open(url)
        else:
            speak("What do you want me to play?")

    # OPEN NOTEPAD
    elif "open notepad" in command:
        speak("Opening Notepad.")
        subprocess.Popen("notepad.exe")

    # OPEN CALCULATOR
    elif "open calculator" in command:
        speak("Opening Calculator.")
        subprocess.Popen("calc.exe")

    # OPEN FILE EXPLORER
    elif "open file explorer" in command:
        speak("Opening File Explorer.")
        subprocess.Popen("explorer.exe")

    # JARVIS INTRO
    elif "who are you" in command:
        speak("I am Jarvis, your personal desktop assistant.")

    # HELP
    elif "help" in command:
        speak(
            "You can ask me to open Google, YouTube, GitHub, "
            "ChatGPT, search Google, play YouTube videos, "
            "tell the time, open Notepad, Calculator, or File Explorer."
        )

    # UNKNOWN COMMAND
    else:
        speak(
            "I don't know how to do that yet. "
            "You can say help to hear my available commands."
        )

    return True


# -----------------------------
# START JARVIS
# -----------------------------

def main():

    print("==============================")
    print("       JARVIS AI ASSISTANT")
    print("==============================")

    speak("Hello. I am Jarvis.")
    speak("I am ready for your command.")

    running = True

    while running:
        command = listen()
        running = execute_command(command)


if __name__ == "__main__":
    main()