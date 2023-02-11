import time
from pathlib import Path

from docker_builder.docker_cli import DockerCli

cwd = Path.cwd()

tags = {
    "flask-bigapp-python-3-7": "docker_tests/Dockerfile_Python_3_7",
    "flask-bigapp-python-3-8": "docker_tests/Dockerfile_Python_3_8",
    "flask-bigapp-python-3-9": "docker_tests/Dockerfile_Python_3_9",
    "flask-bigapp-python-3-10": "docker_tests/Dockerfile_Python_3_10",
    "flask-bigapp-python-3-11": "docker_tests/Dockerfile_Python_3_11",
    "flask-bigapp-python-3-12": "docker_tests/Dockerfile_Python_3_12",
}

enabled_tags = [
    "flask-bigapp-python-3-7",
    "flask-bigapp-python-3-8",
    "flask-bigapp-python-3-9",
    "flask-bigapp-python-3-10",
    "flask-bigapp-python-3-11",
    # "flask-bigapp-python-3-12",
]


def get_logs(tag):
    while True:
        with DockerCli(f"logs {tag}") as output:
            this_log = output

        time.sleep(1)
        if this_log != " ":
            print(this_log)
            break


if __name__ == "__main__":
    print("Building test environments, please wait...")
    # build
    for tag, file in tags.items():
        if tag in enabled_tags:
            with DockerCli(f"build -t {tag} -f {file} .") as output:
                _ = output

    for tag, file in tags.items():
        if tag in enabled_tags:
            with DockerCli(f"create --name {tag} {tag}") as output:
                _ = output

    for tag, file in tags.items():
        if tag in enabled_tags:
            with DockerCli(f"start {tag}") as output:
                _ = output

    print("Gathering logs, please wait...")
    # get logs
    for tag in tags:
        if tag in enabled_tags:
            get_logs(tag)

    cleanup_input = input("Do you want to cleanup? (y/N): ")

    if cleanup_input.lower() == "y":
        print("Cleaning up, please wait...")
        for tag in tags:
            if tag in enabled_tags:
                with DockerCli(f"rm {tag}") as output:
                    _ = output

        for tag in tags:
            if tag in enabled_tags:
                with DockerCli(f"rmi {tag}") as output:
                    _ = output

        with DockerCli(f"container prune -f") as output:
            _ = output
