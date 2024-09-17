import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
from youtube_search import YoutubeSearch
import google.generativeai as genai
import subprocess
import os

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


genai.configure(api_key="Your_API_Key")

def speak(audio):
    """Speaks the given audio string."""
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Greets the user based on the current time."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")   
    else:
        speak("Good Evening!")  
    speak("I am Jarvis Sir. Please tell me how may I help you.")       

def open_windows_apps(query):
    """Opens common Windows applications based on user command."""
    app_dict = {
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'paint': 'mspaint.exe',
        'command prompt': 'cmd.exe',
        'vs code': 'code .',
        'file explorer': 'explorer.exe',
        'settings': 'start ms-settings:',
        'camera': 'start microsoft.windows.camera:',
    }

    app_name = query.replace('open ', '').strip()
    command = app_dict.get(app_name)

    if command:
        try:
            subprocess.run(command, check=True, shell=True)
            speak(f"Opening {app_name}.")
        except Exception as e:
            speak(f"Sorry, I couldn't open {app_name}. Error: {str(e)}")
    else:
        speak("Application not found in my list. Please specify another application.")

def takeCommand():
    """Listens for voice commands from the user."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return "none"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "none"

def sendEmail(to, content):
    """Sends an email to the specified address with the provided content."""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
        server.sendmail(os.getenv('EMAIL_USER'), to, content)
        server.close()
        speak("Email has been sent!")
    except smtplib.SMTPException as e:
        print(f"SMTP error: {str(e)}")
        speak("Sorry, I am not able to send this email.")  

def search_youtube(query):
    """Searches YouTube for the given query and returns the results."""
    results = YoutubeSearch(query, max_results=5).to_dict()
    return results

def get_answer_from_gemini(query):
    """Fetches an answer from Gemini using the configured API."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(query+"give me small reply")
        if response.text:
           return response.text
        else:
            return 0
    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        return 0

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("Multiple results found, please be more specific.")
                print(e)
            except wikipedia.exceptions.PageError:
                speak("Sorry, I could not find a Wikipedia page for that.")

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'youtube' in query:
            query = query.replace('youtube', '').strip()
            if query:
                speak(f"Searching YouTube for {query}")
                results = search_youtube(query)
                if results:
                    webbrowser.open(f"https://www.youtube.com{results[0]['url_suffix']}")
                else:
                    speak("No results found.")
            else:
                speak("I didn't catch the topic. Please try again.")

        elif 'open google' in query:
            webbrowser.open("google.com")
        
        elif 'google' in query:
            speak('Searching Google...')
            query = query.replace("google", "")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")  

        elif 'open camera' in query:
            speak("Opening camera.")
            open_windows_apps(query)
        
        elif query=="what's the time" or query=="time" or query=="tell time":
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "Email_id_of_to_person.com"    
                sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("Sorry, I am not able to send this email.")  

        elif 'open ' in query:
            open_windows_apps(query)
        
        elif 'search' in query:
            speak('Searching Google...')
            query = query.replace("search", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={query}")

        elif 'exit' in query or 'stop' in query:
            speak("Goodbye! Have a great day!")
            break
        
        elif query != "none" and query.strip():
            # Fetch an answer from Gemini
            answer = get_answer_from_gemini(query)
            
            if answer:
                print(f" {answer}")
                speak(answer)
                if 'Please provide me with ' in answer:
                    speak("I Found something on google that may match your result\n")
                    webbrowser.open(f"https://www.google.com/search?q={query}")

            if answer==0:
                # If no answer from Gemini, perform a Google search
                speak(f"Searching Google for {query}")
                webbrowser.open(f"https://www.google.com/search?q={query}")
