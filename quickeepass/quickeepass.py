#!/usr/bin/python3
# Author: @chaignc

from pykeepass import PyKeePass, exceptions as kp_exceptions
from subprocess import Popen, PIPE, check_output
from pathlib import Path
import pickle
import argparse
import sys
import time
import os

def notify(message, do_print=True):
    """ show a message to the user"""
    if do_print:
        print(message)
    check_output(f'rofi -e "{message}"', shell=True)

def notify_error(message, do_print=True):
    """ show a ERROR message to the user"""
    notify(f"QuicKeepass ERROR: {message}\nAuthor: @chaignc", do_print=do_print)

class Config:
    """ config, Keybindings and advanced config
    """
    version = "1.0"
    key_user_pass = "Return"
    key_pass_only = "Alt+Return"
    rofi_conf = f'-sort -mesg QuicKeepass_By_@chaignc_v{version}'
    rofi_choice = f'{rofi_conf} -i -kb-accept-entry {key_pass_only} -kb-custom-1 {key_user_pass}'
    rofi_ask_password = f'{rofi_conf}'
    # args sent by the user from cmdline
    rofi_userargs = f''

def sh(cmd, stdin="", sleep=False):
    """ run a command, send stdin and capture stdout and exit status"""
    if sleep:
        time.sleep(0.5)
    # process = Popen(cmd.split(), stdin=PIPE, stdout=PIPE)
    process = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)
    process.stdin.write(bytes(stdin, "utf-8"))
    stdout = process.communicate()[0].decode('utf-8').strip()
    process.stdin.close()
    returncode = process.returncode
    return returncode, stdout

def rofi(cmd, stdin="", sleep=False):
    returncode, stdout = sh(cmd, stdin, sleep)
    if returncode == 1: # Escape Key
        sys.exit(1)
    return returncode, stdout
    
def ask_password(message):
    """ ask password using rofi """
    return rofi(f'rofi -password -p "{message}" -dmenu {Config.rofi_ask_password} {Config.rofi_userargs}')

def ask_choice(choices, default_filter):
    """ multiple choice using rofi """
    return rofi(f'rofi -dmenu -p URL {Config.rofi_choice} {Config.rofi_userargs} -filter {default_filter}', stdin='\n'.join(choices))

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

def do_check_dependencies(tool, install_instruction):
    returncode, _ = sh(f"which {tool}")
    if returncode:
        print(f"{tool} not found please => {install_instruction}")
        sys.exit(1)

def check_dependencies():
    do_check_dependencies("rofi", "apt install rofi")
    do_check_dependencies("xdotool", "apt install xdotool")

def opendatabase(database, password, keyfile):
    keepassargs = dict()
    if password:
        keepassargs["password"] = ask_password(f"Enter {os.path.basename(database)} Password")[1]
    if keyfile:
        keepassargs["keyfile"] = keyfile
    kp = PyKeePass(database, **keepassargs)
    return kp

class Cache:
    """ help to type password faster with cache
    doesn't cache password only cache keepass password uuid
    """
    def __init__(self):
        self.cache_path = Path(f"{Path.home()}/.config/quickeepass/cache")
        self.dict = {}
        self.load()

    def load(self):
        if self.cache_path.is_file() and os.path.getsize(self.cache_path) > 0:
            with open(self.cache_path, "rb") as F:
                self.dict = pickle.load(F)

    def save(self):
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        with open(self.cache_path, "wb") as F:
            pickle.dump(self.dict, F)

    def get(self, key, default):
        return self.dict.get(key, default)
    
    def set(self, key, value):
        self.dict[key] = value

    def remember(self, windowname, uuid_choice):
        # if windowname in self.dict and self.dict[windowname] != uuid_choice:
        #     # We got wrong once, never predict again for this window
        #     self.set(windowname, "")
        # else:
        # Always remember the last choice
        self.set(windowname, uuid_choice)
        self.save()

def quickeeepass(args):
    """ open filename keepass database and autotype password
    Parameters
    ----------
    filename : str
        Keepass database input
    """
    # save active window
    _, window = sh("xdotool getactivewindow")
    _, windowname = sh("xdotool getactivewindow getwindowname")
    # open keepass database
    kp = opendatabase(args.database, args.password, args.keyfile)
    # prepare rofi selection for user
    choices = [ f"{e.title} {e.url} {e.group}\t\t{e.uuid}" for e in kp.entries ]
    # cache used to remember uuid history choice
    cache = Cache()
    # ask user to choose a password
    # print(f'predicted {cache.get(windowname, "")} for {windowname}')
    predicted = cache.get(windowname, '')
    if predicted:
        entry = kp.find_entries(uuid=predicted, first=True)
        if entry is None:
            predicted = ''
        else:
            predicted = entry.title
    returncode, choice = ask_choice(choices, default_filter=predicted)
    # retriver user choosed password
    entry = kp.entries[choices.index(choice)]
    # remember uuid choice for next time
    cache.remember(windowname, entry.uuid)

    # restore active window
    sh(f"xdotool windowactivate {window}")
    autotype(entry.username, entry.password, returncode)

class ArgumentParser(argparse.ArgumentParser):    

    def error(self, message):
        notify_error(message, do_print=False)
        super(ArgumentParser, self).error(message)

    @staticmethod
    def parse_sys_argv():
        parser = ArgumentParser(prog='QuicKeepass', description='QuicKeepass')
        parser.add_argument('database', type=argparse.FileType('r'), help='keepass database')
        parser.add_argument('--password', dest='password', default=False, action='store_true')
        parser.add_argument('--keyfile', type=argparse.FileType('r'), dest='keyfile')
        parser.add_argument('--rofiargs', type=str, default="", help='aditional parameters for rofi')

        args = parser.parse_args()

        args.database = args.database.name
        Config.rofi_userargs = args.rofiargs

        if args.keyfile is None:
            args.password = True
        else:
            args.keyfile = args.keyfile.name
        return args

def main():
    check_dependencies()
    args = ArgumentParser.parse_sys_argv()
    try:
        quickeeepass(args)
    except Exception as e:
        notify_error(e)
        raise e

if __name__ == "__main__":
    main()
