from abc import ABC, abstractmethod
import platform
import subprocess
import time
import docker
from docker import DockerClient
from docker.models.containers import Container
from docker.errors import NotFound

from Utils.Console import Console

class ContainerBase(ABC):
    def __init__(self, image: str, container_name:str, username: str):
        self.client: DockerClient = docker.from_env()
        self.container: Container = None
        self.__system: str = platform.system().lower()
        self._image = image
        self._container_name = container_name
        self._username: str = username
        self.__wait_for_docker_service()

    def __wait_for_docker_service(self):
        counter: int = 0
        while not self.__is_docker_services_running():
            print(f"[WAIT] waiting for docker_services to start: {counter}", flush=True, end="")
            time.sleep(1)
            counter += 1

    def __is_docker_services_running(self):
        try:
            # Use subprocess to run the appropriate Docker command to check if services are running
            if self.__system is ("linux" or "darwin"):
                result = subprocess.run(["docker", "info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            elif self.__system == "windows":
                result = subprocess.run(["docker", "info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell=True)
            else:
                print(f"Unsupported operating system: {self.__system}")
                return False

            # Check if the output contains information indicating that Docker is running
            return "Server Version" in result.stdout.decode()

        except subprocess.CalledProcessError as e:
            # Handle the case where the Docker command fails (e.g., Docker not installed)
            print(f"Error checking Docker services: {e}")
            return False


    def _start_docker_service(self):
        try:
            # Use subprocess to run the appropriate Docker command to start services
            if self.__system is ("linux" or "darwin") and not self.__is_docker_services_running():
                subprocess.run(["docker-compose", "up", "-d"], check=True)
            elif self.__system == "windows" and not self.__is_docker_services_running():
                subprocess.run(["docker-compose.exe", "up", "-d"], check=True)
            else:
                print(f"Unsupported operating system: {self.__system}")
                return

            print("Docker services started successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error starting Docker services: {e}")


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
            self.container = self.client.containers.create(self._image, tty=True)
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
        
