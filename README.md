# **System Monitoring Python App on Minikube/K8s!**

## Things you will Learn 🤯

1. Python and How to create Monitoring Application in Python using Flask and psutil
2. How to run a Python App locally.
3. Learn Docker and How to containerize a Python application
    1. Creating Dockerfile
    2. Building DockerImage
    3. Running Docker Container
    4. Docker Commands
4. Create Minikube cluster and deploy application locally
5. Create ECR repository using Python Boto3 and pushing Docker Image to ECR
6. Create EKS cluster and Nodegroup
7. Create Kubernetes Deployments and Services using Python!

## **Prerequisites** !

(Things to have before starting the projects)

- [x]  AWS Account.
- [x]  Programmatic access and AWS configured with CLI.
- [x]  Python3 installed.
- [x]  Docker installed.
- [x]  Minikube and Kubectl installed.
- [x]  Code editor (VScode)

# ✨Let’s Start the Project ✨

## **Part 1: Deploying the Flask application locally**

### **Step 1: Clone the code**

Clone the code from the repository:

```
$ git clone https://github.com/Roni-Boiz/system-monitor-app.git
```

### **Step 2: Create and activate virtual environment**

Setup the python environment to development:

```
$ python3 -m venv venv

$ source venv/bin/activate
```

> [!WARNING]
> If you face any erros execute `$ pip install virtualenv` then delete previously created virtual environment `$ sudo rm -rf venv` and try again


### **Step 3: Install dependencies**

The application uses the **`psutil`** and **`Flask`, `Plotly`, `boto3`** libraries. Install them using pip:

```
$ pip install -r requirements.txt
```

### **Step 4: Run the application**

To run the application, navigate to the root directory of the project and execute the following command:

```
$ python3 app.py
```

This will start the Flask server on **`localhost:5000`**. Navigate to [http://localhost:5000/](http://localhost:5000/) on your browser to access the application.

![app-local](https://github.com/user-attachments/assets/52b846ec-352d-48e9-a35a-b06ad5593bf6)

## **Part 2: Dockerizing the Flask application**

### **Step 1: Create a Dockerfile**

Create a **`Dockerfile`** in the root directory of the project with the following contents:

```
# Use the official Python image as the base image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Set the environment variables for the Flask app
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port on which the Flask app will run
EXPOSE 5000

# Start the Flask app when the container is run
CMD ["flask", "run"]
```

### **Step 2: Build the Docker image**

To build the Docker image, execute the following command:

```
$ docker build -t <dockerhub-username>/system-monitor-app:latest .
```

### **Step 3: Run the Docker container**

To run the Docker container, execute the following command:

```
$ docker run -p 5000:5000 <dockerhub-username>/system-monitor-app:latest
```

This will start the Flask server in a Docker container on **`localhost:5000`**. Navigate to [http://localhost:5000/](http://localhost:5000/) on your browser to access the application.

### **Step 4: Push the docker image to Docker Hub**

To push the image to docker hub, execute the following command:

```
$ docker push <dockerhub-username>/system-monitor-app:latest
```

## **Part 3: Deploy application in local Minikube cluster**

### **Step 1: Start Minikube**

To start local kubernetes cluster in Minikube, execute the following command::

```
$ minikube start
```

### **Step 2: Deploy application in Minikube**

To Deploy the application in kubernetes, execute the following command:

```
$ python3 eks.py
```

> [!WARNING]
> Make sure to edit the name of the image on line 28 with your image Uri in `eks.py`

### **Step 3: Start Minikube tunnel**

To get external ip address for service in kubernetes, execute the following commands:

```
$ minikube tunnel
```
seperate tab -->
```
$ kubectl get service
```

![minikube](https://github.com/user-attachments/assets/d32f9758-7437-4600-81f8-00de5cec889d)

This will enable to access the application on **`<external-ip>:5000`**. Navigate to [http://\<external-ip\>:5000]() on your browser to access the application.

## **Part 3: Pushing the Docker image to ECR**

### **Step 1: Create an ECR repository**

Create an ECR repository using Python:

```
import boto3

# Create an ECR client
ecr_client = boto3.client('ecr')

# Create a new ECR repository
repository_name = 'my-ecr-repo'
response = ecr_client.create_repository(repositoryName=repository_name)

# Print the repository URI
repository_uri = response['repository']['repositoryUri']
print(repository_uri)
```

> [!WARNING]
> Make sure to log in to aws through aws-cli and configure the account through IAM user by `$ aws configure` command

### **Step 2: Push the Docker image to ECR**

Push the Docker image to ECR using the push commands on the console:

```
$ docker push <ecr_repo_uri>:<tag>
```

> [!TIP]
> All the required code snippets to push the image to ECR is provided by the AWS ECR `push commands` buton in ECR repository.

## **Part 4: Creating an EKS cluster and deploying the app using Python**

### **Step 1: Create an EKS cluster**

Create an EKS cluster.

> [!IMPORTANT]
> Make sure to attach following policies `AmazonEKSClusterPolicy`, `AmazonEKSVPCResourceController` to EKS cluster role you have created during this step

### **Step 2: Create a node group**

Create a node group in the EKS cluster.

> [!IMPORTANT]
> Make sure to attach following policies `AmazonEKSWorkerNodePolicy`, `AmazonEKS_CNI_Policy`, `AmazonEC2ContainerRegistryReadOnly` to EKS cluster node group role you have created during this step

### **Step 3: Create deployment and service**

```jsx
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
```

> [!WARNING]
> Make sure to edit the name of the image on line 28 with your image Uri

### **Step 4: Change the current context to user the new kubernetes cluster**

To change the context, execute the following commands:

```
$ aws eks update-kubeconfig --region us-east-1 --name <eks-cluster-name>
```

### **Step 5: Deploy application to kubernetes cluster**

To deploy the application, execute the following commands:

```
$ python3 eks.py
```

Once you run this file deployment and service will be created.

> [!CAUTION]
> If you get this error: ERROR:root:exec: plugin api version client.authentication.k8s.io/v1alpha1 does not match client.authentication.k8s.io/v1beta1

> [!TIP]
> Update the file `~/.kube/config` current context apiVersion from ***v1*** or ***v1beta1*** to ***v1alpha1*** temporally to execute the code. Then reverse it back to orginal value by opening the file in suitable text editor.

Execute following commands check the status of deployment:

```jsx
kubectl get deployment -n default (check deployments)
kubectl get pods -n default (check the pods)
kubectl get service -n default (check service)
```

![eks](https://github.com/user-attachments/assets/a8221dc2-4c4c-412d-a776-7db99ee771f0)

Once your pod is up and running, access thee application through the **`<external-ip>:5000`**. Navigate to [http://\<external-ip\>:5000]() on your browser to access the application.

![app-eks](https://github.com/user-attachments/assets/2125d503-d3e4-4e40-b524-0e176ae2514a)
