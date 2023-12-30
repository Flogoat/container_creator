from datetime import datetime
import time
import docker
from docker import DockerClient
from docker.models.containers import Container
from docker.errors import *
from docker.types.daemon import CancellableStream
from BaseClasses.ContainerBase import ContainerBase

# creates a container
# configures a user
# sudoers enabled
# git installed
# 

class DebianContainer(ContainerBase):
    def __init__(self, container_name: str, username: str):
        self._image:str = "debian:latest"
        super().__init__(self._image, container_name, username)

    def _init_container(self):
        self._exec_command("apt update")
        self._exec_command("apt upgrade --yes")
        self._exec_command("apt-get -y install sudo locales")

    def _setup_user(self):
        self._exec_command(f"useradd -m {self._username}")
        self._exec_command(f"echo \"{self._username} ALL=NOPASSWD:ALL\" > /etc/sudoers.d/{self._username}", print_to_console=False)
        # TODO find a way to set password
