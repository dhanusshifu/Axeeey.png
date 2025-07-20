#!/usr/bin/env python3
# Author: Alex a.k.a. VritraSec
# Project: LucidX — AI-Powered Image Synth Engine
# GitHub: https://github.com/VritraSecz


from core.banr import *
from core.colors import *
from core.modulex import *
from core.genx import *
import os
import signal

def handle_interrupt(sig, frame):
    print(f"\n{RED}[!] Interrupted by user. Exiting...{RESET}")
    if os.path.isfile(LAST_STYLE_FILE):
        try:
            os.remove(LAST_STYLE_FILE)
        except Exception as e:
            print(f"{RED}[!] Error: {e}")
    else:
        pass
    lucid_exit()
    exit()
signal.signal(signal.SIGINT, handle_interrupt)

def lucidx_main_menu():

    while True:
        os.system("clear" if os.name != "nt" else "cls")
        print(lucid_Main_logo())
        MAIN_MENU = f"""
{GREEN}..:: MAIN MENU ::..

{GREEN} › [1] {WHITE}Image Generation
{GREEN} › [2] {WHITE}Configure API Key
{GREEN} › [3] {WHITE}Connect With Us
{GREEN} › [4] {WHITE}About LucidX
{GREEN} › [5] {WHITE}Help / Documentation
{GREEN} › [6] {WHITE}Exit

{GRAY}:: Select option (1–6): {GREEN}"""

        main_choice = input(MAIN_MENU).strip()

        if main_choice == "":
            continue

        elif main_choice == "1":
            main_genx()
            exit()

        elif main_choice == "2":
            configure_api_key()

        elif main_choice == "3":
            lucid_connect()

        elif main_choice == "4":
            about_lucidx()

        elif main_choice == "5":
            lucid_help()

        elif main_choice == "6":
            lucid_exit()
            break

        else:
            print(GRAY + "! Invalid option. Please try again.\n")

if __name__ == "__main__":
    lucidx_main_menu()
