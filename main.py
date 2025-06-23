import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import pyjokes

listener = sr.Recognizer()
Alexa = pyttsx3.init()
voices = Alexa.getProperty('voices')
Alexa.setProperty('voice', voices[1].id)  # Set female voice (may vary by system)

def talk(text):
    """Speak the given text using pyttsx3."""
    Alexa.say(text)
    Alexa.runAndWait()

def take_command():
    """Listen for a voice command and return it as text."""
    try:
        with sr.Microphone() as source:
            print("Please speak something...")
            listener.adjust_for_ambient_noise(source, duration=0.5)
            voice = listener.listen(source, timeout=5, phrase_time_limit=7)
            print("Processing your input...")
            command = listener.recognize_google(voice)
            command = command.lower()
            if "alexa" in command:
                command = command.replace("alexa", "").strip()
            return command
    except sr.WaitTimeoutError:
        print("Listening timed out. Please try again.")
    except sr.UnknownValueError:
        print("Sorry, I did not catch that.")
    except sr.RequestError:
        print("Sorry, there was a problem with the speech recognition service.")
    except Exception as e:
        print(f"Error: {e}")
    return ""

def run_alexa():
    """Process the user's command and respond accordingly."""
    command = take_command()
    if not command:
        return
    print(f"Command: {command}")

    if "hello" in command:
        talk("Hello! How can I assist you today?")
    elif "time" in command:
        from datetime import datetime
        current_time = datetime.now().strftime("%I:%M %p")
        talk(f"The current time is {current_time}.")
    elif "play" in command:
        song = command.replace("play", "").strip()
        talk(f"Playing {song} on YouTube.")
        pywhatkit.playonyt(song)
    elif "tell me about" in command:
        look_for = command.replace("tell me about", "").strip()
        try:
            info = wikipedia.summary(look_for, sentences=1)
            print(info)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk("There are multiple results. Please be more specific.")
            print(f"DisambiguationError: {e}")
        except wikipedia.exceptions.PageError:
            talk("Sorry, I could not find any information on that topic.")
        except Exception as e:
            talk("Sorry, something went wrong with Wikipedia.")
            print(f"Wikipedia error: {e}")
    elif "joke" in command:
        joke = pyjokes.get_joke()
        talk(joke)
    elif "date" in command:
        from datetime import datetime
        today = datetime.now().strftime("%B %d, %Y")
        talk(f"Today's date is {today}.")
    elif "stop" in command or "exit" in command or "quit" in command:
        talk("Goodbye!")
        print("Exiting...")
        exit()
    else:
        talk("I didn't understand that. Please try again. I can also search for it online.")
        print("But I can search for it online.")
        pywhatkit.search(command)

if __name__ == "__main__":
    while True:
        run_alexa()
