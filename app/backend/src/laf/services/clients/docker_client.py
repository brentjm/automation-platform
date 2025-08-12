import logging
from typing import Dict, List, Optional, Union
import docker
from docker.errors import DockerException

logger = logging.getLogger(__name__)


class DockerClient:
    def __init__(self):
        try:
            self.client = docker.from_env()
        except DockerException as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            raise

    def launch_container(
        self,
        image: str,
        command: Optional[Union[str, List[str]]] = None,
        env: Optional[Dict[str, str]] = None,
        detach: bool = True,
    ) -> str:
        """
        Launch a Docker container.

        Returns:
            str: Container ID if successful
        """
        try:
            container = self.client.containers.run(
                image, command, environment=env, detach=detach
            )
            logger.info(
                f"Docker container '{container.id}' launched from image '{image}'"
            )
            return container.id

        except DockerException as e:
            logger.error(f"Failed to launch Docker container: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error launching Docker container: {e}")
            raise
