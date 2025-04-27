#!/usr/bin/env python3
# ipc_server.py

import numpy as np
import json
import socket
import struct
import time
from PIL import Image

HOST = '0.0.0.0'
PORT = 9898

def recv_all(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError(f"Expected {length} bytes but received {len(data)} bytes before socket closed.")
        data += more
    return data

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print("[Server Ready] Listening on port 9898...")

    conn, addr = s.accept()

    with conn:
        print('Connected by', addr)

        raw_msglen = recv_all(conn, 4)
        msglen = struct.unpack('>I', raw_msglen)[0]

        full_data = recv_all(conn, msglen)

        image = json.loads(full_data.decode('utf-8'))
        image_array = np.array(image)  # (32, 32, 3)

        start_proc_time = time.time()

        R = image_array[:, :, 0]
        G = image_array[:, :, 1]
        B = image_array[:, :, 2]

        mean_brightness = np.mean(image_array)
        contrast = np.max(image_array) - np.min(image_array)

        mean_R = np.mean(R)
        mean_G = np.mean(G)
        mean_B = np.mean(B)

        dominant_color = 'Red' if mean_R > mean_G and mean_R > mean_B else \
                         'Green' if mean_G > mean_R and mean_G > mean_B else 'Blue'

        grayscale = np.mean(image_array, axis=2)  # (32,32)矩阵
        binarized = np.where(grayscale > 127, 255, 0)
        white_pixels = np.sum(binarized == 255)
        total_pixels = binarized.size
        white_pixel_ratio = (white_pixels / total_pixels) * 100

        grayscale_image = Image.fromarray(grayscale.astype(np.uint8))
        grayscale_image.save('output_grayscale.png')
        print("\n[Info] Grayscale image saved as 'output_grayscale.png'.")

        grayscale_big = grayscale_image.resize((128, 128), Image.BICUBIC)
        grayscale_big.save('output_grayscale_128.png')
        print("[Info] Upscaled grayscale image saved as 'output_grayscale_128.png'.")

        response = (
            f"Mean Brightness: {mean_brightness:.2f}\n"
            f"Contrast: {contrast}\n"
            f"Dominant Color: {dominant_color}\n"
            f"Mean (R, G, B): ({mean_R:.2f}, {mean_G:.2f}, {mean_B:.2f})\n"
            f"Max Pixel Value: {np.max(image_array)}\n"
            f"Min Pixel Value: {np.min(image_array)}\n"
            f"White Pixel Ratio (after binarization): {white_pixel_ratio:.2f}%"
        )

        print("\n[Extracted Features]:\n")
        print(response)

        end_proc_time = time.time()

        processing_time = end_proc_time - start_proc_time
        print(f"\n[Performance] Server Processing Time: {processing_time*1000:.2f} ms")

        conn.sendall(response.encode('utf-8'))
