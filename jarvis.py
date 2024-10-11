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
import pygame
import tkinter as tk
import customtkinter as ctk
from tkinter import scrolledtext
from tkinter import simpledialog
from tkinterweb import HtmlFrame
# from tkinter import messagebox
# from PIL import Image, ImageTk
# import vlc
import threading
import pyjokes
from tkinter import *
from tkintervideo import *
import subprocess
import requests
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL  
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import wmi
import screen_brightness_control as sbc
import schedule
import time
import pyautogui
from PIL import Image, ImageTk, ImageOps  # Pillow library for handling images
# from datetime import datetime


speak_enabled = True


# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

genai.configure(api_key="Your API_KEY") #get your free Gemini API_Key and place it in api_key


def speak(audio):
    """Speaks the given audio string."""
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """Greets the user based on the current time."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        greeting = "Good Morning!"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon!"   
    else:
        greeting = "Good Evening!"  
    return f"{greeting} I am Jarvis. How may I help you?"


def speak(text):
    """Performs text-to-speech if speaking is enabled."""
    if speak_enabled:
        engine.say(text)
        engine.runAndWait()
    else:
        print(f"Speaking disabled. Would have said: '{text}'")

def toggle_speaking():
    """Toggles the speaking functionality on and off and updates the button text."""
    global speak_enabled, toggle_speaking_button
    speak_enabled = not speak_enabled

    if speak_enabled:
        toggle_speaking_button.configure(text="Speaking: On")
        print("Speaking is enabled.")
    else:
        toggle_speaking_button.configure(text="Speaking: Off")
        print("Speaking is disabled.")

def open_windows_apps(query):
    """Opens common Windows applications based on user command."""
    app_dict = {
        'powerpoint': "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\PowerPoint.lnk",
        'excel': "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Excel.lnk",
        'chrome': "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome.lnk",
        'word': "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word.lnk",
        'microsoft edge': "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Edge.lnk",
        'google meet': "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Meet.url",
        'google messages':"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Messages.url",
        'oneDrive':"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\OneDrive.lnk",
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'paint': 'mspaint.exe',
        'vs code': 'code .',
        'file explorer': 'explorer.exe',
        'settings': 'start ms-settings:',
        'camera': 'start microsoft.windows.camera:',
        'command prompt': 'cmd.exe',
    }

    app_name = query.replace('open ', '').strip()
    command = app_dict.get(app_name)

    if command:
        try:
            subprocess.run(command, check=True, shell=True)
            return f"Opening {app_name}."
        except Exception as e:
            return f"Sorry, I couldn't open {app_name}. Error: {str(e)}"
    else:
        return "Application not found in my list. Please specify another application."


def reminder(job_id, message):
    reminder_text = f"Reminder {job_id}: {message} at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    # Schedule a function to safely update the ScrolledText widget
    root.after(0, lambda: text_output.insert(tk.END, reminder_text))

# Function to schedule a reminder
def schedule_reminder(time_str, message):
    job_id = schedule.every().day.at(time_str).do(reminder, job_id=len(schedule.jobs), message=message)
    print(f"Scheduled reminder: {message} at {time_str}")

# Function to run the scheduler in a separate thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


def get_volume_control():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume

def increase_volume():
    try:
        volume_control = get_volume_control()
        current_volume = volume_control.GetMasterVolumeLevelScalar() * 100
        new_volume = min(current_volume + 10, 100) / 100
        volume_control.SetMasterVolumeLevelScalar(new_volume, None)
        return f"Volume increased to {int(new_volume * 100)}%"
    except Exception as e:
        return f"Error increasing volume: {e}"

def decrease_volume():
    try:
        volume_control = get_volume_control()
        current_volume = volume_control.GetMasterVolumeLevelScalar() * 100
        new_volume = max(current_volume - 10, 0) / 100
        volume_control.SetMasterVolumeLevelScalar(new_volume, None)
        return f"Volume decreased to {int(new_volume * 100)}%"
    except Exception as e:
        return f"Error decreasing volume: {e}"

def get_brightness_control():
    wmi_interface = wmi.WMI(namespace='wmi')
    methods = wmi_interface.WmiMonitorBrightnessMethods()[0]
    return methods.WmiGetBrightness()

try:
    brightness = get_brightness_control()
    print(f"Current Brightness: {brightness}")
except Exception as e:
    print(f"Error: {e}")

def set_brightness(level):
    """Set the screen brightness to the specified level (0 to 100)."""
    brightness_control = get_brightness_control()
    brightness_control.WmiSetBrightness(1, level)
    return f"Brightness set to {level}%."

def increase_brightness():
    try:
        current_brightness = sbc.get_brightness(display=0)[0]
        sbc.set_brightness(current_brightness + 10, display=0)
        return f"Brightness increased to {current_brightness + 10}%"
    except Exception as e:
        return f"Error increasing brightness: {e}"

def decrease_brightness():
    try:
        current_brightness = sbc.get_brightness(display=0)[0]
        sbc.set_brightness(current_brightness - 10, display=0)
        return f"Brightness decreased to {current_brightness - 10}%"
    except Exception as e:
        return f"Error decreasing brightness: {e}"

def take_screenshot():
    """Takes a screenshot and saves it in the specified folder."""
    # Set the directory where you want to save the screenshot
    screenshot_dir = os.path.join(os.path.expanduser("~"), "Screenshots_from_jarvis")  # Saving in a folder
    
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)  # Create the directory if it doesn't exist
    
    # Create the screenshot filename
    screenshot_filename = f"screenshot_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
    screenshot_path = os.path.join(screenshot_dir, screenshot_filename)

    # Take screenshot and save it
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    
    response = f"Screenshot saved as {screenshot_filename} in {screenshot_dir}."
    return response

def search_file_explorer(query, search_path="C:\\"):
    """Searches for files in the file explorer based on the user's query."""
    results = []
    query = query.strip().lower()  # Clean up the query
    
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if query in file.lower():  # Check if the query matches any file names
                results.append(os.path.join(root, file))

    return results


def display_weather(city):
    api_key = 'Your API_KEY' #get your free API_KEY from "openweatherapp"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(base_url)
    data = response.json()

    if data['cod'] == 200:
        weather_desc = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        
        # Check for specific conditions
        if 'rain' in weather_desc:
            condition_message = "It's raining! Don't forget your umbrella."
        elif 'clear' in weather_desc:
            condition_message = "The sky is clear. It's a great day outside!"
        elif temperature > 30:
            condition_message = "It's quite hot outside. Stay hydrated!"
        elif temperature < 0:
            condition_message = "It's freezing! Dress warmly!"
        else:
            condition_message = "Weather is pleasant."

        # Return formatted weather report
        return f"Weather: {weather_desc}, Temperature: {temperature}°C, Humidity: {humidity}%. {condition_message}"
    
    else:
        return "City not found or an error occurred."



def take_command():
    """Listens for voice commands from the user."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-in')
        return query.lower()
    except sr.UnknownValueError:
        return "none"
    except sr.RequestError as e:
        return "none"

def send_email(to, content):
    """Sends an email to the specified address with the provided content."""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS')) 
        server.sendmail(os.getenv('EMAIL_USER'), to, content)
        server.close()
        return "Email has been sent!"
    except smtplib.SMTPException as e:
        speak("Sorry, I am not able to send this email.") 
        return f"SMTP error: {str(e)}"

def search_youtube(query):
    """Searches YouTube for the given query and returns the results."""
    results = YoutubeSearch(query, max_results=5).to_dict()
    return results

def play_music():
    """Plays music from a predefined directory or YouTube if not found."""
    pygame.mixer.init()
    music_directory = os.path.join(os.path.expanduser("~"), "Music")

    if os.path.exists(music_directory):
        music_files = [f for f in os.listdir(music_directory) if f.endswith(('.mp3', '.wav'))]

        if music_files:
            first_music_file = os.path.join(music_directory, music_files[0])

            try:
                pygame.mixer.music.load(first_music_file)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    content = take_command()
                    if 'stop' in content.lower() or 'exit' in content.lower():
                        pygame.mixer.music.stop()
                        print("Music Stopped..")
                        break
                
            except pygame.error as e:
                return "Error playing the music file."
        else:
            results = search_youtube("trending music")
            if results:
                webbrowser.open(f"https://www.youtube.com{results[0]['url_suffix']}")
                return "No music files found. Playing from YouTube..."
            else:
                return "No results found."
    else:
        return "Music directory not found."

def toggle_battery_saver(state):
    try:
        if state == "on":
            pyautogui.hotkey('win', 'a')  # Open Action Center
            time.sleep(1)  # Wait for the Action Center to open
            # Click the battery saver button (you may need to adjust the coordinates)
            pyautogui.click(x=200, y=200)  # Adjust x,y to click the battery saver
            return "Battery saver turned on."
        elif state == "off":
            pyautogui.hotkey('win', 'a')  # Open Action Center
            time.sleep(1)  # Wait for the Action Center to open
            # Click the battery saver button again
            pyautogui.click(x=200, y=200)  # Adjust x,y to click the battery saver
            return "Battery saver turned off."
        else:
            return "Invalid Battery Saver command."
    except Exception as e:
        return f"Error controlling Battery Saver: {str(e)}"

def toggle_airplane_mode(state):
    try:
        if state == "on":
            subprocess.run('netsh interface set interface "Wi-Fi" disable', shell=True)
            subprocess.run('netsh interface set interface "Bluetooth Network Connection" disable', shell=True)
            return "Airplane mode activated."
        elif state == "off":
            subprocess.run('netsh interface set interface "Wi-Fi" enable', shell=True)
            subprocess.run('netsh interface set interface "Bluetooth Network Connection" enable', shell=True)
            return "Airplane mode deactivated."
        else:
            return "Invalid Airplane mode command."
    except Exception as e:
        return f"Error controlling Airplane mode: {str(e)}"

def toggle_bluetooth(state):
    try:
        if state == "on":
            subprocess.run('devcon enable *DEV_XXXX', shell=True)  # Replace DEV_XXXX with your Bluetooth device ID
            return "Turning Bluetooth on."
        elif state == "off":
            subprocess.run('devcon disable *DEV_XXXX', shell=True)  # Replace DEV_XXXX with your Bluetooth device ID
            return "Turning Bluetooth off."
        else:
            return "Invalid Bluetooth command."
    except Exception as e:
        return f"Error controlling Bluetooth: {str(e)}"
    
def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"

    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])

def date():
    now = datetime.datetime.now()
    month_name = now.month
    day_name = now.day
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    ordinalnames = [ '1st', '2nd', '3rd', ' 4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd','24rd', '25th', '26th', '27th', '28th', '29th', '30th', '31st'] 
    # print("Today is "+ month_names[month_name-1] +" " + ordinalnames[day_name-1] + '.')
    # speak("Today is "+ month_names[month_name-1] +" " + ordinalnames[day_name-1] + '.')
    return "Today is "+ month_names[month_name-1] +" " + ordinalnames[day_name-1] + '.'


def get_answer_from_gemini(query):
    """Fetches an answer from Gemini using the configured API."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(query + " give me a small reply")
        if response.text:
            return response.text
        else:
            return "No answer found."
    except Exception as e:
        return f"Gemini API error: {str(e)}"

def process_query(query):
    global volume_process, brightness_process, mouse_process 
    volume_process=None
    brightness_process=None
    mouse_process=None
    if 'wikipedia' in query:
        response = 'Searching Wikipedia...'
        query = query.replace("wikipedia", "")
        if query==None:
             response+="what you need from wikipedia.."
            
        else:
            try:
                results = wikipedia.summary(query, sentences=2)
                response += f"\nAccording to Wikipedia: {results}"
            except wikipedia.exceptions.DisambiguationError:
                response += " Multiple results found, please be more specific."
            except wikipedia.exceptions.PageError:
                response += " Could not find a Wikipedia page for that."
    elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            response="opening youtube"
    elif 'youtube' in query:
            query = query.replace('youtube', '').strip()
            query = query.replace('from', '').strip()
            if query:
                speak(f"Searching YouTube for {query}")
                results = search_youtube(query)
                if results:
                    webbrowser.open(f"https://www.youtube.com{results[0]['url_suffix']}")
                else:
                    speak("No results found.")
            else:
                speak("I didn't catch the topic. Please try again.")
                speak("But Opening Youtube..")
                webbrowser.open("youtube.com")
            response= ""
    elif 'open google' in query:
            webbrowser.open("google.com")
            response=""
    elif 'google' in query:
            speak('Searching Google...')
            query = query.replace('from', '').strip()
            query = query.replace("google", "")
            webbrowser.open(f"https://www.google.com/search?q={query}")
            response=""

    elif 'from file explorer' in query:
                speak('Searching in File Explorer... ')
                search_term = query.replace("from file explorer", "").strip()
                search_term = search_term.replace('open', '').strip()

                # Search from a specific directory, you can change the 'C:\\' to other paths
                search_results = search_file_explorer(search_term, search_path="C:\\")
                
                if search_results:
                    speak(f"Found {len(search_results)} results.")
                    for result in search_results[:2]:  # Limiting to 5 results to avoid overload
                        print(f"Found: {result}")
                    speak("providing top results...")
                else:
                    speak("Sorry, no files matched your query.")
                
                response=search_results[0:2]

    elif 'on bluetooth' in query:
        return toggle_bluetooth("on")
    elif 'off bluetooth' in query:
        return toggle_bluetooth("off")

    elif 'on airplane mode' in query:
        return toggle_airplane_mode("on")
    elif 'off airplane mode' in query:
        return toggle_airplane_mode("off")

    elif 'on battery saver' in query:
        return toggle_battery_saver("on")
    elif 'off battery saver' in query:
        return toggle_battery_saver("off")

    elif 'virtual mouse' in query or 'mouse controller' in query:
        if mouse_process is None:
            mouse_process = subprocess.Popen(['python', 'C:\\Users\\Nites\\Gesture-Controlled-Virtual-Mouse\\Gesture_Controller.py'])  # Update with the correct path
            # I uploaded a code with Gesture_Controller.py download it and set path of it in above.
            response = "Opening virtual mouse controller."
        else:
            response = "Mouse controller is already running."

    elif 'stop mouse' in query:
        # Check if mouse_process is not None before calling terminate
        if mouse_process is not None:
            mouse_process.terminate()  # Terminate the process
            mouse_process = None  # Set it back to None after termination
            response = "Stopping virtual mouse controller."
        else:
            response = "Mouse controller is not running."

    elif 'open virtual volume controller' in query or 'open volume controller' in query:
        subprocess.Popen(['python','C:\\Users\\Nites\\Volume_and_Brightness_Control_Using_Hand_Gestures\\volBrtnessControl.py'])  # Update with the correct path
          # I uploaded a code with volBrtnessControl.py download it and set path of it in above.
        response = "Opening virtual volume controller."

    elif 'open virtual brightness controller' in query or 'open brightness controller' in query:
        subprocess.Popen(['python', 'C:\\Users\\Nites\\Volume_and_Brightness_Control_Using_Hand_Gestures\\volBrtnessControl.py'])  # Update with the correct path
          # I uploaded a code with volBrtnessControl.py download it and set path of it in above.
        response = "Opening virtual brightness controller."
    
    elif 'stop virtual volume controller' in query or 'stop volume controller' in query:
        if volume_process is not None:
            volume_process.terminate()
            volume_process = None
            response = "Stopping virtual volume controller."
        else:
            response = "Volume controller is not running."

    # Handle stopping the virtual brightness controller
    elif 'stop virtual brightness controller' in query or 'stop brightness controller' in query:
        if brightness_process is not None:
            brightness_process.terminate()
            brightness_process = None
            response = "Stopping virtual brightness controller."
        else:
            response = "Brightness controller is not running."

    elif 'take screenshot' in query or 'screenshot' in query:
        response = take_screenshot()

    elif 'open ' in query:
        response = open_windows_apps(query)

    elif 'email' in query:
            try:
                speak("What should I say?")
                content = take_command()
                to = "recipient@example.com"  # Replace with actual recipient's email
                send_email(to, content)
            except Exception as e:
                print(e)
                # speak("Sorry, I am not able to send this email.") 
                return "Sorry, I am not able to send this email.\n" 
            response=""

    elif query == "what's the time" or query == "time" or query == "tell time":
        strTime = datetime.datetime.now().strftime("%H:%M:%S")    
        speak(f"The time is {strTime}")
        response=strTime
        
    elif 'play music' in query or 'play song' in query:
        response = play_music()
    
    elif 'make a note' in query or 'note this' in query:
                query = query.replace("make a note", "")
                note(query)
                response="noted"

    elif 'increase volume' in query:
        response = increase_volume()

    elif 'decrease volume' in query:
        response = decrease_volume()

    elif 'increase brightness' in query:
        response = increase_brightness()

    elif 'decrease brightness' in query:
        response = decrease_brightness()

    elif "remind me" in query:
        # Extract time and message from the query
        # You can use regex or NLP libraries for better parsing
        parts = query.split(" at ")
        if len(parts) == 2:
            time_str = parts[1].strip()
            message = parts[0].replace("remind me to", "").strip()
            schedule_reminder(time_str, message)
            return f"Reminder set for {time_str}: {message}"

    elif "who made you" in query or "who created you" in query or "who discovered you" in query:
                speak("I was built by Macha Sandeep...")
                response="I was built by Macha Sandeep..."

    elif 'search' in query:
        query=query.replace("search","")
        response = f"Searching Google for {query}"
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif 'joke' in query:
            response=pyjokes.get_joke()

    elif "weather" in query:
            # Extract the city name from the query
            city_name = query.split("weather in")[-1].strip()
            # Get and display the weather
            response = display_weather(city_name)  # Assuming this function returns a message
            # Response message to the user
            return f"Here's the weather update for {city_name}: {response}"

    elif 'date ' in query or "what's the date" in query:
           response= date()

    elif query != "none" and query.strip():
        answer = get_answer_from_gemini(query)
        response = answer if answer else "Sorry, I couldn't find an answer. Searching Google."
        if 'Please provide ' in answer:
                    speak("I Found something on google that may match your result\n")
                    response="getting from google"
                    webbrowser.open(f"https://www.google.com/search?q={query}")

        elif  'please give ' in answer:
                    speak("I Found something on google that may match your result\n")
                    response="getting from google"
                    webbrowser.open(f"https://www.google.com/search?q={query}")
        elif 'Gemini API error' in answer:
                    speak("i didn't get your point........finding your query from google..")
                    response="i didn't get your point........finding your query from google.."
                    webbrowser.open(f"https://www.google.com/search?q={query}")
        if not answer:
            webbrowser.open(f"https://www.google.com/search?q={query}")
    else:
        response = "Sorry, I didn't catch that. Can you please repeat?"
        
    return response

def listen_for_jarvis():
    """Continuously listens for the wake word 'Jarvis'."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            try:
                print("Listening for wake word 'Jarvis'...")
                audio = r.listen(source)
                query = r.recognize_google(audio, language='en-in').lower()
                if "jarvis" in query:
                    print("Wake word detected: Jarvis")
                    speak("Yes, I'm listening...")
                    # text_output.insert(tk.END, "Jarvis: Yes, I'm listening...\n")
                    text_output.see(tk.END)  # Scroll to the end
                    text_output.update_idletasks()  # Force the GUI to update

                    execute_voice_command()  # Call to process the command
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Request error: {e}")

def execute_voice_command():
    """Executes voice commands after the wake word is detected."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("What can I do for you?")
        print("Listening for your command...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in').lower()
            print(f"Command received: {query}")

            # Display user input in the GUI
            text_output.insert(tk.END, "You: ", "bold")  # Use the bold tag
            text_output.insert(tk.END, f"{query}\n")

            # Process the query and get the response
            response = process_query(query)
            print(f"Response: {response}")

            # Insert the image instead of the text "Jarvis"
            text_output.image_create(tk.END, image=jarvis_photo)
            text_output.insert(tk.END, f" {response}\n")  # Add space before response for alignment
            
            # Force the GUI to update immediately
            text_output.update_idletasks()

            # Print to console after GUI update
            print(f"Jarvis: {response}")  # Print Jarvis' response

            speak(response)  # Speak the response
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            speak(f"Sorry, there was a problem. Error: {str(e)}")



ctk.set_appearance_mode("Light")  # Set the default appearance mode
ctk.set_default_color_theme("blue")  # Set the default theme color

def toggle_theme():
    current_mode = ctk.get_appearance_mode()
    if current_mode == "Light":
        ctk.set_appearance_mode("Dark")  # Switch to dark mode
    else:
        ctk.set_appearance_mode("Light")  # Switch to light mode

# ---- User Interface Section ---- #
def gui_interface():
    global root, text_output, entry, jarvis_photo, toggle_speaking_button   # Declare jarvis_photo as global

    # Set appearance mode and color theme
    ctk.set_appearance_mode("dark")  # Options: "light", "dark", or "system"
    ctk.set_default_color_theme("blue")  # Choose from available themes

    # Initialize the main window
    root = ctk.CTk()  
    root.title("Jarvis Assistant")
    root.geometry("600x600")  # Set a custom size for the window

    # Load the image after creating the root window
    jarvis_image_path = "C:\\Users\\Nites\\OneDrive\\Pictures\\Screenshots 1\\Screenshot 2024-10-10 190537.png"  # Update this path
    jarvis_image = Image.open(jarvis_image_path)
    jarvis_image = jarvis_image.resize((30, 30))  # Resize the image if necessary
    jarvis_photo = ImageTk.PhotoImage(jarvis_image)  # Use ImageTk.PhotoImage for compatibility

    # Create a frame for the text output and entry
    frame = ctk.CTkFrame(root)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Text output area
    text_output = scrolledtext.ScrolledText(frame, wrap="word", font=("Helvetica", 12))
    text_output.pack(padx=10, pady=10, fill="both", expand=True)
    text_output.tag_configure("bold", font=("Helvetica", 12, "bold"))

    # Entry field for user input
    entry = ctk.CTkEntry(frame, placeholder_text="Type your message here...", width=300)
    entry.pack(padx=10, pady=10, fill="x")

    # Create buttons
    button_frame = ctk.CTkFrame(frame)
    button_frame.pack(pady=10)
   

    send_button = ctk.CTkButton(button_frame, text="Send", command=on_send_click)
    send_button.pack(side=ctk.LEFT, padx=5)

    speech_button = ctk.CTkButton(button_frame, text="Speak", command=on_speech_click)
    speech_button.pack(side=ctk.LEFT, padx=5)

    theme_button = ctk.CTkButton(root, text="Toggle Theme", command=toggle_theme)
    theme_button.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)  # Offset the button slightly from the top-right corner

    speaking_label = ctk.CTkLabel(button_frame, text="Jarvis Speaking Mode:")
    speaking_label.pack(side=ctk.LEFT, padx=5)  # Position label next to the button

    # Toggle speaking button with dynamic text
    toggle_speaking_button = ctk.CTkButton(button_frame, text="Speaking: On", command=toggle_speaking)
    toggle_speaking_button.pack(side=ctk.LEFT, padx=5)

    threading.Thread(target=run_scheduler, daemon=True).start()
    threading.Thread(target=listen_for_jarvis, daemon=True).start()

    # Start the GUI main loop
    root.mainloop()

def on_send_click():
    user_input = entry.get()
    if user_input:
        # Insert "You" text in the GUI
        text_output.insert(tk.END, "You: ", "bold")  # Use the bold tag
        text_output.insert(tk.END, f"{user_input}\n")

        # Process the query and get the response
        response = process_query(user_input.lower())

        text_output.image_create(tk.END, image=jarvis_photo)
        text_output.insert(tk.END, f" {response}\n\n")  # Add space before response for alignment

        # Force the GUI to update immediately
        text_output.update_idletasks()

        # Print to console after GUI update
        print(f"You: {user_input}")  # Print "You" input
        print(f"Jarvis: {response}")  # Print Jarvis' response

        speak(response)
        entry.delete(0, tk.END)

def on_speech_click():
    speak("Listening...")
    
    query = take_command()
    if query != "none":
        # Insert "You" text in the GUI
        text_output.insert(tk.END, "You: ", "bold")  # Use the bold tag
        text_output.insert(tk.END, f"{query}\n")

        # Process the query and get the response
        response = process_query(query)

        text_output.image_create(tk.END, image=jarvis_photo)
        text_output.insert(tk.END, f" {response}\n\n")  # Add space before response for alignment
        
        # Force the GUI to update immediately
        text_output.update_idletasks()

        # Print to console after GUI update
        print(f"You: {query}")  # Print "You" input
        print(f"Jarvis: {response}")  # Print Jarvis' response

        speak(response)
    else:
        text_output.insert(tk.END, "Jarvis: I didn't catch that.\n")
        print("Jarvis: I didn't catch that.")  # Print to console for error case


if __name__ == "__main__":
    wish_msg = wishMe()
    speak(wish_msg)
    gui_interface()
