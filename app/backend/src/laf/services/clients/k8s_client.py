import logging
from typing import Dict, List, Optional
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

logger = logging.getLogger(__name__)


class KubernetesClient:
    def __init__(self):
        try:
            config.load_kube_config()
        except Exception:
            try:
                config.load_incluster_config()
            except Exception as e:
                logger.error(f"Failed to load Kubernetes config: {e}")
                raise

        self.batch_v1 = client.BatchV1Api()

    def launch_job(
        self,
        job_name: str,
        image: str,
        command: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None,
        namespace: str = "default",
    ) -> str:
        """
        Launch a Kubernetes Job.

        Returns:
            str: Job name if successful
        """
        try:
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

            self.batch_v1.create_namespaced_job(namespace=namespace, body=job)
            logger.info(
                f"Kubernetes job '{job_name}' launched in namespace '{namespace}'"
            )
            return job_name

        except ApiException as e:
            logger.error(f"Failed to launch Kubernetes job: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error launching Kubernetes job: {e}")
            raise
