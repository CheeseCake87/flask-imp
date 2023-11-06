import multiprocessing
import subprocess
import time
from pathlib import Path
from typing import Optional


class DockerCli:

    def __init__(self, command: str, cwd_: Optional[Path] = None):
        self.command = command.split(" ")
        self.cwd = cwd_ or Path.cwd()

    def __enter__(self) -> str:
        self.process = subprocess.Popen(
            ["docker", *self.command],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.cwd,
        )

        self.process.stdin.close()

        return f"{self.process.stdout.read().decode()} {self.process.stderr.read().decode()}"

    def __exit__(self, exc_type, exc_value, traceback):
        self.process.terminate()


cwd = Path.cwd()

tags = {
    "flask-imp-python-3-8:latest": "test_docker/Dockerfile_Python_3_8",
    "flask-imp-python-3-9:latest": "test_docker/Dockerfile_Python_3_9",
    "flask-imp-python-3-10:latest": "test_docker/Dockerfile_Python_3_10",
    "flask-imp-python-3-11:latest": "test_docker/Dockerfile_Python_3_11",
    "flask-imp-python-3-12:latest": "test_docker/Dockerfile_Python_3_12",
    "flask-imp-python-3-13:latest": "test_docker/Dockerfile_Python_3_13",
}

enabled_tags = [
    "flask-imp-python-3-8:latest",
    "flask-imp-python-3-9:latest",
    "flask-imp-python-3-10:latest",
    "flask-imp-python-3-11:latest",
    "flask-imp-python-3-12:latest",
    "flask-imp-python-3-13:latest",
]

if __name__ == "__main__":

    def get_logs(tag_):
        while True:
            with DockerCli(f"logs {tag_}") as output_:
                this_log = output_

            time.sleep(1)
            if this_log != " ":
                print(this_log)
                break


    def build_docker(tag_, file_):
        with DockerCli(f"build -t {tag_} -f {file_} .") as output_:
            print(f"build -t {tag_} -f {file_} .")
            _ = output_


    def create_docker(tag_):
        with DockerCli(f"create --name {tag_.replace(':latest', '')} {tag_}") as output_:
            print(f"create --name {tag_.replace(':latest', '')} {tag_}")
            _ = output_


    def start_docker(tag_):
        with DockerCli(f"start {tag_}") as output_:
            print(f"start {tag_}")
            _ = output_


    build_pool = multiprocessing.Pool()

    running_builds = []

    print("Building test environments, please wait...")

    for tag, file in tags.items():
        if tag in enabled_tags:
            p_build = build_pool.apply_async(build_docker, args=(tag, file))
            running_builds.append(p_build)

    for pro in running_builds:
        pro.wait()

    print("Creating test environments, please wait...")

    for tag, file in tags.items():
        if tag in enabled_tags:
            create_docker(tag.replace(':latest', ''))

    print("Running test environments, please wait...")

    for tag, file in tags.items():
        if tag in enabled_tags:
            start_docker(tag.replace(':latest', ''))

    print("Gathering logs, please wait...")
    for tag in tags:
        if tag in enabled_tags:
            get_logs(tag.replace(':latest', ''))

    cleanup_input = input("Do you want to cleanup? (Y/n): ")

    if cleanup_input.lower() != "n":
        print("Cleaning up, please wait...")
        for tag in tags:
            if tag in enabled_tags:
                with DockerCli(f"rm {tag.replace(':latest', '')}") as output:
                    _ = output

        for tag in tags:
            if tag in enabled_tags:
                with DockerCli(f"rmi {tag}") as output:
                    _ = output
