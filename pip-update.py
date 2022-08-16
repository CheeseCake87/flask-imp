import subprocess
import os
import sys
import logging

"""
Run this file at the same location you expect requirements.txt to be.

Also run this file while in your virtual environment, in linux this is:
source /venv/bin/activate

(venv) user: python3 pip-update.py
"""

logging.getLogger().setLevel(logging.INFO)


def pip_update():
    logging.info("=> Updating pip if needed...")
    subprocess.check_output([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])


def write_currently_installed():
    current_freeze = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    decode = current_freeze.decode("utf-8")
    with open("requirements.txt", mode="w") as current_req:
        current_req.write(decode.replace("==", ">="))
    logging.info("=> Current packages added to requirements.txt")


def do_update():
    logging.info("=> Doing update...")
    subprocess.check_output([sys.executable, '-m', 'pip', 'install', '--upgrade', '-r', 'requirements.txt'])
    write_currently_installed()


if __name__ == '__main__':
    pip_update()

    if not os.path.isfile("requirements.txt"):
        write_currently_installed()
        do_update()
        exit()

    do_update()
    exit()
