# Jarvis - Personal AI Virtual Assistant for Laptop and PC

Welcome to **Jarvis**, your personal AI Virtual & Voice assistant powered by Python! Jarvis is designed to make your everyday tasks easier by responding to voice commands and performing actions like searching the web, sending emails, playing music, controlling system settings, and much more. Jarvis even has a sleek GUI interface for easy interaction, featuring real-time responses, and image integration for a rich user experience.

## Features

Jarvis is packed with a wide range of features to help automate tasks and make your life easier:

- **Wikipedia Search**: Ask Jarvis to search Wikipedia for quick information.
- **YouTube Integration**: Open YouTube or search directly for videos by voice.
- **Google Search**: Conduct quick Google searches for any query.
- **File Explorer Search**: Search files directly from your system using voice commands.
- **System Controls**: Turn on/off Bluetooth, Airplane mode, or Battery Saver directly,Increase/Decrease Volume & Brightness.
- **Opens System Applications by Voice Commands**:  Opens Applications like Camera,Powerpoint,Excel,Chrome,Word,Microsoft Edge,Google Meet,OneDrive,Calculator,File Explorer,Settings,Vs Code,Paint,Notepad etc.
- **Gesture-Controlled Virtual Mouse**: Control your mouse with hand gestures.
- **Virtual Volume and Brightness Controller**: Adjust system volume and brightness using hand gestures.
- **Virtual Keyboard**: Type without using a physical keyboard by interacting with Jarvis's on-screen virtual keyboard. Operate the virtual keyboard hands-free using gesture recognition
- **Take Screenshots**: Ask Jarvis to take a screenshot instantly.
- **Send Emails**: Compose and send emails using voice commands.
- **Play Music**: Enjoy music with simple voice commands.
- **Note Taking**: Make quick notes by speaking your thoughts out loud.
- **Reminders**: Set reminders for tasks or events.
- **Jokes**: Need a laugh? Ask Jarvis for a joke.
- **Weather Updates**: Get the latest weather information for any city.
- **Customizable GUI**: Switch between light and dark themes with a toggle button.
- **Voice Control and GUI Interaction**: Control Jarvis with your voice or through a user-friendly graphical interface.
- **Generative AI**: Jarvis uses generative AI to provide relevant content and responses to your queries.
- and Many more features....

## Technologies and Libraries Used

Jarvis uses a combination of modern Python libraries and tools to deliver a smooth and efficient experience:

- `pyttsx3`: Text-to-speech conversion
- `speech_recognition`: For recognizing voice commands
- `wikipedia-api`: To fetch summaries from Wikipedia
- `webbrowser`: Open websites and search the web
- `subprocess`: For running system applications and scripts
- `pyjokes`: For generating random jokes
- `pygame`: Play and control music files
- `Pillow`: For image handling in the GUI
- `tkinter` and `customtkinter`: To build an intuitive GUI for user interaction
- `Google Generative AI API`: For answering queries and generating smart responses
- `OpenWeatherMap API`: For fetching weather updates
- `Flask`: For displaying weather information in a web-based format
- `scikit-image`: For gesture-controlled mouse functionality

## Setup and Installation

To get Jarvis up and running on your machine, follow these steps:

### Prerequisites

Before installing Jarvis, ensure you have the following:

- **Python 3.x** installed on your system.
- **pip** (Python package installer) to manage dependencies.

### Clone the Repository
**step1**:
Download or clone the Jarvis repository from GitHub:

git clone https://github.com/sandeepgoudmacha/jarvis.git
cd jarvis

**Step2**: Install the Required Packages
Install the necessary dependencies using pip. These packages are listed in the requirements.txt file. Use the following command:

pip install -r requirements.txt

**Step3**: API Key Setup
To enable all functionalities, you'll need API keys for certain services:

-**OpenWeatherMap API**: Create an account on OpenWeatherMap and get your API key. Replace the YOUR_API_KEY in the code with your actual key:
-**Google Generative AI**: Sign up for Google's Generative AI API. Add your API credentials in the relevant parts of the code.

**step4**:Running Jarvis
After setting up everything, you can run the assistant by navigating to the project folder and executing:

python jarvis.py

This will launch the Jarvis voice assistant, along with its graphical interface.


Here's the complete README.md file for your Jarvis project:

Jarvis - Your Personal AI Assistant
Jarvis is a Python-based voice assistant that can perform a wide range of tasks such as answering questions, searching the web, sending emails, playing music, controlling volume and brightness, telling jokes, and much more. With a graphical interface powered by tkinter and customtkinter, Jarvis can fetch and display images, videos, weather information, and more through integrated APIs.

Features
Voice Commands: Use natural speech to interact with Jarvis.
Search the Web: Get instant results from Wikipedia, Google, and YouTube.
Multimedia: Play music, videos, and even control system volume and brightness.
Jokes: Cheer yourself up with funny jokes from PyJokes.
Custom Interface: Sleek GUI built with tkinter and customtkinter.
Weather Information: Fetch weather data through the OpenWeatherMap API.
AI Integration: Utilize Google's Generative AI for creative tasks.
Requirements
Python 3.8+
Internet connection (for web-based features and APIs)
Setup Instructions
Step 1: Clone the Repository
First, clone the project repository to your local machine.

bash
Copy code
git clone https://github.com/sandeepgoudmacha/jarvis-ai-assistant.git
cd jarvis-ai-assistant
Step 2: Install the Required Packages
Install the necessary dependencies using pip. These packages are listed in the requirements.txt file. Use the following command:

bash
Copy code
pip install -r requirements.txt
Step 3: API Key Setup
To enable all functionalities, you'll need API keys for certain services:

OpenWeatherMap API: Create an account on OpenWeatherMap and get your API key. Replace the YOUR_API_KEY in the code with your actual key:

python
Copy code
weather_api_key = "YOUR_API_KEY"
Google Generative AI: Sign up for Google's Generative AI API. Add your API credentials in the relevant parts of the code.

Step 4: Additional Libraries
If you're using pycaw to control system audio or vlc to play videos, ensure that their system-level dependencies are installed.

For Windows, you can install VLC from here.

For pycaw, ensure that your system has the required components:

bash
Copy code
pip install comtypes
Step 5: Running Jarvis
After setting up everything, you can run the assistant by navigating to the project folder and executing:

bash
Copy code
python jarvis.py
This will launch the Jarvis voice assistant, along with its graphical interface.

Usage
Once you run the script, Jarvis will be ready to accept voice commands. Here are some things you can ask:

Wikipedia Search: "Tell me about Albert Einstein."
Play Music: "Play some music."
Send Email: "Send an email to example@gmail.com."
Tell Jokes: "Tell me a joke."
YouTube Search: "Search for funny cat videos on YouTube."
Control Volume: "Increase the volume."
Weather Information: "What's the weather in Hyderabad?"
Jarvis will respond to your commands and provide relevant information.

Customization
Feel free to customize Jarvis as per your needs! You can add new functionalities, integrate more APIs, or even modify the GUI for a more personalized experience.

Troubleshooting
If you run into any issues, here are some tips:

Module Not Found: Ensure all the dependencies in requirements.txt are installed correctly.
Audio Issues: For audio-related issues, check your microphone settings or install additional system drivers if required.
API Errors: Double-check that your API keys are correct and have the proper permissions.
Contributing
If you'd like to contribute to this project, feel free to submit a pull request or open an issue on GitHub.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
