from libraries_used import *

"""
TRANSLATOR FROM A TEXT TO A VOICE OF YOUR LANGUAGE CHOICE

1. Takes user input and translates it into another language.
2. Outputs an .mp3 file named with the current date.
3. Includes input validation and async translation.
4. Finally, runs the full process with run_program().

Libraries used:
- googletrans (translation)
- elevenlabs (text-to-speech)
- asyncio (asynchronous execution)
- dotenv (read .env files)
"""

# --- INPUT FUNCTION -------------------------------------------------
def information_input():
    """
    Collects user input for source language, destination language, and text to translate.

    Returns:
        tuple: (src_language, dstn_language, question_to_user)
    """
    try:
        # Ask user for source language; default to 'auto' if left blank
        source_language = input(
            'In what language do you have your text to translate?\n'
            'Example: (en, es, ja, ko, eo). Leave blank for automatic detection: '
        ).strip()
        src_language = (source_language or 'auto').lower()

        # Ask user for destination language; default to English
        destination_language = input(
            'To what language do you want the result?\n'
            'Example: (en, es, ja, ko, eo): '
        ).strip()
        dstn_language = (destination_language or 'en').lower()

        # Ask user for the text to translate
        question_to_user = input('Enter the text you would like to translate: ')

        return src_language, dstn_language, question_to_user

    except Exception as e:
        print(f"Error occurred while collecting user input: {e}")


# --- TRANSLATION FUNCTION -------------------------------------------------
async def translator_to_text(question_to_user, source_language, destination_language):
    """
    Translates text asynchronously using GoogleTrans.

    Args:
        question_to_user (str): The text provided by the user.
        source_language (str): Source language code (e.g., 'en', 'es').
        destination_language (str): Destination language code.

    Returns:
        str: Translated text.
    """
    async with Translator() as translator:
        try:
            information_language = await translator.translate(
                question_to_user,
                src=source_language,
                dest=destination_language
            )
            return information_language.text
        except Exception as e:
            print(f"Error occurred while translating: {e}")


# --- CHAT VOICE FUNCTION -------------------------------------------------
def chat_voice(translated_text):
    """
    Converts translated text to speech using ElevenLabs API and saves as .mp3.
    """
    # Load the .env document to get the API_KEY
    load_dotenv()
    try:
        api_key = os.getenv('API_KEY')
        client = ElevenLabs(api_key=api_key)

        # Convert translated text into an audio stream
        audio_stream = client.text_to_speech.convert(
            text=translated_text,
            voice_id='ZthjuvLPty3kTMaNKVKb',
            model_id='eleven_multilingual_v2'
        )

        # Create filename using current date/time
        date_time_str = datetime.now().strftime("%m-%d-%Y_%H-%M")
        file_name = f'voice_saved_{date_time_str}.mp3'

        # Save generated audio stream into an .mp3 file
        with open(file_name, 'wb') as f:
            for chunk in audio_stream:
                f.write(chunk)

        print(f"Audio saved as {file_name}")

    except Exception as e:
        print(f"Error occurred while generating voice: {e}")


# --- RUN FUNCTION -------------------------------------------------
def run_program():
    """
    Runs the full translation and text-to-speech:
    1. Collects user input.
    2. Translates the text.
    3. Converts it into speech and saves as an .mp3 file.
    """
    source_language, destination_language, question_to_user = information_input()

    translated_text = asyncio.run(
        translator_to_text(question_to_user, source_language, destination_language)
    )

    chat_voice(translated_text)


# Execute program
run_program()
