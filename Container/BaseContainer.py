
from abc import ABC, abstractclassmethod
import time
import docker
from docker import DockerClient
from docker.models.containers import Container
from docker.errors import NotFound

from Utils.Console import Console

class BaseContainer:

    def __init__(self, container_name: str, username: str):
        self._container_name:str = container_name
        self._username:str = username
        self._image:str = None
        self.container: Container = None

    def run_setup(self):
        time_start = time.time()

        self._create_container()
        
        self.container.reload()

        self._init_container()

        self._setup_user()

        elapsed_time = time.time() - time_start 
        Console.print_finished(f"elapsed time: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}s",)

    def _create_container(self, tty=True):
        client: DockerClient = docker.from_env()
        try:
            self.container = client.containers.get(self._container_name)
            Console.print_warning(f"\"{self._container_name}\" already exists!")
        except Exception as ex:
            Console.print_exec("creating container...")
            try:
                self.container: Container = client.containers.create(self._image, tty)
                self.container.rename(self._container_name)
            except Exception as ex:
                print(ex)
        
        if not (self.container.status == "running"):
            self._start_container

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

    @abstractclassmethod
    def _init_container(self):
        raise NotImplementedError("_init_container() is not implemented!")

    @abstractclassmethod
    def _setup_user(self):
        raise NotImplementedError("_setup_user() is not implemented!")

    def __del__(self):
        if self.container:
            self.container.stop()