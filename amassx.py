#!/usr/bin/env python3

import subprocess
import time
import httpx
import os
import shutil

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
    live_urls = []  # To store live URLs
    all_urls = []   # To store all URLs

    with open(subdomain_file, "r") as file:
        for line in file:
            subdomain = line.strip()
            url = f"http://{subdomain}"  # Assuming HTTP, you can modify for HTTPS
            all_urls.append(url)
            try:
                response = httpx.head(url, timeout=5)
                if response.status_code == 200:
                    live_urls.append(url)
            except Exception as e:
                pass  # Handle exceptions as needed

    with open("live_url.txt", "w") as live_output_file:
        for url in live_urls:
            live_output_file.write(url + "\n")

    with open("all_url.txt", "w") as all_output_file:
        for url in all_urls:
            all_output_file.write(url + "\n")

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

        print("Collecting all URLs and checking for live URLs...")
        collect_urls(f"sub_{domain}.txt")
        print("Live URLs collected in live_url.txt")
        print("All URLs collected in all_url.txt")