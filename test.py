import docker
from docker.client import DockerClient

client: DockerClient = docker.from_env()
client.containers.create("debian:latest")
