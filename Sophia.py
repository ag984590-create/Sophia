import pyttsx3
#pyttsx3.speak("Hi i am sophia")
import speech_recognition as sr
import datetime
import pywhatkit
import webbrowser
from google import genai


# 1. Setup your API Key
# Make sure this string is exactly what you got from AI Studio
API_KEY = "AIzaSyDaHTQUf2lte74VehFNDRzEWFRdfaN-ey4"

# 2. Initialize the client
client = genai.Client(api_key=API_KEY)

# 🔊 Voice (edge-tts + pygame)
import asyncio
import edge_tts
import pygame
import os
import time

pygame.mixer.init()

async def speak_async(text):
    file = "voice.mp3"
    communicate = edge_tts.Communicate(text, "en-US-JennyNeural")
    await communicate.save(file)

    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.unload()
    os.remove(file)

def speak(text):
    asyncio.run(speak_async(text))


def ask_ai(user_input):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Answer clearly in 1-2 lines: " + user_input
        )

        # 🔥 Try main text
        if hasattr(response, "text") and response.text:
            return response.text

        # 🔥 Fallback (important)
        elif response.candidates:
            return response.candidates[0].content.parts[0].text

        else:
            return "I couldn't understand that properly"

    except Exception as e:
        print("Error:", e)
        return "Sorry, something went wrong"
def process(order):
    if "open youtube" in order.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open whatsapp" in order.lower():
        webbrowser.open("https://web.whatsapp.com/")
    elif "open github" in order.lower():
        webbrowser.open("https://github.com/")
    elif "open instagram" in order.lower():
        webbrowser.open("https://www.instagram.com/")
    elif "open facebook" in order.lower():
        webbrowser.open("https://www.facebook.com/")
    elif "open spotify" in order.lower():
        webbrowser.open("http://spotify.com/")
    elif "play" in order.lower():
        song=order
        song=order.replace("play","").strip()
        pywhatkit.playonyt(song)
        print(f'Playing {song}....')
        speak('playing'+ song)
    elif "who made you " in order or "who created you" in order:
        speak("I am virtual assistant sophia")
        speak("I was created by Coder Shivam")
    elif "who are you" in order.lower():
        speak('Hi i am sophia')
        speak("I can answer your questions and perform tasks like opening google etc")
    elif 'time' in order:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak('Current time is ' + time)
    elif "stop" in order or "exit" in order:
        speak('Goodbye')
        exit()
    elif "ai mode" in order:
        speak("Let me think")
        reply = ask_ai(order)
        print("Sophia:", reply)
        speak(reply)
    elif order != "":
        # 🔥 automatic AI fallback
        reply = ask_ai(order)
        print("Sophia:", reply)
        speak(reply)
    

def listen():
    listener=sr.Recognizer()
    while True:
        try:
         with sr.Microphone() as source:
            print('Listening.....')
            word=listener.listen(source)
            voice=listener.recognize_google(word)
            print(f"You said :{voice}")
            if "jarvis" in voice.lower():
                print('Sophia activated....')
                speak('Yes sir how can I help You')
                with sr.Microphone() as source:
                    print('Recognizing....')
                    word=listener.listen(source)
                    command=listener.recognize_google(word)
                    print(f"You said :{command}")
                    process(command)
        except Exception as e:
            print(e)
if __name__=="__main__":
    speak("Initializing Sophia")
    print('Initializing sophia......')
    listen()




