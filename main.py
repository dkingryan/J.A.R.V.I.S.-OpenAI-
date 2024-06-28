import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import openai
import subprocess
import sys
import time

openai.api_key = "OWN OPENAI API KEY"

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language = "en-in")
            print (f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"

def open_ai_response(query):
    for _ in range(2):
        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo-16k",
                prompt=query,
                max_tokens=256
            )
            return response.choice[0].text.strip()
        except openai.error.RateLimitError:
            print("Rate limit exceeded. Retrying in 3 seconds...")
            time.sleep(3)
        except openai.error.OpenAIError as e:
            print(f"An error occurred: {e}")
            return "I'm sorry, I couldn't process your request at the moment."
    return "I'm sorry, I couldn't process your request after multiple attempts."

if __name__ == '__main__':
    command_executed = False
    say("Hello I am Jarvis A.I.")
    while True:
        say("Listening...")
        print("Listening...")
        query = takeCommand()

        if "stop".lower() in query.lower():
            say("Shutting down...")
            exit(0)

        sites = [["youtube", "https://youtube.com"], ["google","https://google.com"], ["linkedin", "https://www.linkedin.com/feed/"],["canvas", "https://canvas.cpp.edu"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]}...")
                webbrowser.open(site[1])
                command_executed = True
                break

        if "open music".lower() in query.lower():
            musicPath = r"\Users\ryant\Downloads\2 Grown.mp3"
            if sys.platform == "win32":
                os.startfile(musicPath)
            elif sys.platform == "darwin":
                subprocess.call(['open', musicPath])
            elif sys.platform == "linux":
                subprocess.call(['xdg-open', musicPath])
            else:
                say("Unsupported OS")
            command_executed = True

        if not command_executed:
            response = open_ai_response(query)
            say(response)
            print(response)
