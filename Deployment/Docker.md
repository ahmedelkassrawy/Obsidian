```python
docker run -d -p 80:80 docker/getting-started
```

-d  -> run container in background
-p 80:80  -> map port 80 of the host to the port in the container

What is a container?
 a container is another process on your machine that has been isolated from all other processes on the host machine.
#### What is a container image?
- When running a container, it uses an isolated filesystem. 
- This custom filesystem is provided by a **container image**. 
- Since the image contains the container's filesystem, it must include everything needed to run the application - all dependencies, configuration, scripts, binaries, etc. 
- The image also contains other configuration for the container, such as environment variables, a default command to run, and other metadata.

#### Building the App's Container Image
- In order to build the application, we need to use a `Dockerfile`.
- A Dockerfile is simply a text-based script of instructions that is used to create a container image.
```python
FROM node:18-alpine

WORKDIR /app

COPY . .

RUN yarn install --production

CMD ["node","src/index.js"]
```

1.  You might have noticed that a lot of "layers" were downloaded.
	- This is because we instructed the builder that we wanted to start from the `node:18-alpine` image. But, since we didn't have that on our machine, that image needed to be downloaded.
2. After the image was downloaded, we copied in our application and used `yarn` to install our application's dependencies
3. The `CMD` directive specifies the default command to run when starting a container from this image.

build the container image using `docker build`
```python
docker build -t image-name .
```
1. Finally, the `-t` flag tags our image.
2. The `.` at the end of the `docker build` command tells that Docker should look for the `Dockerfile` in the current directory.

lisitng docker images
```python
docker ps
docker image ls
```

Stop the container
```python
docker stop <the-container-id>
```

remove docker image
```python
docker rm -f <the-container-id>
```

Pushing docker image to the dockerhub
```python
docker push docker/getting-started:tagname
```

Volumes
[Volumes](https://docs.docker.com/storage/volumes/) provide the ability to connect specific filesystem paths of the container back to the host machine. 

If a directory in the container is mounted, changes in that directory are also seen on the host machine

create volume
```python
docker volume create todo-db
```

to add volume to docker using -v
```python
docker run -dp 3000:3000 -v todo-db:/etc/todos getting-started
```

Where is the docker actually storing my data when i use a named volume
```python
docker volume inspect volume-name
```

## Container Networking
Remember that containers, by default, run in isolation and don't know anything about other processes or containers on the same machine. 
So, how do we allow one container to talk to another? The answer is **networking**
If two containers are on the same network, they can talk to each other. If they aren't, they can't.

create network
```python
docker network create network-name
```

attaching the MySQL to the network
```python
docker run -d \ 
	--network todo-app --network-alias mysql \ 
	-v todo-mysql-data:/var/lib/mysql \ 
	-e MYSQL_ROOT_PASSWORD=secret \ 
	-e MYSQL_DATABASE=todos \ 
	mysql:8.0
```

#### Docker Compose
create docker-compose.yml
```python
services:
```

```python
docker run -dp 3000:3000 \ 
	-w /app -v "$(pwd):/app" \ 
	--network todo-app \ 
	-e MYSQL_HOST=mysql \ 
	-e MYSQL_USER=root \ 
	-e MYSQL_PASSWORD=secret \ 
	-e MYSQL_DB=todos \ 
	node:18-alpine \ 
	sh -c "yarn install && yarn run dev"
```

creating the docker-compose.tml
```python
services:
  app:
    image: node:18-alpine
    command: sh -c "yarn install && yarn run dev"
    ports:
      - 3000:3000
    working_dir: /app
    volumes:
      - ./:/app
    environment:
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD: secret
      MYSQL_DB: todos
```

defining the MySQL Service
```python
docker run -d \
  --network todo-app --network-alias mysql \
  -v todo-mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=todos \
  mysql:8.0
```

```python
services:
  app:
    image: node:18-alpine
    command: sh -c "yarn install && yarn run dev"
    ports:
      - 3000:3000
    working_dir: /app
    volumes:
      - ./:/app
    environment:
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD: secret
      MYSQL_DB: todos

  mysql:
    image: mysql:8.0
    volumes:
      - todo-mysql-data:/var/lib/mysql
    environment: 
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: todos

volumes:
  todo-mysql-data:
```

```python
docker compose up
docker compose down
```

#### Secuirty Scanning
```python
docker scan image-name
```

#### Image Layering
```python
docker image history image-name
```

You'll notice that several of the lines are truncated. If you add the `--no-trunc` flag, you'll get the full output
```python
docker image history --no-trunc getting-started
```

#### Layer Caching
there's an important lesson to learn to help decrease build times for your container images.

Once a layer changes, all downstream layers have to be recreated as well

Before:
```python
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "src/index.js"]
```

Going back to the image history output, we see that each command in the Dockerfile becomes a new layer in the image. You might remember that when we made a change to the image, the yarn dependencies had to be reinstalled. Is there a way to fix this? It doesn't make much sense to ship around the same dependencies every time we build, right?

After:
```python
FROM node:18-alpine
WORKDIR /app
COPY package.json yarn.lock ./   #new line
RUN yarn install --production
COPY . .
CMD ["node", "src/index.js"]
```

```python
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

First off, you should notice that the build was MUCH faster! You'll see that several steps are using previously cached layers.