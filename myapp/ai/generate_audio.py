from pathlib import Path
from openai import OpenAI
import os

def add_voice(input_script):
    '''
    voice_options = ["alloy", "ash", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer"]
    if not (voice in voice_options):
        voice_opt = "alloy"
    else:
        voice_opt = voice 
    '''
    voice_opt = "alloy"
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice_opt,
        input=input_script,
    ) 

    if response and response.content:
        return response.content

    return None



