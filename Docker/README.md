# Docker Test Application

A simple Node.js application demonstrating Docker containerization with MongoDB integration. This project showcases Docker best practices, including multi-container setups with Docker Compose, environment variables, networking, and persistent volumes.

## 🚀 Docker Hub Repository

This application is available on Docker Hub:
- **Repository**: [muhtasimapon/testapp](https://hub.docker.com/repository/docker/muhtasimapon/testapp/general)
- **Pull Command**: `docker pull muhtasimapon/testapp`

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Building the Docker Image](#building-the-docker-image)
- [Running with Docker Compose](#running-with-docker-compose)
- [Environment Variables](#environment-variables)
- [Docker Commands Reference](#docker-commands-reference)
- [Docker Compose Commands](#docker-compose-commands)
- [Docker Volumes](#docker-volumes)
- [Networking](#networking)
- [Troubleshooting](#troubleshooting)

## 📖 Overview

This application is a user management system built with:
- **Backend**: Node.js with Express
- **Database**: MongoDB
- **Admin UI**: Mongo Express
- **Containerization**: Docker & Docker Compose

The application allows users to sign up and manages user data in MongoDB, demonstrating a complete containerized full-stack application.

## ✅ Prerequisites

Before you begin, ensure you have the following installed:
- [Docker](https://www.docker.com/get-started) (version 20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 1.29 or higher)

## 📁 Project Structure

```
Docker/
├── public/              # Static files
│   ├── index.html      # Frontend HTML
│   └── style.css       # Styling
├── server.js           # Express server
├── package.json        # Node.js dependencies
├── package-lock.json   # Locked dependencies
├── Dockerfile          # Docker image blueprint
├── .dockerignore       # Files to exclude from Docker image
├── mongo.yaml          # Docker Compose configuration
└── README.md           # This file
```

## 🚀 Quick Start

### Using Docker Compose (Recommended)

The easiest way to run the entire application stack:

```bash
# Start all services (MongoDB, Mongo Express, and Node.js app)
docker compose -f mongo.yaml up -d

# The application will be available at:
# - Node.js App: http://localhost:5050
# - Mongo Express: http://localhost:8081
```

### Using Pre-built Image from Docker Hub

```bash
# Pull the image
docker pull muhtasimapon/testapp

# Run the container (requires MongoDB to be running)
docker run -d \
  --name node-app \
  --network mongo-network \
  -p 5050:5050 \
  -e MONGO_URL="mongodb://admin:qwerty@mongodb:27017" \
  muhtasimapon/testapp
```

## 🔨 Building the Docker Image

### Build the Image

```bash
# Build the image with a tag
docker build -t testapp:1.0 .

# Or build with your Docker Hub username
docker build -t muhtasimapon/testapp:latest .
```

### Run the Built Image

```bash
# Run container interactively with shell
docker run -it --entrypoint sh testapp:1.0

# Run container in background with MongoDB connection
docker run -d \
  --name node-app \
  --network mongo-network \
  -p 5050:5050 \
  -e MONGO_URL="mongodb://admin:qwerty@mongodb:27017" \
  testapp:1.0
```

### Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag your image (if not already tagged)
docker tag testapp:1.0 muhtasimapon/testapp:latest

# Push to Docker Hub
docker push muhtasimapon/testapp:latest
```

## 🐳 Running with Docker Compose

The `mongo.yaml` file defines a complete multi-container application with three services:

1. **MongoDB** - Database server
2. **Mongo Express** - Web-based MongoDB admin interface
3. **Node App** - The Node.js application

### Start Services

```bash
# Start all services in detached mode
docker compose -f mongo.yaml up -d

# Start with rebuild (if you made code changes)
docker compose -f mongo.yaml up -d --build
```

### View Services

```bash
# Check running services
docker compose -f mongo.yaml ps

# View logs from all services
docker compose -f mongo.yaml logs

# Follow logs in real-time
docker compose -f mongo.yaml logs -f

# View logs for specific service
docker compose -f mongo.yaml logs node-app
```

### Stop Services

```bash
# Stop services (keeps containers)
docker compose -f mongo.yaml stop

# Stop and remove containers
docker compose -f mongo.yaml down

# Stop and remove containers + volumes
docker compose -f mongo.yaml down -v
```

### Execute Commands in Running Containers

```bash
# Access shell in node-app container
docker compose -f mongo.yaml exec node-app sh

# Access MongoDB shell
docker compose -f mongo.yaml exec mongodb mongosh -u admin -p qwerty
```

## 🔧 Environment Variables

The application uses the following environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGO_URL` | `mongodb://admin:qwerty@localhost:27017` | MongoDB connection string |
| `PORT` | `5050` | Application port (defined in server.js) |

### MongoDB Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `MONGO_INITDB_ROOT_USERNAME` | `admin` | MongoDB root username |
| `MONGO_INITDB_ROOT_PASSWORD` | `qwerty` | MongoDB root password |

### Mongo Express Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `ME_CONFIG_MONGODB_ADMINUSERNAME` | `admin` | Admin username |
| `ME_CONFIG_MONGODB_ADMINPASSWORD` | `qwerty` | Admin password |
| `ME_CONFIG_MONGODB_URL` | `mongodb://admin:qwerty@mongodb:27017` | MongoDB connection URL |

## 📚 Docker Commands Reference

### Container Management

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Start a container
docker start <container_name>

# Stop a container
docker stop <container_name>

# Remove a container
docker rm <container_name>

# Remove all stopped containers
docker container prune -f
```

### Image Management

```bash
# List images
docker images

# Pull an image from Docker Hub
docker pull <image_name>

# Remove an image
docker rmi <image_name>

# Tag an image
docker tag <source_image> <target_image>
```

### Container Interaction

```bash
# View container logs
docker logs <container_name>

# Follow logs (live)
docker logs -f <container_name>

# Execute command in running container
docker exec -it <container_name> /bin/bash

# Execute shell in Alpine-based container
docker exec -it <container_name> sh

# Inspect container details
docker inspect <container_name>
```

### Running Containers with Options

```bash
# Run in interactive mode
docker run -it <image_name>

# Run in detached mode (background)
docker run -d <image_name>

# Run with environment variable
docker run -e MYSQL_ROOT_PASSWORD=secret <image_name>

# Run with custom name
docker run -d --name my-container <image_name>

# Run with port mapping
docker run -d -p 8080:3306 <image_name>

# Run with custom network
docker run -d --network my-network <image_name>

# Complete example with all options
docker run -d \
  --name mysql-container \
  --network app-network \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=secret \
  mysql:8.0
```

## 🐋 Docker Compose Commands

```bash
# Start services
docker compose -f mongo.yaml up -d

# Stop services (keep containers)
docker compose -f mongo.yaml stop

# Stop and remove containers
docker compose -f mongo.yaml down

# Rebuild and start
docker compose -f mongo.yaml up -d --build

# View logs
docker compose -f mongo.yaml logs -f

# List running services
docker compose -f mongo.yaml ps

# Execute command in service
docker compose -f mongo.yaml exec node-app sh

# Remove volumes too
docker compose -f mongo.yaml down -v
```

## 💾 Docker Volumes

Docker volumes provide persistent storage for containers.

### Volume Commands

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect mongo-data

# Create volume
docker volume create mydata

# Remove volume
docker volume rm mydata

# Remove all unused volumes
docker volume prune
```

### Using Volumes with Containers

```bash
# Run container with volume mount
docker run -d \
  --name my-app \
  -v mydata:/app/data \
  <image_name>

# Mount host directory (bind mount)
docker run -d \
  --name my-app \
  -v /host/path:/container/path \
  <image_name>
```

## 🌐 Networking

Docker networking allows containers to communicate with each other.

### Network Commands

```bash
# List networks
docker network ls

# Create a network
docker network create my-network

# Inspect network
docker network inspect mongo-network

# Connect container to network
docker network connect my-network my-container

# Disconnect container from network
docker network disconnect my-network my-container
```

### Network Drivers

- **bridge** (default): Standard network for containers on same host
- **host**: Share host's network stack
- **none**: No networking
- **overlay**: Multi-host networking for Swarm

## 🔍 Troubleshooting

### Common Issues and Solutions

#### Container won't start

```bash
# Check logs for errors
docker logs <container_name>

# Check container details
docker inspect <container_name>
```

#### Port already in use

```bash
# Find process using the port
lsof -i :5050  # On Linux/Mac
netstat -ano | findstr :5050  # On Windows

# Change port mapping
docker run -p 5051:5050 <image_name>
```

#### Cannot connect to MongoDB

1. Ensure MongoDB container is running: `docker ps`
2. Check if containers are on the same network: `docker network inspect mongo-network`
3. Verify environment variables are set correctly
4. Check MongoDB logs: `docker logs mongo`

#### Image build fails

```bash
# Clear Docker cache and rebuild
docker build --no-cache -t testapp:1.0 .

# Check .dockerignore file
cat .dockerignore
```

#### Volume data not persisting

```bash
# Verify volume exists
docker volume inspect mongo-data

# Check volume mount in container
docker inspect <container_name> | grep -A 10 Mounts
```

### Useful Debugging Commands

```bash
# Check Docker system info
docker info

# Check Docker disk usage
docker system df

# Clean up unused resources
docker system prune -a

# Check container resource usage
docker stats

# View container processes
docker top <container_name>
```

## 🎓 Learning Resources

- [Docker Official Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Hub](https://hub.docker.com/)
- [Node.js Docker Best Practices](https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md)

## 📝 Notes

- This is a learning project demonstrating Docker fundamentals
- The application uses basic authentication (not suitable for production)
- Default credentials are for development only
- Always use environment-specific configurations in production

## 🤝 Contributing

This is a personal learning repository. Feel free to fork and experiment with your own modifications!

## 📄 License

This project is for educational purposes.

---

**Author**: [@muhtasim-apon](https://github.com/muhtasim-apon)  
**Docker Hub**: [muhtasimapon/testapp](https://hub.docker.com/repository/docker/muhtasimapon/testapp/general)