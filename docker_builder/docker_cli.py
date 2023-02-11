import subprocess
from pathlib import Path
from typing import Optional


class DockerCli:

    def __init__(self, command: str, cwd: Optional[Path] = None):
        self.command = command.split(" ")
        self.cwd = cwd or Path.cwd()

    def __enter__(self) -> str:
        self.process = subprocess.Popen(
            ["docker", *self.command],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.cwd,
        )

        self.process.stdin.close()

        return self.process.stdout.read().decode()

    def __exit__(self, exc_type, exc_value, traceback):
        self.process.terminate()
