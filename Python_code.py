import serial
import time
import wave
import pyaudio
import whisper
import tkinter as tk
from threading import Thread

arduino_port = 'COM3'  
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)

model = whisper.load_model("base")

def show_recording_window():
    root = tk.Tk()
    root.title("Recording")
    label = tk.Label(root, text="Recording", font=("Arial", 24))
    label.pack()
    root.after(5000, root.destroy)  
    root.mainloop()

def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []

    for _ in range(0, int(44100 / 1024 * 5)):
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open("recording.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))

def transcribe_audio():
    result = model.transcribe("recording.wav")
    print("Transcription:", result["text"])
    return result["text"]

def send_text_to_lcd(text):
    ser.write((text + '\n').encode())

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        
        if line == "SOUND_DETECTED":
            Thread(target=show_recording_window).start()
            record_audio()
            transcribe_audio()
            send_text_to_lcd(transcribe_audio())