from subprocess import Popen, PIPE
from pathlib import Path
import sys
from functools import wraps
from typing import List

WINDOWS_PLATFORM = 'win32'
LINUX_PLATFORM = 'linux'
ENV_NAME = Path('venv')
WINDOWS_ACTIVATION = Path(ENV_NAME, 'Scripts', 'activate.bat')
LINUX_ACTIVATION = Path(ENV_NAME, 'bin', 'activate')
PIP = Path(ENV_NAME, 'Scripts', 'pip.exe') if sys.platform == WINDOWS_PLATFORM else Path(
    ENV_NAME, 'bin', 'pip')
PYTHON_EXE = Path(ENV_NAME, 'Scripts', 'python.exe') if sys.platform == WINDOWS_PLATFORM else Path(
    ENV_NAME, 'bin', 'python')


def print_arg(text: str):
    @wraps(print_arg)
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            print(text)
            return func(*args, **kwargs)
        return inner
    return wrapper


def run_cmd(cmd: List[str]):
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        print(line.decode('utf-8').strip())
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(
            f"Command {' '.join(cmd)} failed with code {proc.returncode}")


@print_arg("Activating virtualenv")
def activate_virtualenv():
    """Activate the virtual environment."""
    if sys.platform == 'win32':
        run_cmd([WINDOWS_ACTIVATION])
    else:
        run_cmd(['source', LINUX_ACTIVATION])


@print_arg("Installing dependencies")
def install_requirements():
    """Install the requirements."""
    run_cmd([PIP, 'install', '-r', 'requirements.txt'])


@print_arg("Creating virtualenv")
def create_virtualenv():
    """Create a virtual environment."""
    run_cmd(['python', '-m', 'venv', ENV_NAME])
    activate_virtualenv()
    install_requirements()


@print_arg("Building website")
def freeze():
    """Freeze the website."""
    run_cmd([PYTHON_EXE, 'src/run.py', 'build'])


@print_arg("Running server")
def run_server():
    """Run the server."""
    run_cmd([PYTHON_EXE, 'src/run.py'])


def main():
    if not ENV_NAME.exists():
        create_virtualenv()
    else:
        activate_virtualenv()
    run_server()


if __name__ == '__main__':
    main()
