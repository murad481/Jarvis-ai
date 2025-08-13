import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import google.generativeai as genai
from gtts import gTTS
import pygame
import os

#pip install pocketsphinx
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "NEWS_API_KEY"

def speak_old(text):
    engine.pyttsx3.init()
    engine.say(text)
    engine.runAndWait()



def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

     # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 


# AI Process function
def aiProcess(command):
    genai.configure(api_key="GEMINI_OR_OPENAI _API_KEY")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(command)
    return response.text

# Command process
def processCommand(command):
    print(f"Command received: {command}")
    reply = aiProcess(command)
    print(f"Jarvis: {reply}")
    speak(reply)


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"NEWS_API_KEY")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles[0:2]:
                speak(article['title'], )

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 
              

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    r = sr.Recognizer()
        # # Listen for the wake word "Jarvis"
        # # obtain audio from the microphone
        # r = sr.Recognizer()
         
    while True:
        try:
            print("recognizing...")
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=3, phrase_time_limit=2)
            word = r.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))
