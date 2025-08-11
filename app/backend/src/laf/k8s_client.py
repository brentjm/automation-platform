import logging
from kubernetes import client, config

logger = logging.getLogger(__name__)


def launch_job(job_name, image, command=None, env=None, namespace="default"):
    """
    Launch a Kubernetes Job.

    Args:
        job_name (str): Name of the job.
        image (str): Docker image to use.
        command (list, optional): Command to run in the container.
        env (dict, optional): Environment variables for the container.
        namespace (str): Kubernetes namespace.

    Returns:
        V1Job: The created Kubernetes Job object.
    """
    try:
        config.load_kube_config()
        batch_v1 = client.BatchV1Api()
        job = client.V1Job(
            metadata=client.V1ObjectMeta(name=job_name),
            spec=client.V1JobSpec(
                template=client.V1PodTemplateSpec(
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name=job_name,
                                image=image,
                                command=command,
                                env=[
                                    client.V1EnvVar(name=k, value=v)
                                    for k, v in (env or {}).items()
                                ],
                            )
                        ],
                        restart_policy="Never",
                    )
                )
            ),
        )
        api_response = batch_v1.create_namespaced_job(namespace=namespace, body=job)
        logger.info(f"Kubernetes job '{job_name}' launched in namespace '{namespace}'.")
        return api_response
    except Exception as e:
        logger.error(f"Failed to launch Kubernetes job: {e}")
        raise
