#!/usr/bin/env python3
# Author: Alex a.k.a. VritraSec
# Project: LucidX — AI-Powered Image Synth Engine
# GitHub: https://github.com/VritraSecz

from datetime import datetime
from time import sleep
from pathlib import Path
import requests
import signal
from core.colors import *
import os
from core.banr import *
#from core.config import *

LAST_STYLE_FILE = "last_style.txt"
LOG_FILE = "generation_log.txt"
STYLE_PRESETS = {
    "1": "photographic",
    "2": "anime",
    "3": "digital-art",
    "4": "neon-punk",
    "5": "fantasy-art",
    "6": "pixel-art",
    "7": "isometric",
    "8": "low-poly"
}


prompt_count = 0
image_count = 0

Path(LAST_STYLE_FILE).unlink(missing_ok=True)

def handle_interrupt(sig, frame):
    print(f"\n{RED}[!] Interrupted by user. Generating summary...{RESET}")
    if os.path.isfile(LAST_STYLE_FILE):
        try:
            os.remove(LAST_STYLE_FILE)
        except Exception as e:
            print(f"{RED}[!] Error: {e}")
    else:
        pass
    print_summary()
    exit()
signal.signal(signal.SIGINT, handle_interrupt)

def get_output_path():
    if Path("/data/data/com.termux/files/usr/bin").exists():
        path = Path("/sdcard/LucidX_Images")
    else:
        path = Path.cwd() / "generated_images"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_user_style():
    os.system("clear")
    print(lucid_logo_banner())
    if Path(LAST_STYLE_FILE).exists():
        with open(LAST_STYLE_FILE, "r") as f:
            return f.read().strip()
    print(f"\n{CYAN}:: Select a style preset below ::{RESET}\n")
    for key, val in STYLE_PRESETS.items():
        print(f"{GRAY} › {GREEN}[{key}] {WHITE}{val}{RESET}")
        
    print()
    while True:
        choice = input(f"{GRAY}:: Select option (1–8): {GREEN}").strip()
        if choice in STYLE_PRESETS:
            selected = STYLE_PRESETS[choice]
            with open(LAST_STYLE_FILE, "w") as f:
                f.write(selected)
            return selected
        else:
            print(f"{RED}[!] Invalid choice. Try again.{RESET}")

def generate_image(prompt, output_path, seed, steps, style):
    from datetime import datetime
    import requests
    from core.colors import GRAY, RED, RESET, QUOTE_BLUE  # assuming color constants here

    # Lazy import of API
    try:
        from core.config import API
    except ImportError:
        print(f"{RED}[!] Missing config file: core/config.py{RESET}")
        return

    if not API.strip():
        print(f"{RED}[!] API key is missing in config.py. Please set it before generating images.{RESET}")
        return

    global image_count
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"
    headers = {
        "Authorization": f"Bearer {API}",
        "Accept": "image/*"
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    time_label = datetime.now().strftime("%H:%M:%S")
    filename = f"{timestamp}.png"
    filepath = output_path / filename

    files = {
        "prompt": (None, prompt),
        "output_format": (None, "png"),
        "style_preset": (None, style),
        "seed": (None, str(seed)),
        "steps": (None, str(steps))
    }

    try:
        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(response.content)
            log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Prompt: \"{prompt}\" -› {filename}\n"
            with open(LOG_FILE, "a") as log:
                log.write(log_entry)
            print(f"{GRAY}[{time_label}] {QUOTE_BLUE}{filename} {GRAY}saved successfully.{RESET}")
            image_count += 1
        else:
            print(f"{RED}[!] Failed: {response.status_code}\n{response.text}{RESET}")
            print(f"{RED}[!] Try to restart the tool\n{RESET}")
    except Exception as e:
        print(f"{RED}[!] Error: {str(e)}{RESET}")
        print(f"{RED}[!] Try to restart the tool.{RESET}")


def print_summary():
    print(f"\n{WHITE}:: LucidX Session Summary ::")
    print(f"{GREEN} › Prompts entered    :{GRAY} {prompt_count}")
    print(f"{GREEN} › Images generated   :{GRAY} {image_count}")
    print(f"{GREEN} › Output directory   :{GRAY} {get_output_path()}")
    print(f"{WHITE} › Session completed.{RESET}\n")

def main_genx():
    global prompt_count
    output_path = get_output_path()
    selected_style = get_user_style()

    while True:
        print(f"\n{CYAN}:: Enter your prompt below ::{RESET}")
        prompt = input(f"{GRAY}■›{WHITE} ").strip()
        if not prompt:
            print(f"{RED}[!] Prompt cannot be empty.{RESET}")
            continue

        prompt_count += 1
        print(f"{GRAY}\n■› Using style: {VALUE}{selected_style}{RESET}")
        print(f"{GREEN}[...] {GRAY}Generating images...\n")

        for i in range(4):
            generate_image(prompt, output_path, seed=1234 + i, steps=30, style=selected_style)
            sleep(1)

        print(f"\n{GREEN}[✓] Process completed.{RESET}")
        choice = input(f"{GRAY}■› Generate new image ({GREEN}y/n{GRAY}): {WHITE}").strip().lower()
        if choice != "y":
            print_summary()
            Path(LAST_STYLE_FILE).unlink(missing_ok=True)
            break
