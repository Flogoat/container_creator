from datetime import datetime
from Container.BaseContainer import BaseContainer

from Utils.Console import Console

# creates a container named "debian"
# configured is a user called admin (passwd: admin)
# sudoers enabled
# git installed
# 

class DebianContainer(BaseContainer):
    def __init__(self, container_name: str, username: str):
        super().__init__(container_name, username)
        self._image:str = "debian"

    def _init_container(self):
        Console.print_exec(f"updating, upgrading and installing sudo...")
        self._exec_command("apt update")
        self._exec_command("apt upgrade --yes")
        self._exec_command("apt-get -y install sudo locales")

    def _setup_user(self):
        self._exec_command(f"useradd -m {self._username}")
        self._exec_command(f"echo \"{self._username} ALL=NOPASSWD:ALL\" > /etc/sudoers.d/{self._username}", print_to_console=False)
        # TODO find a way to set password

