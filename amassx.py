#!/usr/bin/env python3

import subprocess
import time
import os
import shutil
import threading

def animate_running():
    animation = "|/-\\"
    while not animation_stopped:
        for char in animation:
            print(f"\rAMASS RUNNING {char}", end="")
            time.sleep(0.1)

def stop_animation():
    global animation_stopped
    animation_stopped = True

def collect_subdomains(subdomain_file):
    subdomains = []

    with open(subdomain_file, "r") as file:
        for line in file:
            subdomain = line.strip()
            subdomains.append(subdomain)

    with open("subdomains.txt", "w") as output_file:
        for subdomain in subdomains:
            output_file.write(subdomain + "\n")

def install_amassx():
    # Get the current script's location
    script_location = os.path.abspath(__file__)
    script_name = os.path.basename(script_location)

    # Destination directory for installation
    destination_directory = '/usr/local/bin'

    try:
        # Copy the script to the destination directory
        shutil.copy(script_location, os.path.join(destination_directory, script_name))

        # Make the script executable
        os.chmod(os.path.join(destination_directory, script_name), 0o755)

        print(f"{script_name} has been installed to {destination_directory}/{script_name}")
    except Exception as e:
        print(f"Installation failed: {e}")

if __name__ == "__main__":
    animation_stopped = False  # Flag to control the animation
    domain = input("Enter Your Target: ")

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

        print("Collecting subdomains...")
        collect_subdomains(f"sub_{domain}.txt")
        print("Subdomains collected in subdomains.txt")
