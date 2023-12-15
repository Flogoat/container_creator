from DockerInstaller import DockerInstaller
from DebianContainer import DebianContainer

if __name__ == "__main__":
    # DockerInstaller.check_operating_system()
    container_client = DebianContainer("debian", "admin")
    container_client.run_setup()
    # TODO create script to connect to user (preferable in extra console) 
    container_client.__del__()
