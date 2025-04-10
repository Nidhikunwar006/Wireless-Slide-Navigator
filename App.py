from flask import Flask, jsonify
import pyautogui
import os
import time
import pygetwindow as gw  # For checking active window
from flask_cors import CORS  # Allow cross-origin requests

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend to communicate with backend

@app.route('/')
def index():
    return jsonify({"message": "Wireless Slide Controller API is running!"})

@app.route('/power')
def toggle_slideshow():
    ppt_running = any("POWERPNT.EXE" in line for line in os.popen('tasklist').readlines())
    slideshow_active = any("Slide Show" in win.title for win in gw.getWindowsWithTitle("Slide Show"))

    if ppt_running and slideshow_active:
        pyautogui.hotkey('esc')
    elif ppt_running and not slideshow_active:
        pyautogui.hotkey('f5')
    else:
        os.system('start powerpnt.exe')
        time.sleep(5)
        pyautogui.hotkey('f5')

    return jsonify({"status": "success", "action": "power"})

@app.route('/next')
def next_slide():
    pyautogui.hotkey('right')
    return jsonify({"status": "success", "action": "next"})

@app.route('/previous')
def previous_slide():
    pyautogui.hotkey('left')
    return jsonify({"status": "success", "action": "previous"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)