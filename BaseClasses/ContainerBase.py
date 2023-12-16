from abc import ABC, abstractmethod
from time import time
import docker
from docker import DockerClient
from docker.models.containers import Container
from docker.errors import NotFound

from Utils.Console import Console

class ContainerBase(ABC):
    def __init__(self, image: str, container_name:str, username: str):
        self.client: DockerClient = docker.from_env()
        self.container: Container = None
        self._image = image
        self._container_name = container_name
        self._username: str = username

    def run_setup(self):
        time_start = time.time()

        self.create_container()

        self.container.reload()

        Console.print_info("initializing container...")
        self._init_container()
        
        self._setup_user()

        elapsed_time = time.time() - time_start 
        Console.print_finished(f"elapsed time: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}s",)


    def create_container(self):
        try:
            self.container = self.client.containers.get(self._container_name)
            Console.print_info(f"\"{self._container_name}\" already exists!")
        except NotFound:
            Console.print_exec("creating container...")
            self.container: Container = self.client.containers.create(self._image, tty=True)
            self.container.rename(self._container_name)
    
    def start_container(self):
        if self.container.status == "created":
            self.container.start()
        elif self.container.status == "exited":
            self.container.restart()
        elif(self.container.status == "running"):
            Console.print_info(f"container already running!")

    def _exec_command(self, cmd: str, stdin=False, print_to_console=True):
        exec_result = self.container.exec_run(cmd=cmd, tty=True, stream=True, stdin=stdin)
        if(exec_result[0]):
            Console.print_exec(f"exited with exit_code: {exec_result[0]}")

        for line in exec_result[1]:
            line = line.replace(b'\r', b'')
            Console.print_output(line.decode('utf-8'))
            
        exec_result[1].close()
    
    def _print_status(self):
        Console.print_time()
        Console.print_info(f"Image: {self.container.image}")
        Console.print_info(f"Name: {self.container.name}")
        Console.print_info(f"Status: {self.container.status}")

    def __del__(self):
        self.container.stop()

    @abstractmethod
    def _init_container(self):
        raise NotImplementedError("_init_container() is not yet implemented!")
    
    @abstractmethod
    def _setup_user(self):
        raise NotImplementedError("_setup_user() is not yet implemented!")
        
