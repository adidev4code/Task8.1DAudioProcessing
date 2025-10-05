# Code:

import speech_recognition as sr
import RPi.GPIO as GPIO
import time

# GPIO setup
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

# Speech recognizer setup
recognizer = sr.Recognizer()
mic = sr.Microphone()

print("Say 'Turn on the light' or 'Turn off the light'...")

try:
    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print("You said:", command)

            if "turn on the light" in command.lower():
                GPIO.output(LED_PIN, GPIO.HIGH)
                print("Light turned ON")

            elif "turn off the light" in command.lower():
                GPIO.output(LED_PIN, GPIO.LOW)
                print("Light turned OFF")

            else:
                print("Command not recognized")

        except sr.UnknownValueError:
            print("Sorry, I didn’t catch that.")
        except sr.RequestError:
            print("Speech recognition service error.")
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting program...")
    GPIO.cleanup()

