# Code:

import speech_recognition as sr
import RPi.GPIO as GPIO
import tkinter as tk
import threading
import time

# ---------------- GPIO SETUP ----------------
LED_PIN = 14  # GPIO14 for LED

def setup_gpio():
    """Init GPIO pin for LED"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)  # LED OFF

# ---------------- SPEECH RECOGNITION ----------------
recognizer = sr.Recognizer()

def get_bluetooth_mic_index():
    """Find Bluetooth mic if connected, else use default"""
    for i, name in enumerate(sr.Microphone.list_microphone_names()):
        if "Bluetooth" in name:
            print(f"🎧 Bluetooth mic found: {name} (index {i})")
            return i
    print("⚠️ Bluetooth mic not found, using default mic.")
    return None

MIC_INDEX = get_bluetooth_mic_index()

def listen_command():
    """Listen and return 'on'/'off' command"""
    try:
        with sr.Microphone(device_index=MIC_INDEX) as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)
        command = recognizer.recognize_google(audio).lower()
        print(f"🗣️ You said: {command}")
        return command
    except sr.UnknownValueError:
        print("⚠️ Could not understand audio.")
    except sr.RequestError as e:
        print(f"❌ API error: {e}")
    return None

# ---------------- LED CONTROL ----------------
def control_led(command):
    """Turn LED ON/OFF and update GUI"""
    if "on" in command:
        GPIO.output(LED_PIN, GPIO.HIGH)
        update_status("ON")
        print("💡 LED ON")
    elif "off" in command:
        GPIO.output(LED_PIN, GPIO.LOW)
        update_status("OFF")
        print("💡 LED OFF")
    else:
        print("⚠️ Command not recognized")

# ---------------- GUI SETUP ----------------
root = tk.Tk()
root.title("Voice Controlled LED")
root.geometry("350x220")
root.configure(bg="#2c3e50")

title_label = tk.Label(root, text="Voice Controlled LED",
                       font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
title_label.pack(pady=10)

status_label = tk.Label(root, text="LED Status: OFF",
                        font=("Arial", 14), fg="#f1c40f", bg="#2c3e50")
status_label.pack(pady=20)

def update_status(state):
    """Update LED status label"""
    color = "lime" if state == "ON" else "#f1c40f"
    status_label.config(text=f"LED Status: {state}", fg=color)

def exit_app():
    """Turn off LED, cleanup GPIO, close GUI"""
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()
    root.destroy()
    print("🛑 App closed.")

exit_button = tk.Button(root, text="Exit", font=("Arial", 12, "bold"),
                        bg="#e74c3c", fg="white", width=10, command=exit_app)
exit_button.pack(pady=20)

# ---------------- BACKGROUND VOICE THREAD ----------------
def voice_loop():
    """Continuously listen for voice commands"""
    while True:
        cmd = listen_command()
        if cmd:
            control_led(cmd)
        time.sleep(0.5)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    setup_gpio()
    threading.Thread(target=voice_loop, daemon=True).start()
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        exit_app()

