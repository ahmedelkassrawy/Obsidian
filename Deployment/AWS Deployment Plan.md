This plan outlines the steps to deploy our FastAPI + Nginx Docker Compose setup to AWS. We will use Amazon Elastic Compute Cloud (EC2) as it is the most straightforward way to run a [docker-compose.yml](file:///d:/Enviroment/PS/docker-compose.yml) file on AWS without needing to restructure the application for managed services like ECS or EKS.
## Prerequisites
- An AWS Account
- AWS CLI installed and configured on your local machine (optional, but recommended)
- SSH key pair created in AWS for accessing the EC2 instance

## Step 1: Provision an EC2 Instance
1. Log in to the AWS Management Console and navigate to the **EC2** dashboard.
2. Click **Launch Instance**.
3. **Name**: Give your instance a name (e.g., `fastapi-nginx-app`).
4. **AMI**: Select the **Amazon Linux 2023** or **Ubuntu Server 24.04 LTS** Amazon Machine Image (AMI). (Ubuntu is often easier for finding Docker documentation).
5. **Instance Type**: Select `t2.micro` or `t3.micro` (these are Free Tier eligible if your account is new).
6. **Key Pair**: Create a new key pair (e.g., `my-aws-key`) and download the `.pem` file. You will need this to SSH into the server.
7. **Network Settings / Security Group**: 
   - Allow SSH traffic from **My IP** (or Anywhere, but My IP is safer).
   - Allow HTTP traffic from the internet (Port 80).
   - Allow HTTPS traffic from the internet (Port 443) - optional for now, but good for later if you add SSL.
8. Click **Launch Instance**.

## Step 2: Connect to the EC2 Instance
1. Open your terminal.
2. Change the permissions of your downloaded key pair file so it's not publicly viewable (Linux/Mac):
   ```bash
   chmod 400 my-aws-key.pem
   ```
   *(On Windows using PowerShell, you might need to adjust the file's Security properties to remove inheritance and only allow your user).*
3. Connect using SSH. Replace `ec2-user` with `ubuntu` if you chose the Ubuntu AMI, and replace the IP with your instance's Public IPv4 address:
   ```bash
   ssh -i /path/to/my-aws-key.pem ec2-user@<YOUR_EC2_PUBLIC_IP>
   ```

## Step 3: Install Docker and Docker Compose on EC2
Run these commands on your EC2 instance.

**If you chose Amazon Linux:**
```bash
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
# Log out and log back in for group changes to take effect
exit
# Reconnect...

# Install Docker Compose plugin
sudo mkdir -p /usr/local/lib/docker/cli-plugins/
sudo curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
```

**If you chose Ubuntu:**
```bash
sudo apt update
sudo apt install -y docker.io docker-compose-v2
sudo systemctl enable --now docker
sudo usermod -aG docker ubuntu
# Log out and log back in
exit
# Reconnect...
```

## Step 4: Transfer Your Code to the EC2 Instance
You can use `scp` (Secure Copy) from your local machine to copy your project folder to the server.
Run this from the directory *above* your `PS` folder on your local computer:

```bash
scp -i /path/to/my-aws-key.pem -r ./PS ec2-user@<YOUR_EC2_PUBLIC_IP>:~/PS
```
*(Again, use `ubuntu` instead of `ec2-user` if needed).*

Alternatively, if your code is in a GitHub repository, you can install `git` on the EC2 instance and `git clone` your repository directly there.

## Step 5: Run the Application
1. SSH back into your EC2 instance.
2. Navigate to the project directory:
   ```bash
   cd ~/PS
   ```
3. Build and start the containers in detached mode:
   ```bash
   docker compose up -d --build
   ```
4. Verify they are running:
   ```bash
   docker ps
   ```

## Step 6: Test the Deployment
Open your web browser and navigate to your EC2 instance's Public IPv4 address (or Public IPv4 DNS):
`http://<YOUR_EC2_PUBLIC_IP>`

You should see the "Hello from FastAPI through Nginx!" message.

## Next Steps (Optional but Recommended)
- **Domain Name**: Point a domain name (via Route 53 or your registrar) to your EC2 instance's Elastic IP.
- **HTTPS (SSL/TLS)**: Use Let's Encrypt (Certbot) within your Nginx configuration or add another container to automatically manage SSL certificates so your site runs securely over HTTPS.
---
### Trying the instance
Based on your output, your FastAPI/Uvicorn application is mapping port **8000** on the container to port **8000** on your AWS instance.

The URL you should visit in your browser is:
**[http://98.92.81.170:8000](https://www.google.com/search?q=http://98.92.81.170:8000)**

---
### If the page doesn't load:
AWS instances are locked down by default. You likely need to open the "front door" to let traffic reach that port.
1. Go to your **AWS EC2 Console**.
2. Select your instance and click the **Security** tab.
3. Click on the **Security Group** ID (e.g., `sg-0abc123...`).
4. Edit **Inbound Rules** and add a new rule:
    - **Type:** Custom TCP
    - **Port Range:** 8000
    - **Source:** `0.0.0.0/0` (or `My IP` for better security)
### Testing the API
Since you are using Uvicorn/FastAPI, you can also check if the interactive documentation is working by going to:
**http://98.92.81.170:8000/docs**

That "invalid response" error usually happens when your browser tries to connect via **HTTPS** (secure) by default, but your FastAPI/Uvicorn server is only set up for **HTTP** (standard).

Browsers often force `https://` if you just type the IP, but since you haven't set up an SSL certificate yet, the server doesn't know how to handle that secure request.

### The Fix
Manually type the full address into your browser's address bar, making sure it starts with `http` (no **S**):
**`http://98.92.81.170:8000`**