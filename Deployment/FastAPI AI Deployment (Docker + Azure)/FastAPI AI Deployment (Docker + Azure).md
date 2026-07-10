## **Overview**
Deploying a Python FastAPI service with heavy AI dependencies is most stable when **containerized**. This guide uses Docker Hub and Azure App Service.
## **Step 1: Resource Group & Infrastructure**
- Create a **Resource Group** in `Switzerland North` (Student) or `West Europe` (Free).
- Create an **App Service**, but select **Docker Container** as the publish method.

![image.png](Images/image.png)

## **Step 2: Containerization**
1. Write a `Dockerfile` for your FastAPI app.
2. Build the image locally: `docker build -t your-username/image-name:latest .`
3. Push the image to your **Docker Hub** account: `docker push your-username/image-name:latest`.

![image.png](Images/image%201.png)

![image.png](Images/image%202.png)

## **Step 3: Connect Azure to Docker**
- In the App Service **Deployment Center**, set the source to **Docker Hub**.
- Enter your image name and tag.

![image.png](Images/image%203.png)

## **Step 4: GitHub Automation**
1. In your GitHub Repo **Settings** > **Secrets**, add:
    - `DOCKER_USERNAME`
    - `DOCKER_PASSWORD` (or Personal Access Token).

![image.png](Images/image%204.png)

![image.png](Images/image%205.png)

1. Create `.github/workflows/deploy.yaml`.
2. The workflow should:
    - Build the Docker image.
    - Push it to Docker Hub.
    - Trigger an Azure Web App refresh.

![image.png](image%206.png)