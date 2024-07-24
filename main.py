import os
import webbrowser
import datetime
import speech_recognition as sr
import requests
import pyjokes
from googletrans import Translator


def say(text):
    """Function to convert text to speech."""
    os.system(f'say "{text}"')

def takeCommand():
    """Function to take voice commands from the user and return the recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User Said: {query}")
            return query
        except Exception as e:
            print("Error:", e)
            return "Some Error Occurred. Sorry from Divyang Mitra."


def get_news():
    """Function to fetch the top 5 news headlines."""
    api_key = '0efe117d8ddb4edbb928e5aa526f3312'
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(url)
    news_data = response.json()
    headlines = [article['title'] for article in news_data['articles'][:5]]
    return headlines


def tell_joke():
    """Function to fetch a random joke."""
    joke = pyjokes.get_joke()
    return joke


def set_volume(level):
    """Function to set the system volume."""
    os.system(f"osascript -e 'set volume output volume {level}'")


def translate_text(text, dest_lang):
    """Function to translate text to the specified destination language."""
    try:
        translator = Translator()
        translated = translator.translate(text, dest=dest_lang)
        return translated.text
    except Exception as e:
        print("Translation error:", e)
        return "I couldn't translate the text. Please try again."


def get_destination_language():
    """Function to get the destination language from the user."""
    say("To which language would you like to translate?")
    dest_lang = takeCommand().lower()
    return dest_lang


def get_destination_address():
    """Get the destination address from the user."""
    say("Please say the destination address.")
    while True:
        address = takeCommand()
        if address:
            say(f"Navigating to {address}")
            return address
        else:
            say("I didn't catch that. Please say the destination address.")


def get_payment_details():
    """Get the payment details from the user."""
    say("Please say the recipient's name.")
    recipient = takeCommand()
    if not recipient:
        say("I didn't catch that. Please say the recipient's name.")
        recipient = takeCommand()

    say("Please say the amount to send.")
    amount = takeCommand()
    if not amount:
        say("I didn't catch that. Please say the amount to send.")
        amount = takeCommand()

    return recipient, amount


def google_search(query):
    """Function to search on Google."""
    search_query = query.replace("search for", "").strip()
    say(f"Searching Google for {search_query}")
    search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
    webbrowser.open(search_url)


if __name__ == '__main__':
    print('PyCharm')
    print("Hello, my name is Divyang Mitra. How can I help you?")
    say("Hello, my name is Divyang Mitra. How can I help you?")
    while True:
        query = takeCommand().lower()

        # List of sites to open with voice command
        sites = [["youtube", "https://www.youtube.com"],
                 ["wikipedia", "https://www.wikipedia.com"],
                 ["dsi", "https://www.dsatm.edu.in"],
                 ["google", "https://www.google.com"]]

        # Open specified sites based on the command
        for site in sites:
            if f"open {site[0]}" in query:
                say(f"Opening {site[0]}, mam...")
                webbrowser.open(site[1])
                break

        # Play music if command is given
        if "open music" in query:
            musicPath = "/Users/manas/Downloads/play.mp3"
            import subprocess, sys

            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, musicPath])

        # Set the system volume
        elif "set volume to" in query:
            level = int(query.split("to")[-1].strip())
            set_volume(level)
            say(f"Volume set to {level}")
            print(f"Volume set to {level}")

        # Tell the current time
        elif "the time" in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"Mam, the time is {strfTime}")
            say(f"Mam, the time is {strfTime}")

        # Provide top news headlines
        elif "today's news" in query.lower():
            headlines = get_news()
            for i, headline in enumerate(headlines, 1):
                print(f"Headline {i}: {headline}")
                say(f"Headline {i}: {headline}")

        # Tell a random joke
        elif "tell me a joke" in query.lower():
            joke = tell_joke()
            say(joke)
            print(joke)

        # Translate the given text to the specified language
        elif "translate" in query.lower():
            text_to_translate = query.replace("translate", "").strip()
            destination_language = get_destination_language()
            translated_text = translate_text(text_to_translate, destination_language)
            say(translated_text)
            print(translated_text)

        # Opens Google maps. Asks the destinations and directs you to your destination.
        elif query and "open maps" in query:
            say("Opening Google Maps")
            destination = get_destination_address()
            url = f"https://www.google.com/maps/dir/?api=1&destination={destination.replace(' ', '+')}"
            webbrowser.open(url)
            say("Here are the directions to your destination.")

        # Opens payment site. Asks the recipient's name. Asks the amount you want to send.
        elif query and "open payment site" in query:
            say("Opening payment site")
            recipient, amount = get_payment_details()
            # Assuming PayPal URL format. Modify this URL for the appropriate payment site.
            url = f"https://www.paypal.com/cgi-bin/webscr?cmd=_xclick&business={recipient}&amount={amount}"
            webbrowser.open(url)
            say(f"Directing you to the payment site to send {amount} to {recipient}.")

        # Say whatever you want to search on google.
        elif query and "search for" in query:
            google_search(query)
