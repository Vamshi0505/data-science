# Project Title: Voice-Activated AI Chatbot
# Objective: Create a voice-activated AI chatbot using Python, capable of responding
#            to commands, conducting searches, fetching Wikipedia info, and interacting
#            with system commands.

# --- 1. Import necessary libraries ---
import pyttsx3              # For text-to-speech functionality
import speech_recognition as sr # For recognizing voice command
import datetime             # For getting the current date and time
import wikipedia            # For accessing Wikipedia articles
import webbrowser           # For opening websites
import os                   # For interacting with the operating system (e.g., shutdown)
import ctypes               # For system commands like locking the screen on Windows
import subprocess           # For cross-platform commands like shutdown
import time                 # For adding pauses

# --- 2. Initialize the Text-to-Speech Engine ---
# Initializing pyttsx3 engine. 'sapi5' is typically used on Windows.
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# Setting the voice property. voices[0] is often a male voice, voices[1] female.
# Change the index (0 or 1) to select a different voice if available.
try:
    engine.setProperty('voice', voices[0].id)
except IndexError:
    print("Warning: Only one voice available, using default.")
except Exception as e:
    print(f"Error setting voice property: {e}")

# --- 3. Create the function for the chatbot to speak ---
def speak(audio):
    """
    This function takes text, prints it to the console, and speaks it audibly.
    
    Args:
        audio (str): The text string for the chatbot to say.
    """
    print(f"Chatbot: {audio}")
    engine.say(audio)
    # Speaks the queued audio and waits until the speaking is finished
    engine.runAndWait()

# --- 4. Create the greeting function (wishMe) ---
def wishMe():
    """Greets the user based on the time of day and introduces the chatbot."""
    hour = int(datetime.datetime.now().hour)

    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am your AI Chatbot. I'm here to assist you. How may I help you today?")

# --- 5. Create the function to take and recognize voice commands (takeCommand) ---
def takeCommand():
    """
    Listens for a command via microphone, recognizes it, and returns the command as text.
    Handles errors for unrecognized speech.
    
    Returns:
        str: The recognized command in lowercase, or "None" if recognition fails.
    """
    r = sr.Recognizer()
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust pause_threshold for better response time (as per instructions)
        r.pause_threshold = 1 
        # Adjust for ambient noise for better accuracy
        r.adjust_for_ambient_noise(source, duration=1.5)
        
        try:
            # Capture audio from the microphone
            audio = r.listen(source)
        except sr.WaitTimeoutError:
            print("No voice detected within the time limit.")
            return "None"


    try:
        print("Recognizing...")
        # Use Google's online speech recognition service
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except sr.UnknownValueError:
        # Error Handling: Runs if recognition fails
        error_msg = "Sorry, I didn't quite catch that. Could you please repeat your command?"
        print(error_msg)
        speak(error_msg)
        return "None"
    except sr.RequestError:
        # Error Handling: Runs if the API request fails (e.g., no internet connection)
        error_msg = "I'm having trouble connecting to the speech recognition service. Please check your internet connection."
        print(error_msg)
        speak(error_msg)
        return "None"
    except Exception as e:
        # General exception handling
        print(f"An unexpected error occurred during recognition: {e}")
        return "None"

    return query.lower() # Return the command in lowercase

# --- 6. Function to handle system commands (Shutdown, Restart, Lock) ---
def handle_system_command(command_type):
    """
    Executes system commands like shutdown, restart, or screen lock (Windows-specific).
    
    Args:
        command_type (str): 'shutdown', 'restart', or 'lock'.
    """
    if command_type == 'lock':
        speak("Locking the computer now.")
        # Windows-specific API call to lock the screen
        if os.name == 'nt': # Check if OS is Windows
            ctypes.windll.user32.LockWorkStation()
        else:
            speak("Screen lock command is currently only configured for Windows.")
            
    elif command_type == 'shutdown':
        speak("Are you sure you want to shut down the computer? Please confirm by saying 'yes' or 'no'.")
        confirmation = takeCommand()
        if 'yes' in confirmation:
            speak("Shutting down the system. Goodbye!")
            # Cross-platform shutdown command (use force for safety)
            if os.name == 'nt': # Windows
                os.system("shutdown /s /t 1")
            else: # Linux/macOS
                subprocess.call(["shutdown", "-h", "now"])
        else:
            speak("Shutdown aborted.")

    elif command_type == 'restart':
        speak("Are you sure you want to restart the computer? Please confirm by saying 'yes' or 'no'.")
        confirmation = takeCommand()
        if 'yes' in confirmation:
            speak("Restarting the system. See you soon!")
            # Cross-platform restart command
            if os.name == 'nt': # Windows
                os.system("shutdown /r /t 1")
            else: # Linux/macOS
                subprocess.call(["reboot"])
        else:
            speak("Restart aborted.")

# --- 7. Main execution block (The brain of the chatbot) ---

if __name__ == "__main__":
    wishMe() # Greet the user once at startup

    # Infinite loop to continuously listen for commands
    while True:
        # Introduce a small pause before listening to prevent immediate relisten
        time.sleep(0.5)
        query = takeCommand()

        # Check if a command was successfully recognized
        if query == "none":
            continue

        # --- Command Logic ---

        # 1. Wikipedia Search (Fetches summary)
        if 'wikipedia' in query or 'search wikipedia for' in query:
            speak('Searching Wikipedia...')
            # Remove the trigger phrase to get the actual search term
            query = query.replace("wikipedia", "").replace("search for", "").replace("what is", "").strip()
            
            try:
                # Fetching the summary (2 sentences long)
                results = wikipedia.summary(query, sentences=2)
                speak(f"According to Wikipedia, {results}")
            except wikipedia.exceptions.PageError:
                speak(f"Sorry, I could not find a Wikipedia page matching '{query}'.")
            except Exception:
                speak(f"An error occurred while searching Wikipedia for '{query}'.")

        # 2. Open Websites
        elif 'open youtube' in query:
            speak("Opening YouTube in your default browser.")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("Opening Google Search in your default browser.")
            webbrowser.open("google.com")

        elif 'open stack overflow' in query or 'open stackoverflow' in query:
            speak("Opening Stack Overflow, a great resource for developers.")
            webbrowser.open("stackoverflow.com")

        # 3. Time and Date
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p") # e.g., "05:30 PM"
            speak(f"The current time is {strTime}")

        elif 'the date' in query:
            strDate = datetime.datetime.now().strftime("%A, %B %d, %Y") # e.g., "Monday, October 20, 2025"
            speak(f"Today's date is {strDate}")

        # 4. System Automation Commands (using the dedicated function)
        elif 'lock computer' in query or 'lock screen' in query:
            handle_system_command('lock')

        elif 'shutdown computer' in query or 'shut down my pc' in query:
            handle_system_command('shutdown')

        elif 'restart computer' in query or 'reboot my pc' in query:
            handle_system_command('restart')
            
        # 5. Simple Interaction / Small Talk (as per instructions)
        elif 'how are you' in query:
            speak("I am doing great, thank you for asking! I am ready to serve. How are you?")
            
        elif 'who are you' in query:
            speak("I am your voice-activated AI Chatbot, designed to help you automate tasks and find information.")

        elif 'thank you' in query or 'thanks' in query:
            speak("You're very welcome! Is there anything else I can do?")

        # 6. Exit/Stop Command
        elif 'exit' in query or 'quit' in query or 'stop' in query or 'goodbye' in query:
            speak("Goodbye! It was nice assisting you.")
            break # Breaks out of the infinite 'while' loop

        # 7. Unrecognized Command Fallback
        else:
            speak(f"I'm not sure how to handle the command: '{query}'. Could you try a different request?")
