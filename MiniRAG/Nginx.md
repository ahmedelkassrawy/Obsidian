At its core, **NGINX** (pronounced "engine-ex") is high-performance open-source software used for web serving, reverse proxying, caching, load balancing, and media streaming.

While it started as a simple web server designed for maximum stability, it has evolved into a Swiss Army knife for modern web architecture.

---
## What does NGINX actually do?
To understand NGINX, it helps to look at the primary roles it plays in a tech stack:

### 1. Web Server
Like Apache, NGINX can serve HTML files, images, and videos to users over the internet. It is famous for being extremely "lightweight"—it can handle a massive number of concurrent connections using very little RAM.

### 2. Reverse Proxy
This is perhaps its most common use today. Instead of a user connecting directly to your application (like a Node.js or Python backend), they connect to NGINX. NGINX then "talks" to your app on the user's behalf.
- **Security:** It hides the identity and structure of your backend servers.
    
- **SSL Termination:** NGINX handles the encryption (HTTPS), so your app doesn't have to.
### 3. Load Balancer
If you have a popular app running on three different servers, NGINX sits in front of them and distributes incoming traffic evenly. If one server crashes, NGINX stops sending traffic there until it's back online.

### 4. Content Caching
NGINX can store copies of your website's static content. When a second user asks for the same image, NGINX serves it from its own "memory" instantly rather than asking your backend server to process the request again.

---
## Why use NGINX instead of other servers?

The main reason is its **Event-Driven Architecture**.

- **Traditional servers (like Apache):** Often create a new "thread" or process for every single visitor. If you have 10,000 visitors, the server might struggle under the weight of 10,000 threads.
    
- **NGINX:** Uses a non-blocking, event-driven loop. One worker process can handle thousands of connections simultaneously. Think of it like a fast-food worker who takes an order, gives the customer a buzzer, and immediately helps the next person, rather than waiting at the window for the food to be ready for just one person.

## Common Use Cases

| **Feature**             | **Benefit**                                                 |
| ----------------------- | ----------------------------------------------------------- |
| **Static File Serving** | Fast delivery of CSS, JS, and Images.                       |
| **Microservices**       | Acts as a gateway to route traffic to different services.   |
| **DDoS Protection**     | Can limit the rate of incoming requests to prevent crashes. |
| **A/B Testing**         | Can send 10% of users to a "New Version" of your site.      |

---
nginx.conf
```python
server {
    #nginx listen on port 80 (Standard HTTP Port)
    listen 80;

    #your domain name or IP (use localhost for testing)
    server_name localhost;

    #The 'location /' block catches all requests
    location / {
        # forward the request to host machine (Windows) instead of container's own localhost
        proxy_pass http://host.docker.internal:8000;

        #pass essential headers to FASTAPI so it knows about the original client
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Let's break down the Nginx config:**
- `listen 80;`: The server is listening for standard internet traffic.
- `proxy_pass http://127.0.0.1:8000;`: Nginx acts as a middleman. It takes the client's request, makes its _own_ request to your FastAPI app on port 8000, gets the response, and hands it back to the client.
- `proxy_set_header ...`: Because Nginx is making the request to Uvicorn, Uvicorn thinks the request is coming from `127.0.0.1` (Nginx himself). We pass these headers so FastAPI can still see the _actual_ IP address of the user who made the request.
----
nginx/default.conf
```python
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://fastapi:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    #optionally expose metrics endpoint directly
    location /TrhBVe_m5gg2002_E5VVq5 {
        proxy_pass http://fastapi:8000/TrhBVe_m5gg2002_E5VVq5;
    }
}
```

Optionally expose metrics endpoint directly
location /{expose_metrics_endpoint} {proxy_pass http://fastapi:8000/{expose_metrics_endpoint}; }

docker-compose.yml
```python
services:
	nginx:
	    image: nginx:stable-alpine3.21-perl
	    container_name: nginx
	    ports:
	      - "80:80"
	    depends_on:
	      - fastapi
	    volumes:
	      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
	    networks:
	      - backend
	    restart: always
```