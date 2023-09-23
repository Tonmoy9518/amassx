#!/usr/bin/env python3

import subprocess
import time
import httpx
import os
import shutil
import threading
import sys
import requests  # Import the requests library for HTTP requests

def animate_running():
    animation = "|/-\\"
    while not animation_stopped:
        for char in animation:
            print(f"\rAMASS RUNNING {char}", end="")
            time.sleep(0.1)

def stop_animation():
    global animation_stopped
    animation_stopped = True

def collect_urls(subdomain_file):
    # ... (existing code for collecting URLs)

def install_amassx():
    # ... (existing code for installation)

def check_for_updates():
    try:
        # Make a GET request to GitHub to check for updates
        response = requests.get("https://raw.githubusercontent.com/yourusername/amassx/main/amassx.py")
        if response.status_code == 200:
            remote_code = response.text

            # Read the current local code
            with open(__file__, "r") as file:
                local_code = file.read()

            # Check if the remote code is different from the local code
            if remote_code != local_code:
                print("An update is available. Updating...")
                
                # Save the remote code to a temporary file
                with open("temp_amassx.py", "w") as temp_file:
                    temp_file.write(remote_code)

                # Copy the temporary file to the current script
                shutil.copy("temp_amassx.py", __file__)

                # Remove the temporary file
                os.remove("temp_amassx.py")

                print("Update complete. Please run amassx again.")
                sys.exit(0)
            else:
                print("You are already using the latest version.")
                sys.exit(0)
        else:
            print("Failed to check for updates.")
    except Exception as e:
        print(f"Update check failed: {e}")

if __name__ == "__main__":
    animation_stopped = False  # Flag to control the animation
    domain = input("Enter Your Target: ")

    # Check if the script is being run with the -update argument
    if len(sys.argv) > 1 and sys.argv[1] == "-update":
        check_for_updates()

    # Check if the script is being run for installation
    if domain.lower() == "install":
        install_amassx()
    else:
        # Start the animation in a separate thread
        animation_thread = threading.Thread(target=animate_running)
        animation_thread.start()

        subprocess.call(f"amass enum -passive -d {domain} -o sub_{domain}.txt", shell=True)
        stop_animation()  # Stop the animation after "AMASS END" is displayed
        animation_thread.join()  # Wait for the animation thread to finish

        print("\nAMASS END")

        print("Collecting all URLs and checking for live URLs...")
        collect_urls(f"sub_{domain}.txt")
        print("Live URLs collected in live_url.txt")
        print("All URLs collected in all_url.txt")
