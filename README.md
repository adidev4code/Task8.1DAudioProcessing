# Voice-Controlled LED using Raspberry Pi

## Project Overview

This project demonstrates a **voice-controlled LED** using a Raspberry Pi, a **Bluetooth earbud microphone**, and a single **LED circuit**.

The system listens to voice commands ("on" / "off") and toggles the LED. A **Tkinter GUI** shows the **real-time LED status**.

---

## Hardware

* Raspberry Pi 3B / 4 / 4B
* Bluetooth earbud microphone
* 5mm LED
* 220 Ω resistor
* Breadboard & jumper wires

**Connections:**

| Component | Raspberry Pi Pin | Notes                   |
| --------- | ---------------- | ----------------------- |
| LED (+)   | GPIO 14 (Pin 8)  | Anode via 220Ω resistor |
| LED (-)   | GND (Pin 6)      | Cathode                 |
| Mic       | Bluetooth        | Paired wirelessly       |

---

## Software

* Python 3.x
* Python packages:

```bash
sudo apt update
sudo apt install python3-pip
pip3 install SpeechRecognition RPi.GPIO pyaudio tk
```

> If PyAudio fails:

```bash
sudo apt install portaudio19-dev
pip3 install pyaudio
```

---

## Usage

1. Pair Bluetooth mic and set as default input.
2. Connect LED circuit.
3. Run the code:

```bash
python3 voice_led.py
```

4. GUI shows **LED Status: OFF**.
5. Speak commands:

   * **"on"** → LED ON, GUI green
   * **"off"** → LED OFF, GUI yellow
6. Click **Exit** or press **Ctrl+C** to safely close the app.

---


