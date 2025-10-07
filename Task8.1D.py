# Code:

import speech_recognition as sr
import RPi.GPIO as GPIO
import time
import tkinter as tk
import threading

# ---------------- GPIO Setup ----------------
LED_PIN = 14  # GPIO14 (physical pin 8)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

# ---------------- Speech Recognition Setup ----------------
recognizer = sr.Recognizer()

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Voice Controlled LED")
root.geometry("350x220")
root.configure(bg="#2c3e50")

# Heading Label
title_label = tk.Label(
    root,
    text="Voice Controlled LED",
    font=("Arial", 16, "bold"),
    fg="white",
    bg="#2c3e50"
)
title_label.pack(pady=10)

# LED Status Label
status_label = tk.Label(
    root,
    text="LED Status: OFF",
    font=("Arial", 14),
    fg="#f1c40f",
    bg="#2c3e50"
)
status_label.pack(pady=20)

# ---------------- GUI Functions ----------------
def update_status(state):
    """Update LED status text and color"""
    color = "lime" if state == "ON" else "#f1c40f"
    status_label.config(text=f"LED Status: {state}", fg=color)

def exit_app():
    """Clean exit from the app"""
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()
    root.destroy()

# Exit Button
exit_button = tk.Button(
    root,
    text="Exit",
    font=("Arial", 12, "bold"),
    bg="#e74c3c",
    fg="white",
    width=10,
    command=exit_app
)
exit_button.pack(pady=20)

# ---------------- Voice Functions ----------------
def listen_for_command():
    """Listen for voice command and return recognized text"""
    with sr.Microphone() as source:
        print("🎙️ Say 'on' or 'off' to control the LED...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"🗣️ You said: {command}")
            return command
        except sr.UnknownValueError:
            print("⚠️ Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"❌ API error: {e}")
            return None

def control_led(command):
    """Turn LED ON or OFF based on command"""
    if "on" in command:
        GPIO.output(LED_PIN, GPIO.HIGH)
        update_status("ON")
        print("💡 LED turned ON")
    elif "off" in command:
        GPIO.output(LED_PIN, GPIO.LOW)
        update_status("OFF")
        print("💡 LED turned OFF")
    else:
        print("⚠️ Command not recognized as 'on' or 'off'")

def voice_loop():
    """Continuously listen for voice commands"""
    while True:
        cmd = listen_for_command()
        if cmd:
            control_led(cmd)
        time.sleep(1)

# ---------------- Start Background Voice Thread ----------------
threading.Thread(target=voice_loop, daemon=True).start()

# ---------------- Run the GUI ----------------
try:
    root.mainloop()
except KeyboardInterrupt:
    print("🛑 Exiting...")
    GPIO.cleanup()
