# A music player controller for Waybar using playerctl
# Times may not be accurate due to the way playerctl handles time for some services, such as Spotify

import sys
import json
import subprocess
import time

print("TEST")

current_player = None
current_song = None
current_artist = None
current_time = 0

# Format a time in seconds to a human readable format (HH:MM:SS)
def format_time(time):
    hours = int(time / 3600)
    minutes = int((time % 3600) / 60)
    seconds = int((time % 3600) % 60)

    # Pad the minutes and seconds with a leading 0 if they are less than 10
    if minutes < 10:
        minutes = f"0{minutes}"

    if seconds < 10:
        seconds = f"0{seconds}"

    if hours == 0:
        return f"{minutes}:{seconds}"
    else:
        return f"{hours}:{minutes}:{seconds}"


def get_player():
    player = subprocess.check_output(['playerctl', '-l']).decode('utf-8').strip()
    return player

def get_song(player):
    song = subprocess.check_output(['playerctl', '-p', player, 'metadata', 'title']).decode('utf-8').strip()
    return song

def get_artist(player):
    artist = subprocess.check_output(['playerctl', '-p', player, 'metadata', 'artist']).decode('utf-8').strip()
    return artist

def get_time(player):

    # There is an issue with services like Spotify where the time will not be displayed
    # instead, "No player could handle this command" will be displayed
    try:
        # Execute with --no-messages to prevent the "No player could handle this command" message
        time = subprocess.check_output(['playerctl', '-p', player, 'position', '--no-messages']).decode('utf-8').strip()
        return time
    except subprocess.CalledProcessError:
        return "Sometime"

def get_status(player):
    status = subprocess.check_output(['playerctl', '-p', player, 'status']).decode('utf-8').strip()
    return status

artist = get_artist(get_player())
song = get_song(get_player())
playTime = get_time(get_player())
status = get_status(get_player())

while True:

    try:
        if get_artist(get_player()) != current_artist:
            current_time = 0
        elif get_song(get_player()) != current_song:
            current_time = 0

        artist = get_artist(get_player())
        song = get_song(get_player())
        playTime = get_time(get_player())
        status = get_status(get_player())

        if playTime == "Sometime" and status == "Playing":
            current_time += 1


        if status == "Playing":
            status = ""
        elif status == "Paused":
            status = ""

        current_artist = artist
        current_song = song

        output = f"{status} {artist} - {song} | {format_time(current_time)}"
        waybar_output = {
            "text": f"{status} {artist} - {song} | {format_time(current_time)}",
            "tooltip": f"{artist} - {song}",
            "class": "custom-playerctl"
        }

        # Print the JSON-encoded output for Waybar
        print(json.dumps(waybar_output))
        sys.stdout.flush()
        # Return the output back to Waybar



        time.sleep(1)

    except KeyboardInterrupt:
        sys.exit(0)

    except subprocess.CalledProcessError:
        print("No player could handle this command")
        time.sleep(1)

    except:
        print("Error")
        time.sleep(1)


