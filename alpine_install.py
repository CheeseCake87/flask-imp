from os import path
from os import name as system_name
from os import system
from os import mkdir
import re
import subprocess

#
# Functions
#

print_commands = False


def print_action(title):
    print(no_tab(f">>> {title}"))


def print_prompt(prompt):
    print(no_tab(f"!!! {prompt} !!!"))


def cls():
    system('cls' if system_name == 'nt' else 'clear')


def no_tab(_string):
    r_string = re.sub(r'(^[ \t]+|[ \t]+(?=:))', '', _string, flags=re.M)
    rr_string = r_string.replace("^^^", "").replace("^^", "\t")
    return rr_string


def terminal_do(commands):
    terminal = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = terminal.communicate()
    if out:
        if print_commands:
            print(out.decode("utf-8"))
    if err:
        if print_commands:
            print(err.decode("utf-8"))


def terminal_do_list(commands) -> list:
    terminal = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = terminal.communicate()
    return [out, err]


def show_ip_addresses():
    for value in terminal_do_list(['ip', 'address']):
        if value is not None:
            decode = value.decode("utf-8")
            find_inet = [m.start() for m in re.finditer("inet ", decode)]
            for ivalue in find_inet:
                i = ivalue + 25
                snip = decode[ivalue:i]
                split1 = snip.split("/")
                split2 = split1[1].split(" ")
                print(f"{split1[0]}/{split2[0]}")


def get_app_root() -> str:
    """
    Finds the root folder of the app.
    :return str: /app/folder/extend
    """
    strip = path.dirname(path.realpath(__file__)).split("/")[1:]
    return "/" + "/".join(strip) + "/flask_launchpad"


def get_user() -> str:
    split_path = path.dirname(path.realpath(__file__)).split("/")
    if split_path[1] == "home":
        return split_path[2]
    return "root"


#
# Actions
#

def update_system():
    print_action("Updating system")
    terminal_do(['apk', 'update', '&&', 'apk', 'upgrade'])


def update_ip_hostname():
    print_action("Getting IP addresses")
    show_ip_addresses()
    print_prompt("Update IP & Hostname")
    ip_address = input("Enter static IP address (e.g. 192.168.1.x): ")
    netmask_address = input("Enter netmask (e.g. 255.255.255.0): ")
    gateway_address = input("Enter gateway IP address (e.g. 192.168.1.1): ")
    server_hostname = input("Enter hostname (name of app/website/server): ")

    terminal_do(['setup-hostname', server_hostname])

    with open(file="/etc/network/interfaces", mode="w") as network:
        write = no_tab(
            f"""^^^
            iface lo inet loopback

            auto eth0
            iface eth0 inet static
            ^^address {ip_address}
            ^^netmask {netmask_address}
            ^^gateway {gateway_address}
            ^^^"""
        )
        network.write(write)


def install_c():
    print_action("Installing C library & compiler...")
    terminal_do(['apk', 'add', 'musl-dev'])
    terminal_do(['apk', 'add', 'g++'])


def setup_venv():
    print_action("Setting up venv environment...")
    terminal_do(['python3', '-m', 'venv', f'{get_app_root()}/venv'])


def pip_install():
    print_action("Installing app requirements...")
    with open(file=f"{get_app_root()}/pip_install.sh", mode="w") as pip:
        write = no_tab(
            f"""^^^
            source {get_app_root()}/venv/bin/activate &&
            pip install --upgrade pip &&
            pip install wheel &&
            pip install Flask &&
            pip install gunicorn
            pip install -r {get_app_root()}/requirements.txt
            ^^^"""
        )
        pip.write(write)
    terminal_do(['ash', f'{get_app_root()}/pip_install.sh'])


def install_supervisor():
    print_action("Installing supervisor...")
    terminal_do(['apk', 'add', 'supervisor'])


def setup_supervisor():
    print_action("Setting up supervisor...")
    if not path.exists("/etc/supervisor.d"):
        mkdir("/etc/supervisor.d")
    with open(file="/etc/supervisor.d/flask_launchpad.ini", mode="w") as supervisord_conf:
        write = no_tab(
            f"""^^^
            [program:flask_launchpad]
            directory={get_app_root()}
            command={get_app_root()}/venv/bin/gunicorn -b 0.0.0.0:5000 -w 3 run:flask_launchpad
            user={get_user()}
            autostart=true
            autorestart=true
            stopasgroup=true
            killasgroup=true
            stdout_logfile={get_app_root()}/supervisor.out.log
            stderr_logfile={get_app_root()}/supervisor.err.log
            ^^^"""
        )
        supervisord_conf.write(write)

    terminal_do(['rc-update', 'add', 'supervisord', 'boot'])


update_system()
update_ip_hostname()
install_c()
setup_venv()
pip_install()
install_supervisor()
setup_supervisor()
