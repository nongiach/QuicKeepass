#!/usr/bin/python3
# Author: @chaignc

from pykeepass import PyKeePass, exceptions as kp_exceptions
from subprocess import Popen, PIPE
from gi.repository import Notify
import sys
import time

Notify.init("pyrofipass")
def notify(message):
    message = str(message)
    print(message)
    Notify.Notification.new(message).show()

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

def autotype(username, password, returncode):
    if returncode == 10: # type password
        sh(f"xdotool type --file /dev/stdin", stdin=username, sleep=True)
        sh(f"xdotool key Tab", sleep=True)
    sh(f"xdotool type --file /dev/stdin", stdin=password, sleep=True)
    sh(f"xdotool key Return", sleep=True)

def check_dependencies():
    pass

def main(filename):
    # save mouse position and focused windows
    x, y, screen, window = [ v.split(':')[1] for v in sh("xdotool getmouselocation")[1].split() ]
    kp = PyKeePass(filename, password=ask_password(f"{filename} Password")[1])
    choices = [ f"{e.title} {e.url} {e.group}" for e in kp.entries ]
    returncode, choice = ask_choice(choices)
    entry = kp.entries[choices.index(choice)]
    # restore mouse position
    sh(f"xdotool mousemove {x} {y}")
    autotype(entry.username, entry.password, returncode)

if __name__ == "__main__":
    check_dependencies()
    if len(sys.argv) == 2:
        try:
            main(sys.argv[1])
        except kp_exceptions.CredentialsIntegrityError as e:
            notify(e)
        except Exception as e:
            notify(e)
    else:
        notify(f"Usage: {sys.argv[0]} [Filename]\nAuthor: @chaignc")
