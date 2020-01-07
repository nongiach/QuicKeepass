#!/usr/bin/python3
# Author: @chaignc

from pykeepass import PyKeePass, exceptions as kp_exceptions
from subprocess import Popen, PIPE
import sys
import time

# apt install rofi xdotool
# sudo pip3 install pykeepass
# i3 config: bindsym $mod+u exec "/home/cc/perso/keepass/keeprofi.py /home/cc/perso/keepass/kali.kdbx"
class Config:
    userpass_key = "Alt+Return"

def sh(cmd, stdin="", sleep=False):
    if sleep:
        time.sleep(0.5)
    process = Popen(cmd.split(), stdin=PIPE, stdout=PIPE)
    process.stdin.write(bytes(stdin, "utf-8"))
    stdout = process.communicate()[0].decode('utf-8').strip()
    process.stdin.close()
    returncode = process.returncode
    if returncode == 1: # Escape Key
        sys.exit(1)
    return returncode, stdout

def ask_password(message):
    return sh(f'rofi -password -p "{message}" -dmenu')

def ask_choice(choices):
    return sh(f'rofi -dmenu -p By_@chaignc -kb-custom-1 {Config.userpass_key}', stdin='\n'.join(choices))

def autotype(window, *, username=None, password=None):
    if username:
        sh(f"xdotool type --window {window} --file /dev/stdin", stdin=username, sleep=True)
        sh(f"xdotool key --window {window} Tab", sleep=True)
    sh(f"xdotool type --window {window} --file /dev/stdin", stdin=password, sleep=True)
    sh(f"xdotool key --window {window} Return", sleep=True)

def main(filename):
    _, window = sh("xdotool getactivewindow")
    try:
        kp = PyKeePass(filename, password=ask_password(f"{filename} Password")[1])
    except kp_exceptions.CredentialsIntegrityError as e:
        print(e)
        return
    choices = [ f"{e.title} {e.username} {e.url} {e.group}" for e in kp.entries ]
    returncode, choice = ask_choice(choices)
    entry = kp.entries[choices.index(choice)]
    print(returncode, entry.password, window)
    if returncode == 10:
        autotype(window, username=entry.username, password=entry.password)
    else:
        autotype(window, password=entry.password)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print(f"Usage: {sys.argv[0]} [Filename]\nAuthor: @chaignc")
