import logging
import docker

logger = logging.getLogger(__name__)


def launch_container(image, command=None, env=None, detach=True):
    """
    Launch a Docker container.

    Args:
        image (str): Docker image to use.
        command (str or list, optional): Command to run in the container.
        env (dict, optional): Environment variables for the container.
        detach (bool): Run container in detached mode.

    Returns:
        str: Container ID.
    """
    try:
        client = docker.from_env()
        container = client.containers.run(
            image, command, environment=env, detach=detach
        )
        logger.info(f"Docker container '{container.id}' launched from image '{image}'.")
        return container.id
    except Exception as e:
        logger.error(f"Failed to launch Docker container: {e}")
        raise
