# EF - hack things (Puru)

import sounddevice as sd
import numpy as np
import wave
import openai

# Set up OpenAI API key
openai.api_key = "<API_KEY>"
# Function to record audio using sounddevice
def record_audio(duration=5, sample_rate=44100):
    print("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    print("Recording stopped.")
    return audio_data

# Function to save audio to a WAV file
def save_audio_to_file(filename, audio_data, sample_rate=44100):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 2 bytes for 'int16'
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data)

# Function to recognize speech using OpenAI's Whisper (via a transcription service)
def transcribe_audio(filename):
    with open(filename, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript['text']

# Function to interpret the command based on the transcribed text
def interpret_command(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Map voice input to a command based on the options below."},
            {"role": "user", "content": (
                "Given the following voice input, map it to one of the four specific commands below:\n"
                "1. command_one: If the user says 'I want to add something to my library', execute command_one.\n"
                "2. command_two: If the user says 'I want to add something to my calendar', execute command_two.\n"
                "3. command_three: If the user says 'I want to reorganize something', execute command_three.\n\n"
                f"Voice input: {text}\n\n"
                "Return the name of the command (e.g., 'command_one')."
            )}
        ],
        max_tokens=20
    )
    return response['choices'][0]['message']['content'].strip()

# Command functions
def command_one():
    print("Executing Command One...")

def command_two():
    print("Executing Command Two...")

def command_three():
    print("Executing Command Three...")

# Map the interpreted command to a function call
def execute_command(command):
    command_map = {
        "command_one": command_one,
        "command_two": command_two,
        "command_three": command_three,
    }
    if command in command_map:
        command_map[command]()
    else:
        print("Unknown command.")

if __name__ == "__main__":
    # Record and save audio
    audio_data = record_audio(duration=5)
    save_audio_to_file("input.wav", audio_data)

    # Transcribe audio to text using OpenAI's Whisper
    text = transcribe_audio("input.wav")
    print(f"Transcribed text: {text}")

    # If text is successfully recognized, interpret the command
    if text:
        command = interpret_command(text)
        execute_command(command)