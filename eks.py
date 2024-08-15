from kubernetes import client, config

# Load Kubernetes configuration
config.load_kube_config()

# Create a Kubernetes API client
api_client = client.ApiClient()

# Define the deployment
deployment = client.V1Deployment(
    api_version="apps/v1",
    kind="Deployment",
    metadata=client.V1ObjectMeta(name="system-monitor-app"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "system-monitor-app"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "system-monitor-app"}
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="system-monitor-container",
                        # image="146855485831.dkr.ecr.us-east-1.amazonaws.com/system_monitor_app:latest", 
                        image="don361/system-monitor:latest",
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    )
)

# Create the deployment
api_instance = client.AppsV1Api(api_client)
api_instance.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

# Define the service
service = client.V1Service(
    api_version="v1",
    kind="Service",
    metadata=client.V1ObjectMeta(name="system-monitor-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "system-monitor-app"},
        ports=[client.V1ServicePort(port=5000)],
        type="LoadBalancer"
    )
)

# Create the service
api_instance = client.CoreV1Api(api_client)
api_instance.create_namespaced_service(
    namespace="default",
    body=service
)