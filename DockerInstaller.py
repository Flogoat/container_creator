import subprocess
import platform

import urllib.request

from Utils.Console import Console

class DockerInstaller:
    @staticmethod
    def check_operating_system():
        system = platform.system()

        if system == "Windows":
            print("You are using Windows.")
            DockerInstaller._install_docker_windows()
        elif system == "Linux":
            print("You are using Linux.")
            DockerInstaller._install_docker_linux()
        elif system == "Darwin":
            print("You are using macOS.")
            print("installing docker is not yet available for macOS...")
        else:
            print("The operating system is not recognized or supported.")

    @staticmethod
    def _install_docker_linux() -> bool:
        try:
            # Run the command to install Docker
            subprocess.run(['sudo', 'apt-get', 'update', '-y'])
            subprocess.run(['sudo', 'apt-get', 'install', 'docker-ce', 'docker-ce-cli', 'containerd.io', '-y'])

            print("Docker installation successful!")
        except Exception as e:
            print(f"Error installing Docker: {e}")

    @staticmethod
    def _is_docker_installed():
        try:
            # Attempt to run a Docker command
            subprocess.run(['docker', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def _run_command(command) -> bool:
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {e}")

    @staticmethod
    def _install_docker_windows():
        if DockerInstaller._is_docker_installed():
            Console.print_info("Docker is already installed.")
            return

        download_url = 'https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe'
        installer_filename = "DockerDesktopInstaller.exe"
        
        # Download Docker Desktop installer
        
        urllib.request.urlretrieve(download_url, installer_filename)

        # Install Docker Desktop
        DockerInstaller._run_command([installer_filename])

        print("Docker installation on Windows completed successfully.")

if __name__ == "__main__":
    DockerInstaller._install_docker_windows()