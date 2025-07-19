# Personal AI Assistant

A voice-powered AI assistant built with Python that can handle various tasks including answering questions, saving notes, opening applications, and logging all interactions to Firebase.

## Features

- **Voice Recognition**: Uses speech recognition to understand voice commands
- **Text-to-Speech**: Provides natural voice responses
- **Task Automation**: Can save notes, open applications, and perform system tasks
- **Smart Responses**: Handles questions about time, weather, general information, and decision-making
- **Firebase Logging**: All interactions are logged to Firebase Firestore with timestamps
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Prerequisites

- Python 3.7 or higher
- Microphone access
- Internet connection for speech recognition and Firebase
- Firebase project with Firestore enabled

## Installation

### 1. Install Python Dependencies

```bash
cd assistant
pip install -r requirements.txt
```

**Note for different operating systems:**

- **Windows**: PyAudio should install automatically
- **macOS**: You might need to install portaudio first:
  ```bash
  brew install portaudio
  pip install pyaudio
  ```
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt-get install python3-pyaudio
  # or
  sudo apt-get install portaudio19-dev python3-all-dev
  pip install pyaudio
  ```

### 2. Firebase Setup

#### Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or use an existing one
3. Enable Firestore Database
4. Set up Firestore rules (for development, you can use test mode)

#### Get Service Account Key
1. In Firebase Console, go to Project Settings > Service Accounts
2. Click "Generate new private key"
3. Download the JSON file
4. Rename it to `serviceAccountKey.json`
5. Place it in the `assistant/` directory

**Important**: Never commit the service account key to version control!

#### Configure Firestore Rules (Optional)
For development, you can use these permissive rules:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

For production, implement proper authentication and security rules.

## Usage

### Running the Assistant

```bash
python assistant.py
```

### Voice Commands

The assistant responds to various types of commands:

#### Information Queries
- "What time is it?"
- "What's the weather like?"
- "What day is today?"

#### Note Taking
- "Save note: Buy groceries tomorrow"
- "Take note: Meeting with John at 3 PM"

#### Application Control
- "Open calculator"
- "Open browser"
- "Open notepad"
- "Open file manager"

#### Decision Making
- "Should I go for a walk?"
- "Help me decide what to eat"
- "What should I do today?"

#### General Questions
- "What is artificial intelligence?"
- "How do I learn Python?"
- "Why is the sky blue?"

#### Exit Commands
- "Goodbye"
- "Exit"
- "Stop"
- "Quit"

## Configuration

### Customizing Voice Settings

You can modify the TTS settings in the `init_tts()` method:

```python
# Speech rate (words per minute)
self.tts_engine.setProperty('rate', 180)

# Volume (0.0 to 1.0)
self.tts_engine.setProperty('volume', 0.9)

# Voice selection (if multiple voices available)
voices = self.tts_engine.getProperty('voices')
self.tts_engine.setProperty('voice', voices[0].id)  # Change index for different voice
```

### Adding New Applications

To add support for new applications, modify the `apps` dictionary in the `open_application()` method:

```python
apps = {
    'your_app': 'command_to_open_app',
    'vscode': 'code',  # Example for VS Code
    'discord': 'start discord',  # Example for Discord
}
```

### Extending Command Processing

Add new command types in the `process_command()` method:

```python
elif 'your_keyword' in command:
    return self.your_custom_function(command)
```

## Troubleshooting

### Common Issues

1. **Microphone not working**
   - Check microphone permissions
   - Ensure microphone is not being used by another application
   - Try running as administrator (Windows) or with sudo (Linux)

2. **Speech recognition errors**
   - Check internet connection
   - Speak clearly and at moderate pace
   - Reduce background noise

3. **Firebase connection issues**
   - Verify service account key is in the correct location
   - Check Firebase project ID and permissions
   - Ensure Firestore is enabled in your Firebase project

4. **TTS not working**
   - Check system audio settings
   - Try different TTS engines if available
   - Restart the application

5. **PyAudio installation issues**
   - Install system dependencies first (see installation section)
   - Use conda instead of pip: `conda install pyaudio`

### Debug Mode

To enable more detailed logging, modify the logging level:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## File Structure

```
assistant/
├── assistant.py          # Main assistant application
├── requirements.txt      # Python dependencies
├── serviceAccountKey.json # Firebase service account (not in repo)
├── notes.txt            # Saved notes (created automatically)
└── README.md           # This file
```

## Security Considerations

- Never commit `serviceAccountKey.json` to version control
- Use proper Firestore security rules in production
- Consider implementing user authentication for multi-user scenarios
- Regularly rotate Firebase service account keys

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

If you encounter issues:

1. Check the troubleshooting section
2. Verify all dependencies are installed correctly
3. Ensure Firebase is configured properly
4. Check the console output for error messages

For additional help, please create an issue in the repository with:
- Your operating system
- Python version
- Error messages
- Steps to reproduce the issue
