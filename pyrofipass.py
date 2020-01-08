#!/usr/bin/python3
# Author: @chaignc

from pykeepass import PyKeePass, exceptions as kp_exceptions
from subprocess import Popen, PIPE, check_output
import sys
import time

def notify(message):
    """ show a message to the user"""
    print(message)
    check_output(f'rofi -e "{message}"', shell=True)

# apt install rofi xdotool
# sudo pip3 install pykeepass
import sys
# i3 config: bindsym $mod+u exec "/home/cc/github/pyrofipass/pyrofipass.py /home/cc/perso/keepass/kali.kdbx"

class Config:
    """ config
    userpass_key: keybinding to type username and password
    """
    version = "0.1b"
    key_user_pass = "Alt+Return"
    key_pass_only = "Return"
    # rofi_conf = f'-matching fuzzy' # not good
    # -theme solarized 
    rofi_conf = f'-sort -mesg pyrofipass_By_@chaignc_v{version}'
    rofi_choice = f'{rofi_conf} -kb-accept-entry {key_pass_only} -kb-custom-1 {key_user_pass}'

def sh(cmd, stdin="", sleep=False):
    """ run a command, send stdin and capture stdout and exit status"""
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
    """ ask password using rofi """
    return sh(f'rofi -password -p "{message}" -dmenu')

def ask_choice(choices):
    """ multiple choice using rofi """
    return sh(f'rofi -dmenu -p URL {Config.rofi_choice}', stdin='\n'.join(choices))

def autotype(username, password, returncode):
    """ autotype username and password
    Parameters
    ----------
    returncode : str
        user typed key to decide if we autotype password only or username&password
    """
    if returncode == 10: # type username
        sh(f"xdotool type --file /dev/stdin", stdin=username, sleep=True)
        sh(f"xdotool key Tab", sleep=True)
    # type password
    sh(f"xdotool type --file /dev/stdin", stdin=password, sleep=True)
    sh(f"xdotool key Return", sleep=True)

def check_dependencies():
    pass

def main(filename):
    """ open filename keepass database and autotype password
    Parameters
    ----------
    filename : str
        Keepass database input
    """
    # save active window
    window = sh("xdotool getactivewindow")[1]
    # open keepass database
    kp = PyKeePass(filename, password=ask_password(f"{filename} Password")[1])
    # prepare rofi selection for user
    choices = [ f"{e.title} {e.url} {e.group}" for e in kp.entries ]
    # ask user to choose a password
    returncode, choice = ask_choice(choices)
    # retriver user choosed password
    entry = kp.entries[choices.index(choice)]
    # restore active window
    sh(f"xdotool windowactivate {window}")
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
