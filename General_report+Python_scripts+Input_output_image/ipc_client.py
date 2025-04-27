#!/usr/bin/env python3
# ipc_client.py

import numpy as np
import socket
import json
import time
import struct
from PIL import Image

HOST = '172.17.0.2'
PORT = 9898

time.sleep(1)

image_path = 'eevee.png'  # path to the image
try:
    img = Image.open(image_path)
except FileNotFoundError:
    print(f"[Error] Image file '{image_path}' not found!")
    exit(1)

if img.mode != 'RGB':
    print(f"[Info] Converting image to RGB...")
    img = img.convert('RGB')

if img.size != (32, 32):
    print(f"[Info] Resizing image to 32x32...")
    img = img.resize((32, 32))

image_array = np.array(img).tolist()

json_data = json.dumps(image_array).encode('utf-8')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    start_time = time.time()

    # send 4 bytes to tell the size of the data
    s.sendall(struct.pack('>I', len(json_data)))

    # send all data
    s.sendall(json_data)

    print("\n[Info] Sent image data to server.")

    end_time = time.time()

    offloading_time = end_time - start_time
    print(f"\n[Performance] Offloading Time: {offloading_time*1000:.2f} ms")
    
    response = s.recv(4096)
    print("\n[Received Features from Server]:\n")
    print(response.decode('utf-8'))
