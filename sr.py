import speech_recognition as sr
import pyttsx3
import datetime
import os
import subprocess
#import pygame

recognizer = sr.Recognizer()
speaker = pyttsx3.init()
notepad_process = None  # To track notepad process

# Path to your music folder
music_folder = "C:/Users/YourUsername/Music"  # <-- Change this path

def speak(text):
    speaker.say(text)
    speaker.runAndWait()

def get_greeting():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"

def recognize_voice():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source) 
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Sorry, the speech service is down.")
            return None

def open_notepad():
    global notepad_process
    notepad_process = subprocess.Popen(["notepad.exe"])
    speak("Opening Notepad.")

def close_notepad():
    global notepad_process
    if notepad_process:
        notepad_process.terminate()
        speak("Closing Notepad.")
        notepad_process = None
    else:
        speak("Notepad is not open.")

def play_music():
    try:
        files = [f for f in os.listdir(music_folder) if f.endswith(('.mp3', '.wav'))]
        if files:
            pygame.mixer.init()
            pygame.mixer.music.load(os.path.join(music_folder, files[0]))
            pygame.mixer.music.play()
            speak(f"Playing {files[0]}")
        else:
            speak("No music files found in the folder.")
    except Exception as e:
        speak("There was an error playing music.")
        print(e)

def main():
    greeting = get_greeting() 
    speak(f"{greeting}! How can I assist you today?")
    
    while True:
        print("Say something...")
        command = recognize_voice()
        
        if command:
            if 'morning' in command:
                speak("Good Morning!")
            elif 'afternoon' in command:
                speak("Good Afternoon!")
            elif 'evening' in command:
                speak("Good Evening!")
            elif 'open notepad' in command:
                open_notepad()
            elif 'close notepad' in command:
                close_notepad()
            elif 'play music' in command:
                play_music()
            elif 'exit' in command or 'quit' in command:
                speak("Goodbye!")
                break
            else:
                speak(f"You said: {command}")

if __name__ == "__main__":
    main()
