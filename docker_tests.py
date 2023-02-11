from pathlib import Path

from docker_builder.docker_cli import DockerCli

cwd = Path.cwd()


def build_run(tag, file):
    with DockerCli(f"build -t {tag} -f {file} .") as output:
        print(output)

    with DockerCli(f"create --name {tag} {tag}") as output:
        print(output)

    with DockerCli(f"run {tag} -d") as output:
        print(output)

    with DockerCli(f"start {tag}") as output:
        print(output)


if __name__ == "__main__":
    build_run("flask-bigapp-python-3-7", "docker_tests/Dockerfile_Python_3_7")
    build_run("flask-bigapp-python-3-8", "docker_tests/Dockerfile_Python_3_8")
    build_run("flask-bigapp-python-3-9", "docker_tests/Dockerfile_Python_3_9")
    build_run("flask-bigapp-python-3-10", "docker_tests/Dockerfile_Python_3_10")
    build_run("flask-bigapp-python-3-11", "docker_tests/Dockerfile_Python_3_11")
    build_run("flask-bigapp-python-3-12", "docker_tests/Dockerfile_Python_3_12")
