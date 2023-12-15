from datetime import datetime
import time
import docker
from docker import DockerClient
from docker.models.containers import Container
from docker.errors import *
from docker.types.daemon import CancellableStream

from Utils.Console import Console

# creates a container named "debian"
# configured is a user called admin (passwd: admin)
# sudoers enabled
# git installed
# 

class DebianContainer:
    def __init__(self, container_name: str, username: str):
        self._container_name:str = container_name
        self._username:str = username
        self._image:str = "debian:latest"
        self.container: Container = None

    def run_setup(self):
        time_start = time.time()

        self._create_container()
        
        self.container.reload()

        Console.print_exec(f"updating, upgrading and installing sudo...")
        self._init_container()

        self._setup_user()

        elapsed_time = time.time() - time_start 
        Console.print_finished(f"elapsed time: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}s",)

    def _create_container(self):
        client: DockerClient = docker.from_env()
        try:
            self.container = client.containers.get(self._container_name)
            Console.print_warning(f"\"{self._container_name}\" already exists!")
            if(self.container.status == "running"):
                Console.print_warning(f"container already running!")
            else:
                Console.print_exec(f"starting already existing container...")
                self.container.restart()
        except NotFound:
            Console.print_exec("creating container...")
            self.container: Container = client.containers.create("debian:latest", tty=True)
            self.container.rename(self._container_name)
            self.container.start()

    def _start_container(self):
        Console.print_exec(f"starting {self._container_name}...")
        self.container.start()

    def _exec_command(self, cmd: str, stdin=False, print_to_console=True):
        exec_result = self.container.exec_run(cmd=cmd, tty=True, stream=True, stdin=stdin)
        if(exec_result[0]):
            Console.print_exec(f"exited with exit_code: {exec_result[0]}")

        for line in exec_result[1]:
            line = line.replace(b'\r', b'')
            Console.print_output(line.decode('utf-8'))
            
        exec_result[1].close()

    def _print_status(self, container: Container):
        Console.print_time()
        Console.print_info(f"Image: {container.image}")
        Console.print_info(f"Name: {container.name}")
        Console.print_info(f"Status: {container.status}")

    def _init_container(self):
        self._exec_command("apt update")
        self._exec_command("apt upgrade --yes")
        self._exec_command("apt-get -y install sudo locales")

    def _setup_user(self):
        self._exec_command(f"useradd -m {self._username}")
        self._exec_command(f"echo \"{self._username} ALL=NOPASSWD:ALL\" > /etc/sudoers.d/{self._username}", print_to_console=False)
        # TODO find a way to set password

    def __del__(self):
        self.container.stop()

