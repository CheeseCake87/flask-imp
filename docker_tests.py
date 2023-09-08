import multiprocessing
import time
from pathlib import Path

from docker_builder.docker_cli import DockerCli

cwd = Path.cwd()

tags = {
    "flask-imp-python-3-8": "docker_tests/Dockerfile_Python_3_8",
    "flask-imp-python-3-9": "docker_tests/Dockerfile_Python_3_9",
    "flask-imp-python-3-10": "docker_tests/Dockerfile_Python_3_10",
    "flask-imp-python-3-11": "docker_tests/Dockerfile_Python_3_11",
    "flask-imp-python-3-12": "docker_tests/Dockerfile_Python_3_12",
}

enabled_tags = [
    "flask-imp-python-3-8",
    # "flask-imp-python-3-9",
    # "flask-imp-python-3-10",
    # "flask-imp-python-3-11",
    # "flask-imp-python-3-12",
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
            _ = output_


    def create_docker(tag_):
        with DockerCli(f"create --name {tag_} {tag_}") as output_:
            _ = output_


    def start_docker(tag_):
        with DockerCli(f"start {tag_}") as output_:
            _ = output_


    build_pool = multiprocessing.Pool()
    create_pool = multiprocessing.Pool()
    start_pool = multiprocessing.Pool()

    running_builds = []
    running_creates = []
    running_starts = []

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
            p_create = create_pool.apply_async(create_docker, args=(tag,))
            running_creates.append(p_create)

    for pro in running_creates:
        pro.wait()

    print("Running test environments, please wait...")

    for tag, file in tags.items():
        if tag in enabled_tags:
            p_starts = start_pool.apply_async(start_docker, args=(tag,))
            running_starts.append(p_starts)

    for pro in running_starts:
        pro.wait()

    print("Gathering logs, please wait...")
    for tag in tags:
        if tag in enabled_tags:
            get_logs(tag)

    cleanup_input = input("Do you want to cleanup? (Y/n): ")

    if cleanup_input.lower() != "n":
        print("Cleaning up, please wait...")
        for tag in tags:
            if tag in enabled_tags:
                with DockerCli(f"rm {tag}") as output:
                    _ = output

        for tag in tags:
            if tag in enabled_tags:
                with DockerCli(f"rmi {tag}") as output:
                    _ = output
