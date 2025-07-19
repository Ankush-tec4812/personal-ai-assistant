import speech_recognition as sr
import pyttsx3
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import os
import subprocess
import sys
import time

class PersonalAIAssistant:
    def __init__(self):
        """Initialize the Personal AI Assistant"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = None
        self.db = None
        
        # Initialize Firebase
        self.init_firebase()
        
        # Initialize Text-to-Speech
        self.init_tts()
        
        # Adjust for ambient noise
        print("Adjusting for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        print("Ready to listen!")

    def init_firebase(self):
        """Initialize Firebase connection"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Look for service account key
                service_account_path = "assistant/serviceAccountKey.json"
                if os.path.exists(service_account_path):
                    cred = credentials.Certificate(service_account_path)
                    firebase_admin.initialize_app(cred)
                    self.db = firestore.client()
                    print("Firebase initialized successfully!")
                else:
                    print("Warning: Firebase service account key not found. Logging will be disabled.")
                    print("Please place your serviceAccountKey.json in the assistant/ directory.")
            else:
                self.db = firestore.client()
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            self.db = None

    def init_tts(self):
        """Initialize Text-to-Speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configure voice settings
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to use a female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 180)  # Speed of speech
            self.tts_engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
            
            print("Text-to-Speech engine initialized!")
        except Exception as e:
            print(f"Error initializing TTS engine: {e}")
            self.tts_engine = None

    def speak(self, text):
        """Convert text to speech"""
        print(f"Assistant: {text}")
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"Error in text-to-speech: {e}")
        else:
            print("TTS engine not available")

    def listen_command(self):
        """Listen for voice command and convert to text"""
        try:
            print("Listening...")
            with self.microphone as source:
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("Processing...")
            # Use Google's speech recognition
            command = self.recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
            
        except sr.WaitTimeoutError:
            return "timeout"
        except sr.UnknownValueError:
            return "unknown"
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            return "error"
        except Exception as e:
            print(f"Unexpected error in speech recognition: {e}")
            return "error"

    def get_current_time(self):
        """Get current time"""
        now = datetime.datetime.now()
        time_str = now.strftime("%I:%M %p on %B %d, %Y")
        return f"The current time is {time_str}"

    def get_weather_info(self):
        """Get weather information (placeholder)"""
        return "I'm sorry, I don't have access to real-time weather data yet. You can check your weather app or ask me to open it for you."

    def save_note(self, note_text):
        """Save a note to a text file"""
        try:
            notes_file = "assistant/notes.txt"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(notes_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {note_text}\n")
            
            return f"Note saved successfully: {note_text}"
        except Exception as e:
            return f"Error saving note: {e}"

    def open_application(self, app_name):
        """Open an application"""
        try:
            app_name = app_name.lower()
            
            # Common applications mapping
            apps = {
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe',
                'browser': 'start chrome',
                'chrome': 'start chrome',
                'firefox': 'start firefox',
                'explorer': 'explorer.exe',
                'file manager': 'explorer.exe',
                'music': 'start spotify',
                'spotify': 'start spotify'
            }
            
            if app_name in apps:
                if os.name == 'nt':  # Windows
                    os.system(apps[app_name])
                else:  # Linux/Mac
                    subprocess.run(['xdg-open' if os.name == 'posix' else 'open', app_name], check=True)
                return f"Opening {app_name}"
            else:
                return f"I don't know how to open {app_name}. You can teach me by updating my application list."
                
        except Exception as e:
            return f"Error opening application: {e}"

    def make_system_call(self, action):
        """Handle system calls like making phone calls (placeholder)"""
        return "I'm sorry, I cannot make actual phone calls yet. This feature would require integration with your phone system or VoIP service."

    def process_command(self, command):
        """Process the voice command and return appropriate response"""
        command = command.lower().strip()
        
        try:
            # Time queries
            if any(word in command for word in ['time', 'clock', 'what time']):
                return self.get_current_time()
            
            # Weather queries
            elif any(word in command for word in ['weather', 'temperature', 'forecast']):
                return self.get_weather_info()
            
            # Note saving
            elif 'save note' in command or 'take note' in command:
                # Extract note content
                if 'save note' in command:
                    note_content = command.split('save note', 1)[1].strip()
                else:
                    note_content = command.split('take note', 1)[1].strip()
                
                if note_content:
                    return self.save_note(note_content)
                else:
                    return "What would you like me to save as a note?"
            
            # Opening applications
            elif 'open' in command:
                app_name = command.replace('open', '').strip()
                if app_name:
                    return self.open_application(app_name)
                else:
                    return "What application would you like me to open?"
            
            # Making calls
            elif 'call' in command or 'phone' in command:
                return self.make_system_call('call')
            
            # General questions and decision making
            elif any(word in command for word in ['what', 'how', 'why', 'when', 'where', 'should i', 'help me decide']):
                return self.handle_general_question(command)
            
            # Greeting
            elif any(word in command for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
                return "Hello! I'm your personal AI assistant. How can I help you today?"
            
            # Exit commands
            elif any(word in command for word in ['goodbye', 'bye', 'exit', 'quit', 'stop']):
                return "Goodbye! Have a great day!"
            
            else:
                return "I'm not sure how to help with that. You can ask me about the time, weather, save notes, open applications, or ask general questions."
                
        except Exception as e:
            return f"I encountered an error processing your request: {e}"

    def handle_general_question(self, question):
        """Handle general questions and provide helpful responses"""
        question = question.lower()
        
        # Simple decision making
        if 'should i' in question:
            import random
            responses = [
                "Based on what you've told me, I think you should go for it!",
                "It might be worth considering the pros and cons first.",
                "Trust your instincts - you usually know what's best.",
                "Maybe sleep on it and decide tomorrow?",
                "What does your gut feeling tell you?"
            ]
            return random.choice(responses)
        
        # General information
        elif 'what is' in question or 'what are' in question:
            return "That's an interesting question! I'd recommend checking a reliable source like Wikipedia or asking a more specialized AI for detailed information."
        
        # How-to questions
        elif 'how to' in question or 'how do' in question:
            return "For step-by-step instructions, I'd suggest searching online or checking tutorial websites. Is there a specific part you'd like help with?"
        
        else:
            return "That's a thoughtful question! While I can help with basic tasks, you might want to consult specialized resources for detailed information."

    def log_to_firestore(self, log_type, command, response):
        """Log interaction to Firestore"""
        if not self.db:
            return
        
        try:
            doc_ref = self.db.collection('assistantLogs').document()
            doc_ref.set({
                'timestamp': firestore.SERVER_TIMESTAMP,
                'command': command,
                'response': response,
                'type': log_type
            })
            print("Logged to Firestore successfully")
        except Exception as e:
            print(f"Error logging to Firestore: {e}")

    def run(self):
        """Main loop for the assistant"""
        self.speak("Hello! I'm your personal AI assistant. I'm ready to help you!")
        
        while True:
            try:
                # Listen for command
                command = self.listen_command()
                
                if command == "timeout":
                    continue
                elif command == "unknown":
                    self.speak("I didn't catch that. Could you please repeat?")
                    continue
                elif command == "error":
                    self.speak("I'm having trouble with speech recognition. Please try again.")
                    continue
                
                # Process command
                response = self.process_command(command)
                
                # Speak response
                self.speak(response)
                
                # Log interaction
                self.log_to_firestore("command", command, response)
                
                # Check for exit command
                if any(word in command.lower() for word in ['goodbye', 'bye', 'exit', 'quit', 'stop']):
                    break
                    
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                break
            except Exception as e:
                error_msg = f"An unexpected error occurred: {e}"
                print(error_msg)
                self.speak("I encountered an error. Let me try to continue.")
                self.log_to_firestore("error", "system_error", error_msg)

if __name__ == "__main__":
    try:
        assistant = PersonalAIAssistant()
        assistant.run()
    except Exception as e:
        print(f"Failed to start assistant: {e}")
        print("Make sure all dependencies are installed and try again.")
