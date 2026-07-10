## **Overview**
This guide covers deploying a full-stack application (React frontend and .NET backend) to **Azure App Service** using GitHub Actions for CI/CD, without the need for containerization.
## **Step 1: Resource Group Setup**
- Log in to the **Azure Portal**.
- Create a new **Resource Group**.
    - **Region:** Use `Switzerland North` if using an Azure for Students subscription.
    - **Region:** Use `West Europe` if using a standard Free Tier account.

![image 8.png](image%208.png)

## **Step 2: App Service Configuration**

- Create a new **App Service**.
- **Runtime Stack:** Select `.NET` (for backend) or `Node` (for React).
- **Operating System:** Linux is generally recommended for cost-efficiency.
- *Note: Since we aren't using containers here, Azure will handle dependency installation via the build script.*

![image.png](image%201%202.png)

## **Step 3: Authentication & Secrets**

- In the App Service "Overview" blade, click **Get publish profile**.
- Download the file; you will need the contents for GitHub.

![image.png](image%202%202.png)

## **Step 4: GitHub Actions Setup**

1. Navigate to your **GitHub Repository** > **Settings**.
2. Go to **Secrets and variables** > **Actions**.
3. Add a new Repository Secret:
    - **Name:** `AZURE_WEBAPP_PUBLISH_PROFILE`
    - **Value:** (Paste the entire content of the file downloaded in Step 3).

![image.png](image%203%201.png)

![image.png](image%204%201.png)

## **Step 5: CI/CD Pipeline**

- In your deployment branch, create the path: `.github/workflows/deploy.yaml`.
- Define the build and deploy steps, ensuring the workflow uses the secret to authenticate with Azure.

> 💡 **Pro-Tip:** Expect to iterate on the `deploy.yaml` file; check the **Actions** tab in GitHub to debug logs if the initial deployment fails.
> 

![image.png](image%205%201.png)