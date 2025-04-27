COMP40660 - Group Assignment: Edge Computing

Student 1 Name: Sheng Wang
Student 1 ID: 20403764

Student 2 Name: Tianru Ji
Student 2 ID: 24208429

Student 2 Name: Bingxin Li
Student 2 ID: 20205615

---

Docker Images Links:

1. Task 1 - Static Web Server (Nginx serving index.html)
   Docker Hub Link:
   https://hub.docker.com/r/izlx/awn_assign2_task1

2. Task 2 - IPC Ubuntu Server
   (Receives image, extracts features, saves grayscale images)
   Docker Hub Link:
   https://hub.docker.com/r/izlx/awn_assign2_task2_ipc_server

3. Task 2 - IPC Ubuntu Client
   (Prepares and transmits 32×32 RGB images to server)
   Docker Hub Link:
   https://hub.docker.com/r/izlx/awn_assign2_task2_ipc_client

---

GitHub Repository Link:

All related Dockerfiles, Python scripts, and project documents are available at:

https://github.com/SIZLX/comp40660-assign2

---

Important Notes:

- All Python scripts inside the containers are located in the `/root/` directory.
- Container descriptions, usage instructions, and technical details are available directly on the Docker Hub pages.
- Each Docker image contains a clear embedded README in its Docker Hub repository.

---

Thank you for reviewing my submission.


---

# COMP40660 - Edge Computing Assignment

## Overview

This repository contains the complete deliverables for the COMP40660 Group Assignment on Edge Computing.  
It includes all Dockerfiles, Python scripts, static web files, and the general design report.

The assignment simulates a lightweight edge computing system where image preprocessing and feature extraction tasks are offloaded from an edge device (client) to an edge server.

## How to Use

### Task 1: Static Web Server

```
docker pull izlx/awn_assign2_task1:v1
docker run --rm -d -p 8080:80 --name web izlx/awn_assign2_task1:v1
```

Access the web page via `http://localhost:8080`.

---

### Task 2: Edge Client and Server

Start the server container:

```
docker pull izlx/ipc_ubuntu_server
docker run --rm -it -p 9898:9898 --name ipc_server yourusername/ipc_ubuntu_server
```

In another terminal, start the client container:

```
docker pull izlx/ipc_ubuntu_client
docker run --rm -it --name ipc_client yourusername/ipc_ubuntu_client
```

Ensure that the input image (`eevee.png`) is available under `/root/` in the client container.

The client will send the image, and the server will process it and return feature extraction results.

---

## Notes

- All Python scripts (`ipc_client.py` and `ipc_server.py`) are located inside the `/root/` directory within their respective containers.
- Grayscale output images are saved by the server at `/root/output_grayscale.png` and `/root/output_grayscale_128.png`.
- Communication between client and server follows a length-prefixed TCP socket protocol.
- Performance statistics such as offloading time and processing time are included in the general report (`DesignDocument.pdf`).

