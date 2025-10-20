import tkinter as tk
from tkinter import scrolledtext
import threading
from main import takeCommand, speak, wishMe  # Import your existing chatbot functions
import webbrowser
import wikipedia
import datetime
import ctypes
import os

# --- GUI Setup ---
root = tk.Tk()
root.title("Voice-Activated AI Chatbot")
root.geometry("700x550")
root.configure(bg="#1e1e1e")  # Dark background

# --- Chat history box ---
chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=80, height=25, font=("Arial", 11), bg="#2b2b2b", fg="white")
chat_history.pack(padx=10, pady=10)

# --- Function to add messages to chat history ---
def add_chat_message(sender, message):
    chat_history.configure(state='normal')
    chat_history.insert(tk.END, f"{sender}: {message}\n")
    chat_history.configure(state='disabled')
    chat_history.yview(tk.END)

# --- Chatbot logic wrapped for GUI ---
def handle_command():
    add_chat_message("System", "Listening for your command...")
    query = takeCommand()
    if query != "none":
        add_chat_message("User", query)
        query_lower = query.lower()

        # Wikipedia
        if 'wikipedia' in query_lower:
            add_chat_message("Chatbot", "Searching Wikipedia...")
            query_term = query_lower.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query_term, sentences=2)
                add_chat_message("Chatbot", results)
                speak(results)
            except:
                msg = f"Sorry, I could not find results for {query_term}"
                add_chat_message("Chatbot", msg)
                speak(msg)

        # Websites
        elif 'open youtube' in query_lower:
            add_chat_message("Chatbot", "Opening YouTube...")
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        elif 'open google' in query_lower:
            add_chat_message("Chatbot", "Opening Google...")
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        # Time
        elif 'the time' in query_lower:
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            add_chat_message("Chatbot", f"The time is {strTime}")
            speak(f"The time is {strTime}")

        # Lock screen
        elif 'lock screen' in query_lower or 'lock the computer' in query_lower:
            add_chat_message("Chatbot", "Locking the screen...")
            speak("Locking the screen")
            ctypes.windll.user32.LockWorkStation()

        # Exit
        elif 'exit' in query_lower or 'quit' in query_lower or 'stop' in query_lower:
            add_chat_message("Chatbot", "Goodbye!")
            speak("Goodbye!")
            root.quit()

        # Default response
        else:
            msg = "I heard you but can't perform that command yet."
            add_chat_message("Chatbot", msg)
            speak(msg)
    else:
        add_chat_message("System", "No command detected. Try again.")

# --- Run voice command in separate thread to avoid freezing GUI ---
def listen_thread():
    t = threading.Thread(target=handle_command)
    t.start()

# --- Speak button ---
speak_button = tk.Button(root, text="🎤 Speak", command=listen_thread, font=("Arial", 12, "bold"), bg="#4caf50", fg="white", width=20, height=2)
speak_button.pack(pady=10)

# --- Greet user on GUI startup ---
def greet_user():
    wishMe()
    add_chat_message("Chatbot", "Hello! I am your AI Chatbot. How may I help you?")

root.after(500, greet_user)  # Delay slightly to load GUI first

# --- Run GUI loop ---
root.mainloop()
